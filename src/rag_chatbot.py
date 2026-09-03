import os

from dotenv import load_dotenv
from openai import OpenAI

from src.basic_rag import search


def build_prompt(question: str, results: list[dict]) -> str:
    context = "\n\n".join(
        f"Source: {result['source']}\n{result['text']}" for result in results
    )
    return (
        "Answer the question using only the context below. "
        "If the answer is not in the context, say you do not know.\n\n"
        f"Context:\n{context}\n\nQuestion: {question}"
    )


def answer_question(collection, question: str) -> str:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set in .env")

    results = search(collection, question)
    prompt = build_prompt(question, results)
    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        instructions="You are a helpful assistant answering questions about personal documents.",
        input=prompt,
    )
    return response.output_text