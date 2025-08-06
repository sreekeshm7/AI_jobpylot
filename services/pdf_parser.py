import PyPDF2
from typing import BinaryIO
import pdfplumber
from fastapi import UploadFile
import io

class PDFParser:
    def __init__(self):
        pass

    async def parse_pdf(self, file: UploadFile) -> str:
        # Read the file contents into memory
        contents = await file.read()
        text = ""
        with pdfplumber.open(io.BytesIO(contents)) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
