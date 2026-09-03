import sys
import sqlite3
from pathlib import Path

from langgraph.checkpoint.sqlite import SqliteSaver

from src.basic_rag import add_pdf_to_collection, create_collection
from src.graph import build_graph


def main():
    collection = create_collection()
    for pdf in Path("data/documents").glob("*.pdf"):
        add_pdf_to_collection(collection, str(pdf))

    connection = sqlite3.connect("data/checkpoints.sqlite", check_same_thread=False)
    checkpointer = SqliteSaver(connection)
    checkpointer.setup()
    graph = build_graph(collection, checkpointer)
    config = {"configurable": {"thread_id": "personal-ai"}}
    questions = [" ".join(sys.argv[1:])] if sys.argv[1:] else iter(input, "")

    for question in questions:
        if not question.strip():
            break
        result = graph.invoke({
            "messages": [{"role": "user", "content": question}],
        }, config)
        print(result["messages"][-1]["content"])

    connection.close()


if __name__ == "__main__":
    main()
