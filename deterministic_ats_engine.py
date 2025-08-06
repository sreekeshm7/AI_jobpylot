import re
import json
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class DeterministicScore:
    score: float
    max_score: float = 10.0
    weight: float = 1.0

    def get_percentage(self) -> float:
        return (self.score / self.max_score) * 100

class DeterministicATSEngine:
    """Deterministic ATS scoring engine with rule-based evaluation"""
    
    def __init__(self):
        # Weak verbs that should be replaced with stronger alternatives
        self.weak_verbs = {
            'helped', 'assisted', 'worked on', 'participated in', 'was involved in',
            'contributed to', 'supported', 'helped with', 'was part of', 'took part in',
            'was responsible for', 'did', 'made', 'got', 'had', 'used', 'did work on',
            'was working on', 'was helping with', 'was supporting', 'was contributing to'
        }
        
        # Strong action verbs for better impact
        self.strong_verbs = {
            'developed', 'implemented', 'designed', 'created', 'built', 'launched',
            'managed', 'led', 'directed', 'orchestrated', 'spearheaded', 'initiated',
            'established', 'founded', 'founded', 'optimized', 'improved', 'enhanced',
            'streamlined', 'automated', 'integrated', 'deployed', 'delivered',
            'achieved', 'accomplished', 'exceeded', 'surpassed', 'generated',
            'increased', 'reduced', 'saved', 'cut', 'boosted', 'drove', 'facilitated',
            'coordinated', 'collaborated', 'mentored', 'trained', 'educated',
            'researched', 'analyzed', 'evaluated', 'assessed', 'reviewed',
            'maintained', 'upgraded', 'modernized', 'migrated', 'converted'
        }
        
        # Buzzwords and clichés to avoid
        self.buzzwords = {
            'synergy', 'leverage', 'paradigm', 'disruptive', 'innovative',
            'cutting-edge', 'best-in-class', 'world-class', 'game-changer',
            'thought leader', 'guru', 'ninja', 'rockstar', 'wizard',
            'passionate', 'dynamic', 'proactive', 'results-driven',
            'detail-oriented', 'team player', 'self-starter', 'go-getter',
            'hard-working', 'dedicated', 'committed', 'motivated',
            'problem solver', 'quick learner', 'fast-paced', 'high-energy',
            'out-of-the-box', 'outside the box', 'think outside the box',
            'value-added', 'value proposition', 'core competency',
            'mission-critical', 'strategic', 'tactical', 'scalable',
            'robust', 'comprehensive', 'holistic', 'end-to-end'
        }
        
        # Quantifiable indicators for measurable impact
        self.quantifiable_indicators = [
            r'\d+%', r'\d+\s*percent', r'\d+\s*%',  # Percentages
            r'\$\d+', r'\d+\s*dollars', r'\d+\s*USD',  # Money
            r'\d+\s*people', r'\d+\s*users', r'\d+\s*customers',  # People
            r'\d+\s*years', r'\d+\s*months', r'\d+\s*weeks',  # Time
            r'\d+\s*projects', r'\d+\s*applications', r'\d+\s*systems',  # Projects
            r'\d+\s*times', r'\d+\s*fold', r'\d+x',  # Multipliers
            r'increased\s+by\s+\d+', r'decreased\s+by\s+\d+',  # Changes
            r'reduced\s+by\s+\d+', r'improved\s+by\s+\d+',  # Improvements
            r'from\s+\d+\s+to\s+\d+', r'grew\s+from\s+\d+\s+to\s+\d+'  # Ranges
        ]
        
        # Date patterns for consistency checking
        self.date_patterns = [
            r'\d{4}-\d{2}',  # YYYY-MM
            r'\d{2}/\d{4}',  # MM/YYYY
            r'\d{4}/\d{2}',  # YYYY/MM
            r'\w+\s+\d{4}',  # Month YYYY
            r'\d{2}-\d{4}',  # MM-YYYY
            r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
            r'\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY
            r'\d{4}/\d{2}/\d{2}'   # YYYY/MM/DD
        ]
        
        # Teamwork and collaboration indicators
        self.teamwork_indicators = [
            'team', 'collaborate', 'collaboration', 'coordinate', 'coordination',
            'lead', 'led', 'managed', 'mentor', 'mentored', 'train', 'trained',
            'supervise', 'supervised', 'guide', 'guided', 'facilitate',
            'facilitated', 'organize', 'organized', 'plan', 'planned',
            'work with', 'worked with', 'partner', 'partnered', 'joint',
            'cross-functional', 'cross-functional team', 'multi-disciplinary',
            'stakeholder', 'stakeholders', 'client', 'clients', 'customer',
            'customers', 'vendor', 'vendors', 'supplier', 'suppliers'
        ]
        
        # Contact information fields
        self.required_contact_fields = [
            'email', 'phone', 'address', 'location', 'city', 'state',
            'linkedin', 'github', 'portfolio', 'website'
        ]
        
        # ATS keywords for different roles
        self.ats_keywords = {
            'software_developer': [
                'python', 'javascript', 'java', 'react', 'node.js', 'sql',
                'aws', 'docker', 'kubernetes', 'git', 'agile', 'scrum',
                'api', 'rest', 'graphql', 'microservices', 'ci/cd',
                'machine learning', 'ai', 'data science', 'full stack',
                'frontend', 'backend', 'devops', 'cloud', 'database'
            ],
            'data_scientist': [
                'python', 'r', 'sql', 'pandas', 'numpy', 'scikit-learn',
                'tensorflow', 'pytorch', 'machine learning', 'deep learning',
                'statistics', 'data analysis', 'data visualization',
                'tableau', 'power bi', 'jupyter', 'spark', 'hadoop',
                'nlp', 'computer vision', 'predictive modeling'
            ],
            'project_manager': [
                'agile', 'scrum', 'kanban', 'waterfall', 'project management',
                'stakeholder management', 'risk management', 'budget management',
                'timeline', 'milestone', 'deliverable', 'scope', 'requirements',
                'jira', 'asana', 'trello', 'ms project', 'prince2', 'pmp',
                'team leadership', 'communication', 'presentation'
            ]
        }
    
    def score_summary(self, summary: str) -> DeterministicScore:
        """Score resume summary section"""
        if not summary or len(summary.strip()) < 10:
            return DeterministicScore(2.0)
        
        score = 5.0  # Base score
        summary_lower = summary.lower()
        
        # Check length (ideal: 3-4 sentences)
        sentences = summary.split('.')
        if 3 <= len(sentences) <= 4:
            score += 1.0
        elif len(sentences) > 4:
            score -= 1.0
        
        # Check for strong verbs
        strong_verb_count = sum(1 for verb in self.strong_verbs if verb in summary_lower)
        score += min(strong_verb_count * 0.5, 2.0)
        
        # Check for quantifiable achievements
        quantifiable_count = sum(1 for pattern in self.quantifiable_indicators 
                               if re.search(pattern, summary, re.IGNORECASE))
        score += min(quantifiable_count * 1.0, 2.0)
        
        # Penalize buzzwords
        buzzword_count = sum(1 for buzzword in self.buzzwords if buzzword in summary_lower)
        score -= min(buzzword_count * 0.5, 2.0)
        
        return DeterministicScore(max(0.0, min(10.0, score)))
    
    def score_dates(self, resume_data: Dict[str, Any]) -> DeterministicScore:
        """Score date formatting consistency"""
        score = 5.0  # Base score
        date_count = 0
        consistent_format = True
        previous_format = None
        
        # Check work experience dates
        for experience in resume_data.get('WorkExperience', []):
            duration = experience.get('Duration', '')
            if duration:
                date_count += 1
                current_format = self._get_date_format(duration)
                if previous_format and current_format != previous_format:
                    consistent_format = False
                previous_format = current_format
        
        # Check education dates
        for education in resume_data.get('Education', []):
            start_year = education.get('StartYear', '')
            end_year = education.get('EndYear', '')
            if start_year or end_year:
                date_count += 1
        
        if date_count > 0:
            if consistent_format:
                score += 3.0
            else:
                score -= 2.0
            
            # Bonus for proper date ranges
            if date_count >= 2:
                score += 1.0
        
        return DeterministicScore(max(0.0, min(10.0, score)))
    
    def score_weak_verbs(self, resume_data: Dict[str, Any]) -> DeterministicScore:
        """Score weak verb usage"""
        score = 5.0  # Base score
        weak_verb_count = 0
        strong_verb_count = 0
        total_verbs = 0
        
        # Analyze all text content
        all_text = self._extract_all_text(resume_data)
        
        for weak_verb in self.weak_verbs:
            weak_verb_count += len(re.findall(r'\b' + weak_verb + r'\b', all_text, re.IGNORECASE))
        
        for strong_verb in self.strong_verbs:
            strong_verb_count += len(re.findall(r'\b' + strong_verb + r'\b', all_text, re.IGNORECASE))
        
        total_verbs = weak_verb_count + strong_verb_count
        
        if total_verbs > 0:
            weak_verb_ratio = weak_verb_count / total_verbs
            strong_verb_ratio = strong_verb_count / total_verbs
            
            if weak_verb_ratio > 0.5:
                score -= 3.0
            elif weak_verb_ratio > 0.3:
                score -= 1.5
            
            if strong_verb_ratio > 0.7:
                score += 2.0
            elif strong_verb_ratio > 0.5:
                score += 1.0
        
        return DeterministicScore(max(0.0, min(10.0, score)))
    
    def score_quantity_impact(self, resume_data: Dict[str, Any]) -> DeterministicScore:
        """Score quantifiable achievements and impact"""
        score = 5.0  # Base score
        quantifiable_count = 0
        all_text = self._extract_all_text(resume_data)
        
        for pattern in self.quantifiable_indicators:
            matches = re.findall(pattern, all_text, re.IGNORECASE)
            quantifiable_count += len(matches)
        
        if quantifiable_count >= 5:
            score += 3.0
        elif quantifiable_count >= 3:
            score += 2.0
        elif quantifiable_count >= 1:
            score += 1.0
        else:
            score -= 2.0
        
        return DeterministicScore(max(0.0, min(10.0, score)))
    
    def score_teamwork(self, resume_data: Dict[str, Any]) -> DeterministicScore:
        """Score teamwork and collaboration indicators"""
        score = 5.0  # Base score
        teamwork_count = 0
        all_text = self._extract_all_text(resume_data)
        
        for indicator in self.teamwork_indicators:
            matches = re.findall(r'\b' + indicator + r'\b', all_text, re.IGNORECASE)
            teamwork_count += len(matches)
        
        if teamwork_count >= 5:
            score += 3.0
        elif teamwork_count >= 3:
            score += 2.0
        elif teamwork_count >= 1:
            score += 1.0
        else:
            score -= 1.0
        
        return DeterministicScore(max(0.0, min(10.0, score)))
    
    def score_buzzwords(self, resume_data: Dict[str, Any]) -> DeterministicScore:
        """Score buzzword usage"""
        score = 5.0  # Base score
        buzzword_count = 0
        all_text = self._extract_all_text(resume_data)
        
        for buzzword in self.buzzwords:
            matches = re.findall(r'\b' + buzzword + r'\b', all_text, re.IGNORECASE)
            buzzword_count += len(matches)
        
        if buzzword_count == 0:
            score += 3.0
        elif buzzword_count <= 2:
            score += 1.0
        elif buzzword_count <= 5:
            score -= 1.0
        else:
            score -= 3.0
        
        return DeterministicScore(max(0.0, min(10.0, score)))
    
    def score_contact_details(self, resume_data: Dict[str, Any]) -> DeterministicScore:
        """Score contact information completeness"""
        score = 5.0  # Base score
        contact_fields = 0
        
        for field in self.required_contact_fields:
            if field in resume_data and resume_data[field]:
                contact_fields += 1
        
        # Essential fields: email, phone
        essential_fields = ['email', 'phone']
        essential_count = sum(1 for field in essential_fields 
                            if field in resume_data and resume_data[field])
        
        if essential_count == 2:
            score += 3.0
        elif essential_count == 1:
            score += 1.0
        else:
            score -= 2.0
        
        # Bonus for additional fields
        if contact_fields >= 4:
            score += 1.0
        
        return DeterministicScore(max(0.0, min(10.0, score)))
    
    def score_grammar_spelling(self, resume_data: Dict[str, Any]) -> DeterministicScore:
        """Score grammar and spelling (basic check)"""
        score = 5.0  # Base score
        all_text = self._extract_all_text(resume_data)
        
        # Basic grammar checks (simplified)
        common_errors = [
            r'\b(i)\s+',  # Lowercase 'i' instead of 'I'
            r'\b(its)\s+(?=\w)',  # 'its' instead of 'it\'s'
            r'\b(youre)\b',  # 'youre' instead of 'you\'re'
            r'\b(theyre)\b',  # 'theyre' instead of 'they\'re'
            r'\b(weve)\b',  # 'weve' instead of 'we\'ve'
            r'\b(ive)\b',  # 'ive' instead of 'I\'ve'
        ]
        
        error_count = 0
        for pattern in common_errors:
            matches = re.findall(pattern, all_text, re.IGNORECASE)
            error_count += len(matches)
        
        if error_count == 0:
            score += 3.0
        elif error_count <= 2:
            score += 1.0
        elif error_count <= 5:
            score -= 1.0
        else:
            score -= 3.0
        
        return DeterministicScore(max(0.0, min(10.0, score)))
    
    def score_formatting_layout(self, resume_data: Dict[str, Any]) -> DeterministicScore:
        """Score formatting and layout (basic assessment)"""
        score = 5.0  # Base score
        
        # Check for required sections
        required_sections = ['WorkExperience', 'Education', 'Skills']
        present_sections = sum(1 for section in required_sections 
                             if section in resume_data and resume_data[section])
        
        if present_sections == 3:
            score += 2.0
        elif present_sections == 2:
            score += 1.0
        else:
            score -= 1.0
        
        # Check for skills organization
        skills = resume_data.get('Skills', {})
        if isinstance(skills, dict) and len(skills) > 0:
            score += 1.0
        
        # Check for work experience details
        work_exp = resume_data.get('WorkExperience', [])
        if work_exp and len(work_exp) > 0:
            first_job = work_exp[0]
            if 'Responsibilities' in first_job and len(first_job['Responsibilities']) > 0:
                score += 1.0
        
        return DeterministicScore(max(0.0, min(10.0, score)))
    
    def score_ats_keywords(self, resume_data: Dict[str, Any], job_keywords: List[str] = None) -> DeterministicScore:
        """Score ATS keyword optimization"""
        score = 5.0  # Base score
        all_text = self._extract_all_text(resume_data)
        
        if job_keywords:
            # Score against provided keywords
            keyword_matches = 0
            for keyword in job_keywords:
                if re.search(r'\b' + re.escape(keyword) + r'\b', all_text, re.IGNORECASE):
                    keyword_matches += 1
            
            if keyword_matches >= len(job_keywords) * 0.8:
                score += 3.0
            elif keyword_matches >= len(job_keywords) * 0.5:
                score += 2.0
            elif keyword_matches >= len(job_keywords) * 0.3:
                score += 1.0
        else:
            # Score against general tech keywords
            general_keywords = [
                'python', 'javascript', 'java', 'sql', 'react', 'node.js',
                'aws', 'docker', 'git', 'agile', 'api', 'database'
            ]
            
            keyword_matches = 0
            for keyword in general_keywords:
                if re.search(r'\b' + keyword + r'\b', all_text, re.IGNORECASE):
                    keyword_matches += 1
            
            if keyword_matches >= 5:
                score += 2.0
            elif keyword_matches >= 3:
                score += 1.0
        
        return DeterministicScore(max(0.0, min(10.0, score)))
    
    def score_skills_relevance(self, resume_data: Dict[str, Any]) -> DeterministicScore:
        """Score skills section relevance"""
        score = 5.0  # Base score
        skills = resume_data.get('Skills', {})
        
        if not skills:
            return DeterministicScore(2.0)
        
        # Check if skills are categorized
        if isinstance(skills, dict) and len(skills) > 1:
            score += 1.0
        
        # Check for technical skills
        tech_skills = skills.get('TechStack', [])
        if tech_skills and len(tech_skills) >= 3:
            score += 2.0
        elif tech_skills and len(tech_skills) >= 1:
            score += 1.0
        
        # Check for soft skills
        soft_skills = skills.get('soft_skills', [])
        if soft_skills and len(soft_skills) >= 2:
            score += 1.0
        
        return DeterministicScore(max(0.0, min(10.0, score)))
    
    def score_achievements_vs_responsibilities(self, resume_data: Dict[str, Any]) -> DeterministicScore:
        """Score balance between achievements and responsibilities"""
        score = 5.0  # Base score
        achievement_count = 0
        responsibility_count = 0
        
        # Analyze work experience
        for experience in resume_data.get('WorkExperience', []):
            responsibilities = experience.get('Responsibilities', [])
            for resp in responsibilities:
                # Check for achievement indicators
                if any(indicator in resp.lower() for indicator in ['achieved', 'increased', 'improved', 'reduced', 'saved', 'generated', 'led to']):
                    achievement_count += 1
                else:
                    responsibility_count += 1
        
        if achievement_count > 0 and responsibility_count > 0:
            ratio = achievement_count / (achievement_count + responsibility_count)
            if ratio >= 0.6:
                score += 2.0
            elif ratio >= 0.4:
                score += 1.0
            elif ratio < 0.2:
                score -= 1.0
        elif achievement_count > 0:
            score += 1.0
        else:
            score -= 2.0
        
        return DeterministicScore(max(0.0, min(10.0, score)))
    
    def score_unnecessary_sections(self, resume_data: Dict[str, Any]) -> DeterministicScore:
        """Score unnecessary sections"""
        score = 5.0  # Base score
        
        # Check for unnecessary sections
        unnecessary_sections = ['Hobbies', 'Interests', 'Personal', 'References']
        found_unnecessary = 0
        
        for section in unnecessary_sections:
            if section in resume_data and resume_data[section]:
                found_unnecessary += 1
        
        if found_unnecessary == 0:
            score += 2.0
        elif found_unnecessary == 1:
            score += 1.0
        else:
            score -= 1.0
        
        return DeterministicScore(max(0.0, min(10.0, score)))
    
    def analyze_line(self, line: str) -> DeterministicScore:
        """Analyze a single line of text"""
        score = 5.0  # Base score
        
        # Check for strong verbs
        strong_verb_count = sum(1 for verb in self.strong_verbs if verb in line.lower())
        score += min(strong_verb_count * 0.5, 2.0)
        
        # Check for weak verbs
        weak_verb_count = sum(1 for verb in self.weak_verbs if verb in line.lower())
        score -= min(weak_verb_count * 0.5, 2.0)
        
        # Check for quantifiable metrics
        quantifiable_count = sum(1 for pattern in self.quantifiable_indicators 
                               if re.search(pattern, line, re.IGNORECASE))
        score += min(quantifiable_count * 1.0, 2.0)
        
        # Check for buzzwords
        buzzword_count = sum(1 for buzzword in self.buzzwords if buzzword in line.lower())
        score -= min(buzzword_count * 0.5, 2.0)
        
        return DeterministicScore(max(0.0, min(10.0, score)))
    
    def _extract_all_text(self, resume_data: Dict[str, Any]) -> str:
        """Extract all text content from resume data"""
        text_parts = []
        
        # Add summary
        if 'Summary' in resume_data:
            text_parts.append(str(resume_data['Summary']))
        
        # Add work experience
        for exp in resume_data.get('WorkExperience', []):
            text_parts.append(str(exp.get('JobTitle', '')))
            text_parts.append(str(exp.get('Company', '')))
            text_parts.append(str(exp.get('Responsibilities', [])))
        
        # Add education
        for edu in resume_data.get('Education', []):
            text_parts.append(str(edu.get('Degree', '')))
            text_parts.append(str(edu.get('Institution', '')))
        
        # Add skills
        skills = resume_data.get('Skills', {})
        if isinstance(skills, dict):
            for category, skill_list in skills.items():
                if isinstance(skill_list, list):
                    text_parts.extend(str(skill) for skill in skill_list)
                else:
                    text_parts.append(str(skill_list))
        
        return ' '.join(text_parts).lower()
    
    def _get_date_format(self, date_string: str) -> str:
        """Get the format of a date string"""
        if re.match(r'\d{4}-\d{2}', date_string):
            return 'YYYY-MM'
        elif re.match(r'\d{2}/\d{4}', date_string):
            return 'MM/YYYY'
        elif re.match(r'\d{4}/\d{2}', date_string):
            return 'YYYY/MM'
        elif re.match(r'\w+\s+\d{4}', date_string):
            return 'Month YYYY'
        else:
            return 'other' 