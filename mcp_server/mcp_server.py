from fastmcp import FastMCP

my_mcp = FastMCP("My MCP server")

@my_mcp.tool()
def add_two_number(a,b):
    """This functions adds 2 numbers"""
    c = a + b
    return f"{a} + {b} = {c}"

@my_mcp.tool()
def greet_person(name):
    """This functions greets the user"""
    return f"Hi {name}, Welcome to MCP"

if __name__ == "__main__":
    print("MCP Server running...")
    my_mcp.run()
