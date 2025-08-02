#!/usr/bin/env python3
"""
OpenAI SDK Streaming Demo

This project demonstrates various streaming concepts with the OpenAI API:
- Basic chat completion streaming
- Function calling with streaming
- Real-time response handling
- Error handling and retry logic
"""

import asyncio
import os
import sys
from typing import AsyncGenerator, Dict, Any
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.live import Live
from rich.layout import Layout
from rich.table import Table
import openai

# Load environment variables
load_dotenv()

# Initialize Rich console for beautiful output
console = Console()

class StreamingDemo:
    """Main class for demonstrating OpenAI SDK streaming capabilities."""
    
    def __init__(self):
        """Initialize the streaming demo with OpenAI client."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            console.print("[red]Error: OPENAI_API_KEY not found in environment variables[/red]")
            console.print("Please create a .env file with your OpenAI API key:")
            console.print("OPENAI_API_KEY=your_api_key_here")
            sys.exit(1)
        
        self.client = openai.AsyncOpenAI(api_key=api_key)
        self.model = "gpt-3.5-turbo"
    
    async def basic_streaming_demo(self) -> None:
        """Demonstrate basic chat completion streaming."""
        console.print(Panel.fit(
            "[bold blue]Basic Streaming Demo[/bold blue]\n"
            "This shows how to stream responses from OpenAI's chat completion API",
            title="Demo 1: Basic Streaming"
        ))
        
        messages = [
            {"role": "system", "content": "You are a helpful assistant. Respond in a conversational manner."},
            {"role": "user", "content": "Write a short story about a robot learning to paint. Make it about 3 paragraphs."}
        ]
        
        full_response = ""
        
        try:
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True,
                max_tokens=500
            )
            
            with console.status("[bold green]Streaming response...", spinner="dots"):
                async for chunk in stream:
                    if chunk.choices[0].delta.content is not None:
                        content = chunk.choices[0].delta.content
                        full_response += content
                        console.print(content, end="", style="green")
            
            console.print("\n\n[bold]Full response collected:[/bold]")
            console.print(Panel(full_response, title="Complete Response"))
            
        except Exception as e:
            console.print(f"[red]Error during streaming: {e}[/red]")
    
    async def function_calling_streaming_demo(self) -> None:
        """Demonstrate function calling with streaming."""
        console.print(Panel.fit(
            "[bold blue]Function Calling with Streaming[/bold blue]\n"
            "This shows how to use function calling while streaming responses",
            title="Demo 2: Function Calling"
        ))
        
        # Define a function that the model can call
        functions = [
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "Get the current weather for a location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city and state, e.g. San Francisco, CA"
                            },
                            "unit": {
                                "type": "string",
                                "enum": ["celsius", "fahrenheit"],
                                "description": "The temperature unit to use"
                            }
                        },
                        "required": ["location"]
                    }
                }
            }
        ]
        
        messages = [
            {"role": "user", "content": "What's the weather like in New York? Please use Celsius."}
        ]
        
        try:
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                functions=functions,
                stream=True
            )
            
            function_calls = []
            content_parts = []
            
            with console.status("[bold green]Streaming with function calls...", spinner="dots"):
                async for chunk in stream:
                    if chunk.choices[0].delta.content is not None:
                        content = chunk.choices[0].delta.content
                        content_parts.append(content)
                        console.print(content, end="", style="cyan")
                    
                    if chunk.choices[0].delta.function_call is not None:
                        function_call = chunk.choices[0].delta.function_call
                        if function_call.name:
                            function_calls.append({
                                "name": function_call.name,
                                "arguments": function_call.arguments or ""
                            })
                        elif function_call.arguments:
                            if function_calls:
                                function_calls[-1]["arguments"] += function_call.arguments
            
            console.print("\n\n[bold]Function calls detected:[/bold]")
            for func_call in function_calls:
                console.print(Panel(
                    f"Function: {func_call['name']}\nArguments: {func_call['arguments']}",
                    title="Function Call"
                ))
                
        except Exception as e:
            console.print(f"[red]Error during function calling: {e}[/red]")
    
    async def real_time_processing_demo(self) -> None:
        """Demonstrate real-time processing of streamed content."""
        console.print(Panel.fit(
            "[bold blue]Real-time Processing Demo[/bold blue]\n"
            "This shows how to process streamed content in real-time",
            title="Demo 3: Real-time Processing"
        ))
        
        messages = [
            {"role": "user", "content": "List the top 5 programming languages and explain why they're popular. Format as a numbered list."}
        ]
        
        word_count = 0
        sentence_count = 0
        current_sentence = ""
        
        # Create a live display
        layout = Layout()
        layout.split_column(
            Layout(name="stats", size=3),
            Layout(name="content", ratio=1)
        )
        
        stats_table = Table(title="Real-time Statistics")
        stats_table.add_column("Metric", style="cyan")
        stats_table.add_column("Count", style="green")
        
        content_panel = Panel("", title="Streaming Content")
        
        try:
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True,
                max_tokens=400
            )
            
            with Live(layout, refresh_per_second=4):
                async for chunk in stream:
                    if chunk.choices[0].delta.content is not None:
                        content = chunk.choices[0].delta.content
                        current_sentence += content
                        word_count += len(content.split())
                        
                        # Count sentences (simple heuristic)
                        if any(punct in content for punct in '.!?'):
                            sentence_count += content.count('.') + content.count('!') + content.count('?')
                        
                        # Update the live display
                        stats_table.rows = [
                            ["Words", str(word_count)],
                            ["Sentences", str(sentence_count)],
                            ["Characters", str(len(current_sentence))]
                        ]
                        
                        layout["stats"].update(stats_table)
                        layout["content"].update(Panel(current_sentence, title="Streaming Content"))
                        
                        await asyncio.sleep(0.01)  # Small delay for smooth display
                        
        except Exception as e:
            console.print(f"[red]Error during real-time processing: {e}[/red]")
    
    async def error_handling_demo(self) -> None:
        """Demonstrate error handling in streaming."""
        console.print(Panel.fit(
            "[bold blue]Error Handling Demo[/bold blue]\n"
            "This shows how to handle errors during streaming",
            title="Demo 4: Error Handling"
        ))
        
        # Simulate a potential error scenario
        try:
            # Try with an invalid model to demonstrate error handling
            stream = await self.client.chat.completions.create(
                model="invalid-model-name",
                messages=[{"role": "user", "content": "Hello"}],
                stream=True
            )
            
            async for chunk in stream:
                pass
                
        except openai.BadRequestError as e:
            console.print(f"[yellow]Handled BadRequestError: {e}[/yellow]")
        except openai.AuthenticationError as e:
            console.print(f"[red]Authentication Error: {e}[/red]")
        except openai.RateLimitError as e:
            console.print(f"[yellow]Rate Limit Error: {e}[/yellow]")
        except Exception as e:
            console.print(f"[red]Unexpected Error: {e}[/red]")
        else:
            console.print("[green]No errors occurred[/green]")
    
    async def run_all_demos(self) -> None:
        """Run all streaming demos in sequence."""
        console.print(Panel.fit(
            "[bold magenta]OpenAI SDK Streaming Demo[/bold magenta]\n"
            "This project demonstrates various streaming concepts with the OpenAI API",
            title="🚀 Welcome to Streaming Demo"
        ))
        
        demos = [
            self.basic_streaming_demo,
            self.function_calling_streaming_demo,
            self.real_time_processing_demo,
            self.error_handling_demo
        ]
        
        for i, demo in enumerate(demos, 1):
            console.print(f"\n[bold]Demo {i}/{len(demos)}[/bold]")
            await demo()
            console.print("\n" + "="*50 + "\n")
        
        console.print(Panel.fit(
            "[bold green]All demos completed![/bold green]\n"
            "Check out the blog post for detailed explanations.",
            title="✅ Demo Complete"
        ))

async def main():
    """Main entry point for the streaming demo."""
    demo = StreamingDemo()
    await demo.run_all_demos()

if __name__ == "__main__":
    asyncio.run(main())
