import json
import logging
from typing import Dict, List, Any
from schemas.resume import ResumeAnalysis
from services.gemini_service import generate_structured_response

class ResumeAnalyzer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def analyze_resume(self, text: str) -> ResumeAnalysis:
        """Analyze resume text and return comprehensive analysis using Gemini AI."""
        
        # Define the expected response structure
        response_schema = {
            "score": "integer (0-100)",
            "strengths": ["array of strings"],
            "missing_skills": ["array of strings"],
            "improvement_suggestions": ["array of strings"],
            "skill_gap_analysis": {
                "technical_skills": ["array of strings"],
                "soft_skills": ["array of strings"]
            }
        }
        
        # Create comprehensive prompt for Gemini
        prompt = f"""
You are an expert career counselor and resume analyst. Please analyze the following resume text and provide detailed feedback.

Resume Text:
{text}

Please provide:
1. A score from 0-100 evaluating the overall quality of the resume
2. Key strengths that make this resume effective
3. Missing skills that would improve the resume
4. Specific improvement suggestions
5. Skill gap analysis identifying both technical and soft skills

Consider these evaluation criteria:
- Resume structure and formatting
- Experience and achievements presentation
- Skills and qualifications
- Professional language and clarity
- Industry relevance

Be specific and actionable in your feedback.
"""
        
        try:
            # Get structured response from Gemini
            analysis = generate_structured_response(prompt, response_schema)
            
            if not analysis:
                # Fallback to basic analysis if Gemini fails
                return self._fallback_analysis(text)
            
            # Validate and clean the response
            score = max(0, min(100, int(analysis.get("score", 50))))
            strengths = self._ensure_list(analysis.get("strengths", []))
            missing_skills = self._ensure_list(analysis.get("missing_skills", []))
            improvement_suggestions = self._ensure_list(analysis.get("improvement_suggestions", []))
            
            skill_gap_analysis = analysis.get("skill_gap_analysis", {})
            if isinstance(skill_gap_analysis, dict):
                technical_skills = self._ensure_list(skill_gap_analysis.get("technical_skills", []))
                soft_skills = self._ensure_list(skill_gap_analysis.get("soft_skills", []))
            else:
                technical_skills = []
                soft_skills = []
            
            return ResumeAnalysis(
                score=score,
                strengths=strengths,
                missing_skills=missing_skills,
                improvement_suggestions=improvement_suggestions,
                skill_gap_analysis={
                    "technical_skills": technical_skills,
                    "soft_skills": soft_skills
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error analyzing resume with Gemini: {str(e)}")
            return self._fallback_analysis(text)
    
    def _ensure_list(self, items: Any) -> List[str]:
        """Ensure the input is a list of strings."""
        if not items:
            return []
        if isinstance(items, list):
            return [str(item) for item in items if item]
        return [str(items)]
    
    def _fallback_analysis(self, text: str) -> ResumeAnalysis:
        """Fallback analysis method when Gemini is not available."""
        # Basic keyword-based analysis
        text_lower = text.lower()
        
        # Common tech skills to look for
        tech_skills = ['python', 'java', 'javascript', 'react', 'node.js', 'sql', 'aws', 'docker', 'git']
        found_skills = [skill for skill in tech_skills if skill in text_lower]
        
        # Basic scoring
        score = 50
        if len(found_skills) >= 5:
            score += 20
        if 'experience' in text_lower and 'year' in text_lower:
            score += 15
        if 'education' in text_lower or 'degree' in text_lower:
            score += 10
        if 'project' in text_lower:
            score += 5
        
        return ResumeAnalysis(
            score=min(100, score),
            strengths=[
                "Resume contains relevant technical skills",
                "Includes professional experience"
            ],
            missing_skills=[
                "Consider adding more specific achievements",
                "Include quantifiable results"
            ],
            improvement_suggestions=[
                "Add more specific metrics and achievements",
                "Consider including a professional summary",
                "Highlight key accomplishments with numbers"
            ],
            skill_gap_analysis={
                "technical_skills": found_skills,
                "soft_skills": []
            }
        )
