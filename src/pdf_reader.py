"""
V1 — PDF Reader

Purpose:
    Load PDF files and extract text from pages.
    Understand how Python reads PDFs before introducing RAG.

Pipeline:
    PDF file → pypdf → PDF object → Extract text → Python strings
"""

from pathlib import Path

# PDF reading library
# PYPDF: This is the core library for reading PDFs
# Without pypdf, we would need to understand PDF binary format (not worth it)
from pypdf import PdfReader


def load_pdf(pdf_path: str) -> PdfReader:
    """
    Load a PDF file into memory.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        PdfReader object
        
    Raises:
        FileNotFoundError: If PDF doesn't exist
        Exception: If PDF is corrupted
    """
    # Convert string path to Path object (modern Python style)
    path = Path(pdf_path)
    
    # Check if file exists
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    
    # Load the PDF using pypdf
    # PdfReader is the main class that reads and parses PDF files
    try:
        pdf = PdfReader(pdf_path)
        return pdf
    except Exception as e:
        raise Exception(f"Error reading PDF '{pdf_path}': {e}")


def get_pdf_info(pdf: PdfReader) -> dict:
    """
    Extract metadata from a PDF.
    
    Metadata includes:
    - Number of pages
    - Title, Author, Subject, Creator
    - Creation date, modification date
    
    Args:
        pdf: PdfReader object
        
    Returns:
        Dictionary with metadata
    """
    info = {}
    
    # Get number of pages
    info["num_pages"] = len(pdf.pages)
    
    # Get metadata (title, author, etc.)
    # Note: Some PDFs don't have metadata
    if pdf.metadata:
        info["metadata"] = {
            "title": pdf.metadata.get("/Title", "N/A"),
            "author": pdf.metadata.get("/Author", "N/A"),
            "subject": pdf.metadata.get("/Subject", "N/A"),
            "creator": pdf.metadata.get("/Creator", "N/A"),
        }
    else:
        info["metadata"] = "No metadata available"
    
    return info


def extract_text_from_page(pdf: PdfReader, page_number: int) -> str:
    """
    Extract text from a specific page.
    
    Args:
        pdf: PdfReader object
        page_number: Page number (0-indexed)
        
    Returns:
        Extracted text as string
        
    Raises:
        IndexError: If page number is out of range
    """
    # Check if page exists
    if page_number < 0 or page_number >= len(pdf.pages):
        raise IndexError(f"Page {page_number} does not exist. PDF has {len(pdf.pages)} pages.")
    
    # Get the page object
    page = pdf.pages[page_number]
    
    # Extract text from the page
    # This is where pypdf does the heavy lifting:
    # It parses the PDF format and converts embedded text to Python strings
    text = page.extract_text()
    
    return text


def extract_text_from_pdf(pdf: PdfReader) -> dict:
    """
    Extract text from ALL pages in a PDF.
    
    Args:
        pdf: PdfReader object
        
    Returns:
        Dictionary with:
        - "pages": List of text from each page
        - "full_text": All text concatenated
        - "num_pages": Total number of pages
    """
    pages_text = []
    
    # Iterate through each page
    for page_number, page in enumerate(pdf.pages):
        # Extract text from this page
        text = page.extract_text()
        pages_text.append(text)
        
        # Progress indicator
        print(f"  ✓ Extracted page {page_number + 1}/{len(pdf.pages)}")
    
    # Combine all text
    full_text = "\n\n--- PAGE BREAK ---\n\n".join(pages_text)
    
    return {
        "pages": pages_text,
        "full_text": full_text,
        "num_pages": len(pdf.pages),
    }


def inspect_pdf(pdf_path: str) -> None:
    """
    Load a PDF and print useful information about it.
    
    This is the main function to understand what a PDF contains.
    
    Args:
        pdf_path: Path to the PDF file
    """
    print(f"\n📄 Loading PDF: {pdf_path}")
    print("-" * 60)
    
    try:
        # Step 1: Load the PDF
        pdf = load_pdf(pdf_path)
        print("✓ PDF loaded successfully\n")
        
        # Step 2: Get metadata
        print("📋 PDF Information:")
        info = get_pdf_info(pdf)
        print(f"   Number of pages: {info['num_pages']}")
        if isinstance(info["metadata"], dict):
            print(f"   Title: {info['metadata']['title']}")
            print(f"   Author: {info['metadata']['author']}")
        else:
            print(f"   {info['metadata']}")
        print()
        
        # Step 3: Extract text from all pages
        print("📖 Extracting text from all pages...")
        extraction = extract_text_from_pdf(pdf)
        print(f"✓ Extraction complete: {extraction['num_pages']} pages\n")
        
        # Step 4: Print first 500 characters of each page
        for i, page_text in enumerate(extraction["pages"]):
            print(f"\n--- PAGE {i + 1} (first 500 characters) ---")
            # Show first 500 chars
            preview = page_text[:500] if len(page_text) > 500 else page_text
            print(preview)
            if len(page_text) > 500:
                print(f"... [Total: {len(page_text)} characters]")
        
        print("\n" + "=" * 60)
        print(f"✓ Successfully processed: {pdf_path}")
        print("=" * 60 + "\n")
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("   Make sure the PDF exists in data/documents/\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")


if __name__ == "__main__":
    """
    Main entry point.
    
    This allows the script to be run directly:
        python src/pdf_reader.py
    """
    # Example: Try to load a sample PDF
    # Replace this with an actual PDF file
    sample_pdf = "data/documents/sample.pdf"
    
    # Check if sample exists
    if not Path(sample_pdf).exists():
        print(f"⚠️  No PDF found at: {sample_pdf}")
        print("\nTo test this script:")
        print("1. Place a PDF in data/documents/")
        print("2. Edit this file and change the filename")
        print("3. Run: python src/pdf_reader.py")
    else:
        inspect_pdf(sample_pdf)
