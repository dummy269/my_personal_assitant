# Personal AI Agent

An educational project to learn Agentic AI from fundamentals.

## Purpose

Build an AI assistant that understands personal documents (resume, education, projects, certificates, experience, skills) using:
- RAG (Retrieval-Augmented Generation)
- Agents
- LangChain & LangGraph
- Memory & Persistence
- Production API/UI

## Learning Approach

This project is built incrementally with versions (V0, V1, V2, ..., V10).

Each version introduces one concept at a time. No skipping ahead.

**Current Version:** V9 (Evaluation)

## Project Structure

```
personal-ai/
│
├── README.md              # This file
├── .gitignore            # Git ignore rules
├── .env                  # Environment variables (secrets)
├── requirements.txt      # Python dependencies
│
├── data/
│   └── documents/        # Personal documents (PDFs, etc.)
│
├── src/
│   └── __init__.py       # Python package marker
│
└── tests/
    └── __init__.py       # Test package marker
```

## Setup

1. Create virtual environment:
   ```bash
   python3 -m venv myenv
   ```

2. Activate virtual environment:
   ```bash
   source myenv/bin/activate  # Linux/Mac
   # OR
   myenv\Scripts\activate     # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file with your settings (see `.env.template` if available)

## Running the Project

**V1 — PDF Reader:**

```bash
# Process all PDFs
python main.py

# Simple example
python learn_v1.py
```

**V2 — Basic RAG:**

```bash
# Index PDFs and retrieve relevant chunks
python rag_demo.py

# Ask a different question
python rag_demo.py "What projects have I worked on?"
```

**V3 — RAG Chatbot:**

```bash
python chatbot_demo.py "What technologies have I used?"
```

**V4 — Agent:**

```bash
python agent_demo.py "What technologies have I used?"
python agent_demo.py "What is 25 * 4?"
```

**V5 — LangGraph:**

```bash
python main.py "What is 25 * 4?"
python main.py "What technologies have I used?"
```

**V6 — Conversation memory:**

```bash
python main.py
```

Ask more than one question in the same run. Earlier messages remain in the graph state.

**V7 — Persistence:**

```bash
python main.py
```

Conversation checkpoints are stored in `data/checkpoints.sqlite`. The `personal-ai` thread ID lets later runs continue the same conversation.

**V8 — Advanced Agent:**

```bash
python main.py "When did my B.Tech end?"
```

The workflow uses planner, researcher, verifier, and final-answer nodes.

**V9 — Evaluation:**

```bash
python evaluate.py
```

The evaluation dataset checks retrieval using expected terms and reports `recall@3` and `precision@3`.

## Development

All Python code should be run inside the virtual environment.

Always activate before working:
```bash
source myenv/bin/activate
```

## Versions

- **V0:** Environment (current)
- **V1:** PDF Reader
- **V2:** Basic RAG
- **V3:** RAG Chatbot
- **V4:** Agent (Tools & Tool Calling)
- **V5:** LangGraph Fundamentals
- **V6:** Memory (Conversation & Long-term)
- **V7:** Persistence (Checkpoints & Database)
- **V8:** Advanced Agent Architecture
- **V9:** Evaluation & Testing
- **V10:** Production (API, UI, Docker)

## Important Notes

- Do NOT skip versions. Each builds on the previous one.
- Each version focuses on ONE concept.
- Code is intentionally simple and educational, not production-optimized.
- All LangChain/LangGraph usage is explicitly marked.
