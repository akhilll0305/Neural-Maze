"""
Utility functions for working with LLM completions and chat history management.

This module provides:
1. Clean API wrappers for Groq completions
2. Smart chat history management to prevent context overflow
3. Helper functions for building prompts
"""


def completions_create(client, messages: list, model: str) -> str:
    """
    A clean wrapper around the Groq API completion call.
    
    WHY THIS EXISTS:
    - Simplifies the API call (no need to type the full path every time)
    - Extracts just the content string (not the whole response object)
    - Makes it easy to add retry logic, error handling, or logging later
    
    Args:
        client (Groq): The Groq client object
        messages (list[dict]): Chat history with roles and content
        model (str): Model name like "llama-3.3-70b-versatile"
    
    Returns:
        str: The text content of the LLM's response
    
    Example:
        >>> from groq import Groq
        >>> client = Groq()
        >>> messages = [{"role": "user", "content": "Hello!"}]
        >>> response = completions_create(client, messages, "llama-3.3-70b-versatile")
        >>> print(response)  # Just the text, not the full object
    """
    response = client.chat.completions.create(messages=messages, model=model)
    return str(response.choices[0].message.content)


def build_prompt_structure(prompt: str, role: str, tag: str = "") -> dict:
    """
    Builds a properly formatted message dictionary for chat APIs.
    
    WHY THIS EXISTS:
    - Ensures consistency in message format
    - Optionally wraps content in XML-style tags for structured output
    - Reduces repetitive dictionary creation
    
    Args:
        prompt (str): The actual message content
        role (str): The speaker role - "system", "user", or "assistant"
        tag (str, optional): If provided, wraps content in <tag>content</tag>
    
    Returns:
        dict: A message dictionary with "role" and "content" keys
    
    Example:
        >>> build_prompt_structure("Hello!", "user")
        {'role': 'user', 'content': 'Hello!'}
        
        >>> build_prompt_structure("Think step by step", "user", tag="instruction")
        {'role': 'user', 'content': '<instruction>Think step by step</instruction>'}
    """
    if tag:
        # Wrap content in XML-style tags for easier extraction later
        prompt = f"<{tag}>{prompt}</{tag}>"
    
    return {"role": role, "content": prompt}


def update_chat_history(history: list, msg: str, role: str):
    """
    Convenience function to add a message to chat history.
    
    WHY THIS EXISTS:
    - One-liner instead of history.append(build_prompt_structure(...))
    - Consistent message formatting across the codebase
    
    Args:
        history (list): The chat history to update (modified in-place)
        msg (str): The message content to add
        role (str): The role - "user", "assistant", or "system"
    
    Example:
        >>> history = []
        >>> update_chat_history(history, "Hello", "user")
        >>> print(history)
        [{'role': 'user', 'content': 'Hello'}]
    """
    history.append(build_prompt_structure(prompt=msg, role=role))


class ChatHistory(list):
    """
    A smart list that automatically limits its size (like a circular buffer).
    
    WHY THIS EXISTS:
    - LLMs have context limits (e.g., 8K tokens, 128K tokens)
    - Long conversations can exceed these limits
    - This automatically removes old messages when the limit is reached
    
    Think of it like a queue: when full, adding a new item removes the oldest one.
    """
    
    def __init__(self, messages: list | None = None, total_length: int = -1):
        """
        Initialize the chat history with optional size limit.
        
        Args:
            messages (list | None): Initial messages to start with
            total_length (int): Max number of messages (-1 means unlimited)
        """
        if messages is None:
            messages = []
        
        super().__init__(messages)
        self.total_length = total_length
    
    def append(self, msg: dict):
        """
        Add a message to the history.
        
        If we're at capacity, remove the OLDEST message first (index 0),
        then add the new message.
        
        Args:
            msg (dict): The message to add (should have 'role' and 'content')
        """
        if len(self) == self.total_length:
            # Remove the oldest message (at index 0)
            self.pop(0)
        
        super().append(msg)


class FixedFirstChatHistory(ChatHistory):
    """
    A smart chat history that ALWAYS keeps the first message (usually the system prompt).
    
    WHY THIS IS CRITICAL:
    - The system prompt defines the agent's behavior
    - In long conversations, we want to drop old messages but KEEP the system prompt
    - Without this, the agent would "forget" who it is after many iterations
    
    Example use case:
        System prompt: "You are a helpful coding assistant"
        After 100 messages, we still want the agent to remember it's a coding assistant!
        
    How it works:
        - Index 0: Always the system prompt (never removed)
        - Index 1+: Regular messages (oldest removed when full)
    """
    
    def __init__(self, messages: list | None = None, total_length: int = -1):
        """
        Initialize with a protected first message.
        
        Args:
            messages (list | None): Initial messages (first one is protected)
            total_length (int): Max total messages (-1 means unlimited)
        """
        super().__init__(messages, total_length)
    
    def append(self, msg: dict):
        """
        Add a message while protecting the first one.
        
        If at capacity:
        - Don't remove index 0 (the system prompt)
        - Remove index 1 (the oldest non-system message)
        - Then add the new message
        
        Args:
            msg (dict): The message to add
        """
        if len(self) == self.total_length:
            # Remove the second message (index 1), NOT the first (index 0)
            self.pop(1)
        
        # Use the parent's append (from list class)
        list.append(self, msg)


# ============================================================================
# EXAMPLE USAGE (for learning purposes)
# ============================================================================
if __name__ == "__main__":
    print("=" * 80)
    print("Testing FixedFirstChatHistory")
    print("=" * 80)
    
    # Create a history that holds max 3 messages
    history = FixedFirstChatHistory(
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
        ],
        total_length=3
    )
    
    print("\nInitial state (1 message):")
    for i, msg in enumerate(history):
        print(f"  [{i}] {msg['role']}: {msg['content']}")
    
    # Add second message
    history.append({"role": "user", "content": "Hello!"})
    print("\nAfter adding user message (2 messages):")
    for i, msg in enumerate(history):
        print(f"  [{i}] {msg['role']}: {msg['content']}")
    
    # Add third message (now at capacity)
    history.append({"role": "assistant", "content": "Hi there!"})
    print("\nAfter adding assistant message (3 messages - at capacity):")
    for i, msg in enumerate(history):
        print(f"  [{i}] {msg['role']}: {msg['content']}")
    
    # Add fourth message (should remove index 1, keep index 0)
    history.append({"role": "user", "content": "How are you?"})
    print("\nAfter adding another user message (still 3 messages):")
    print("Notice: The system prompt (index 0) is still there!")
    print("But 'Hello!' (the first user message) was removed.")
    for i, msg in enumerate(history):
        print(f"  [{i}] {msg['role']}: {msg['content']}")
