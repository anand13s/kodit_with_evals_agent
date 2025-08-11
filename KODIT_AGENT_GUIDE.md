# Kodit MCP Agent - Intelligent Code Assistant

The Kodit MCP Agent is an advanced AI-powered code assistant that combines the retrieval capabilities of the Kodit MCP server with the reasoning power of GPT-4o. It provides an intelligent interface to query, understand, and work with codebases.

## 🎯 Overview

### What it does:
- **Intelligent Code Search**: Uses Kodit MCP server to find relevant code snippets
- **Contextual Analysis**: Leverages GPT-4o to analyze and explain code patterns
- **Interactive Chat**: Provides a conversational interface for codebase exploration
- **Practical Guidance**: Offers actionable development advice with concrete examples

### Key Features:
- ✅ **GPT-4o Integration**: Latest OpenAI model for advanced reasoning
- ✅ **MCP Protocol**: Seamless integration with Kodit MCP server
- ✅ **Interactive & Batch Modes**: Both chat interface and single-query modes
- ✅ **Context-Aware**: Maintains conversation history for follow-up questions
- ✅ **Code-Focused**: Specialized prompts for software development tasks

## 🚀 Quick Start

### Prerequisites

1. **Kodit MCP Server**: Must be installed and working
   ```bash
   kodit --version  # Should show version information
   ```

2. **OpenAI API Key**: Valid GPT-4o access
   - Get from: https://platform.openai.com/api-keys
   - Format: `sk-...` (starts with "sk-")

3. **Python 3.8+**: Required for async/await support

### Installation

#### Step 1: Install Dependencies
```bash
# Install required packages
pip install -r kodit_agent_requirements.txt

# Or install manually
pip install openai>=1.30.0
```

#### Step 2: Verify Setup
```bash
# Test Kodit installation
kodit index  # Should show any indexed repositories

# Test agent without API calls
python kodit_agent.py --help
```

## 📋 Usage Instructions

### Interactive Chat Mode (Recommended)

Start an interactive conversation with the agent:

```bash
python kodit_agent.py --api-key YOUR_OPENAI_API_KEY --interactive
```

**Example Session:**
```
🤖 Kodit Agent - Interactive Chat
==================================================
Ask questions about your codebase. Type 'quit' or 'exit' to stop.

You: How does the server start in this application?
🤖 Agent: Thinking...
🤖 Agent: Based on the codebase analysis, the server starts through the following mechanism:

1. **Main Entry Point** (grip/command.py):
   ```python
   def main(argv=None, force_utf8=True, patch_svg=True):
       # ... argument parsing ...
       serve(path, host, port, ...)
   ```

2. **Server Creation** (grip/api.py):
   ```python
   def serve(path=None, host=None, port=None, ...):
       app = create_app(path, user_content, context, ...)
       app.run(host, port, open_browser=browser)
   ```

The server uses Flask as the underlying framework and supports:
- Custom host/port configuration
- Browser auto-opening
- Authentication options
- Wide rendering mode

You can start it with: `grip [options] [<path>] [<hostname>:]<port>`

You: What about error handling?
🤖 Agent: Thinking...
🤖 Agent: The application implements several layers of error handling...
```

### Single Query Mode

Process a single question and exit:

```bash
python kodit_agent.py --api-key YOUR_OPENAI_API_KEY --query "How does authentication work?"
```

### Advanced Options

```bash
# Use different GPT model
python kodit_agent.py --api-key YOUR_KEY --model gpt-4o-mini --interactive

# Enable verbose logging
python kodit_agent.py --api-key YOUR_KEY --verbose --query "Find database code"

# Process specific query
python kodit_agent.py --api-key YOUR_KEY --query "Show me all API endpoints"
```

## 🔧 Configuration Options

### Command Line Arguments

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `--api-key` | ✅ | OpenAI API key | `sk-1234...` |
| `--model` | ❌ | OpenAI model | `gpt-4o` (default), `gpt-4o-mini` |
| `--query` | ❌ | Single query mode | `"How does routing work?"` |
| `--interactive` | ❌ | Force interactive mode | Use for chat interface |
| `--verbose` | ❌ | Enable debug logging | Shows detailed logs |

### Environment Variables (Alternative)

You can also set the API key via environment variable:

```bash
export OPENAI_API_KEY="sk-your-key-here"
python kodit_agent.py --interactive
```

## 💡 Example Use Cases

### 1. Understanding Code Architecture
```bash
python kodit_agent.py --api-key YOUR_KEY --query "What is the overall architecture of this application?"
```

### 2. Finding Specific Functionality
```bash
python kodit_agent.py --api-key YOUR_KEY --query "How are files uploaded and processed?"
```

### 3. Debugging Help
```bash
python kodit_agent.py --api-key YOUR_KEY --query "Show me error handling patterns in this codebase"
```

### 4. API Documentation
```bash
python kodit_agent.py --api-key YOUR_KEY --query "List all API endpoints and their purposes"
```

### 5. Security Analysis
```bash
python kodit_agent.py --api-key YOUR_KEY --query "How is authentication and authorization implemented?"
```

## 🎯 Sample Interactions

### Example 1: Server Startup Query
**User**: "How do I start the server with custom settings?"

**Agent Response**:
```
Based on the codebase analysis, here's how to start the server with custom settings:

## Command Line Usage
```bash
grip [options] [<path>] [<hostname>:]<port>
```

## Key Options:
- **Custom Port**: `grip --port 8080` or `grip localhost:8080`
- **Custom Host**: `grip 0.0.0.0:6419` 
- **Browser Auto-open**: `grip --browser`
- **Authentication**: `grip --user username --pass password`
- **Theme**: `grip --theme dark`

## Code Implementation:
The server uses this flow:
1. Parse arguments in `main()` function
2. Create Flask app via `create_app()`
3. Start server with `app.run(host, port, ...)`

## Example Commands:
```bash
# Start on port 8080 with browser
grip --browser localhost:8080

# Start with authentication
grip --user admin --pass secret123 .

# Start with dark theme
grip --theme dark README.md
```
```

### Example 2: Code Pattern Query
**User**: "What design patterns are used in this codebase?"

**Agent Response**:
```
Based on my analysis, this codebase uses several key design patterns:

## 1. **Factory Pattern**
The `create_app()` function acts as a factory:
```python
def create_app(path=None, user_content=False, ...):
    # Chooses appropriate reader
    if text is not None:
        source = TextReader(text, display_filename)
    elif path == '-':
        source = StdinReader()
    else:
        source = DirectoryReader(path)
    
    # Chooses appropriate renderer
    if render_offline:
        renderer = OfflineRenderer(user_content, context)
    elif user_content or context or api_url:
        renderer = GitHubRenderer(user_content, context, api_url)
```

## 2. **Strategy Pattern**
Different readers handle different input sources:
- `TextReader`: For direct text input
- `StdinReader`: For piped input
- `DirectoryReader`: For file/directory input

## 3. **Template Method Pattern**
The `Grip` class extends Flask with a consistent run pattern while allowing customization.

These patterns provide flexibility and maintainability for different use cases.
```

## 🔍 Technical Details

### Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Input    │───▶│  Kodit Agent    │───▶│    GPT-4o       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │ Kodit MCP Server│
                       │   (stdio mode)  │
                       └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │ Indexed Codebase│
                       │  (109 snippets) │
                       └─────────────────┘
```

### Communication Flow

1. **User Query** → Agent receives question
2. **MCP Search** → Agent queries Kodit for relevant code
3. **Context Building** → Search results formatted for GPT-4o
4. **LLM Processing** → GPT-4o analyzes code and generates response
5. **Response** → Formatted answer returned to user

### Error Handling

The agent includes comprehensive error handling:

- **MCP Connection Errors**: Graceful fallback with helpful messages
- **OpenAI API Errors**: Retry logic and clear error reporting
- **Invalid Input**: Validation and user guidance
- **Process Cleanup**: Proper resource cleanup on exit

## 🛠 Troubleshooting

### Common Issues

#### 1. "kodit command not found"
```bash
# Solution: Install or reinstall Kodit
uv tool install .
export PATH="$HOME/.local/bin:$PATH"
```

#### 2. "Invalid OpenAI API key"
```bash
# Solution: Check key format
echo $OPENAI_API_KEY  # Should start with 'sk-'
```

#### 3. "MCP server failed to start"
```bash
# Solution: Test Kodit manually
kodit stdio  # Should start without errors (Ctrl+C to exit)
```

#### 4. "No indexed repositories"
```bash
# Solution: Index a codebase first
kodit index /path/to/your/code
```

### Debug Mode

Enable verbose logging for troubleshooting:

```bash
python kodit_agent.py --api-key YOUR_KEY --verbose --query "test query"
```

This shows:
- MCP communication details
- Search request/response data
- GPT-4o API calls
- Timing information

## 🔒 Security Considerations

### API Key Protection
- Never commit API keys to version control
- Use environment variables or secure credential storage
- Rotate keys regularly
- Monitor usage on OpenAI dashboard

### Data Privacy
- Code snippets are sent to OpenAI for analysis
- Consider using GPT-4o models with data processing agreements
- For sensitive code, consider self-hosted alternatives

## 📊 Performance

### Typical Response Times
- **MCP Search**: 1-3 seconds (depends on index size)
- **GPT-4o Processing**: 2-5 seconds (depends on complexity)
- **Total Query Time**: 3-8 seconds

### Optimization Tips
1. **Specific Queries**: More targeted questions get faster, better results
2. **Conversation History**: Follow-up questions leverage context efficiently
3. **Model Selection**: `gpt-4o-mini` is faster but less capable than `gpt-4o`

## 🚀 Advanced Usage

### Custom System Prompts

Modify the `system_prompt` in `KoditAgent` class to customize behavior:

```python
self.system_prompt = """You are a security-focused code assistant...
Focus on identifying potential vulnerabilities and security best practices..."""
```

### Integration with IDEs

The agent can be integrated into development workflows:

```bash
# VS Code integration example
{
    "terminal.integrated.profiles.linux": {
        "Kodit Agent": {
            "path": "python",
            "args": ["kodit_agent.py", "--api-key", "$OPENAI_API_KEY", "--interactive"]
        }
    }
}
```

### Batch Processing

Process multiple queries from a file:

```bash
# Create queries.txt with one question per line
while IFS= read -r query; do
    python kodit_agent.py --api-key "$OPENAI_API_KEY" --query "$query"
    echo "---"
done < queries.txt
```

## 🤝 Contributing

To extend the agent:

1. **Add new MCP tools**: Extend `KoditMCPClient` class
2. **Customize prompts**: Modify system prompts for domain-specific use
3. **Add output formats**: Implement different response formatters
4. **Enhance UI**: Add rich terminal output or web interface

## 📚 Additional Resources

- **Kodit Documentation**: See main README.md for Kodit setup
- **OpenAI API Docs**: https://platform.openai.com/docs
- **MCP Protocol**: https://spec.modelcontextprotocol.io/
- **Python Asyncio**: https://docs.python.org/3/library/asyncio.html

---

This agent demonstrates the power of combining specialized retrieval systems (Kodit) with general-purpose LLMs (GPT-4o) to create intelligent, code-aware assistants that understand your specific codebase context. 