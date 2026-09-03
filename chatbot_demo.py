import sys
from pathlib import Path

from src.basic_rag import add_pdf_to_collection, create_collection
from src.rag_chatbot import answer_question


def main():
    collection = create_collection()
    indexed = sum(
        add_pdf_to_collection(collection, str(pdf))
        for pdf in Path("data/documents").glob("*.pdf")
    )
    question = " ".join(sys.argv[1:]) or "What is my educational background?"
    print(f"Indexed chunks: {indexed}")
    print(f"Answer: {answer_question(collection, question)}")


if __name__ == "__main__":
    main()