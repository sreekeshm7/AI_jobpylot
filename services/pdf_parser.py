import PyPDF2
from typing import BinaryIO

class PDFParser:
    @staticmethod
    def extract_text_from_pdf(file: BinaryIO) -> str:
        """Extract text content from PDF file, preserving bullet points using common bullet characters."""
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                raw_text = page.extract_text()
                # Insert a linebreak before any typical bullet character to help LLMs segment bullets
                for bullet_char in ['•', '▪', '■', '‣', '- ', '* ']:
                    raw_text = raw_text.replace(bullet_char, f"\n{bullet_char}")
                text += raw_text + "\n"
            return text.strip()
        except Exception as e:
            raise Exception(f"Error parsing PDF: {str(e)}")
