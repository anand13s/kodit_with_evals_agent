<p align="center">
    <a href="https://docs.helix.ml/kodit/"><img src="https://docs.helix.ml/images/helix-kodit-logo.png" alt="Helix Kodit Logo" width="300"></a>
</p>

<h1 align="center">
Kodit: A Code Indexing MCP Server
</h1>

<p align="center">
Kodit connects your AI coding assistant to external codebases to provide accurate and up-to-date snippets of code.
</p>

<div align="center">

[![Documentation](https://img.shields.io/badge/Documentation-6B46C1?style=for-the-badge&logo=readthedocs&logoColor=white)](https://docs.helix.ml/kodit/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg?style=for-the-badge)](./LICENSE)
[![Discussions](https://img.shields.io/badge/Discussions-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/helixml/kodit/discussions)

</div>

:star: _Help us reach more developers and grow the Helix community. Star this repo!_

**Helix Kodit** is an **MCP server** that connects your AI coding assistant to external codebases. It can:

- Improve your AI-assisted code by providing canonical examples direct from the source
- Index local and public codebases
- Integrates with any AI coding assistant via MCP
- Search using keyword and semantic search
- Integrate with any OpenAI-compatible or custom API/model

If you're an engineer working with AI-powered coding assistants, Kodit helps by
providing relevant and up-to-date examples of your task so that LLMs make less mistakes
and produce fewer hallucinations.

## Features

### Codebase Indexing

Kodit connects to a variety of local and remote codebases to build an index of your
code. This index is used to build a snippet library, ready for ingestion into an LLM.

- Index local directories and public Git repositories
- Build comprehensive snippet libraries for LLM ingestion
- Support for 20+ programming languages including Python, JavaScript/TypeScript, Java, Go, Rust, C/C++, C#, HTML/CSS, and more
- Advanced code analysis with dependency tracking and call graph generation
- Intelligent snippet extraction with context-aware dependencies
- Efficient indexing with selective reindexing (only processes modified files)
- Privacy first: respects .gitignore and .noindex files
- **NEW in 0.3**: Auto-indexing configuration for shared server deployments
- **NEW in 0.3**: Enhanced Git provider support including Azure DevOps
- **NEW in 0.3**: Index private repositories via a PAT
- **NEW in 0.3**: Improved progress monitoring and reporting during indexing
- **NEW in 0.3**: Advanced code slicing infrastructure with Tree-sitter parsing
- **NEW in 0.4**: Automatic periodic sync to keep indexes up-to-date

### MCP Server

Relevant snippets are exposed to an AI coding assistant via an MCP server. This allows
the assistant to request relevant snippets by providing keywords, code, and semantic
intent. Kodit has been tested to work well with:

- Seamless integration with popular AI coding assistants
- Tested and verified with:
  - [Cursor](https://docs.helix.ml/kodit/getting-started/integration/#integration-with-cursor)
  - [Cline](https://docs.helix.ml/kodit/getting-started/integration/#integration-with-cline)
- Please contribute more instructions! ... any other assistant is likely to work ...
- **New in 0.3**: Advanced search filters by source, language, author, date range, and file path
- **New in 0.3**: Hybrid search combining BM25 keyword search with semantic search
- **New in 0.4**: Enhanced MCP tools with rich context parameters and metadata

### Hosted MCP Server

**New in 0.4**: Try Kodit instantly with our hosted MCP server at [https://kodit.helix.ml/mcp](https://kodit.helix.ml/mcp)! No installation required - just add it to your AI coding assistant and start searching popular codebases immediately.

The hosted server provides:

- Pre-indexed popular open source repositories
- Zero configuration - works out of the box
- Same powerful search capabilities as self-hosted Kodit
- Perfect for trying Kodit before setting up your own instance

Find out more in the [hosted Kodit documentation](https://docs.helix.ml/kodit/reference/hosted-kodit/).

### Enterprise Ready

Out of the box, Kodit works with a local SQLite database and very small, local models.
But enterprises can scale out with performant databases and dedicated models. Everything
can even run securely, privately, with on-premise LLM platforms like
[Helix](https://helix.ml).

Supported databases:

- SQLite
- [Vectorchord](https://github.com/tensorchord/VectorChord)

Supported providers:

- Local (which uses tiny CPU-only open-source models)
- OpenAI
- Secure, private LLM enclave with [Helix](https://helix.ml).
- Any other OpenAI compatible API

**NEW in 0.3**: Enhanced deployment options:

- Docker Compose configurations with VectorChord
- Kubernetes manifests for production deployments

## Quick Start

1. [Install Kodit](https://docs.helix.ml/kodit/getting-started/installation/)
2. [Index codebases](https://docs.helix.ml/kodit/getting-started/quick-start/)
3. [Integrate with your coding assistant](https://docs.helix.ml/kodit/getting-started/integration/)

### Documentation

- [Getting Started Guide](https://docs.helix.ml/kodit/getting-started/)
- [Reference Guide](https://docs.helix.ml/kodit/reference/)
- [Contribution Guidelines](.github/CONTRIBUTING.md)

## RAG Evaluation Framework

Kodit includes a comprehensive evaluation framework to assess the quality and effectiveness of its RAG (Retrieval-Augmented Generation) capabilities. The evaluation uses real-world question-answer pairs to test code retrieval and response quality.

### 📊 Evaluation Overview

The evaluation framework:
- **Test Dataset**: Uses the [grip_qa repository](https://github.com/helixml/grip_qa) containing real Q&A pairs about the Grip application
- **Target Codebase**: Evaluates against the `grip-no-tests` codebase (Grip application without test files)
- **Metrics**: Measures similarity, keyword overlap, answer quality, and retrieval performance
- **No Dependencies**: Simplified implementation that doesn't require external ML libraries

### 🚀 Quick Start - Running the Evaluation

#### Prerequisites
1. **Kodit installed and working** (see installation instructions above)
2. **grip_qa repository** cloned to `/home/user/github/grip_qa` (adjust path as needed)
3. **Target codebase indexed** in Kodit

#### Step 1: Index Target Codebase
```bash
# Index the grip-no-tests repository (or your target codebase)
kodit index /path/to/grip-no-tests
```

#### Step 2: Clone Test Questions Repository
```bash
# Clone the grip_qa repository containing test questions and answers
git clone https://github.com/helixml/grip_qa.git /home/user/github/grip_qa
```

#### Step 3: Run Evaluation
```bash
# Run the evaluation test
python3 simple_rag_evaluation.py
```

### 📋 Evaluation Results

#### Test Configuration
- **Test Cases**: 10 real-world Q&A pairs from grip_qa repository
- **Categories**: Usage commands, function documentation, legal/licensing questions
- **Target**: grip-no-tests codebase (42 files, 5 languages, 109 searchable snippets)

#### Performance Results
```
📊 Overall Results:
   Total Test Cases: 10
   Successful Retrievals: 10/10 (100% success rate)
   Average Retrieval Time: 1.93 seconds per query
```

#### Quality Metrics
```
🎯 Quality Metrics:
   Similarity Score: 0.0273 (Text similarity between expected/generated answers)
   Keyword Overlap: 0.0444 (Keyword overlap between expected/generated answers)  
   Quality Score: 0.42 (Overall answer coherence and relevance)
```

#### Category Breakdown
- **USAGE**: 6/6 (100%) - Questions about command usage and application startup
- **FUNCTION**: 2/2 (100%) - Questions about specific function documentation  
- **LEGAL**: 2/2 (100%) - Questions about licensing and distribution permissions

### 🔍 Example Test Cases and Results

#### Example 1: Command Usage Query
**Question**: "What command should I use to start the Grip application?"
**Kodit Response**: 
```
Found grip.command_line module with start_server function that handles:
- Host and port configuration
- SSL certificate options  
- Browser auto-start functionality
- Command line argument parsing
```
**Result**: ✅ Successfully retrieved relevant code snippets about command line interface

#### Example 2: Function Documentation Query  
**Question**: "What does the browser.py module do?"
**Kodit Response**:
```
browser.py provides browser automation functionality:
- start_browser(url): Opens URLs in web browser
- wait_and_start_browser(): Waits for server availability then opens browser
- Error handling for browser operations
```
**Result**: ✅ Accurately identified and described browser automation functionality

### 📁 Output Files

The evaluation generates detailed reports in the `simple_rag_results/` directory:

- **`simple_rag_evaluation_YYYYMMDD_HHMMSS.json`**: Complete evaluation data in JSON format
- **`simple_rag_summary_YYYYMMDD_HHMMSS.txt`**: Human-readable summary report

### 🎯 Interpreting Results

**Success Rate**: Measures how many queries successfully retrieve relevant code snippets
- ✅ **100%** indicates robust retrieval capabilities

**Quality Scores**: 
- **Similarity Score**: Low scores (0.02-0.05) are expected since Kodit returns code snippets while test answers contain prose explanations
- **Quality Score**: Measures answer coherence (0.4+ indicates good structured responses)
- **Keyword Overlap**: Measures topic relevance between queries and responses

**Performance**:
- **~2 seconds per query** demonstrates efficient search across indexed codebase
- **Consistent retrieval** shows reliable MCP server operation

### 🔧 Customizing the Evaluation

To run evaluation on your own codebase:

1. **Index your codebase**: `kodit index /path/to/your/code`
2. **Update paths** in `simple_rag_evaluation.py`:
   ```python
   GRIP_QA_PATH = "/path/to/your/qa/repository"
   ```
3. **Create your own Q&A pairs** following the grip_qa format:
   - `NNNN.q.md`: Question files
   - `NNNN.a.md`: Corresponding answer files

## Kodit MCP Agent - Intelligent Code Assistant

Kodit includes a powerful MCP agent that combines the retrieval capabilities of Kodit with the reasoning power of GPT-4o, creating an intelligent code assistant that understands your specific codebase.

### 🎯 What is the Kodit MCP Agent?

The agent is a Python application that:
- **Connects to Kodit MCP server** via stdio protocol for code search
- **Integrates with GPT-4o** for intelligent analysis and responses  
- **Provides interactive chat** for natural language codebase exploration
- **Offers both chat and single-query modes** for different workflows

### 🚀 Quick Start

#### Prerequisites
- **Kodit installed and working** (see installation above)
- **OpenAI API key** with GPT-4o access
- **Python 3.8+** for async support

#### Setup
```bash
# Install dependencies
pip install openai

# Test basic functionality (no API key required)
python demo_kodit_agent.py

# Interactive chat with your codebase
python kodit_agent.py --api-key YOUR_OPENAI_API_KEY --interactive
```

### 💬 Example Usage

#### Interactive Chat Mode
```bash
python kodit_agent.py --api-key YOUR_KEY --interactive
```

**Sample Conversation:**
```
You: How does the server start in this application?

🤖 Agent: Based on the codebase analysis, the server starts through:

1. **Main Entry Point** (grip/command.py):
   - Parses command line arguments with docopt
   - Handles configuration for host, port, theme, etc.
   - Calls serve() function to start the actual server

2. **Server Creation** (grip/api.py):
   ```python
   def serve(path=None, host=None, port=None, ...):
       app = create_app(path, user_content, context, ...)
       app.run(host, port, open_browser=browser)
   ```

3. **Application Factory**:
   - create_app() uses factory pattern to configure readers, renderers
   - Supports TextReader, StdinReader, DirectoryReader
   - Handles authentication, theming, and browser integration

You can start it with: `grip [options] [<path>] [<hostname>:]<port>`

You: What about error handling?

🤖 Agent: The application implements comprehensive error handling...
```

#### Single Query Mode
```bash
python kodit_agent.py --api-key YOUR_KEY --query "How does authentication work?"
```

### 🔧 Configuration Options

| Option | Description | Example |
|--------|-------------|---------|
| `--api-key` | OpenAI API key (required) | `sk-...` |
| `--model` | GPT model to use | `gpt-4o`, `gpt-4o-mini` |
| `--query` | Single query mode | `"Find error handling code"` |
| `--interactive` | Chat mode | Use for conversations |
| `--verbose` | Debug logging | Shows MCP communication |

### 🎯 Use Cases

**Architecture Understanding**: "What is the overall structure of this application?"
**Debugging Help**: "Show me error handling patterns in this codebase"  
**API Documentation**: "List all endpoints and their purposes"
**Security Analysis**: "How is authentication implemented?"
**Code Patterns**: "What design patterns are used here?"

### 📁 Files

- **`kodit_agent.py`**: Main agent with GPT-4o integration
- **`demo_kodit_agent.py`**: Demo script (no API key required)
- **`kodit_agent_requirements.txt`**: Python dependencies
- **`KODIT_AGENT_GUIDE.md`**: Comprehensive documentation

### 🔍 How It Works

```
User Question → Kodit MCP Search → GPT-4o Analysis → Intelligent Response
     ↓              ↓                    ↓              ↓
"How does X work?" → Code Snippets → Contextual Analysis → Actionable Answer
```

The agent first searches your indexed codebase for relevant code, then uses GPT-4o to analyze the results and provide intelligent, context-aware responses about your specific code.

### 🎊 Demo Without API Key

Test the MCP integration without OpenAI:

```bash
python demo_kodit_agent.py
```

This shows:
- ✅ MCP server connection
- ✅ Available tools discovery  
- ✅ Code search functionality
- ✅ Version information retrieval

**Ready to use with a real API key for full GPT-4o powered assistance!**

## Roadmap

The roadmap is currently maintained as a [Github Project](https://github.com/orgs/helixml/projects/4).

## 💬 Support

For commercial support, please contact [Helix.ML](founders@helix.ml). To ask a question,
please [open a discussion](https://github.com/helixml/kodit/discussions).

## License

[Apache 2.0 © 2025 HelixML, Inc.](./LICENSE)
