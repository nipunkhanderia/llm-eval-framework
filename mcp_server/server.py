import ollama
import json
from fastmcp import Client
import asyncio

async def main():
    # Connect to your MCP server
    async with Client("mcp_server.py") as client:
        
        # Get the list of tools from the MCP server
        tools = await client.list_tools()
        print("🔧 Tools available on MCP server:")
        for tool in tools:
            print(f"   - {tool.name}: {tool.description}")
        
        print("\n💬 Asking Llama3.2 a question...")
        
        # Ask Llama a question
        response = ollama.chat(
            model="llama3.2",
            messages=[{"role": "user", "content": "Can you add 42 and 58 for me?"}],
            tools=tools  # give Llama the MCP tools
        )
        
        print(f"🤖 Llama wants to call: {response.message.tool_calls}")
        
        # If Llama wants to use a tool, call it on the MCP server
        if response.message.tool_calls:
            for tool_call in response.message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = tool_call.function.arguments
                
                print(f"\n🔌 Calling MCP tool: {tool_name} with args {tool_args}")
                result = await client.call_tool(tool_name, tool_args)
                print(f"✅ MCP server returned: {result.content[0].text}")

asyncio.run(main())