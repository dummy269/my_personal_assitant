import sys
from pathlib import Path

from src.basic_rag import add_pdf_to_collection, create_collection, search


def main():
    collection = create_collection()
    pdf_files = Path("data/documents").glob("*.pdf")
    indexed = sum(add_pdf_to_collection(collection, str(pdf)) for pdf in pdf_files)

    question = " ".join(sys.argv[1:]) or "What is my educational background?"
    results = search(collection, question)

    print(f"Indexed chunks: {indexed}")
    print(f"\nQuestion: {question}\n")
    for index, result in enumerate(results, 1):
        print(f"Result {index} ({result['source']}):")
        print(result["text"])
        print()


if __name__ == "__main__":
    main()