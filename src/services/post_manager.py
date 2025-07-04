"""
Post Manager module for handling post history, content similarity, and post persistence.
Manages post storage, retrieval, and content uniqueness checking.
"""

import json
import os
from typing import List, Dict, Any
from ..core.config import SIMILARITY_THRESHOLD, DATA_DIRECTORY


class PostManager:
    """Manages post history, content similarity, and post persistence."""
    
    def __init__(self, history_file: str = None):
        # Use DATA_DIRECTORY for file paths
        if history_file is None:
            history_file = os.path.join(DATA_DIRECTORY, 'post_history.json')
        else:
            history_file = os.path.join(DATA_DIRECTORY, history_file)
        
        self.history_file = history_file
        self.post_history = self.load_post_history()
    
    def load_post_history(self) -> List[Dict[str, Any]]:
        """Load previously generated posts to avoid repetition."""
        try:
            with open(self.history_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def save_post_history(self):
        """Save post history to file."""
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
        with open(self.history_file, 'w') as f:
            json.dump(self.post_history, f, indent=2)
    
    def add_post(self, post: Dict[str, Any]):
        """Add a new post to history and save."""
        self.post_history.append(post)
        self.save_post_history()
    
    def is_content_similar(self, new_content: str) -> bool:
        """Check if new content is too similar to recent posts."""
        if len(self.post_history) < 5:
            return False
        
        recent_posts = self.post_history[-5:]
        new_words = set(new_content.lower().split())
        
        for post in recent_posts:
            existing_words = set(post['content'].lower().split())
            similarity = len(new_words.intersection(existing_words)) / len(new_words.union(existing_words))
            if similarity > SIMILARITY_THRESHOLD:  # 30% similarity threshold
                return True
        
        return False
    
    def get_recent_posts(self, count: int = 5) -> List[Dict[str, Any]]:
        """Get the most recent posts from history."""
        return self.post_history[-count:] if self.post_history else []
    
    def save_daily_post(self, post: Dict[str, Any]):
        """Save current post to daily file."""
        from datetime import datetime
        
        daily_filename = f"daily_posts_{datetime.now().strftime('%Y%m%d')}.json"
        daily_filepath = os.path.join(DATA_DIRECTORY, daily_filename)
        
        # Ensure directory exists
        os.makedirs(DATA_DIRECTORY, exist_ok=True)
        
        try:
            with open(daily_filepath, 'r') as f:
                daily_posts = json.load(f)
        except FileNotFoundError:
            daily_posts = []
        
        daily_posts.append(post)
        
        with open(daily_filepath, 'w') as f:
            json.dump(daily_posts, f, indent=2)
        
        return daily_filepath 