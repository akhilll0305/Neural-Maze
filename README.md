# My AI Agent Learning Journey 🤖

A hands-on implementation of AI agent patterns and projects, built from scratch to deeply understand how AI agents work.

## 📚 Learning Philosophy

This repository is my personal learning journey where I:
- **Don't just clone** - I understand every line of code
- **Build from scratch** - Implement concepts manually before using frameworks
- **Reference, don't copy** - Use Neural Maze's projects as blueprints, not shortcuts
- **Learn by doing** - Each pattern is built step-by-step with clear understanding

## 🗂️ Project Structure

```
My_Learnings/
├── agentic_patterns/          # Core agentic patterns implementation
│   ├── src/                   # Source code
│   │   └── agentic_patterns/
│   │       ├── utils/         # Reusable utilities
│   │       ├── reflection_pattern/
│   │       ├── tool_pattern/
│   │       ├── planning_pattern/
│   │       └── multiagent_pattern/
│   └── examples/              # Usage examples
└── [future projects]/         # More projects to come!
```


### 1. Reflection Pattern 🤔
**Status:** ✅ Complete

An iterative self-improvement pattern where an LLM generates content, critiques itself, and refines through multiple iterations.

**Key Components:**
- `utils/completions.py` - API wrappers and chat history management
- `utils/logging.py` - Colored output for better debugging
- `utils/extraction.py` - Tag extraction utilities
- `reflection_pattern/reflection_agent.py` - Main agent implementation

**What I Learned:**
- Two separate chat histories create different "mindsets"
- LLMs critique better than they create on first try
- Context management prevents overflow (FixedFirstChatHistory)
- Stop conditions (<OK>) prevent unnecessary iterations

**Try it:**
```bash
cd agentic_patterns
python examples/example_reflection.py
```

---

### 2. Tool Pattern 🛠️
**Status:** ✅ Complete

A pattern that enables LLMs to use external tools and functions to access real-world data and perform actions they couldn't do alone.

**Key Components:**
- `tool_pattern/tool.py` - Function signature extraction and @tool decorator
- `tool_pattern/tool_agent.py` - Agent orchestration with dual chat histories

**What I Learned:**
- Type hints extraction creates automatic API schemas for LLMs
- Dual chat histories pattern: one for tool selection, one clean for final answer
- Tool calls use XML tags and JSON for structured function calling
- LLMs can intelligently decide when to use tools vs answer directly
- Argument validation converts string inputs to proper types (int, float, etc.)

**Try it:**
```bash
cd agentic_patterns
python examples/example_tool.py
```

---

### 3. Planning Pattern (ReAct) 🧠
Status: ✅ Complete

An implementation of the ReAct (Reasoning + Acting) pattern where the agent runs a structured loop:

Thought → Action → Observation → Repeat → Final Response

**Key Components:**
- `tool_pattern/tool.py` - Function signature extraction and @tool decorator
- `planning_pattern/react_agent.py` - Core ReAct loop implementation

**What I Learned:**
- ReAct separates reasoning from acting, making tool use reliable
- Tool schemas must be explicit for structured function calling
- Argument validation prevents runtime crashes from type mismatches
- Agents must guard against malformed JSON from LLMs
- Loop-based planning requires max-iteration safeguards
- Proper tagging (<thought>, <tool_call>, <observation>, <response>) stabilizes agent behavior

**Try it:**
```bash
cd agentic_patterns
python examples/example_planning.py
```

### 4. Multi-Agent Pattern 🧑🏽‍🤝‍🧑🏻
**Status:** ✅ Complete
A modular multi-agent orchestration system built on top of the ReAct agent.
Implements a Crew-style architecture:
Crew (Orchestrator)
    ├── Researcher
    ├── Analyst
    └── Writer

**Key Components:**
- `multiagent_pattern/agent.py` - Agent abstraction (role + internal ReactAgent)
- `multiagent_pattern/crew.py` - Orchestrator with dependency graph
- Topological sorting for execution order
- Context propagation between agents

## 🎯 Learning Goals

- Multi-agent systems are DAG execution problems
- Orchestration logic is separate from reasoning logic
- Outputs become downstream context
- Modular intelligence > monolithic prompts
- Dependency validation prevents circular execution

**Try it:**
```bash
cd agentic_patterns
python examples/example_multiagent.py
```

## 🙏 Acknowledgments

Learning from [Neural Maze](https://github.com/neural-maze) - Building AI Agents from scratch without frameworks.

## 📝 Notes

This is a **learning repository**. The code is heavily commented to demonstrate understanding, not for production use. Each pattern is built with educational clarity in mind.

---

