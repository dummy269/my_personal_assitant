from src.pdf_reader import load_pdf, get_pdf_info, extract_text_from_page, extract_text_from_pdf


pdf_path = "data/documents/abhay_resume.pdf"

pdf = load_pdf(pdf_path)
info = get_pdf_info(pdf)
print(f"Pages: {info['num_pages']}")

text = extract_text_from_page(pdf, 0)
print(f"\nFirst page ({len(text)} chars):")
print(text[:300])

result = extract_text_from_pdf(pdf)
print(f"\nAll pages: {result['num_pages']}")
print(f"Total characters: {len(result['full_text'])}")
