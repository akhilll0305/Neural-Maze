"""
Utilities for extracting structured content from LLM responses.

This module provides:
- XML-style tag extraction from text
- Support for multiple occurrences of the same tag
- Clean data structures for extracted content
"""

import re
from dataclasses import dataclass


@dataclass
class TagContentResult:
    """
    A data class to represent the result of extracting tag content.
    
    WHY USE A DATACLASS:
    - Cleaner than returning a dict
    - Type hints make it clear what we're returning
    - Easy to access with dot notation (result.content, result.found)
    
    Attributes:
        content (list[str]): All content found between the specified tags
        found (bool): Whether any content was found for the given tag
    
    Example:
        >>> result = TagContentResult(content=["Hello", "World"], found=True)
        >>> print(result.content)
        ['Hello', 'World']
        >>> print(result.found)
        True
    """
    content: list[str]
    found: bool


def extract_tag_content(text: str, tag: str) -> TagContentResult:
    """
    Extracts all content enclosed by specified XML-style tags.
    
    WHY THIS EXISTS:
    - LLMs can output structured data using tags
    - We need to parse these tags reliably
    - Supports multiple occurrences of the same tag
    
    USE CASES:
    1. Reflection Pattern: Check for <OK> stop signal
    2. ReAct Pattern: Extract <thought>, <action>, <observation>
    3. Tool Pattern: Extract <tool_call> blocks
    
    Args:
        text (str): The input string containing potential tags
        tag (str): The tag name to search for (without < >)
    
    Returns:
        TagContentResult: Object with 'content' list and 'found' boolean
    
    Example:
        >>> text = "<thought>First idea</thought> some text <thought>Second idea</thought>"
        >>> result = extract_tag_content(text, "thought")
        >>> print(result.content)
        ['First idea', 'Second idea']
        >>> print(result.found)
        True
        
        >>> text = "No tags here"
        >>> result = extract_tag_content(text, "thought")
        >>> print(result.content)
        []
        >>> print(result.found)
        False
    """
    # Build regex pattern dynamically: <tag>CONTENT</tag>
    # (.*?) means: capture any content (non-greedy)
    # re.DOTALL means: . matches newlines too (for multi-line content)
    tag_pattern = rf"<{tag}>(.*?)</{tag}>"
    
    # Find all matches (returns list of captured groups)
    matched_contents = re.findall(tag_pattern, text, re.DOTALL)
    
    # Return structured result
    return TagContentResult(
        content=[content.strip() for content in matched_contents],
        found=bool(matched_contents)  # True if we found at least one match
    )


# ============================================================================
# EXAMPLE USAGE (for learning purposes)
# ============================================================================
if __name__ == "__main__":
    print("=" * 80)
    print("Testing Tag Extraction")
    print("=" * 80)
    
    # Test 1: Single tag
    print("\n1. Extracting single <answer> tag:")
    text1 = "Let me think... <answer>The answer is 42</answer>"
    result1 = extract_tag_content(text1, "answer")
    print(f"   Text: {text1}")
    print(f"   Found: {result1.found}")
    print(f"   Content: {result1.content}")
    
    # Test 2: Multiple tags
    print("\n2. Extracting multiple <thought> tags:")
    text2 = """
    <thought>First, I need to understand the problem</thought>
    Some other text here
    <thought>Then, I'll break it down into steps</thought>
    More text
    <thought>Finally, I'll solve it</thought>
    """
    result2 = extract_tag_content(text2, "thought")
    print(f"   Found: {result2.found}")
    print(f"   Number of thoughts: {len(result2.content)}")
    for i, thought in enumerate(result2.content, 1):
        print(f"   Thought {i}: {thought}")
    
    # Test 3: No tags found
    print("\n3. Trying to extract non-existent <missing> tag:")
    text3 = "This text has no tags at all"
    result3 = extract_tag_content(text3, "missing")
    print(f"   Text: {text3}")
    print(f"   Found: {result3.found}")
    print(f"   Content: {result3.content}")
    
    # Test 4: Stop condition (reflection pattern use case)
    print("\n4. Checking for <OK> stop signal:")
    text4 = "The content looks good now. <OK>"
    result4 = extract_tag_content(text4, "OK")
    print(f"   Text: {text4}")
    print(f"   Should stop? {result4.found}")
    
    # Test 5: Multi-line content
    print("\n5. Extracting multi-line content:")
    text5 = """
    <code>
    def hello():
        print("Hello, World!")
        return True
    </code>
    """
    result5 = extract_tag_content(text5, "code")
    print(f"   Found: {result5.found}")
    print(f"   Code:\n{result5.content[0]}")
    
    print("\n" + "=" * 80)
    print("✅ All extraction tests complete!")
    print("=" * 80)
