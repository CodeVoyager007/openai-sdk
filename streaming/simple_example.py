#!/usr/bin/env python3
"""
Simple OpenAI Streaming Example

This is a minimal example showing how to implement basic streaming
with the OpenAI SDK. Perfect for getting started with streaming concepts.
"""

import asyncio
import os
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

async def simple_streaming():
    """
    Basic streaming example - the simplest way to get started with streaming.
    """
    # Initialize the OpenAI client
    client = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Define your conversation
    messages = [
        {"role": "user", "content": "Tell me a short joke about programming."}
    ]
    
    print("🤖 AI Response:")
    print("-" * 40)
    
    try:
        # Create a streaming request
        stream = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True  # This is the key parameter for streaming
        )
        
        # Process the stream chunk by chunk
        async for chunk in stream:
            # Check if there's content in this chunk
            if chunk.choices[0].delta.content is not None:
                # Print the content immediately (real-time)
                print(chunk.choices[0].delta.content, end="", flush=True)
        
        print("\n" + "-" * 40)
        print("✅ Streaming complete!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

async def streaming_with_collection():
    """
    Example that collects the full response while streaming.
    Useful when you need both real-time display and the complete text.
    """
    client = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    messages = [
        {"role": "user", "content": "Write a haiku about artificial intelligence."}
    ]
    
    print("🎯 Streaming with Collection:")
    print("-" * 40)
    
    full_response = ""
    
    try:
        stream = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True
        )
        
        async for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                full_response += content
                print(content, end="", flush=True)
        
        print("\n" + "-" * 40)
        print("📝 Complete response:")
        print(full_response)
        
    except Exception as e:
        print(f"❌ Error: {e}")

async def interactive_streaming():
    """
    Interactive streaming example - ask user for input and stream the response.
    """
    client = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    print("💬 Interactive Streaming Demo")
    print("Type 'quit' to exit")
    print("-" * 40)
    
    conversation_history = []
    
    while True:
        # Get user input
        user_input = input("\n👤 You: ")
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("👋 Goodbye!")
            break
        
        # Add user message to conversation
        conversation_history.append({"role": "user", "content": user_input})
        
        print("🤖 AI: ", end="", flush=True)
        
        try:
            # Stream the response
            stream = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=conversation_history,
                stream=True
            )
            
            response_content = ""
            
            async for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    response_content += content
                    print(content, end="", flush=True)
            
            # Add AI response to conversation history
            conversation_history.append({"role": "assistant", "content": response_content})
            
        except Exception as e:
            print(f"\n❌ Error: {e}")

def main():
    """
    Main function to run the examples.
    """
    print("🚀 OpenAI Streaming Examples")
    print("=" * 50)
    
    # Check if API key is available
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found!")
        print("Please create a .env file with your OpenAI API key:")
        print("OPENAI_API_KEY=your_api_key_here")
        return
    
    # Run examples
    examples = [
        ("Simple Streaming", simple_streaming),
        ("Streaming with Collection", streaming_with_collection),
        ("Interactive Streaming", interactive_streaming)
    ]
    
    for i, (name, example_func) in enumerate(examples, 1):
        print(f"\n{i}. {name}")
        print("Press Enter to run this example...")
        input()
        
        try:
            asyncio.run(example_func())
        except KeyboardInterrupt:
            print("\n⏹️  Example interrupted by user")
        except Exception as e:
            print(f"\n❌ Error running example: {e}")
        
        print("\n" + "=" * 50)

if __name__ == "__main__":
    main() 