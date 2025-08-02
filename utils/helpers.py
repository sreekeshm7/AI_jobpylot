import re
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

class TextProcessor:
    """Utility class for text processing operations"""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove special characters but keep important punctuation
        text = re.sub(r'[^\w\s\-\.\,\(\)\@]', '', text)
        
        return text
    
    @staticmethod
    def extract_email(text: str) -> Optional[str]:
        """Extract email address from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        matches = re.findall(email_pattern, text)
        return matches[0] if matches else None
    
    @staticmethod
    def extract_phone(text: str) -> Optional[str]:
        """Extract phone number from text"""
        phone_patterns = [
            r'\+?\d{1,3}[-.\s]?$?\d{3}$?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            r'$\d{3}$\s?\d{3}[-.]?\d{4}'
        ]
        
        for pattern in phone_patterns:
            matches = re.findall(pattern, text)
            if matches:
                # Clean the phone number
                phone = re.sub(r'[^\d+]', '', matches[0])
                return phone
        
        return None
    
    @staticmethod
    def extract_urls(text: str) -> List[str]:
        """Extract URLs from text"""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\$\$,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.findall(url_pattern, text)
    
    @staticmethod
    def split_sentences(text: str) -> List[str]:
        """Split text into sentences"""
        if not text:
            return []
        
        # Simple sentence splitting
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]

class ResumeValidator:
    """Utility class for resume validation"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        if not email:
            return False
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number format"""
        if not phone:
            return False
        
        # Remove all non-digit characters except +
        cleaned = re.sub(r'[^\d+]', '', phone)
        
        # Check if it's a valid length (7-15 digits, optionally starting with +)
        if cleaned.startswith('+'):
            return 8 <= len(cleaned) <= 16
        else:
            return 7 <= len(cleaned) <= 15
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL format"""
        if not url:
            return False
        
        url_pattern = r'^https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:\w*))?)?$'
        return bool(re.match(url_pattern, url))
    
    @staticmethod
    def validate_date_format(date_str: str) -> bool:
        """Validate date format"""
        if not date_str:
            return True  # Empty dates are okay
        
        common_formats = [
            '%Y-%m-%d',  # 2023-01-01
            '%m/%d/%Y',  # 01/01/2023
            '%d/%m/%Y',  # 01/01/2023
            '%Y',        # 2023
            '%m/%Y',     # 01/2023
            '%B %Y',     # January 2023
            '%b %Y',     # Jan 2023
        ]
        
        for fmt in common_formats:
            try:
                datetime.strptime(date_str, fmt)
                return True
            except ValueError:
                continue
        
        return False

class ScoreCalculator:
    """Utility class for ATS score calculations"""
    
    @staticmethod
    def calculate_keyword_density(text: str, keywords: List[str]) -> float:
        """Calculate keyword density in text"""
        if not text or not keywords:
            return 0.0
        
        text_lower = text.lower()
        word_count = len(text.split())
        
        if word_count == 0:
            return 0.0
        
        keyword_count = 0
        for keyword in keywords:
            keyword_count += text_lower.count(keyword.lower())
        
        return (keyword_count / word_count) * 100
    
    @staticmethod
    def calculate_section_completeness(section_data: Any) -> float:
        """Calculate completeness score for a resume section"""
        if not section_data:
            return 0.0
        
        if isinstance(section_data, str):
            return 100.0 if section_data.strip() else 0.0
        
        if isinstance(section_data, list):
            if not section_data:
                return 0.0
            
            # Check if list items are meaningful
            meaningful_items = [item for item in section_data if str(item).strip()]
            return (len(meaningful_items) / len(section_data)) * 100 if section_data else 0.0
        
        if isinstance(section_data, dict):
            total_fields = len(section_data)
            if total_fields == 0:
                return 0.0
            
            filled_fields = 0
            for value in section_data.values():
                if value and str(value).strip():
                    filled_fields += 1
            
            return (filled_fields / total_fields) * 100
        
        return 50.0  # Default for unknown types
    
    @staticmethod
    def calculate_action_verb_score(text: str) -> float:
        """Calculate score based on action verbs usage"""
        if not text:
            return 0.0
        
        strong_verbs = [
            'achieved', 'accomplished', 'delivered', 'implemented', 'developed',
            'created', 'designed', 'built', 'launched', 'managed', 'led',
            'optimized', 'improved', 'increased', 'decreased', 'reduced',
            'streamlined', 'automated', 'innovated', 'pioneered', 'spearheaded'
        ]
        
        weak_verbs = [
            'responsible for', 'worked on', 'helped with', 'assisted',
            'participated in', 'involved in', 'handled', 'dealt with'
        ]
        
        text_lower = text.lower()
        strong_count = sum(1 for verb in strong_verbs if verb in text_lower)
        weak_count = sum(1 for verb in weak_verbs if verb in text_lower)
        
        total_sentences = len(TextProcessor.split_sentences(text))
        
        if total_sentences == 0:
            return 0.0
        
        # Score based on ratio of strong to weak verbs
        if weak_count == 0:
            return min(100.0, (strong_count / total_sentences) * 100)
        
        ratio = strong_count / (strong_count + weak_count)
        return ratio * 100

class DataFormatter:
    """Utility class for data formatting"""
    
    @staticmethod
    def format_resume_json(raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format and clean raw resume JSON data"""
        if not raw_data:
            return {}
        
        # Deep copy to avoid modifying original
        formatted_data = json.loads(json.dumps(raw_data))
        
        # Clean text fields
        def clean_nested_data(data):
            if isinstance(data, dict):
                return {k: clean_nested_data(v) for k, v in data.items()}
            elif isinstance(data, list):
                return [clean_nested_data(item) for item in data]
            elif isinstance(data, str):
                return TextProcessor.clean_text(data)
            else:
                return data
        
        return clean_nested_data(formatted_data)
    
    @staticmethod
    def standardize_date_format(date_str: str) -> str:
        """Standardize date format to MM/YYYY"""
        if not date_str:
            return ""
        
        # Common formats to try
        formats_to_try = [
            ('%Y-%m-%d', '%m/%Y'),  # 2023-01-01 -> 01/2023
            ('%m/%d/%Y', '%m/%Y'),  # 01/01/2023 -> 01/2023
            ('%d/%m/%Y', '%m/%Y'),  # 01/01/2023 -> 01/2023
            ('%Y', '%Y'),           # 2023 -> 2023
            ('%m/%Y', '%m/%Y'),     # 01/2023 -> 01/2023
            ('%B %Y', '%m/%Y'),     # January 2023 -> 01/2023
            ('%b %Y', '%m/%Y'),     # Jan 2023 -> 01/2023
        ]
        
        for input_fmt, output_fmt in formats_to_try:
            try:
                parsed_date = datetime.strptime(date_str, input_fmt)
                return parsed_date.strftime(output_fmt)
            except ValueError:
                continue
        
        # If no format matches, return original
        return date_str
    
    @staticmethod
    def extract_tech_stack(text: str) -> List[str]:
        """Extract technology stack from text"""
        if not text:
            return []
        
        # Common technologies (this could be expanded)
        tech_keywords = [
            # Programming Languages
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust',
            'swift', 'kotlin', 'scala', 'r', 'matlab', 'sql',
            
            # Frameworks & Libraries
            'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring', 'laravel',
            'rails', '.net', 'jquery', 'bootstrap', 'tailwind',
            
            # Databases
            'mysql', 'postgresql', 'mongodb', 'redis', 'cassandra', 'dynamodb', 'sqlite',
            
            # Cloud & DevOps
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'github', 'gitlab',
            'terraform', 'ansible',
            
            # Tools
            'visual studio code', 'intellij', 'eclipse', 'pycharm', 'postman', 'jira', 'confluence',
            'slack', 'trello', 'notion', 'figma', 'adobe xd', 'canva'
        ]