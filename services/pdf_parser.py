import PyPDF2
from typing import BinaryIO, Dict, Any
import pdfplumber
from fastapi import UploadFile
import io
import openai
import os
import json
import logging

logger = logging.getLogger(__name__)

class PDFParser:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        # Initialize OpenAI client (v1.x syntax)
        from openai import OpenAI
        self.client = OpenAI(api_key=self.api_key)
    
    async def parse_pdf(self, file: UploadFile) -> str:
        """Extract text from PDF file"""
        try:
            contents = await file.read()
            text = ""
            
            # Use pdfplumber for better text extraction
            with pdfplumber.open(io.BytesIO(contents)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            return text
        except Exception as e:
            logger.error(f"PDF parsing failed: {str(e)}")
            raise Exception(f"Failed to extract text from PDF: {str(e)}")
    
    def parse_resume_to_json(self, resume_text: str) -> Dict[str, Any]:
        """Convert resume text to structured JSON format"""
        prompt = f"""
        Parse the following resume text and convert it to the exact JSON format specified below. 
        Extract all available information and structure it properly. If any field is not available, use empty string or empty array as appropriate.

        Resume Text:
        {resume_text}

        Required JSON Format:
        {{
          "resume": {{
            "Name": "...",
            "Email": "...",
            "Phone": "...",
            "Links": {{
              "LinkedIn": "...",
              "GitHub": "...",
              "Portfolio": "...",
              "OtherLinks": [],
              "Projects": [
                {{
                  "Title": "...",
                  "Description": "...",
                  "LiveLink": "...",
                  "GitHubLink": "...",
                  "StartDate": "...",
                  "EndDate": "...",
                  "Role": "...",
                  "description": "...",
                  "bullets": [],
                  "TechStack": []
                }}
              ]
            }},
            "Summary": "...",
            "Skills": {{
              "Tools": [],
              "soft_skills": [],
              "TechStack": [],
              "Languages": [],
              "Others": []
            }},
            "WorkExperience": [
              {{
                "JobTitle": "...",
                "Company": "...",
                "Duration": "...",
                "Location": "...",
                "Responsibilities": [],
                "TechStack": []
              }}
            ],
            "Education": [
              {{
                "Degree": "...",
                "Mark": "...",
                "Institution": "...",
                "Location": "...",
                "StartYear": "...",
                "EndYear": "..."
              }}
            ],
            "Certifications": [],
            "Languages": [],
            "Achievements": [],
            "Awards": [],
            "VolunteerExperience": [],
            "Hobbies": [],
            "Interests": [],
            "References": []
          }},
          "summary": "One-paragraph professional summary (same as Summary above)"
        }}

        Return only the JSON object, no additional text.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse OpenAI response as JSON: {str(e)}")
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

    def _simple_parse_resume(self, resume_text: str) -> Dict[str, Any]:
        """Fallback simple parsing when OpenAI fails"""
        logger.info("Using fallback simple parsing")
        
        lines = resume_text.split('\n')
        
        # Default structure matching your ResumeResponse schema
        default_structure = {
            "resume": {
                "Name": "",
                "Email": "",
                "Phone": "",
                "Links": {
                    "LinkedIn": "",
                    "GitHub": "",
                    "Portfolio": "",
                    "OtherLinks": [],
                    "Projects": []
                },
                "Summary": "",
                "Skills": {
                    "Tools": [],
                    "soft_skills": [],
                    "TechStack": [],
                    "Languages": [],
                    "Others": []
                },
                "WorkExperience": [],
                "Education": [],
                "Certifications": [],
                "Languages": [],
                "Achievements": [],
                "Awards": [],
                "VolunteerExperience": [],
                "Hobbies": [],
                "Interests": [],
                "References": []
            },
            "summary": ""
        }
        
        # Simple extraction logic
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Extract email
            if '@' in line and not default_structure["resume"]["Email"]:
                import re
                email_match = re.search(r'\S+@\S+\.\S+', line)
                if email_match:
                    default_structure["resume"]["Email"] = email_match.group()
            
            # Extract phone
            if any(char.isdigit() for char in line) and not default_structure["resume"]["Phone"]:
                import re
                phone_match = re.search(r'[\+]?[\d\s\-\(\)]{10,}', line)
                if phone_match:
                    default_structure["resume"]["Phone"] = phone_match.group()
            
            # Extract name (first non-empty line that doesn't contain @ or numbers)
            if not default_structure["resume"]["Name"] and not any(char in line for char in '@+0123456789'):
                if len(line.split()) <= 4:  # Likely a name
                    default_structure["resume"]["Name"] = line
        
        return default_structure
