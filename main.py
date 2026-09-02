from pathlib import Path
from src.pdf_reader import load_pdf, extract_text_from_pdf


def process_pdfs():
    docs_dir = Path("data/documents")
    pdfs = list(docs_dir.glob("*.pdf"))
    
    if not pdfs:
        print("No PDFs found in data/documents/")
        return
    
    print(f"\nFound {len(pdfs)} PDF(s)\n")
    
    for pdf_file in pdfs:
        try:
            pdf = load_pdf(str(pdf_file))
            result = extract_text_from_pdf(pdf)
            print(f"✓ {pdf_file.name}")
            print(f"  Pages: {result['num_pages']}, Characters: {len(result['full_text'])}\n")
        except Exception as e:
            print(f"✗ {pdf_file.name}: {e}\n")


if __name__ == "__main__":
    process_pdfs()
