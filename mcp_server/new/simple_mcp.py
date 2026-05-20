from fastmcp import FastMCP

mcp = FastMCP("My First MCP Server")

@mcp.tool()
def add_numbers(a: int, b: int) -> str:
    """Adds two numbers together."""
    result = a + b
    return f"{a} + {b} = {result}"

@mcp.tool()
def greet_person(name: str) -> str:
    """Greets a person by name."""
    return f"Hello, {name}! Welcome to MCP."

if __name__ == "__main__":
    print("MCP Server running...")
    mcp.run()