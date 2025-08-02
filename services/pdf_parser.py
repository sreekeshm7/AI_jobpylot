import PyPDF2
from typing import BinaryIO

class PDFParser:
    @staticmethod
    def extract_text_from_pdf(file: BinaryIO) -> str:
        """Extract text content from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            raise Exception(f"Error parsing PDF: {str(e)}")