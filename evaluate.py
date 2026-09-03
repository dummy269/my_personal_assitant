from pathlib import Path

from src.basic_rag import add_pdf_to_collection, create_collection, search


DATASET = [
    {
        "question": "What is my educational background?",
        "expected_terms": ["M.Tech", "B.Tech"],
    },
    {
        "question": "What technologies have I used?",
        "expected_terms": ["Python", "LangChain"],
    },
    {
        "question": "Where did I complete my internship?",
        "expected_terms": ["CelebAI", "Python"],
    },
]


def evaluate_retrieval(collection, case: dict, number_of_results: int = 3) -> dict:
    results = search(collection, case["question"], number_of_results)
    retrieved_text = " ".join(result["text"] for result in results).lower()
    expected_terms = [term.lower() for term in case["expected_terms"]]
    matched_terms = [term for term in expected_terms if term in retrieved_text]
    relevant_results = sum(
        any(term in result["text"].lower() for term in expected_terms)
        for result in results
    )

    return {
        "question": case["question"],
        "recall_at_k": len(matched_terms) / len(expected_terms),
        "precision_at_k": relevant_results / len(results),
        "matched_terms": matched_terms,
        "results": results,
    }


def evaluate_answer(answer: str, expected_terms: list[str]) -> bool:
    answer_lower = answer.lower()
    return all(term.lower() in answer_lower for term in expected_terms)


def main():
    collection = create_collection()
    for pdf in Path("data/documents").glob("*.pdf"):
        add_pdf_to_collection(collection, str(pdf))

    scores = [evaluate_retrieval(collection, case) for case in DATASET]
    average_recall = sum(score["recall_at_k"] for score in scores) / len(scores)
    average_precision = sum(score["precision_at_k"] for score in scores) / len(scores)

    for score in scores:
        print(
            f"{score['question']} | "
            f"recall@3={score['recall_at_k']:.2f} | "
            f"precision@3={score['precision_at_k']:.2f}"
        )
    print(f"Average recall@3: {average_recall:.2f}")
    print(f"Average precision@3: {average_precision:.2f}")


if __name__ == "__main__":
    main()