from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
import config
from src.utils.helpers import (
    generate_candidate_id,
    save_json,
    load_json,
    sanitize_filename,
    format_timestamp
)

class StorageService:
    """Service for storing and retrieving candidate data"""
    
    def __init__(self):
        self.candidates_dir = config.CANDIDATES_DIR
    
    def save_candidate(
        self,
        candidate_data: Dict[str, Any],
        session_id: str
    ) -> Optional[str]:
        """
        Save candidate information to file
        
        Args:
            candidate_data: Dictionary containing candidate info
            session_id: Session identifier
            
        Returns:
            Candidate ID if successful, None otherwise
        """
        try:
            # Generate candidate ID if not present
            if 'candidate_id' not in candidate_data:
                candidate_data['candidate_id'] = generate_candidate_id()
            
            # Add metadata
            candidate_data['session_id'] = session_id
            candidate_data['created_at'] = format_timestamp()
            candidate_data['updated_at'] = format_timestamp()
            
            # Create filename
            candidate_id = candidate_data['candidate_id']
            name = candidate_data.get('name', 'unknown')
            safe_name = sanitize_filename(name)
            filename = f"{candidate_id}_{safe_name}.json"
            
            filepath = self.candidates_dir / filename
            
            # Save to file
            if save_json(candidate_data, filepath):
                return candidate_id
            
            return None
        
        except Exception as e:
            print(f"Error saving candidate: {e}")
            return None
    
    def load_candidate(self, candidate_id: str) -> Optional[Dict[str, Any]]:
        """
        Load candidate information from file
        
        Args:
            candidate_id: Candidate identifier
            
        Returns:
            Dictionary containing candidate info or None
        """
        try:
            # Find file with candidate_id
            for filepath in self.candidates_dir.glob(f"{candidate_id}_*.json"):
                return load_json(filepath)
            
            return None
        
        except Exception as e:
            print(f"Error loading candidate: {e}")
            return None
    
    def update_candidate(
        self,
        candidate_id: str,
        updates: Dict[str, Any]
    ) -> bool:
        """
        Update candidate information
        
        Args:
            candidate_id: Candidate identifier
            updates: Dictionary of fields to update
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Load existing data
            candidate_data = self.load_candidate(candidate_id)
            
            if not candidate_data:
                return False
            
            # Update fields
            candidate_data.update(updates)
            candidate_data['updated_at'] = format_timestamp()
            
            # Find and update file
            for filepath in self.candidates_dir.glob(f"{candidate_id}_*.json"):
                return save_json(candidate_data, filepath)
            
            return False
        
        except Exception as e:
            print(f"Error updating candidate: {e}")
            return False
    
    def list_candidates(
        self,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        List all candidates
        
        Args:
            limit: Maximum number of candidates to return
            
        Returns:
            List of candidate dictionaries
        """
        try:
            candidates = []
            
            for filepath in sorted(
                self.candidates_dir.glob("*.json"),
                key=lambda p: p.stat().st_mtime,
                reverse=True
            )[:limit]:
                data = load_json(filepath)
                if data:
                    candidates.append(data)
            
            return candidates
        
        except Exception as e:
            print(f"Error listing candidates: {e}")
            return []
    
    def delete_candidate(self, candidate_id: str) -> bool:
        """
        Delete candidate data (for GDPR compliance)
        
        Args:
            candidate_id: Candidate identifier
            
        Returns:
            True if successful, False otherwise
        """
        try:
            for filepath in self.candidates_dir.glob(f"{candidate_id}_*.json"):
                filepath.unlink()
                return True
            
            return False
        
        except Exception as e:
            print(f"Error deleting candidate: {e}")
            return False
    
    def export_candidate_summary(
        self,
        candidate_id: str
    ) -> Optional[str]:
        """
        Export candidate data as formatted text
        
        Args:
            candidate_id: Candidate identifier
            
        Returns:
            Formatted text summary or None
        """
        try:
            candidate_data = self.load_candidate(candidate_id)
            
            if not candidate_data:
                return None
            
            from src.utils.helpers import create_candidate_summary
            return create_candidate_summary(candidate_data)
        
        except Exception as e:
            print(f"Error exporting candidate: {e}")
            return None
    
    def search_candidates(
        self,
        query: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Search candidates by criteria
        
        Args:
            query: Dictionary of search criteria
            
        Returns:
            List of matching candidates
        """
        try:
            all_candidates = self.list_candidates(limit=1000)
            results = []
            
            for candidate in all_candidates:
                match = True
                
                for key, value in query.items():
                    if key not in candidate:
                        match = False
                        break
                    
                    if isinstance(value, str):
                        if value.lower() not in str(candidate[key]).lower():
                            match = False
                            break
                    elif candidate[key] != value:
                        match = False
                        break
                
                if match:
                    results.append(candidate)
            
            return results
        
        except Exception as e:
            print(f"Error searching candidates: {e}")
            return []
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about stored candidates
        
        Returns:
            Dictionary containing statistics
        """
        try:
            candidates = self.list_candidates(limit=10000)
            
            total = len(candidates)
            
            # Count by tech stack
            tech_counts = {}
            for candidate in candidates:
                if 'tech_stack' in candidate:
                    for tech in candidate['tech_stack']:
                        tech_counts[tech] = tech_counts.get(tech, 0) + 1
            
            # Average experience
            experiences = [
                candidate.get('experience', 0) 
                for candidate in candidates 
                if 'experience' in candidate
            ]
            avg_experience = sum(experiences) / len(experiences) if experiences else 0
            
            return {
                'total_candidates': total,
                'popular_technologies': dict(sorted(
                    tech_counts.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:10]),
                'average_experience': round(avg_experience, 2)
            }
        
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {}