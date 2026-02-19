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

## ✅ Completed Patterns

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

### 2. Tool Pattern 🛠
**Status:** 🚧 Coming next...

### 3. Planning Pattern (ReAct) 🧠
**Status:** 📅 Planned

### 4. Multi-Agent Pattern 🧑🏽‍🤝‍🧑🏻
**Status:** 📅 Planned

## 🎯 Learning Goals

- [x] Understand the Reflection Pattern
- [ ] Master the Tool Pattern
- [ ] Implement ReAct (Planning Pattern)
- [ ] Build Multi-Agent systems
- [ ] Create real-world applications using these patterns

## 🙏 Acknowledgments

Learning from [Neural Maze](https://github.com/neural-maze) - Building AI Agents from scratch without frameworks.

## 📝 Notes

This is a **learning repository**. The code is heavily commented to demonstrate understanding, not for production use. Each pattern is built with educational clarity in mind.

---

**Last Updated:** February 19, 2026  
**Current Focus:** Reflection Pattern ✅ → Tool Pattern 🚧
