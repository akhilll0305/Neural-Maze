"""
Reflection Pattern Agent

The reflection agent implements an iterative loop:
1. Generate content based on user request
2. Reflect/critique the generated content
3. Revise based on the critique
4. Repeat for N steps or until satisfied

Key concept: Two separate chat histories for different roles
"""

from colorama import Fore
from dotenv import load_dotenv
from groq import Groq

from agentic_patterns.utils.completions import build_prompt_structure
from agentic_patterns.utils.completions import completions_create
from agentic_patterns.utils.completions import FixedFirstChatHistory
from agentic_patterns.utils.completions import update_chat_history
from agentic_patterns.utils.logging import fancy_step_tracker

load_dotenv()


# Base prompts that will be APPENDED to custom prompts
# This ensures consistent behavior even with custom instructions
BASE_GENERATION_SYSTEM_PROMPT = """
Your task is to Generate the best content possible for the user's request.
If the user provides critique, respond with a revised version of your previous attempt.
You must always output the revised content.
"""

BASE_REFLECTION_SYSTEM_PROMPT = """
You are tasked with generating critique and recommendations to the user's generated content.
If the user content has something wrong or something to be improved, output a list of recommendations
and critiques. If the user content is ok and there's nothing to change, output this: <OK>
"""


class ReflectionAgent:
    """
    A class that implements the Reflection Pattern.
    
    HOW IT WORKS:
    - Maintains TWO separate chat histories (generator and reflector)
    - Generator creates content based on user request
    - Reflector critiques the generated content
    - Generator revises based on critique
    - Loop continues for N steps or until reflector says <OK>
    
    WHY IT WORKS:
    - LLMs are often better at critiquing than creating perfectly on first try
    - Iterative refinement improves quality
    - Separate roles (via different system prompts) create different "mindsets"
    
    Attributes:
        model (str): The LLM model to use (default: llama-3.3-70b-versatile)
        client (Groq): Groq API client instance
    """
    
    def __init__(self, model: str = "llama-3.3-70b-versatile"):
        """
        Initialize the ReflectionAgent.
        
        Args:
            model (str): The Groq model to use for both generation and reflection
        """
        self.client = Groq()
        self.model = model
    
    def _request_completion(
        self,
        history: list,
        verbose: int = 0,
        log_title: str = "COMPLETION",
        log_color: str = "",
    ) -> str:
        """
        Private method to request a completion from the LLM.
        
        WHY THIS IS A PRIVATE METHOD:
        - Avoids code duplication between generate() and reflect()
        - Centralizes the API call logic
        - Easy to add error handling, retries, or logging in one place
        
        Args:
            history (list): The chat history to send to the LLM
            verbose (int): Verbosity level (0 = quiet, 1+ = show output)
            log_title (str): Title to display in verbose mode
            log_color (str): Color code for the output (from colorama)
        
        Returns:
            str: The LLM's response
        """
        # Call the LLM using our utility function
        output = completions_create(self.client, history, self.model)
        
        # If verbose, print the output with color and title
        if verbose > 0:
            print(log_color, f"\n\n{log_title}\n\n", output)
        
        return output
    
    def generate(self, generation_history: list, verbose: int = 0) -> str:
        """
        Generate content based on the generation history.
        
        This is the "creator" role - it produces content.
        
        Args:
            generation_history (list): The generator's chat history
            verbose (int): Verbosity level
        
        Returns:
            str: The generated content
        """
        return self._request_completion(
            generation_history, 
            verbose, 
            log_title="GENERATION", 
            log_color=Fore.BLUE
        )
    
    def reflect(self, reflection_history: list, verbose: int = 0) -> str:
        """
        Reflect on (critique) the generated content.
        
        This is the "critic" role - it analyzes and suggests improvements.
        
        Args:
            reflection_history (list): The reflector's chat history
            verbose (int): Verbosity level
        
        Returns:
            str: The critique/feedback
        """
        return self._request_completion(
            reflection_history, 
            verbose, 
            log_title="REFLECTION", 
            log_color=Fore.GREEN
        )
    
    def run(
        self,
        user_msg: str,
        generation_system_prompt: str = "",
        reflection_system_prompt: str = "",
        n_steps: int = 10,
        verbose: int = 0,
    ) -> str:
        """
        Run the full reflection loop.
        
        THIS IS THE MAIN METHOD - it orchestrates the entire pattern!
        
        THE LOOP:
        1. Generator creates content
        2. Reflector critiques it
        3. If critique contains <OK>, stop (content is good)
        4. Otherwise, send critique to generator
        5. Generator revises
        6. Repeat from step 2
        
        Args:
            user_msg (str): The user's initial request
            generation_system_prompt (str): Custom instructions for the generator
            reflection_system_prompt (str): Custom instructions for the reflector
            n_steps (int): Maximum number of reflection iterations
            verbose (int): Verbosity level (0 = quiet, 1+ = show progress)
        
        Returns:
            str: The final generated content after all iterations
        
        Example:
            >>> agent = ReflectionAgent()
            >>> result = agent.run(
            ...     user_msg="Write a haiku about AI",
            ...     generation_system_prompt="You are a creative poet",
            ...     reflection_system_prompt="You are a poetry critic",
            ...     n_steps=5,
            ...     verbose=1
            ... )
        """
        # Append base prompts to custom prompts
        # This ensures consistent behavior while allowing customization
        generation_system_prompt += BASE_GENERATION_SYSTEM_PROMPT
        reflection_system_prompt += BASE_REFLECTION_SYSTEM_PROMPT
        
        # Initialize TWO separate chat histories
        # WHY total_length=3?
        # - Keeps system prompt (index 0)
        # - Keeps last user message (index 1)
        # - Keeps last assistant message (index 2)
        # This prevents context overflow in long iterations
        
        generation_history = FixedFirstChatHistory(
            [
                build_prompt_structure(prompt=generation_system_prompt, role="system"),
                build_prompt_structure(prompt=user_msg, role="user"),
            ],
            total_length=3,
        )
        
        reflection_history = FixedFirstChatHistory(
            [build_prompt_structure(prompt=reflection_system_prompt, role="system")],
            total_length=3,
        )
        
        # The reflection loop
        for step in range(n_steps):
            # Show progress if verbose
            if verbose > 0:
                fancy_step_tracker(step, n_steps)
            
            # STEP 1: Generate content
            generation = self.generate(generation_history, verbose=verbose)
            
            # Update histories:
            # - Add to generator's history (so it remembers what it created)
            # - Add to reflector's history as USER message (so reflector can critique it)
            update_chat_history(generation_history, generation, "assistant")
            update_chat_history(reflection_history, generation, "user")
            
            # STEP 2: Reflect on the generated content
            critique = self.reflect(reflection_history, verbose=verbose)
            
            # STEP 3: Check for stop condition
            if "<OK>" in critique:
                # Reflector is satisfied - stop the loop!
                if verbose > 0:
                    print(
                        Fore.RED,
                        "\n\nStop Sequence found. Stopping the reflection loop ... \n\n",
                    )
                break
            
            # STEP 4: Send critique back to generator (as if user sent it)
            # Also update reflector's history (so it remembers what it said)
            update_chat_history(generation_history, critique, "user")
            update_chat_history(reflection_history, critique, "assistant")
            
            # Loop continues - generator will revise based on critique
        
        # Return the final generated content
        return generation


# ============================================================================
# EXAMPLE USAGE (for learning purposes)
# ============================================================================
if __name__ == "__main__":
    print("=" * 80)
    print("Testing ReflectionAgent")
    print("=" * 80)
    
    # Create an agent
    agent = ReflectionAgent()
    
    # Run a simple test
    result = agent.run(
        user_msg="Write a short haiku about machine learning",
        generation_system_prompt="You are a creative poet specializing in haiku.",
        reflection_system_prompt="You are a haiku expert who critiques structure and meaning.",
        n_steps=3,
        verbose=1  # Show the process
    )
    
    print("\n" + "=" * 80)
    print("FINAL RESULT:")
    print("=" * 80)
    print(result)
    print("=" * 80)
