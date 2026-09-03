import sys
from pathlib import Path

from src.basic_rag import add_pdf_to_collection, create_collection
from src.graph import build_graph


def main():
    collection = create_collection()
    for pdf in Path("data/documents").glob("*.pdf"):
        add_pdf_to_collection(collection, str(pdf))

    question = " ".join(sys.argv[1:]) or "What technologies have I used?"
    result = build_graph().invoke({
        "messages": [{"role": "user", "content": question}],
        "collection": collection,
    })
    print(result["messages"][-1]["content"])


if __name__ == "__main__":
    main()
