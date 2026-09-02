"""
V1 Learning Script — Understanding PDF Reading

This script teaches you how the PDF reader works by example.

Concepts demonstrated:
1. Loading a PDF file
2. Accessing page count
3. Extracting text from individual pages
4. Error handling
5. Understanding page vs document structure
"""

from pathlib import Path
from src.pdf_reader import load_pdf, get_pdf_info, extract_text_from_page, extract_text_from_pdf


def lesson_1_load_pdf():
    """
    LESSON 1: Loading a PDF file
    
    What's happening:
    - We point Python to a PDF file
    - pypdf opens and reads the binary data
    - We get a PdfReader object in memory
    """
    print("\n" + "=" * 60)
    print("LESSON 1 — Loading a PDF File")
    print("=" * 60)
    
    pdf_path = "data/documents/abhay_resume.pdf"
    
    print(f"\nCode: pdf = load_pdf('{pdf_path}')")
    print("What this does:")
    print("  1. Opens the file from disk")
    print("  2. Reads the PDF binary format")
    print("  3. Parses the PDF structure")
    print("  4. Returns a PdfReader object\n")
    
    try:
        pdf = load_pdf(pdf_path)
        print(f"✓ Success! Got a PdfReader object: {type(pdf)}")
        return pdf
    except FileNotFoundError as e:
        print(f"❌ {e}")
        return None


def lesson_2_pdf_info(pdf):
    """
    LESSON 2: Understanding PDF metadata
    
    What's happening:
    - We extract information ABOUT the PDF
    - This is NOT the content, just metadata
    """
    print("\n" + "=" * 60)
    print("LESSON 2 — PDF Metadata (Information About the PDF)")
    print("=" * 60)
    
    print("\nCode: info = get_pdf_info(pdf)")
    print("What this does:")
    print("  - Counts the number of pages")
    print("  - Reads metadata (title, author, etc.)")
    print("  - Returns a dictionary\n")
    
    info = get_pdf_info(pdf)
    print(f"Number of pages: {info['num_pages']}")
    print(f"Metadata: {info['metadata']}\n")
    
    # Explain pages
    print("Key concept: PAGES")
    print(f"  - This PDF has {info['num_pages']} page(s)")
    print(f"  - Each page is a separate object")
    print(f"  - We can extract text from each page individually")
    print(f"  - Or extract from ALL pages at once")
    
    return info


def lesson_3_single_page(pdf):
    """
    LESSON 3: Extracting text from a single page
    
    What's happening:
    - We select ONE page
    - We extract its text
    - We see what's on that page
    """
    print("\n" + "=" * 60)
    print("LESSON 3 — Extracting Text from a Single Page")
    print("=" * 60)
    
    print("\nCode: text = extract_text_from_page(pdf, page_number=0)")
    print("What this does:")
    print("  - Selects page 0 (first page, 0-indexed)")
    print("  - Extracts text from that page")
    print("  - Returns the text as a Python string\n")
    
    try:
        # Extract from first page (page 0)
        text = extract_text_from_page(pdf, 0)
        
        print(f"✓ Extracted text from page 1")
        print(f"  Length: {len(text)} characters\n")
        
        # Show preview
        preview = text[:300] if len(text) > 300 else text
        print("Preview (first 300 characters):")
        print("-" * 60)
        print(preview)
        if len(text) > 300:
            print("... [truncated]")
        print("-" * 60)
        
    except Exception as e:
        print(f"❌ {e}")


def lesson_4_all_pages(pdf):
    """
    LESSON 4: Extracting text from all pages
    
    What's happening:
    - We loop through ALL pages
    - We extract text from each
    - We organize the results
    """
    print("\n" + "=" * 60)
    print("LESSON 4 — Extracting Text from ALL Pages")
    print("=" * 60)
    
    print("\nCode: extraction = extract_text_from_pdf(pdf)")
    print("What this does:")
    print("  - Loops through EVERY page")
    print("  - Extracts text from each")
    print("  - Returns:")
    print("    * 'pages': list of text (one per page)")
    print("    * 'full_text': all pages concatenated")
    print("    * 'num_pages': total count\n")
    
    extraction = extract_text_from_pdf(pdf)
    
    print(f"Result:")
    print(f"  - Total pages: {extraction['num_pages']}")
    print(f"  - Total characters: {len(extraction['full_text'])}")
    print(f"  - Average per page: {len(extraction['full_text']) // max(extraction['num_pages'], 1)}")
    
    # Show breakdown per page
    print("\nText per page:")
    for i, page_text in enumerate(extraction['pages']):
        print(f"  Page {i + 1}: {len(page_text)} characters")


def lesson_5_pipeline():
    """
    LESSON 5: Understanding the complete pipeline
    
    What's happening:
    - We visualize the FLOW of data
    - From file to Python strings
    """
    print("\n" + "=" * 60)
    print("LESSON 5 — The Complete PDF Reading Pipeline")
    print("=" * 60)
    
    print("\nWhen you read a PDF, here's what happens:\n")
    print("1. PDF FILE (on disk)")
    print("   └─ Binary format (not human-readable)")
    print("\n2. OPEN & LOAD (pypdf does this)")
    print("   └─ File is read into memory")
    print("   └─ PDF structure is parsed")
    print("\n3. GET METADATA (get_pdf_info())")
    print("   └─ Extract title, author, page count, etc.")
    print("\n4. GET PAGES (pdf.pages)")
    print("   └─ Access individual page objects")
    print("\n5. EXTRACT TEXT (page.extract_text())")
    print("   └─ Convert PDF text to Python strings")
    print("\n6. PYTHON STRINGS (we can use!)")
    print("   └─ Now we can manipulate with normal Python")
    
    print("\nVisualized:")
    print("""
    PDF File
        ↓
    PdfReader (load_pdf)
        ↓
    Metadata (get_pdf_info)
    Pages (pdf.pages)
        ↓
    Extract Text (extract_text_from_page)
        ↓
    Python Strings
        ↓
    [Ready for V2: Chunking & Embeddings]
    """)


def main():
    print("\n" + "=" * 70)
    print("V1 — PDF READER LEARNING GUIDE")
    print("Understanding how Python reads PDF files")
    print("=" * 70)
    
    # Lesson 1: Load PDF
    pdf = lesson_1_load_pdf()
    if pdf is None:
        return
    
    # Lesson 2: Understand pages and metadata
    info = lesson_2_pdf_info(pdf)
    
    # Lesson 3: Extract from single page
    lesson_3_single_page(pdf)
    
    # Lesson 4: Extract from all pages
    lesson_4_all_pages(pdf)
    
    # Lesson 5: Understand the pipeline
    lesson_5_pipeline()
    
    # Summary
    print("\n" + "=" * 70)
    print("WHAT YOU'VE LEARNED")
    print("=" * 70)
    print("""
✓ PDFs are binary files, not plain text
✓ pypdf library handles the complexity of reading PDFs
✓ A PDF consists of PAGES
✓ Each page contains TEXT that can be extracted
✓ Text is extracted as Python strings
✓ We can extract single pages or all pages
✓ Metadata tells us about the PDF (title, author, etc.)
✓ Extracted text can be used for further processing

NEXT STEPS (V2):
→ Take extracted text and break it into CHUNKS
→ Convert chunks to EMBEDDINGS (vectors)
→ Store in CHROMA vector database
→ Learn RETRIEVAL (similarity search)
    """)
    print("=" * 70)


if __name__ == "__main__":
    main()
