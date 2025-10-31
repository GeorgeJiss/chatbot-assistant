"""
Helper utility functions with role-based difficulty detection
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import config

def generate_session_id() -> str:
    """Generate a unique session ID"""
    return str(uuid.uuid4())

def generate_candidate_id() -> str:
    """Generate a unique candidate ID"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique = str(uuid.uuid4())[:8]
    return f"CAND_{timestamp}_{unique}"

def save_json(data: Dict[Any, Any], filepath: Path) -> bool:
    """Save data to JSON file"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving JSON: {e}")
        return False

def load_json(filepath: Path) -> Dict[Any, Any]:
    """Load data from JSON file"""
    try:
        if not filepath.exists():
            return {}
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return {}

def parse_tech_stack(tech_string: str) -> List[str]:
    """Parse tech stack string into list of technologies"""
    if not tech_string:
        return []
    
    # Split by comma and clean
    techs = [tech.strip().lower() for tech in tech_string.split(',')]
    
    # Remove empty strings
    techs = [tech for tech in techs if tech]
    
    # Remove duplicates while preserving order
    seen = set()
    unique_techs = []
    for tech in techs:
        if tech not in seen:
            seen.add(tech)
            unique_techs.append(tech)
    
    return unique_techs

def format_timestamp(dt: datetime = None) -> str:
    """Format datetime as string"""
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def categorize_technology(tech: str) -> str:
    """Categorize a technology into its type"""
    tech_lower = tech.lower()
    
    # Check all categories and subcategories
    for category, subcategories in config.TECH_CATEGORIES.items():
        if isinstance(subcategories, dict):
            for subcat, tech_list in subcategories.items():
                if tech_lower in tech_list:
                    return f"{category}/{subcat}"
        elif isinstance(subcategories, list):
            if tech_lower in subcategories:
                return category
    
    # Try partial matching
    for category, subcategories in config.TECH_CATEGORIES.items():
        if isinstance(subcategories, dict):
            for subcat, tech_list in subcategories.items():
                for known_tech in tech_list:
                    if known_tech in tech_lower or tech_lower in known_tech:
                        return f"{category}/{subcat}"
    
    return "other"

def get_experience_level(years: float) -> str:
    """Get experience level based on years"""
    for (min_years, max_years), level in config.EXPERIENCE_DIFFICULTY.items():
        if min_years <= years < max_years:
            return level
    
    return "junior"

def get_difficulty_from_role(role: str) -> Optional[str]:
    """
    Determine difficulty level from job role
    
    Args:
        role: Job role/position (e.g., 'Senior Software Engineer')
        
    Returns:
        Difficulty level or None if not determined
    """
    if not role:
        return None
    
    role_lower = role.lower()
    
    # Check exact matches first
    for role_keyword, difficulty in config.ROLE_DIFFICULTY_MAP.items():
        if role_keyword in role_lower:
            return difficulty
    
    return None

def sanitize_filename(name: str) -> str:
    """Sanitize string for use as filename"""
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '_')
    
    # Remove leading/trailing spaces and dots
    name = name.strip('. ')
    
    # Limit length
    if len(name) > 100:
        name = name[:100]
    
    return name

def extract_number(text: str) -> float:
    """Extract numeric value from text"""
    import re
    
    # Remove common words
    text = text.lower()
    text = re.sub(r'years?|months?|experience', '', text)
    
    # Find numbers (including decimals)
    matches = re.findall(r'\d+\.?\d*', text)
    
    if matches:
        return float(matches[0])
    
    return 0.0

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to maximum length"""
    if len(text) <= max_length:
        return text
    
    return text[:max_length-3] + "..."

def create_candidate_summary(candidate_data: Dict[str, Any]) -> str:
    """Create a summary of candidate data"""
    summary_parts = []
    
    if candidate_data.get('name'):
        summary_parts.append(f"**Name:** {candidate_data['name']}")
    
    if candidate_data.get('email'):
        summary_parts.append(f"**Email:** {candidate_data['email']}")
    
    if candidate_data.get('phone'):
        summary_parts.append(f"**Phone:** {candidate_data['phone']}")
    
    if candidate_data.get('experience'):
        summary_parts.append(f"**Experience:** {candidate_data['experience']} years")
    
    if candidate_data.get('position'):
        summary_parts.append(f"**Position:** {candidate_data['position']}")
    
    if candidate_data.get('location'):
        summary_parts.append(f"**Location:** {candidate_data['location']}")
    
    if candidate_data.get('tech_stack'):
        tech_list = ', '.join(candidate_data['tech_stack'])
        summary_parts.append(f"**Tech Stack:** {tech_list}")
    
    return '\n'.join(summary_parts)

def get_tech_stack_summary(tech_stack: List[str]) -> Dict[str, List[str]]:
    """Categorize tech stack into groups"""
    categorized = {
        'languages': [],
        'frameworks': [],
        'databases': [],
        'cloud': [],
        'devops': [],
        'tools': [],
        'other': []
    }
    
    for tech in tech_stack:
        category = categorize_technology(tech)
        main_category = category.split('/')[0] if '/' in category else category
        
        if main_category in categorized:
            categorized[main_category].append(tech)
        else:
            categorized['other'].append(tech)
    
    # Remove empty categories
    return {k: v for k, v in categorized.items() if v}