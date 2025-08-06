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

    async def parse_resume_to_json(self, resume_text: str) -> dict:
        """
        Use OpenAI to parse resume text into structured JSON format
        """
        prompt = f"""
        Parse the following resume text into a structured JSON format with these sections:
        - Summary: Professional summary
        - Experience: List of work experiences
        - Education: Educational background
        - Skills: Technical and soft skills
        - Contact: Contact information
        
        Resume text:
        {resume_text}
        
        Return only valid JSON without any additional text.
        """
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.1
            )
            
            # Parse the JSON response
            import json
            result = json.loads(response.choices[0].message.content)
            return result
        except Exception as e:
            # Fallback to simple parsing
            return self._simple_parse_resume(resume_text)
