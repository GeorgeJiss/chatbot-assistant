"""
Helper utility functions
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
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
    """
    Save data to JSON file
    
    Args:
        data: Dictionary to save
        filepath: Path to save file
        
    Returns:
        bool: Success status
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving JSON: {e}")
        return False

def load_json(filepath: Path) -> Dict[Any, Any]:
    """
    Load data from JSON file
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        Dictionary containing loaded data
    """
    try:
        if not filepath.exists():
            return {}
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return {}

def parse_tech_stack(tech_string: str) -> List[str]:
    """
    Parse tech stack string into list of technologies
    
    Args:
        tech_string: Comma-separated string of technologies
        
    Returns:
        List of cleaned technology names
    """
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
    """
    Format datetime as string
    
    Args:
        dt: Datetime object (default: now)
        
    Returns:
        Formatted timestamp string
    """
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def categorize_technology(tech: str) -> str:
    """
    Categorize a technology into its type
    
    Args:
        tech: Technology name
        
    Returns:
        Category name
    """
    from src.utils.constants import TECH_CATEGORIES
    
    tech_lower = tech.lower()
    
    for category, techs in TECH_CATEGORIES.items():
        if tech_lower in techs:
            return category
    
    # Try partial matching
    for category, techs in TECH_CATEGORIES.items():
        for known_tech in techs:
            if known_tech in tech_lower or tech_lower in known_tech:
                return category
    
    return "other"

def get_experience_level(years: float) -> str:
    """
    Get experience level based on years
    
    Args:
        years: Years of experience
        
    Returns:
        Experience level string
    """
    from src.utils.constants import EXPERIENCE_LEVELS
    
    for level, (min_years, max_years) in EXPERIENCE_LEVELS.items():
        if min_years <= years < max_years:
            return level
    
    return "junior"

def sanitize_filename(name: str) -> str:
    """
    Sanitize string for use as filename
    
    Args:
        name: Original name
        
    Returns:
        Sanitized filename
    """
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
    """
    Extract numeric value from text
    
    Args:
        text: Text containing number
        
    Returns:
        Extracted number or 0.0
    """
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
    """
    Truncate text to maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length-3] + "..."

def create_candidate_summary(candidate_data: Dict[str, Any]) -> str:
    """
    Create a summary of candidate data
    
    Args:
        candidate_data: Dictionary containing candidate information
        
    Returns:
        Formatted summary string
    """
    summary_parts = []
    
    if candidate_data.get('name'):
        summary_parts.append(f"**Name:** {candidate_data['name']}")
    
    if candidate_data.get('email'):
        summary_parts.append(f"**Email:** {candidate_data['email']}")
    
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