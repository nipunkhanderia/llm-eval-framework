import ollama
import json
from fastmcp import Client
import asyncio

async def main():
    async with Client("simple_mcp.py") as client:
        
        # Get tools from MCP server
        mcp_tools = await client.list_tools()
        
        print("🔧 Tools available on MCP server:")
        for tool in mcp_tools:
            print(f"   - {tool.name}: {tool.description}")

        # ✅ Convert MCP tools → Ollama tool format manually
        ollama_tools = []
        for tool in mcp_tools:
            ollama_tools.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema  # MCP already gives us JSON schema
                }
            })

        print("\n💬 Asking Llama3.2 a question...")
        
        response = ollama.chat(
            model="llama3.2",
            messages=[{"role": "user", "content": "Can you add 42 and 58 for me?"}],
            tools=ollama_tools  # ✅ now in correct format
        )
        
        print(f"🤖 Llama's response: {response.message.content}")
        print(f"🤖 Llama wants to call: {response.message.tool_calls}")
        
        # If Llama decided to use a tool, call it on MCP server
        if response.message.tool_calls:
            for tool_call in response.message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = tool_call.function.arguments
                
                print(f"\n🔌 Calling MCP tool: {tool_name} with args {tool_args}")
                result = await client.call_tool(tool_name, tool_args)
                print(f"✅ MCP server returned: {result.content[0].text}")
        else:
            print("\n⚠️ Llama didn't call any tool — it answered directly")

asyncio.run(main())