import json
import logging
from typing import Dict, List, Any
from datetime import datetime, timedelta
from services.gemini_service import generate_structured_response

class RecommendationAgent:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def generate_career_roadmap(self, user_skills: List[str], target_role: str, experience_level: str = "beginner") -> Dict[str, Any]:
        """Generate a personalized career roadmap using Gemini AI."""
        
        # Define the expected response structure
        response_schema = {
            "target_role": "string",
            "experience_level": "string",
            "roadmap": [
                {
                    "week_range": "string (e.g., '1-4')",
                    "skills": ["array of strings"],
                    "projects": ["array of strings"],
                    "resources": ["array of strings"],
                    "focus_areas": ["array of strings"]
                }
            ],
            "milestones": [
                {
                    "month": "integer",
                    "milestone": "string",
                    "description": "string"
                }
            ],
            "certifications": [
                {
                    "name": "string",
                    "provider": "string",
                    "duration": "string",
                    "difficulty": "string"
                }
            ],
            "courses": [
                {
                    "title": "string",
                    "platform": "string",
                    "duration": "string",
                    "rating": "number"
                }
            ],
            "estimated_completion": "string",
            "success_metrics": ["array of strings"]
        }
        
        # Create comprehensive prompt for Gemini
        prompt = f"""
You are an expert career counselor and learning path designer. Please create a comprehensive career roadmap for the following scenario:

User's Current Skills: {', '.join(user_skills)}
Target Role: {target_role}
Experience Level: {experience_level}

Please provide:
1. A detailed weekly roadmap (12-36 weeks depending on experience level) with:
   - Week ranges
   - Skills to learn
   - Practice projects
   - Learning resources
   - Focus areas

2. Key milestones with timelines

3. Recommended certifications with providers and difficulty levels

4. Suggested courses with platforms and ratings

5. Estimated completion time

6. Success metrics to track progress

Make the roadmap:
- Realistic and achievable
- Specific with actionable steps
- Progressive in difficulty
- Industry-relevant for {target_role}
- Tailored to {experience_level} level

Consider current industry standards, job requirements, and learning best practices.
"""
        
        try:
            # Get structured response from Gemini
            roadmap = generate_structured_response(prompt, response_schema)
            
            if not roadmap:
                # Fallback to basic roadmap if Gemini fails
                return self._fallback_roadmap(user_skills, target_role, experience_level)
            
            # Validate and clean the response
            roadmap_data = roadmap.get("roadmap", [])
            milestones = roadmap.get("milestones", [])
            certifications = roadmap.get("certifications", [])
            courses = roadmap.get("courses", [])
            success_metrics = roadmap.get("success_metrics", [])
            
            return {
                "target_role": target_role,
                "experience_level": experience_level,
                "roadmap": roadmap_data,
                "milestones": milestones,
                "certifications": certifications,
                "courses": courses,
                "estimated_completion": roadmap.get("estimated_completion", "3 months"),
                "success_metrics": success_metrics
            }
            
        except Exception as e:
            self.logger.error(f"Error generating roadmap with Gemini: {str(e)}")
            return self._fallback_roadmap(user_skills, target_role, experience_level)
    
    def _fallback_roadmap(self, user_skills: List[str], target_role: str, experience_level: str) -> Dict[str, Any]:
        """Fallback roadmap method when Gemini is not available."""
        
        # Basic roadmap based on experience level
        if experience_level == "beginner":
            roadmap = [
                {
                    "week_range": "1-4",
                    "skills": ["Fundamentals of " + target_role],
                    "projects": ["Basic project setup"],
                    "resources": ["Online tutorials", "Documentation"],
                    "focus_areas": ["Basic concepts", "Environment setup"]
                },
                {
                    "week_range": "5-8",
                    "skills": ["Core skills development"],
                    "projects": ["Small practice project"],
                    "resources": ["Video courses", "Books"],
                    "focus_areas": ["Practical application", "Best practices"]
                },
                {
                    "week_range": "9-12",
                    "skills": ["Advanced topics"],
                    "projects": ["Portfolio project"],
                    "resources": ["Advanced tutorials", "Community forums"],
                    "focus_areas": ["Problem solving", "Real-world application"]
                }
            ]
            milestones = [
                {"month": 1, "milestone": "Complete fundamentals", "description": "Master basic concepts"},
                {"month": 2, "milestone": "Build first project", "description": "Create working application"},
                {"month": 3, "milestone": "Portfolio ready", "description": "Have portfolio pieces ready"}
            ]
        elif experience_level == "intermediate":
            roadmap = [
                {
                    "week_range": "1-6",
                    "skills": ["Advanced " + target_role + " concepts"],
                    "projects": ["Complex project"],
                    "resources": ["Advanced courses", "Documentation"],
                    "focus_areas": ["Architecture", "Optimization"]
                },
                {
                    "week_range": "7-12",
                    "skills": ["Specialization"],
                    "projects": ["Specialized project"],
                    "resources": ["Specialized resources", "Mentorship"],
                    "focus_areas": ["Expertise development", "Industry trends"]
                }
            ]
            milestones = [
                {"month": 3, "milestone": "Advanced skills", "description": "Master complex concepts"},
                {"month": 6, "milestone": "Specialization", "description": "Develop expertise area"}
            ]
        else:  # advanced
            roadmap = [
                {
                    "week_range": "1-8",
                    "skills": ["Leadership and architecture"],
                    "projects": ["Leadership project"],
                    "resources": ["Leadership resources", "Industry papers"],
                    "focus_areas": ["Team leadership", "System design"]
                },
                {
                    "week_range": "9-16",
                    "skills": ["Innovation and research"],
                    "projects": ["Innovation project"],
                    "resources": ["Research papers", "Conferences"],
                    "focus_areas": ["Innovation", "Industry contribution"]
                }
            ]
            milestones = [
                {"month": 4, "milestone": "Leadership role", "description": "Take on leadership responsibilities"},
                {"month": 8, "milestone": "Industry recognition", "description": "Gain industry recognition"}
            ]
        
        # Basic certifications and courses
        certifications = [
            {
                "name": f"{target_role.title()} Certification",
                "provider": "Industry Standard",
                "duration": "3 months",
                "difficulty": "intermediate"
            }
        ]
        
        courses = [
            {
                "title": f"Complete {target_role.title()} Course",
                "platform": "Online Platform",
                "duration": "2 months",
                "rating": 4.5
            }
        ]
        
        success_metrics = [
            f"Complete {len(roadmap)} roadmap phases",
            "Build portfolio projects",
            "Achieve certification",
            "Apply for target positions"
        ]
        
        return {
            "target_role": target_role,
            "experience_level": experience_level,
            "roadmap": roadmap,
            "milestones": milestones,
            "certifications": certifications,
            "courses": courses,
            "estimated_completion": f"{len(roadmap) * 4} weeks",
            "success_metrics": success_metrics
        }
