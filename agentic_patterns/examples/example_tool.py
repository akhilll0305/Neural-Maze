"""
Example: Using the Tool Pattern

This example demonstrates how an LLM can intelligently
decide when to call tools versus answering directly.
"""

from agentic_patterns.tool_pattern.tool_agent import ToolAgent
from agentic_patterns.tool_pattern.tool import tool


# ---------------------------------------------------------------------------
# Define Tools
# ---------------------------------------------------------------------------

@tool
def calculator(a: int, b: int, operation: str):
    """
    Perform a mathematical operation on two numbers.

    Args:
        a (int): First number
        b (int): Second number
        operation (str): add, subtract, multiply, divide
    """
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        return a / b if b != 0 else "Cannot divide by zero"
    else:
        return "Unknown operation"


@tool
def get_current_weather(location: str, unit: str):
    """
    Mock weather lookup.
    """
    return {"temperature": 25, "unit": unit, "location": location}


# ---------------------------------------------------------------------------
# Examples
# ---------------------------------------------------------------------------

def example_1_math():
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Math using Tool Pattern")
    print("=" * 80)

    agent = ToolAgent(tools=[calculator])

    result = agent.run("What is 15 multiplied by 3?")
    print("\nFINAL ANSWER:")
    print(result)


def example_2_weather():
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Weather Lookup")
    print("=" * 80)

    agent = ToolAgent(tools=[get_current_weather])

    result = agent.run("What is the weather in London in celsius?")
    print("\nFINAL ANSWER:")
    print(result)


def example_3_direct_answer():
    print("\n" + "=" * 80)
    print("EXAMPLE 3: No Tool Needed")
    print("=" * 80)

    agent = ToolAgent(tools=[calculator])

    result = agent.run("Explain what machine learning is.")
    print("\nFINAL ANSWER:")
    print(result)


if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════════╗
║                      TOOL PATTERN EXAMPLES                     ║
║                                                                ║
║  Watch how the LLM decides when to use tools!                 ║
║                                                                ║
║  Observe:                                                      ║
║  - When the tool is selected                                  ║
║  - How arguments are structured                                ║
║  - When it answers directly without tools                      ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
""")

    # Uncomment what you want to try
    example_1_math()
    # example_2_weather()
    # example_3_direct_answer()

    print("\n" + "=" * 80)
    print("🎓 KEY LEARNINGS:")
    print("=" * 80)
    print("""
1. LLMs can select tools intelligently
2. JSON schemas guide structured function calls
3. Argument validation prevents runtime crashes
4. Not every question requires a tool
5. Clean separation: tool selection vs final response
""")
