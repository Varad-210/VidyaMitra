import json
import logging
from typing import Dict, List, Any
from services.gemini_service import generate_structured_response

class SkillMapper:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def analyze_skill_gap(self, user_skills: List[str], target_role: str) -> Dict[str, Any]:
        """Analyze skill gaps for a target role using Gemini AI."""
        
        # Define the expected response structure
        response_schema = {
            "target_role": "string",
            "skill_match_percentage": "number",
            "required_skills_match": "number",
            "missing_skills": {
                "required": ["array of strings"],
                "preferred": ["array of strings"],
                "emerging": ["array of strings"]
            },
            "learning_recommendations": [
                {
                    "skill": "string",
                    "priority": "string (high/medium/low)",
                    "resource": {
                        "platform": "string",
                        "course": "string",
                        "duration": "string"
                    },
                    "estimated_time": "string",
                    "difficulty": "string (beginner/intermediate/advanced)"
                }
            ]
        }
        
        # Create comprehensive prompt for Gemini
        prompt = f"""
You are an expert career counselor and skills analyst. Please analyze the skill gaps for the following scenario.

User's Current Skills: {', '.join(user_skills)}
Target Role: {target_role}

Please provide:
1. Overall skill match percentage (0-100)
2. Required skills match percentage (0-100)
3. Missing skills categorized as:
   - Required (must-have skills)
   - Preferred (nice-to-have skills)
   - Emerging (future-focused skills)
4. Learning recommendations for the top 5 missing skills with specific resources

For learning recommendations, include:
- Skill name
- Priority level
- Specific learning resource (platform, course, duration)
- Estimated learning time
- Difficulty level

Be specific and actionable in your recommendations. Consider current industry trends and job market demands for {target_role} roles.
"""
        
        try:
            # Get structured response from Gemini
            analysis = generate_structured_response(prompt, response_schema)
            
            if not analysis:
                # Fallback to basic analysis if Gemini fails
                return self._fallback_analysis(user_skills, target_role)
            
            # Validate and clean the response
            skill_match_percentage = max(0, min(100, float(analysis.get("skill_match_percentage", 50))))
            required_skills_match = max(0, min(100, float(analysis.get("required_skills_match", 50))))
            
            missing_skills = analysis.get("missing_skills", {})
            if isinstance(missing_skills, dict):
                required = self._ensure_list(missing_skills.get("required", []))
                preferred = self._ensure_list(missing_skills.get("preferred", []))
                emerging = self._ensure_list(missing_skills.get("emerging", []))
            else:
                required = preferred = emerging = []
            
            learning_recommendations = analysis.get("learning_recommendations", [])
            if isinstance(learning_recommendations, list):
                learning_recommendations = [rec for rec in learning_recommendations if isinstance(rec, dict)]
            else:
                learning_recommendations = []
            
            return {
                "target_role": target_role,
                "skill_match_percentage": round(skill_match_percentage, 1),
                "required_skills_match": round(required_skills_match, 1),
                "missing_skills": {
                    "required": required,
                    "preferred": preferred,
                    "emerging": emerging
                },
                "learning_recommendations": learning_recommendations
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing skill gap with Gemini: {str(e)}")
            return self._fallback_analysis(user_skills, target_role)
    
    def _ensure_list(self, items: Any) -> List[str]:
        """Ensure the input is a list of strings."""
        if not items:
            return []
        if isinstance(items, list):
            return [str(item) for item in items if item]
        return [str(items)]
    
    def _fallback_analysis(self, user_skills: List[str], target_role: str) -> Dict[str, Any]:
        """Fallback analysis method when Gemini is not available."""
        # Basic skill gap analysis
        user_skills_lower = [skill.lower() for skill in user_skills]
        
        # Common skills by role
        role_skills = {
            "software_engineer": {
                "required": ["python", "javascript", "git", "sql", "html", "css"],
                "preferred": ["react", "node.js", "docker", "aws", "postgresql"],
                "emerging": ["kubernetes", "graphql", "typescript", "microservices"]
            },
            "data_scientist": {
                "required": ["python", "machine learning", "sql", "statistics"],
                "preferred": ["tensorflow", "pandas", "numpy", "jupyter"],
                "emerging": ["deep learning", "nlp", "mlops", "airflow"]
            },
            "product_manager": {
                "required": ["project management", "communication", "analytics"],
                "preferred": ["agile", "scrum", "user research", "roadmap planning"],
                "emerging": ["data-driven decision making", "growth hacking", "product analytics"]
            }
        }
        
        if target_role not in role_skills:
            target_role = "software_engineer"
        
        target_skills = role_skills[target_role]
        
        # Find missing skills
        missing_required = [skill for skill in target_skills["required"] if skill not in user_skills_lower]
        missing_preferred = [skill for skill in target_skills["preferred"] if skill not in user_skills_lower]
        missing_emerging = [skill for skill in target_skills["emerging"] if skill not in user_skills_lower]
        
        # Calculate match percentage
        total_required = len(target_skills["required"])
        matched_required = total_required - len(missing_required)
        required_match = (matched_required / total_required * 100) if total_required > 0 else 0
        
        total_all = total_required + len(target_skills["preferred"])
        matched_all = matched_required + len([s for s in target_skills["preferred"] if s in user_skills_lower])
        overall_match = (matched_all / total_all * 100) if total_all > 0 else 0
        
        # Basic learning recommendations
        recommendations = []
        for skill in (missing_required + missing_preferred)[:5]:
            recommendations.append({
                "skill": skill,
                "priority": "high" if skill in missing_required else "medium",
                "resource": {
                    "platform": "Coursera",
                    "course": f"{skill.title()} Fundamentals",
                    "duration": "2 months"
                },
                "estimated_time": "2 months",
                "difficulty": "beginner"
            })
        
        return {
            "target_role": target_role,
            "skill_match_percentage": round(overall_match, 1),
            "required_skills_match": round(required_match, 1),
            "missing_skills": {
                "required": missing_required,
                "preferred": missing_preferred,
                "emerging": missing_emerging
            },
            "learning_recommendations": recommendations
        }
    
    def get_market_trends(self) -> Dict[str, Any]:
        """Get current market trends and in-demand skills using Gemini AI."""
        
        response_schema = {
            "trending_skills": [
                {
                    "skill": "string",
                    "growth": "string",
                    "demand": "string (high/medium/low)"
                }
            ],
            "market_insight": "string",
            "recommendation": "string"
        }
        
        prompt = """
You are an expert in tech industry trends and job market analysis. Please provide current insights on:

1. Top 8 trending tech skills with their growth rates and demand levels
2. A key market insight for job seekers
3. A strategic recommendation for career development

Focus on current 2024 trends and near-future predictions. Include specific growth percentages and demand levels.
"""
        
        try:
            trends = generate_structured_response(prompt, response_schema)
            
            if trends:
                return trends
        except Exception as e:
            self.logger.error(f"Error getting market trends with Gemini: {str(e)}")
        
        # Fallback trends
        return {
            "trending_skills": [
                {"skill": "artificial intelligence", "growth": "+45%", "demand": "high"},
                {"skill": "cloud computing", "growth": "+38%", "demand": "high"},
                {"skill": "cybersecurity", "growth": "+35%", "demand": "high"},
                {"skill": "data science", "growth": "+32%", "demand": "high"},
                {"skill": "devops", "growth": "+28%", "demand": "medium"},
                {"skill": "machine learning", "growth": "+25%", "demand": "high"},
                {"skill": "blockchain", "growth": "+22%", "demand": "medium"},
                {"skill": "iot", "growth": "+20%", "demand": "medium"}
            ],
            "market_insight": "AI and cloud computing skills are seeing the highest growth in demand",
            "recommendation": "Focus on Python, AWS, and machine learning for maximum career opportunities"
        }
