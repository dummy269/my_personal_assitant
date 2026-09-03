import sys
import sqlite3
from pathlib import Path

from langgraph.checkpoint.sqlite import SqliteSaver

from src.advanced_graph import build_advanced_graph
from src.basic_rag import add_pdf_to_collection, create_collection


def main():
    collection = create_collection()
    for pdf in Path("data/documents").glob("*.pdf"):
        add_pdf_to_collection(collection, str(pdf))

    connection = sqlite3.connect("data/checkpoints.sqlite", check_same_thread=False)
    checkpointer = SqliteSaver(connection)
    checkpointer.setup()
    graph = build_advanced_graph(collection, checkpointer)
    config = {"configurable": {"thread_id": "personal-ai-v8"}}
    questions = [" ".join(sys.argv[1:])] if sys.argv[1:] else iter(input, "")

    for question in questions:
        if not question.strip():
            break
        result = graph.invoke({"question": question}, config)
        print(result["answer"])

    connection.close()


if __name__ == "__main__":
    main()
