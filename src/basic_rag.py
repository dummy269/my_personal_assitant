from pathlib import Path

import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

from src.pdf_reader import extract_text_from_pdf, load_pdf


def split_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    if chunk_size <= overlap:
        raise ValueError("chunk_size must be greater than overlap")

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def create_collection(db_path: str = "data/chroma_db"):
    client = chromadb.PersistentClient(path=db_path)
    return client.get_or_create_collection(
        name="personal_documents",
        embedding_function=DefaultEmbeddingFunction(),
    )


def add_pdf_to_collection(collection, pdf_path: str) -> int:
    pdf = load_pdf(pdf_path)
    text = extract_text_from_pdf(pdf)["full_text"]
    chunks = split_text(text)
    document_name = Path(pdf_path).name

    if not chunks:
        return 0

    collection.upsert(
        ids=[f"{document_name}-{index}" for index in range(len(chunks))],
        documents=chunks,
        metadatas=[{"source": document_name} for _ in chunks],
    )
    return len(chunks)


def search(collection, question: str, number_of_results: int = 3) -> list[dict]:
    result = collection.query(
        query_texts=[question],
        n_results=number_of_results,
    )

    return [
        {"text": text, "source": metadata["source"]}
        for text, metadata in zip(result["documents"][0], result["metadatas"][0])
    ]