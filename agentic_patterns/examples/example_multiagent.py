"""
Example: Using the Multi-Agent Pattern

This example shows how to create a crew of agents
that work together on a complex task.
"""

# TODO: Add example usage once Crew is implemented
"""
Example: Using the Multi-Agent Pattern

This example demonstrates how multiple agents:
- Have specialized roles
- Depend on each other
- Pass context forward
- Execute in correct order (DAG scheduling)

Workflow:
Researcher → Analyst → Writer
"""

from agentic_patterns.multiagent_pattern.crew import Crew
from agentic_patterns.multiagent_pattern.agent import Agent


# ---------------------------------------------------------------------------
# Example
# ---------------------------------------------------------------------------

def example_basic_pipeline():
    print("\n" + "=" * 80)
    print("MULTI-AGENT EXAMPLE: Sequential Pipeline")
    print("=" * 80)

    # Create Crew Context
    with Crew() as crew:

        # -------------------------------------------------------------------
        # Agent 1: Researcher
        # -------------------------------------------------------------------
        researcher = Agent(
            name="Researcher",
            backstory=(
                "You are an expert AI researcher. "
                "You provide structured and factual information."
            ),
            task_description=(
                "Research the top 5 applications of AI in healthcare."
            ),
            task_expected_output=(
                "Provide a numbered list of 5 applications "
                "with short explanations (2 sentences each)."
            ),
        )

        # -------------------------------------------------------------------
        # Agent 2: Analyst
        # -------------------------------------------------------------------
        analyst = Agent(
            name="Analyst",
            backstory=(
                "You are a strategic business analyst. "
                "You extract business insights from research."
            ),
            task_description=(
                "Based on the research in the context, "
                "identify 3 major business opportunities."
            ),
            task_expected_output=(
                "Provide 3 business opportunities with clear reasoning."
            ),
        )

        # -------------------------------------------------------------------
        # Agent 3: Writer
        # -------------------------------------------------------------------
        writer = Agent(
            name="Writer",
            backstory=(
                "You are a professional executive writer. "
                "You write concise and compelling summaries."
            ),
            task_description=(
                "Using the business opportunities from the context, "
                "write an executive summary."
            ),
            task_expected_output=(
                "Write a 3-4 paragraph executive summary."
            ),
        )

        # -------------------------------------------------------------------
        # Define Dependencies
        # -------------------------------------------------------------------
        print("\n📌 Defining Workflow:")
        print("Researcher → Analyst → Writer\n")

        researcher >> analyst >> writer

        # Optional: visualize graph (if graphviz installed)
        # crew.plot()

        # -------------------------------------------------------------------
        # Execute
        # -------------------------------------------------------------------
        print("🚀 Running Multi-Agent Workflow...\n")
        crew.run()

        print("\n✅ Workflow Complete!")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":

    print("""
╔════════════════════════════════════════════════════════════════╗
║                    MULTI-AGENT PATTERN DEMO                    ║
║                                                                ║
║  Observe:                                                      ║
║  - Agents executing in dependency order                        ║
║  - Context flowing between agents                              ║
║  - Each agent having a specialized role                        ║
║                                                                ║
║  Architecture:                                                 ║
║  Crew (orchestrator)                                           ║
║      ├── Researcher                                            ║
║      ├── Analyst                                               ║
║      └── Writer                                                ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
""")

    example_basic_pipeline()

    print("\n" + "=" * 80)
    print("🎓 KEY LEARNINGS:")
    print("=" * 80)
    print("""
1. Each agent has its own reasoning engine (ReactAgent inside)
2. Dependencies create a Directed Acyclic Graph (DAG)
3. Crew enforces execution order via topological sort
4. Outputs automatically become context for dependents
5. Multi-agent systems enable modular intelligence
""")

    print("\n" + "=" * 80)
    print("🚀 NEXT EXPERIMENTS:")
    print("=" * 80)
    print("""
Try:
- Adding a Critic agent at the end
- Creating multiple dependencies (writer depends on both researcher & analyst)
- Giving tools only to specific agents
- Introducing a circular dependency to test validation

Next: Parallel Multi-Agent Execution ⚡
""")