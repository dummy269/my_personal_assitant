import sys
from pathlib import Path

from src.agent import run_agent
from src.basic_rag import add_pdf_to_collection, create_collection


def main():
    collection = create_collection()
    indexed = sum(
        add_pdf_to_collection(collection, str(pdf))
        for pdf in Path("data/documents").glob("*.pdf")
    )
    question = " ".join(sys.argv[1:]) or "What technologies have I used?"
    print(f"Indexed chunks: {indexed}")
    print(f"Answer: {run_agent(collection, question)}")


if __name__ == "__main__":
    main()