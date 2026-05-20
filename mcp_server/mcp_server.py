from fastmcp import FastMCP

my_mcp = FastMCP("My MCP server")

def add_two_number(a,b):
    c = a + b
    print("result ")
    return f"{a} + {b} = {c}"

print(add_two_number(1,2))
