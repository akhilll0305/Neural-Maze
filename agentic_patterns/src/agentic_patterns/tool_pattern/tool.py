"""
Tool abstraction for function calling.

This module provides the core building blocks for creating LLM-callable tools:
1. Automatic function signature extraction
2. Type validation and conversion
3. Tool wrapper class
4. Decorator for easy tool creation

The Tool Pattern allows LLMs to CALL Python functions to get real-world data.
"""

import json
from typing import Callable


def get_fn_signature(fn: Callable) -> dict:
    """
    Automatically generates a JSON schema for a function.
    
    WHY THIS EXISTS:
    - LLMs need to know what functions are available
    - They need to know what parameters each function takes
    - This auto-generates that info from the function itself!
    
    HOW IT WORKS:
    - Reads the function name
    - Reads the docstring (becomes the description)
    - Reads type annotations (like `location: str`) to know parameter types
    
    Args:
        fn (Callable): The Python function to analyze
    
    Returns:
        dict: A schema describing the function
        
    Example:
        >>> def add(a: int, b: int):
        ...     '''Add two numbers'''
        ...     return a + b
        >>> get_fn_signature(add)
        {
            "name": "add",
            "description": "Add two numbers",
            "parameters": {
                "properties": {
                    "a": {"type": "int"},
                    "b": {"type": "int"}
                }
            }
        }
    """
    # Start building the signature dictionary
    fn_signature: dict = {
        "name": fn.__name__,                    # Function name
        "description": fn.__doc__,              # Docstring as description
        "parameters": {"properties": {}},       # Will hold parameter info
    }
    
    # Extract parameter types from type annotations
    # fn.__annotations__ = {"a": int, "b": int, "return": int}
    # We skip "return" because we only care about input parameters
    schema = {
        k: {"type": v.__name__}  # Convert int -> "int", str -> "str"
        for k, v in fn.__annotations__.items()
        if k != "return"  # Ignore the return type
    }
    
    fn_signature["parameters"]["properties"] = schema
    return fn_signature


def validate_arguments(tool_call: dict, tool_signature: dict) -> dict:
    """
    Validates and converts tool call arguments to the correct types.
    
    WHY THIS EXISTS:
    - LLMs might return "5" (string) when we need 5 (integer)
    - This ensures arguments match the expected types
    - Prevents crashes from type mismatches
    
    Args:
        tool_call (dict): The tool call from the LLM with arguments
        tool_signature (dict): The expected function signature
    
    Returns:
        dict: The tool call with arguments converted to correct types
    
    Example:
        >>> tool_call = {"name": "add", "arguments": {"a": "5", "b": "3"}}
        >>> signature = {"parameters": {"properties": {"a": {"type": "int"}, "b": {"type": "int"}}}}
        >>> validate_arguments(tool_call, signature)
        {"name": "add", "arguments": {"a": 5, "b": 3}}  # Strings converted to ints!
    """
    properties = tool_signature["parameters"]["properties"]
    
    # Map type names to actual Python types
    type_mapping = {
        "int": int,
        "str": str,
        "bool": bool,
        "float": float,
    }
    
    # Check each argument and convert if needed
    for arg_name, arg_value in tool_call["arguments"].items():
        expected_type = properties[arg_name].get("type")
        
        # If the value is not the right type, convert it
        if not isinstance(arg_value, type_mapping[expected_type]):
            tool_call["arguments"][arg_name] = type_mapping[expected_type](arg_value)
    
    return tool_call


class Tool:
    """
    A wrapper that makes a Python function callable by an LLM.
    
    WHY THIS EXISTS:
    - Bundles the function with its signature
    - Makes it easy to pass tools to the agent
    - Provides a clean interface for running tools
    
    Attributes:
        name (str): The function name
        fn (Callable): The actual Python function
        fn_signature (str): JSON string describing the function
    
    Example:
        >>> def greet(name: str):
        ...     '''Greet someone'''
        ...     return f"Hello, {name}!"
        >>> sig = get_fn_signature(greet)
        >>> tool = Tool("greet", greet, json.dumps(sig))
        >>> tool.run(name="Alice")
        "Hello, Alice!"
    """
    
    def __init__(self, name: str, fn: Callable, fn_signature: str):
        """
        Initialize a Tool.
        
        Args:
            name (str): Name of the tool
            fn (Callable): The function to wrap
            fn_signature (str): JSON signature of the function
        """
        self.name = name
        self.fn = fn
        self.fn_signature = fn_signature
    
    def __str__(self):
        """Return the function signature when printing the tool."""
        return self.fn_signature
    
    def run(self, **kwargs):
        """
        Execute the tool with the provided arguments.
        
        Args:
            **kwargs: Keyword arguments to pass to the function
        
        Returns:
            The result of the function call
        
        Example:
            >>> tool.run(name="Bob")
            "Hello, Bob!"
        """
        return self.fn(**kwargs)


def tool(fn: Callable):
    """
    Decorator to turn any Python function into an LLM-callable Tool.
    
    WHY THIS IS AWESOME:
    - One line (@tool) transforms any function into a tool!
    - Automatically extracts signature
    - No manual configuration needed
    
    Args:
        fn (Callable): The function to convert to a tool
    
    Returns:
        Tool: A Tool object wrapping the function
    
    Example:
        >>> @tool
        ... def add(a: int, b: int):
        ...     '''Add two numbers together'''
        ...     return a + b
        >>> 
        >>> # Now 'add' is a Tool object, not just a function!
        >>> add.name
        'add'
        >>> add.run(a=5, b=3)
        8
    """
    def wrapper():
        # Generate the function signature automatically
        fn_signature = get_fn_signature(fn)
        
        # Create and return a Tool object
        return Tool(
            name=fn_signature.get("name"),
            fn=fn,
            fn_signature=json.dumps(fn_signature)
        )
    
    return wrapper()


# ============================================================================
# EXAMPLE USAGE (for learning purposes)
# ============================================================================
if __name__ == "__main__":
    print("=" * 80)
    print("Testing Tool Creation")
    print("=" * 80)
    
    # Example 1: Create a simple calculator tool
    @tool
    def calculator(a: int, b: int, operation: str):
        """
        Perform a mathematical operation on two numbers.
        
        Args:
            a (int): First number
            b (int): Second number
            operation (str): Operation to perform (add, subtract, multiply, divide)
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
    
    print("\n1. Tool created:")
    print(f"   Name: {calculator.name}")
    print(f"   Signature:\n{json.dumps(json.loads(calculator.fn_signature), indent=2)}")
    
    print("\n2. Running the tool:")
    result = calculator.run(a=10, b=5, operation="add")
    print(f"   calculator(10, 5, 'add') = {result}")
    
    result = calculator.run(a=10, b=5, operation="multiply")
    print(f"   calculator(10, 5, 'multiply') = {result}")
    
    # Example 2: Test argument validation
    print("\n3. Testing argument validation:")
    tool_call = {
        "name": "calculator",
        "arguments": {"a": "15", "b": "3", "operation": "divide"}  # Note: a and b are strings
    }
    print(f"   Tool call (before validation): {tool_call}")
    
    validated = validate_arguments(tool_call, json.loads(calculator.fn_signature))
    print(f"   Tool call (after validation): {validated}")
    print(f"   Type of a: {type(validated['arguments']['a'])}")  # Should be int now
    
    print("\n" + "=" * 80)
    print("✅ Tool system is working!")
    print("=" * 80)
