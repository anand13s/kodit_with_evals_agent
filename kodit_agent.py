#!/usr/bin/env python3
"""
Kodit MCP Agent - An intelligent code assistant powered by GPT-4o and Kodit MCP Server

This agent provides an interactive interface to query codebases indexed by Kodit,
combining the retrieval capabilities of Kodit with the reasoning power of GPT-4o.

Features:
- Interactive chat interface with GPT-4o
- Seamless integration with Kodit MCP server via stdio
- Intelligent code search and analysis
- Context-aware responses with code examples
- Support for multiple search strategies (keyword, semantic, hybrid)

Usage:
    python kodit_agent.py --api-key YOUR_OPENAI_API_KEY
    python kodit_agent.py --api-key YOUR_OPENAI_API_KEY --interactive
    python kodit_agent.py --api-key YOUR_OPENAI_API_KEY --query "How does authentication work?"
"""

import asyncio
import json
import sys
import argparse
import subprocess
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import logging
from datetime import datetime

try:
    import openai
    from openai import OpenAI
except ImportError:
    print("Error: OpenAI library not found. Install with: pip install openai")
    sys.exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class MCPToolCall:
    """Represents an MCP tool call"""
    tool_name: str
    parameters: Dict[str, Any]

@dataclass
class MCPResponse:
    """Represents an MCP tool response"""
    success: bool
    result: Any
    error: Optional[str] = None

class KoditMCPClient:
    """Client for interacting with Kodit MCP server via stdio"""
    
    def __init__(self):
        self.process = None
        self.message_id = 0
        
    async def start(self):
        """Start the Kodit MCP server process"""
        try:
            self.process = await asyncio.create_subprocess_exec(
                'kodit', 'stdio',
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Initialize the MCP session
            init_request = {
                "jsonrpc": "2.0",
                "id": 0,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "clientInfo": {
                        "name": "kodit-agent",
                        "version": "1.0.0"
                    }
                }
            }
            
            # Send initialization
            init_data = json.dumps(init_request) + '\n'
            self.process.stdin.write(init_data.encode())
            await self.process.stdin.drain()
            
            # Read initialization response
            response_data = await self.process.stdout.readline()
            init_response = json.loads(response_data.decode().strip())
            
            if "error" in init_response:
                logger.error(f"Failed to initialize MCP: {init_response['error']}")
                return False
                
            # Send initialized notification
            initialized_request = {
                "jsonrpc": "2.0",
                "method": "notifications/initialized",
                "params": {}
            }
            
            init_notif_data = json.dumps(initialized_request) + '\n'
            self.process.stdin.write(init_notif_data.encode())
            await self.process.stdin.drain()
            
            logger.info("✅ Kodit MCP server started and initialized successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to start Kodit MCP server: {e}")
            return False
    
    async def send_request(self, method: str, params: Dict[str, Any]) -> MCPResponse:
        """Send a request to the MCP server"""
        if not self.process:
            return MCPResponse(False, None, "MCP server not started")
        
        self.message_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self.message_id,
            "method": method,
            "params": params
        }
        
        try:
            # Send request
            request_data = json.dumps(request) + '\n'
            self.process.stdin.write(request_data.encode())
            await self.process.stdin.drain()
            
            # Read response
            response_data = await self.process.stdout.readline()
            response = json.loads(response_data.decode().strip())
            
            if "error" in response:
                return MCPResponse(False, None, response["error"])
            
            return MCPResponse(True, response.get("result"))
            
        except Exception as e:
            logger.error(f"Error communicating with MCP server: {e}")
            return MCPResponse(False, None, str(e))
    
    async def list_tools(self) -> MCPResponse:
        """List available tools from the MCP server"""
        return await self.send_request("tools/list", {})
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> MCPResponse:
        """Call a tool using the MCP tools/call method"""
        params = {
            "name": tool_name,
            "arguments": arguments
        }
        return await self.send_request("tools/call", params)
    
    async def search(self, query: str, search_type: str = "keyword", **kwargs) -> MCPResponse:
        """Search the codebase using Kodit"""
        arguments = {
            "user_intent": query,
            "keywords": [query],
            "related_file_paths": [],
            "related_file_contents": []
        }
        arguments.update(kwargs)
        
        return await self.call_tool("search", arguments)
    
    async def get_version(self) -> MCPResponse:
        """Get Kodit version"""
        return await self.call_tool("get_version", {})
    
    async def stop(self):
        """Stop the MCP server"""
        if self.process:
            self.process.terminate()
            await self.process.wait()
            logger.info("🛑 Kodit MCP server stopped")

class KoditAgent:
    """Intelligent code assistant powered by GPT-4o and Kodit MCP"""
    
    def __init__(self, api_key: str, model: str = "gpt-4o"):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.mcp_client = KoditMCPClient()
        self.conversation_history = []
        
        # System prompt for the agent
        self.system_prompt = """You are an intelligent code assistant powered by the Kodit MCP server. 
You help developers understand, navigate, and work with codebases by:

1. **Code Search & Analysis**: Use the Kodit MCP tools to search for relevant code snippets
2. **Contextual Understanding**: Provide insights about code structure, patterns, and relationships
3. **Practical Guidance**: Give actionable advice for development tasks
4. **Code Examples**: Show relevant code examples from the indexed codebase

Available MCP Tools:
- kodit.search: Search the codebase with semantic understanding
- kodit.get_version: Get Kodit version information

When users ask about code, always:
1. Use Kodit search to find relevant code snippets
2. Analyze the retrieved code to provide comprehensive answers
3. Include specific code examples and explanations
4. Suggest related areas to explore

Be helpful, accurate, and provide code-focused responses with concrete examples."""

    async def initialize(self) -> bool:
        """Initialize the agent and MCP connection"""
        logger.info("🚀 Initializing Kodit Agent...")
        success = await self.mcp_client.start()
        if success:
            # List available tools to verify connection
            tools_response = await self.mcp_client.list_tools()
            if tools_response.success:
                logger.info(f"✅ Connected to Kodit MCP server")
                if tools_response.result and 'tools' in tools_response.result:
                    tools = [tool['name'] for tool in tools_response.result['tools']]
                    logger.info(f"📋 Available tools: {tools}")
                return True
            else:
                logger.error("❌ Failed to list MCP tools")
                return False
        return False
    
    async def search_codebase(self, user_query: str, **search_params) -> str:
        """Search the codebase and format results for the LLM"""
        logger.info(f"🔍 Searching codebase for: {user_query}")
        
        response = await self.mcp_client.search(
            query=user_query,
            user_intent=user_query,
            keywords=[user_query],
            **search_params
        )
        
        if response.success and response.result:
            # Format search results for LLM consumption
            results = response.result
            formatted_results = f"## Search Results for: '{user_query}'\n\n"
            
            if isinstance(results, list):
                for i, result in enumerate(results[:5], 1):  # Limit to top 5 results
                    if isinstance(result, dict):
                        formatted_results += f"### Result {i}\n"
                        formatted_results += f"**File**: {result.get('path', 'Unknown')}\n"
                        formatted_results += f"**Language**: {result.get('lang', 'Unknown')}\n"
                        formatted_results += f"**Score**: {result.get('score', 'N/A')}\n"
                        formatted_results += f"**Code**:\n```{result.get('lang', '')}\n{result.get('code', '')}\n```\n"
                        if result.get('summary'):
                            formatted_results += f"**Summary**: {result['summary']}\n"
                        formatted_results += "\n---\n\n"
            else:
                formatted_results += f"Search returned: {results}\n"
            
            return formatted_results
        else:
            error_msg = response.error or "Unknown error"
            return f"❌ Search failed: {error_msg}"
    
    async def process_user_query(self, user_input: str) -> str:
        """Process user query with GPT-4o and MCP tools"""
        logger.info(f"💭 Processing query: {user_input}")
        
        # First, search the codebase for relevant information
        search_results = await self.search_codebase(user_input)
        
        # Add the search results to conversation context
        context_message = f"""User asked: "{user_input}"

Kodit search results:
{search_results}

Please analyze this code and provide a comprehensive response to the user's question."""
        
        # Build conversation messages
        messages = [
            {"role": "system", "content": self.system_prompt},
            *self.conversation_history,
            {"role": "user", "content": context_message}
        ]
        
        try:
            # Get response from GPT-4o
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=2000,
                temperature=0.7
            )
            
            assistant_response = response.choices[0].message.content
            
            # Update conversation history
            self.conversation_history.extend([
                {"role": "user", "content": user_input},
                {"role": "assistant", "content": assistant_response}
            ])
            
            # Keep conversation history manageable
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
            
            return assistant_response
            
        except Exception as e:
            logger.error(f"Error calling GPT-4o: {e}")
            return f"❌ Error processing query: {e}"
    
    async def interactive_chat(self):
        """Run interactive chat session"""
        print("\n🤖 Kodit Agent - Interactive Chat")
        print("=" * 50)
        print("Ask questions about your codebase. Type 'quit' or 'exit' to stop.")
        print("Type 'help' for available commands.\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if user_input.lower() == 'help':
                    self.show_help()
                    continue
                
                if not user_input:
                    continue
                
                print("🤖 Agent: Thinking...")
                response = await self.process_user_query(user_input)
                print(f"🤖 Agent: {response}\n")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def show_help(self):
        """Show help information"""
        help_text = """
📚 Kodit Agent Commands:
- Ask any question about your codebase
- 'help' - Show this help message
- 'quit', 'exit', 'q' - Exit the agent

💡 Example queries:
- "How does authentication work in this codebase?"
- "Show me functions that handle file uploads"
- "What are the main API endpoints?"
- "How is error handling implemented?"
- "Find database connection logic"
"""
        print(help_text)
    
    async def cleanup(self):
        """Cleanup resources"""
        await self.mcp_client.stop()

async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Kodit MCP Agent - Intelligent code assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python kodit_agent.py --api-key sk-... --interactive
  python kodit_agent.py --api-key sk-... --query "How does the server start?"
  python kodit_agent.py --api-key sk-... --query "Find error handling code" --model gpt-4o-mini
        """
    )
    
    parser.add_argument(
        '--api-key', 
        required=True,
        help='OpenAI API key (required)'
    )
    
    parser.add_argument(
        '--model',
        default='gpt-4o',
        help='OpenAI model to use (default: gpt-4o)'
    )
    
    parser.add_argument(
        '--query',
        help='Single query to process (non-interactive mode)'
    )
    
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Run in interactive chat mode (default if no --query)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Validate API key format
    if not args.api_key.startswith('sk-'):
        print("❌ Error: Invalid OpenAI API key format. Should start with 'sk-'")
        sys.exit(1)
    
    # Initialize agent
    agent = KoditAgent(args.api_key, args.model)
    
    try:
        # Initialize MCP connection
        if not await agent.initialize():
            print("❌ Failed to initialize Kodit MCP connection")
            print("   Make sure 'kodit' is installed and working:")
            print("   kodit --version")
            sys.exit(1)
        
        if args.query:
            # Single query mode
            print(f"🔍 Processing query: {args.query}")
            response = await agent.process_user_query(args.query)
            print(f"\n🤖 Response:\n{response}")
        else:
            # Interactive mode
            await agent.interactive_chat()
            
    except KeyboardInterrupt:
        print("\n👋 Interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"❌ Unexpected error: {e}")
    finally:
        await agent.cleanup()

if __name__ == "__main__":
    asyncio.run(main()) 