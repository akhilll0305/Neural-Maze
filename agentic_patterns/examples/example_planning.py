"""
Example: Using the ReAct Planning Pattern

This example demonstrates how an agent:
- Thinks
- Acts (calls tools)
- Observes
- Repeats
Until it produces a final answer.
"""

from agentic_patterns.planning_pattern.react_agent import ReactAgent
from agentic_patterns.tool_pattern.tool import tool


# ---------------------------------------------------------------------------
# Define Tools
# ---------------------------------------------------------------------------

@tool
def calculator(a: int, b: int, operation: str):
    """
    Perform a mathematical operation on two numbers.
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

def example_1_single_step():
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Single Tool Reasoning")
    print("=" * 80)

    agent = ReactAgent(tools=[get_current_weather])

    result = agent.run("What is the weather in New York?")
    print("\nFINAL RESPONSE:")
    print(result)


def example_2_multi_step_reasoning():
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Multi-Step Planning")
    print("=" * 80)

    agent = ReactAgent(tools=[calculator, get_current_weather])

    result = agent.run(
        "What is the weather in Paris and what is 5 multiplied by 6?"
    )
    print("\nFINAL RESPONSE:")
    print(result)


def example_3_no_tool():
    print("\n" + "=" * 80)
    print("EXAMPLE 3: No Tool Required")
    print("=" * 80)

    agent = ReactAgent(tools=[calculator])

    result = agent.run("Explain what reinforcement learning is.")
    print("\nFINAL RESPONSE:")
    print(result)


if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════════╗
║                     REACT PATTERN EXAMPLES                     ║
║                                                                ║
║  Observe the Thought → Action → Observation loop!              ║
║                                                                ║
║  What to watch:                                                ║
║  - The reasoning step (<thought>)                              ║
║  - Structured tool calls (<tool_call>)                         ║
║  - Observations fed back into the model                        ║
║  - Loop stopping at <response>                                 ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
""")

    # Uncomment what you want to try
    example_1_single_step()
    # example_2_multi_step_reasoning()
    # example_3_no_tool()

    print("\n" + "=" * 80)
    print("🎓 KEY LEARNINGS:")
    print("=" * 80)
    print("""
1. ReAct separates reasoning from acting
2. The model plans before executing tools
3. Observations influence future reasoning
4. Looping enables multi-step problem solving
5. Max iteration limits prevent infinite loops
""")

    print("\n" + "=" * 80)
    print("🚀 NEXT STEP:")
    print("=" * 80)
    print("""
Try:
- Increasing max_rounds
- Adding more tools
- Asking multi-step reasoning questions
- Combining this with Reflection Pattern

Next: Multi-Agent Systems 🧑🏽‍🤝‍🧑🏻
""")
