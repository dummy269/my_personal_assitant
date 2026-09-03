from pathlib import Path
import sys

from src.basic_rag import add_pdf_to_collection, create_collection
from src.graph import build_graph


def main():
    collection = create_collection()
    for pdf in Path("data/documents").glob("*.pdf"):
        add_pdf_to_collection(collection, str(pdf))

    graph = build_graph()
    history = []
    questions = [" ".join(sys.argv[1:])] if sys.argv[1:] else iter(input, "")

    for question in questions:
        if not question.strip():
            break
        result = graph.invoke({
            "messages": history + [{"role": "user", "content": question}],
            "collection": collection,
        })
        history = result["messages"]
        print(history[-1]["content"])


if __name__ == "__main__":
    main()
