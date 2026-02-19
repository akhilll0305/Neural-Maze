"""
Logging and display utilities for agentic patterns.

This module provides:
- Colored console output for better readability
- Progress tracking for multi-step agent executions
- Visual separators for different stages
"""

import time
from colorama import Fore, Style


def fancy_print(message: str) -> None:
    """
    Displays a message with fancy formatting and colors.
    
    WHY THIS EXISTS:
    - Makes agent output more readable and professional
    - Clearly separates different sections of output
    - Adds visual hierarchy to terminal output
    
    Args:
        message (str): The message to display
    
    Example:
        >>> fancy_print("GENERATION STEP")
        
        ==================================================
        GENERATION STEP
        ==================================================
    """
    print(Style.BRIGHT + Fore.CYAN + f"\n{'=' * 50}")
    print(Fore.MAGENTA + f"{message}")
    print(Style.BRIGHT + Fore.CYAN + f"{'=' * 50}\n")
    # Small delay for better visual pacing
    time.sleep(0.5)


def fancy_step_tracker(step: int, total_steps: int) -> None:
    """
    Displays a progress tracker for iterative agent loops.
    
    WHY THIS EXISTS:
    - Shows user where we are in the reflection loop
    - Helps debug by knowing which iteration failed
    - Provides feedback that the agent is working
    
    Args:
        step (int): Current step number (0-indexed)
        total_steps (int): Total number of steps to complete
    
    Example:
        >>> for step in range(5):
        ...     fancy_step_tracker(step, 5)
        
        ==================================================
        STEP 1/5
        ==================================================
        
        ==================================================
        STEP 2/5
        ==================================================
        ...
    """
    fancy_print(f"STEP {step + 1}/{total_steps}")


# ============================================================================
# EXAMPLE USAGE (for learning purposes)
# ============================================================================
if __name__ == "__main__":
    print("Testing logging utilities...")
    print("\n1. Testing fancy_print:")
    fancy_print("GENERATION PHASE")
    
    print("\n2. Testing fancy_step_tracker:")
    for i in range(3):
        fancy_step_tracker(i, 3)
        print(f"   Doing work in step {i+1}...")
    
    print("\n✅ All logging tests complete!")
