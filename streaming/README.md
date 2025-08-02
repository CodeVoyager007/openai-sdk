# OpenAI SDK Streaming Demo

A comprehensive demonstration of streaming capabilities with the OpenAI SDK, featuring real-time response handling, function calling, and beautiful console output.

## 🚀 Features

- **Basic Streaming**: Real-time chat completion streaming
- **Function Calling**: Streaming with function invocation capabilities
- **Real-time Processing**: Live statistics and content processing
- **Error Handling**: Comprehensive error handling and retry logic
- **Rich Console**: Beautiful terminal output using Rich library
- **Async/Await**: Full async implementation for optimal performance

## 📋 Prerequisites

- Python 3.10 or higher
- OpenAI API key
- Basic understanding of async/await in Python

## 🛠️ Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -e .
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## 🎯 Quick Start

1. **Set your OpenAI API key** in the `.env` file

2. **Run the streaming demo**:
   ```bash
   python main.py
   ```

3. **Watch the magic happen!** The demo will show:
   - Basic streaming responses
   - Function calling with streaming
   - Real-time processing with live statistics
   - Error handling demonstrations

## 📖 What You'll Learn

### Demo 1: Basic Streaming
- How to implement basic chat completion streaming
- Processing chunks as they arrive
- Displaying content in real-time

### Demo 2: Function Calling
- Streaming with function invocation
- Handling function calls during streaming
- Processing both content and function calls

### Demo 3: Real-time Processing
- Live statistics during streaming
- Word count, sentence count, character count
- Beautiful live display with Rich library

### Demo 4: Error Handling
- Comprehensive error handling for streaming
- Rate limiting, authentication, and timeout handling
- Best practices for production use

## 🏗️ Project Structure

```
streaming/
├── main.py              # Main streaming demo application
├── pyproject.toml       # Project dependencies and metadata
├── README.md           # This file
├── streaming_blog.md   # Comprehensive blog post about streaming
└── .env                # Environment variables (create this)
```

## 💡 Key Concepts

### Streaming vs Non-Streaming

**Non-Streaming (Traditional)**:
```python
response = await client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello"}]
)
print(response.choices[0].message.content)  # Wait for complete response
```

**Streaming**:
```python
stream = await client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello"}],
    stream=True
)

async for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")  # Real-time output
```

### Benefits of Streaming

1. **Immediate Feedback**: Users see responses as they're generated
2. **Better UX**: Reduces perceived latency
3. **Real-time Processing**: Can process content as it arrives
4. **Interactive Applications**: Enables dynamic, conversational interfaces

## 🔧 Customization

### Changing the Model

Edit the `model` variable in the `StreamingDemo` class:

```python
self.model = "gpt-4"  # or any other available model
```

### Adding Custom Functions

Modify the `functions` list in `function_calling_streaming_demo()`:

```python
functions = [
    {
        "type": "function",
        "function": {
            "name": "your_custom_function",
            "description": "Your function description",
            "parameters": {
                "type": "object",
                "properties": {
                    "param1": {"type": "string"}
                },
                "required": ["param1"]
            }
        }
    }
]
```

### Custom Error Handling

Add your own error handling logic:

```python
try:
    # Your streaming code
    pass
except openai.RateLimitError as e:
    # Handle rate limiting
    pass
except openai.AuthenticationError as e:
    # Handle authentication errors
    pass
```

## 📚 Learning Resources

### Blog Post
Check out `streaming_blog.md` for a comprehensive guide covering:
- Detailed explanations of streaming concepts
- Advanced implementation techniques
- Real-world applications
- Performance considerations
- Best practices

### Official Documentation
- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference/chat/create)
- [OpenAI Python SDK](https://github.com/openai/openai-python)
- [Rich Library Documentation](https://rich.readthedocs.io/)

## 🚨 Troubleshooting

### Common Issues

1. **API Key Not Found**
   ```
   Error: OPENAI_API_KEY not found in environment variables
   ```
   **Solution**: Create a `.env` file with your API key

2. **Authentication Error**
   ```
   Authentication Error: Invalid API key
   ```
   **Solution**: Check your API key in the `.env` file

3. **Rate Limit Error**
   ```
   Rate Limit Error: Rate limit exceeded
   ```
   **Solution**: Wait a moment and try again, or implement retry logic

4. **Import Errors**
   ```
   ModuleNotFoundError: No module named 'openai'
   ```
   **Solution**: Install dependencies with `pip install -e .`

### Debug Mode

Enable debug output by modifying the console initialization:

```python
console = Console(force_terminal=True, color_system="auto")
```

## 🤝 Contributing

Feel free to contribute to this project by:
- Adding new streaming demos
- Improving error handling
- Enhancing the documentation
- Adding new features

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- OpenAI for providing the excellent API and SDK
- Rich library for beautiful console output
- Python community for async/await support

---

**Happy Streaming! 🎉**

For questions or issues, please refer to the blog post (`streaming_blog.md`) or the official OpenAI documentation.
