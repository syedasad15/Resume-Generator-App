
import pdfplumber

def extract_text_from_pdf(uploaded_file) -> str:
    """Extracts plain text from uploaded PDF file."""
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()
