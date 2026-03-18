# Session 1 — IDE, Extensions & AI Agents

**Goal:** Set up a productive development environment and understand how to use AI assistance responsibly.

---

## 1.1 Choosing an IDE

### What is an IDE?

An IDE (Integrated Development Environment) is a full development application that combines a code editor, debugger, terminal, project tools, and language-specific features in a single environment. Examples include PyCharm, IntelliJ IDEA, Eclipse and Visual Studio.

Visual Studio Code (VS Code), however, is not a full IDE in the traditional sense: it is a highly extensible code editor. In practice, once you add the right extensions, it can provide an IDE-like experience for Python development. For this course, the practical comparison is:

| Feature             | VS Code           | PyCharm                       |
| ------------------- | ----------------- | ----------------------------- |
| Cost                | Free              | Free (Community) / Paid (Pro) |
| Product type        | Extensible editor | Full IDE                      |
| Language support    | Multi-language    | Python-first                  |
| Extension ecosystem | Very large        | Moderate                      |
| Resource usage      | Light             | Heavy                         |
| Refactoring tools   | Good              | Excellent                     |

> **Recommendation for this course:** VS Code. It is free, lightweight, and flexible.

### Installing VS Code

1. Download from https://code.visualstudio.com
2. Install the `code` CLI command (View → Command Palette → "Shell Command: Install 'code' in PATH") (optional) to open VS Code from the terminal
3. Familiarise yourself with the layout: Explorer, Search, Source Control, Extensions, Terminal

---

## 1.2 Essential VS Code Extensions for Python

For this course, start with a small, reliable Python setup rather than installing dozens of extensions.

### Core extensions

| Extension   | Publisher | Why install it                                 |
| ----------- | --------- | ---------------------------------------------- |
| **Python**  | Microsoft | Python support, debugging, test discovery      |
| **Pylance** | Microsoft | Autocomplete, navigation, and type information |
| **Jupyter** | Microsoft | Notebook support in VS Code                    |

### Optional extensions

| Extension          | Publisher | Why it can help                      |
| ------------------ | --------- | ------------------------------------ |
| **GitLens**        | GitKraken | Better Git history, blame, and diffs |
| **Codex**          | OpenAI    | AI agent for multi-step tasks        |
| **Github Copilot** | GitHub    | AI code completion and chat          |
| **GitHub Theme**   | GitHub    | GitHub-themed editor themes          |

---

## 1.3 AI Agents in the IDE

### The Landscape (2024–2026)

AI-assisted development is now part of the standard tooling landscape. We are likely to encounter three broad categories of tools:

| Category             | What it does                                               | Typical examples           |
| -------------------- | ---------------------------------------------------------- | -------------------------- |
| **Completion tools** | Suggest code as you type                                   | GitHub Copilot, Tabnine    |
| **Chat assistants**  | Answer questions, explain code, generate tests or snippets | Microsoft Copilot, ChatGPT |
| **Agentic tools**    | Perform multi-step tasks across files, terminal, and tests | Cursor, Claude, Codex      |

The important distinction is not the brand name, but the level of autonomy:

- **Autocomplete** tools suggest the next few tokens or lines
- **Chat** tools respond to prompts and work interactively with the user
- **Agents** can plan and execute several steps, often modifying multiple files

For this course, VS Code matters more than any single vendor. Most of these capabilities can be added either through extensions or through external tools that integrate with the editor.

### What AI Agents Can Do

- **Autocomplete** — single-line and multi-line suggestions as you type
- **Chat** — ask questions about your code, explain functions, generate boilerplate
- **Inline edits** — refactor a selected block on instruction
- **Agent mode** — multi-step tasks: create files, run tests, fix errors autonomously
- **Codebase Q&A** — "Where is the database connection initialised?"

### Demo: GitHub Copilot in Action

```python
# Type this comment, then let Copilot complete the function:

def parse_iso_date(date_string: str) -> datetime:
    """Parse an ISO 8601 date string and return a datetime object.
    Raise ValueError with a clear message if the format is invalid."""
```

Observe:

1. Copilot suggests the implementation
2. Ask Chat: _"What edge cases does this not handle?"_
3. Ask Chat: _"Write a pytest for this function"_

---

## The Critical Discussion: Proper Use of AI Agents

This is one of the most important topics in the course. AI agents are powerful — and easily misused.

Relevant examples:

- [The Guardian: Deloitte to pay money back to Albanese government after using AI in $440,000 report](https://www.theguardian.com/australia-news/2025/oct/06/deloitte-to-pay-money-back-to-albanese-government-after-using-ai-in-440000-report)
- [Nature: "Hey ChatGPT, write me a fictional paper: these LLMs are willing to commit academic fraud"](https://www.nature.com/articles/d41586-026-00595-9)

### The Core Principle

> Your job is to specify, review, and validate. Its job is to draft.

### What AI Gets Right (Most of the Time)

- Boilerplate and repetitive patterns
- Translating well-known algorithms into code
- Generating a first draft of tests for clearly specified behaviour
- Renaming, reformatting, and small refactors
- Summarising code structure or suggesting documentation

### What AI Might Get Wrong (Sometimes)

- Inventing function signatures for libraries it does not know well
- Hallucinating that a library version supports a feature it does not
- Producing code that looks plausible but is logically incorrect
- Missing edge cases and failure modes
- Writing tests that pass trivially without testing real behaviour
- Missing security implications (SQL injection, path traversal, secret exposure)
- Failing to understand the broader context of the codebase and its architecture

### Practical Rules for Responsible Use

#### ✅ DO

- Always read every line of generated code before accepting
- Run the tests — and check that the tests actually assert something meaningful
- Ask the AI to _explain_ what it generated; if it cannot, be suspicious
- Use AI for first drafts, not final code in security-sensitive paths
- Treat AI output as a starting point for your own thinking

#### ❌ DON'T

- Paste code you do not understand into production
- Trust AI-generated dependency versions without checking the package's changelog
- Let agent mode make file system changes you have not reviewed
- Use AI chat with confidential source code on untrusted endpoints
- "The AI said it was fine" for accepting code without review
