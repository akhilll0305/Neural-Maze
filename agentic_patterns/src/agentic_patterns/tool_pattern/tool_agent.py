"""
Tool Pattern Agent

This module implements the ToolAgent - an LLM that can use external tools.

THE COMPLETE FLOW:
1. User asks a question
2. LLM sees available tools and decides if it needs to use any
3. LLM returns a tool call (if needed)
4. We execute the tool and get the result
5. We give the result back to the LLM
6. LLM answers the user with the tool's data

This allows LLMs to access the real world!
"""

import json
from colorama import Fore
from dotenv import load_dotenv
from groq import Groq

from agentic_patterns.tool_pattern.tool import Tool, validate_arguments
from agentic_patterns.utils.completions import build_prompt_structure
from agentic_patterns.utils.completions import ChatHistory
from agentic_patterns.utils.completions import completions_create
from agentic_patterns.utils.completions import update_chat_history
from agentic_patterns.utils.extraction import extract_tag_content

load_dotenv()


# This is the system prompt that tells the LLM how to use tools
TOOL_SYSTEM_PROMPT = """
You are a function calling AI model. You are provided with function signatures within <tools></tools> XML tags.
You may call one or more functions to assist with the user query. Don't make assumptions about what values to plug
into functions. Pay special attention to the properties 'types'. You should use those types as in a Python dict.
For each function call return a json object with function name and arguments within <tool_call></tool_call>
XML tags as follows:

<tool_call>
{"name": <function-name>, "arguments": <args-dict>, "id": <monotonically-increasing-id>}
</tool_call>

Here are the available tools:

<tools>
%s
</tools>
"""


class ToolAgent:
    """
    An LLM agent that can use external tools to answer questions.
    
    HOW IT WORKS:
    1. Initialize with a list of tools
    2. When user asks a question, LLM sees all available tools
    3. LLM decides if it needs to use a tool
    4. If yes, we parse the tool call, run the tool, and give result back
    5. LLM uses the result to answer the user
    
    Attributes:
        tools (list[Tool]): List of tools the agent can use
        model (str): The LLM model to use
        client (Groq): The Groq API client
        tools_dict (dict): Dictionary mapping tool names to Tool objects
    
    Example:
        >>> @tool
        ... def add(a: int, b: int):
        ...     '''Add two numbers'''
        ...     return a + b
        >>> 
        >>> agent = ToolAgent(tools=[add])
        >>> result = agent.run("What is 5 + 3?")
        >>> print(result)  # "The result is 8"
    """
    
    def __init__(
        self,
        tools: Tool | list[Tool],
        model: str = "llama-3.3-70b-versatile",
    ) -> None:
        """
        Initialize the ToolAgent with tools.
        
        Args:
            tools (Tool | list[Tool]): Single tool or list of tools
            model (str): The LLM model to use
        """
        self.client = Groq()
        self.model = model
        
        # Ensure tools is always a list
        self.tools = tools if isinstance(tools, list) else [tools]
        
        # Create a dictionary for quick tool lookup by name
        # Example: {"add": Tool(...), "calculator": Tool(...)}
        self.tools_dict = {tool.name: tool for tool in self.tools}
    
    def add_tool_signatures(self) -> str:
        """
        Collect all tool signatures into a single string.
        
        WHY THIS EXISTS:
        - The system prompt needs to list all available tools
        - This concatenates all tool signatures (JSON) into one string
        - The LLM reads this to know what tools it can use
        
        Returns:
            str: Concatenated JSON signatures of all tools
        
        Example:
            >>> # If we have two tools: add and multiply
            >>> agent.add_tool_signatures()
            '{"name":"add",...}{"name":"multiply",...}'
        """
        return "".join([tool.fn_signature for tool in self.tools])
    
    def process_tool_calls(self, tool_calls_content: list) -> dict:
        """
        Execute all tool calls and collect the results.
        
        WHY THIS EXISTS:
        - LLM might call multiple tools at once
        - We need to run each tool and collect all results
        - Results are stored by tool call ID so LLM knows which is which
        
        THE PROCESS:
        1. Parse each tool call (JSON string → Python dict)
        2. Validate arguments (ensure correct types)
        3. Run the tool
        4. Store the result with its ID
        
        Args:
            tool_calls_content (list): List of tool call JSON strings
        
        Returns:
            dict: Mapping of tool call IDs to their results
        
        Example:
            >>> # LLM says: "Call add(5, 3) with id=0"
            >>> tool_calls = ['{"name":"add","arguments":{"a":5,"b":3},"id":0}']
            >>> results = agent.process_tool_calls(tool_calls)
            >>> results
            {0: 8}
        """
        observations = {}
        
        for tool_call_str in tool_calls_content:
            # Parse the JSON string into a Python dict
            tool_call = json.loads(tool_call_str)
            tool_name = tool_call["name"]
            
            # Get the corresponding tool object
            tool = self.tools_dict[tool_name]
            
            print(Fore.GREEN + f"\n🔧 Using Tool: {tool_name}")
            
            # Validate arguments (convert types if needed)
            validated_tool_call = validate_arguments(
                tool_call, json.loads(tool.fn_signature)
            )
            print(Fore.GREEN + f"   Arguments: {validated_tool_call['arguments']}")
            
            # Run the tool with validated arguments
            result = tool.run(**validated_tool_call["arguments"])
            print(Fore.GREEN + f"   Result: {result}\n")
            
            # Store result using the tool call ID
            observations[validated_tool_call["id"]] = result
        
        return observations
    
    def run(self, user_msg: str) -> str:
        """
        Run the full tool agent loop.
        
        THE COMPLETE FLOW:
        1. Create system prompt with tool signatures
        2. Send user query to LLM
        3. Check if LLM wants to use any tools
        4. If yes:
           a. Parse and execute tool calls
           b. Send results back to LLM
           c. Get final answer
        5. If no:
           - Return LLM's direct response
        
        Args:
            user_msg (str): The user's question/request
        
        Returns:
            str: The LLM's final answer (possibly using tool results)
        
        Example:
            >>> agent.run("What is 15 + 27?")
            # LLM uses calculator tool, gets 42, returns "The result is 42"
        """
        # Build the user message
        user_prompt = build_prompt_structure(prompt=user_msg, role="user")
        
        # Create chat history for tool selection
        # This history includes the system prompt with tool signatures
        tool_chat_history = ChatHistory([
            build_prompt_structure(
                prompt=TOOL_SYSTEM_PROMPT % self.add_tool_signatures(),
                role="system",
            ),
            user_prompt,
        ])
        
        # Create chat history for final answer (no tool info)
        agent_chat_history = ChatHistory([user_prompt])
        
        # STEP 1: Ask LLM if it wants to use any tools
        print(Fore.CYAN + "\n" + "=" * 80)
        print(Fore.CYAN + "Sending query to LLM...")
        print(Fore.CYAN + "=" * 80)
        
        tool_call_response = completions_create(
            self.client, messages=tool_chat_history, model=self.model
        )
        
        # STEP 2: Check if LLM returned any tool calls
        tool_calls = extract_tag_content(str(tool_call_response), "tool_call")
        
        if tool_calls.found:
            # LLM wants to use tools!
            print(Fore.YELLOW + "\n📞 LLM decided to use tools!")
            
            # Execute all tool calls
            observations = self.process_tool_calls(tool_calls.content)
            
            # Add tool results to chat history
            update_chat_history(
                agent_chat_history, 
                f"Observation: {observations}", 
                "user"
            )
            
            print(Fore.CYAN + "\n" + "=" * 80)
            print(Fore.CYAN + "Getting final answer from LLM...")
            print(Fore.CYAN + "=" * 80 + "\n")
        else:
            # LLM didn't need tools, it can answer directly
            print(Fore.YELLOW + "\n💬 LLM answering without tools\n")
        
        # STEP 3: Get final answer (with or without tool results)
        return completions_create(self.client, agent_chat_history, self.model)


# ============================================================================
# EXAMPLE USAGE (for learning purposes)
# ============================================================================
if __name__ == "__main__":
    from tool import tool
    
    print("=" * 80)
    print("Testing ToolAgent")
    print("=" * 80)
    
    # Create some simple tools
    @tool
    def add(a: int, b: int):
        """Add two numbers together"""
        return a + b
    
    @tool
    def multiply(a: int, b: int):
        """Multiply two numbers together"""
        return a * b
    
    @tool
    def get_current_time():
        """Get the current time"""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")
    
    # Create agent with all tools
    agent = ToolAgent(tools=[add, multiply, get_current_time])
    
    # Test 1: Simple calculation (should use add tool)
    print("\n" + "=" * 80)
    print("TEST 1: Simple Addition")
    print("=" * 80)
    result = agent.run("What is 127 + 389?")
    print(Fore.MAGENTA + f"\n✨ Final Answer: {result}\n")
    
    # Test 2: Question that doesn't need tools
    print("\n" + "=" * 80)
    print("TEST 2: General Question (No Tools Needed)")
    print("=" * 80)
    result = agent.run("What is the capital of France?")
    print(Fore.MAGENTA + f"\n✨ Final Answer: {result}\n")
    
    # Test 3: Multiplication
    print("\n" + "=" * 80)
    print("TEST 3: Multiplication")
    print("=" * 80)
    result = agent.run("Calculate 15 times 23")
    print(Fore.MAGENTA + f"\n✨ Final Answer: {result}\n")
    
    print("=" * 80)
    print("✅ ToolAgent tests complete!")
    print("=" * 80)
