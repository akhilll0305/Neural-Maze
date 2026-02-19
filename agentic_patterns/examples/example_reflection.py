"""
Example: Using the Reflection Pattern

This example demonstrates how to use the reflection agent
to iteratively improve generated content through multiple use cases.
"""

from agentic_patterns.reflection_pattern.reflection_agent import ReflectionAgent


def example_1_code_generation():
    """
    Example 1: Generating and improving Python code
    
    The reflection pattern is great for code because:
    - First attempts often have bugs or inefficiencies
    - Critics can spot issues like missing edge cases
    - Iterative refinement leads to better code quality
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Code Generation with Reflection")
    print("=" * 80)
    
    agent = ReflectionAgent()
    
    result = agent.run(
        user_msg="Write a Python function to find the longest common subsequence (LCS) of two strings",
        generation_system_prompt="You are an experienced Python developer who writes clean, efficient code.",
        reflection_system_prompt="You are a senior code reviewer who checks for correctness, edge cases, and efficiency.",
        n_steps=5,
        verbose=1
    )
    
    print("\n" + "=" * 80)
    print("FINAL CODE:")
    print("=" * 80)
    print(result)


def example_2_creative_writing():
    """
    Example 2: Writing a compelling story opening
    
    Creative writing benefits from reflection because:
    - First drafts are rarely perfect
    - Feedback on tone, pacing, and imagery helps
    - Multiple iterations polish the writing
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Creative Writing with Reflection")
    print("=" * 80)
    
    agent = ReflectionAgent()
    
    result = agent.run(
        user_msg="Write the opening paragraph of a sci-fi story about an AI that becomes self-aware",
        generation_system_prompt="You are a creative fiction writer specializing in science fiction.",
        reflection_system_prompt="You are a literary editor who critiques narrative flow, imagery, and emotional impact.",
        n_steps=5,
        verbose=1
    )
    
    print("\n" + "=" * 80)
    print("FINAL STORY OPENING:")
    print("=" * 80)
    print(result)


def example_3_technical_explanation():
    """
    Example 3: Explaining a complex technical concept
    
    Technical explanations improve with reflection because:
    - Clarity is paramount
    - Analogies and examples can be refined
    - The critic ensures accuracy and accessibility
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Technical Explanation with Reflection")
    print("=" * 80)
    
    agent = ReflectionAgent()
    
    result = agent.run(
        user_msg="Explain how transformers work in machine learning to someone with basic programming knowledge",
        generation_system_prompt="You are a technical educator who explains complex concepts clearly.",
        reflection_system_prompt="You are an expert who ensures explanations are accurate, clear, and well-structured.",
        n_steps=5,
        verbose=1
    )
    
    print("\n" + "=" * 80)
    print("FINAL EXPLANATION:")
    print("=" * 80)
    print(result)


def example_4_minimal_iterations():
    """
    Example 4: Short reflection loop
    
    Sometimes you just want 1-2 rounds of feedback.
    This shows how to use fewer iterations.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Minimal Reflection (2 steps)")
    print("=" * 80)
    
    agent = ReflectionAgent()
    
    result = agent.run(
        user_msg="Write a professional email requesting a meeting with a potential client",
        generation_system_prompt="You write professional business communications.",
        reflection_system_prompt="You review emails for clarity, tone, and professionalism.",
        n_steps=2,  # Just 2 iterations
        verbose=1
    )
    
    print("\n" + "=" * 80)
    print("FINAL EMAIL:")
    print("=" * 80)
    print(result)


if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║                  REFLECTION PATTERN EXAMPLES                   ║
    ║                                                                ║
    ║  Watch how content improves through iterative reflection!     ║
    ║                                                                ║
    ║  What to observe:                                             ║
    ║  - First drafts vs final outputs                              ║
    ║  - How critiques guide improvements                           ║
    ║  - When the loop stops early (<OK> found)                     ║
    ║                                                                ║
    ╚════════════════════════════════════════════════════════════════╝
    """)
    
    # Run the examples
    # Uncomment the ones you want to try
    
    # example_1_code_generation()
    # example_2_creative_writing()
    # example_3_technical_explanation()
    example_4_minimal_iterations()  # Start with the quickest one
    
    print("\n" + "=" * 80)
    print("🎓 KEY LEARNINGS FROM THESE EXAMPLES:")
    print("=" * 80)
    print("""
    1. TWO DIFFERENT ROLES create different perspectives
       - Generator: Creative, producing content
       - Reflector: Critical, analyzing quality
    
    2. ITERATIVE REFINEMENT improves quality
       - Each round addresses specific issues
       - Final output is usually much better
    
    3. STOP CONDITION prevents unnecessary iterations
       - <OK> signals satisfaction
       - Saves API calls and time
    
    4. CUSTOM PROMPTS adapt the pattern
       - Different tasks need different expertise
       - System prompts define the "personality"
    
    5. CONTEXT MANAGEMENT prevents overflow
       - FixedFirstChatHistory keeps system prompt
       - Only recent messages are retained
    """)
    
    print("\n" + "=" * 80)
    print("🚀 NEXT STEPS:")
    print("=" * 80)
    print("""
    Try modifying the examples:
    - Change n_steps to see more/fewer iterations
    - Adjust the system prompts for different expertise
    - Try your own tasks and use cases
    - Experiment with different models (if available)
    
    Then we'll move on to the TOOL PATTERN! 🛠️
    """)
