"""
V1 Demo — PDF Reader

This script shows how to use the PDF reader module.

It demonstrates:
1. Loading a PDF file
2. Extracting metadata
3. Extracting text from pages
4. Handling errors
"""

from pathlib import Path
from src.pdf_reader import inspect_pdf


def main():
    """
    Main demo function.
    Looks for PDFs in data/documents/ and processes them.
    """
    print("\n" + "=" * 60)
    print("V1 — PDF Reader Demo")
    print("=" * 60)
    
    documents_dir = Path("data/documents")
    
    # Check if documents directory exists
    if not documents_dir.exists():
        print(f"❌ Directory not found: {documents_dir}")
        return
    
    # Find all PDF files
    pdf_files = list(documents_dir.glob("*.pdf"))
    
    if not pdf_files:
        print(f"\n⚠️  No PDF files found in {documents_dir}/")
        print("\nTo test this script:")
        print("1. Download or create a PDF file")
        print("2. Place it in: data/documents/")
        print("3. Run this script again: python main.py")
        return
    
    # Process each PDF
    print(f"\n📂 Found {len(pdf_files)} PDF file(s) in data/documents/:\n")
    
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"{i}. {pdf_file.name}")
    
    print()
    
    # Process each file
    for pdf_file in pdf_files:
        inspect_pdf(str(pdf_file))


if __name__ == "__main__":
    main()
