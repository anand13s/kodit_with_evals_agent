#!/usr/bin/env python3
"""
Demo script for Kodit MCP Agent - shows MCP integration without requiring real OpenAI API key
"""

import asyncio
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kodit_agent import KoditMCPClient

async def demo_mcp_integration():
    """Demonstrate the MCP integration capabilities"""
    print("🚀 Kodit MCP Agent Demo")
    print("=" * 50)
    print("This demo shows the MCP integration without requiring OpenAI API key")
    print()
    
    # Initialize MCP client
    mcp_client = KoditMCPClient()
    
    try:
        # Start MCP server
        print("📡 Starting Kodit MCP server...")
        success = await mcp_client.start()
        
        if not success:
            print("❌ Failed to start MCP server")
            print("   Make sure 'kodit' is installed and in PATH")
            return
        
        print("✅ MCP server started successfully")
        
        # List available tools
        print("\n🔧 Listing available tools...")
        tools_response = await mcp_client.list_tools()
        
        if tools_response.success:
            tools = tools_response.result.get('tools', [])
            print(f"📋 Available tools: {[tool['name'] for tool in tools]}")
            
            for tool in tools:
                print(f"   • {tool['name']}: {tool.get('description', 'No description')}")
        else:
            print(f"❌ Failed to list tools: {tools_response.error}")
            return
        
        # Test search functionality
        print("\n🔍 Testing search functionality...")
        search_response = await mcp_client.search(
            "What does the browser.py module do?",
            keywords=["browser", "module", "function"]
        )
        
        if search_response.success:
            print("✅ Search completed successfully")
            result = search_response.result
            
            if isinstance(result, list) and len(result) > 0:
                print(f"📊 Found {len(result)} results:")
                for i, item in enumerate(result[:3], 1):  # Show first 3
                    if isinstance(item, dict):
                        print(f"   {i}. File: {item.get('path', 'Unknown')}")
                        print(f"      Language: {item.get('lang', 'Unknown')}")
                        print(f"      Score: {item.get('score', 'N/A')}")
                        if item.get('summary'):
                            print(f"      Summary: {item['summary'][:100]}...")
                        print()
            else:
                print("📝 Search returned:", result)
        else:
            print(f"❌ Search failed: {search_response.error}")
        
        # Test version functionality
        print("🔖 Testing version functionality...")
        version_response = await mcp_client.get_version()
        
        if version_response.success:
            print(f"✅ Version check successful: {version_response.result}")
        else:
            print(f"❌ Version check failed: {version_response.error}")
        
        print("\n🎯 Demo Complete!")
        print("=" * 50)
        print("The MCP integration is working correctly.")
        print("To use with GPT-4o, provide a real OpenAI API key:")
        print("  python kodit_agent.py --api-key YOUR_REAL_API_KEY --interactive")
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
    finally:
        # Cleanup
        await mcp_client.stop()

if __name__ == "__main__":
    asyncio.run(demo_mcp_integration()) 