import sqlite3
import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from langgraph.checkpoint.sqlite import SqliteSaver
from pydantic import BaseModel

from src.advanced_graph import build_advanced_graph
from src.basic_rag import add_pdf_to_collection, create_collection


class AskRequest(BaseModel):
    question: str
    thread_id: str | None = None


class AskResponse(BaseModel):
    answer: str
    thread_id: str


collection = create_collection()
for pdf in Path("data/documents").glob("*.pdf"):
    add_pdf_to_collection(collection, str(pdf))

connection = sqlite3.connect("data/checkpoints.sqlite", check_same_thread=False)
checkpointer = SqliteSaver(connection)
checkpointer.setup()
graph = build_advanced_graph(collection, checkpointer)
app = FastAPI(title="Personal AI Agent")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    thread_id = request.thread_id or str(uuid.uuid4())
    result = graph.invoke(
        {"question": question},
        {"configurable": {"thread_id": thread_id}},
    )
    return AskResponse(answer=result["answer"], thread_id=thread_id)


@app.get("/", response_class=HTMLResponse)
def home():
    return """<!doctype html>
<html><head><title>Personal AI Agent</title>
<style>
body { max-width: 760px; margin: 48px auto; padding: 0 20px; font: 16px sans-serif; background: #f4f1ea; color: #202b2c; }
h1 { font: 700 42px Georgia, serif; margin-bottom: 8px; }
form { display: flex; gap: 8px; margin: 28px 0; }
input { flex: 1; padding: 14px; border: 1px solid #9da9a4; border-radius: 4px; font-size: 16px; }
button { padding: 14px 20px; border: 0; border-radius: 4px; background: #d35d38; color: white; cursor: pointer; }
#answer { white-space: pre-wrap; line-height: 1.6; border-top: 1px solid #9da9a4; padding-top: 20px; }
</style></head>
<body><h1>Personal AI Agent</h1><p>Ask about your personal documents.</p>
<form><input id="question" placeholder="What technologies have I used?" autofocus><button>Ask</button></form>
<div id="answer"></div>
<script>
const form = document.querySelector('form');
const input = document.querySelector('#question');
const output = document.querySelector('#answer');
let threadId;
form.addEventListener('submit', async (event) => {
  event.preventDefault(); output.textContent = 'Thinking...';
  const response = await fetch('/ask', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({question: input.value, thread_id: threadId})});
  const data = await response.json();
  if (!response.ok) { output.textContent = data.detail || 'Request failed'; return; }
  threadId = data.thread_id; output.textContent = data.answer;
});
</script></body></html>"""