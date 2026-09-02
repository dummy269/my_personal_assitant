from pathlib import Path
from pypdf import PdfReader


def load_pdf(pdf_path: str) -> PdfReader:
    if not Path(pdf_path).exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    return PdfReader(pdf_path)


def get_pdf_info(pdf: PdfReader) -> dict:
    return {
        "num_pages": len(pdf.pages),
        "metadata": pdf.metadata if pdf.metadata else None
    }


def extract_text_from_page(pdf: PdfReader, page_num: int) -> str:
    if page_num < 0 or page_num >= len(pdf.pages):
        raise IndexError(f"Page {page_num} out of range")
    return pdf.pages[page_num].extract_text()


def extract_text_from_pdf(pdf: PdfReader) -> dict:
    pages_text = [page.extract_text() for page in pdf.pages]
    return {
        "pages": pages_text,
        "full_text": "\n\n".join(pages_text),
        "num_pages": len(pages_text)
    }
