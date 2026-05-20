import asyncio
from fastmcp import Client
import ollama

async def main():
    async with Client("mcp_server.py") as client:
        mcp_tools = await client.list_tools()
        print("The tools available to llama to choose from")

        for tool in mcp_tools:
            print(f"  {tool.name} + {tool.description}")

        ollama_tools = []
        for tool in mcp_tools:
            ollama_tools.append({
                "type":"function",
                "function":{
                    "name" : tool.name,
                    "description":tool.description,
                    "parameter":tool.inputSchema
                }
            })
        print("Asking llama 3.2 question")

        response = ollama.chat(
            model="llama3.2",
            messages=[{"role": "user", "content": "Why is sky blue?"}],
            tools = ollama_tools
        )

        print("Llama is responding with this response" + response.message.content)
        print (f"Llama is selecting this tool   {response.message.tool_name}")

        if response.message.tool_calls:
            for tools in response.message.tool_calls:
                tool_name = tools.function.name
                tool_args = tools.function.arguments
                print(f"calling mcp tool {tool_name}")
                print(f"the arguements passed are {tool_args}")
                result = await client.call_tool(tool_name, tool_args)
                print(f"mcp server retrned with content {result.content[0].text}")
        else:
            print("ollama gave answer and not mcp")


asyncio.run(main())

            



    