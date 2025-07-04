"""
Autonomous Social Media Agent.
Main agent class that orchestrates post generation, image creation, and social media posting.
"""

import os
import json
import sys
from datetime import datetime
from typing import Dict, Any
from openai import OpenAI
from .utils import load_environment

# Configure console for Unicode support on Windows
if sys.platform == 'win32':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')

# Import our new modular components
from .config import COMPANY_CONFIG, MAX_DAILY_POSTS
from ..services.holiday_manager import HolidayManager
from ..services.post_manager import PostManager
from ..services.post_generator import PostGenerator
from ..services.image_generator import ImageGenerator

# Import autonomous social media poster
try:
    from ..services.social_media_poster import AutonomousSocialMediaPoster
    SOCIAL_MEDIA_AVAILABLE = True
except ImportError:
    SOCIAL_MEDIA_AVAILABLE = False
    print("Social media poster not available - posts will be generated but not posted")


class AutonomousSocialMediaAgent:
    """Main autonomous social media agent that orchestrates all functionality."""
    
    def __init__(self):
        # Load environment using shared utility
        load_environment()
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Initialize autonomous social media poster
        self.social_media_poster = None
        if SOCIAL_MEDIA_AVAILABLE:
            try:
                self.social_media_poster = AutonomousSocialMediaPoster()
                if self.social_media_poster.facebook_enabled:
                    print("Autonomous Facebook posting enabled")
                else:
                    print("Facebook credentials not configured - posting disabled")
            except Exception as e:
                print(f"Social media poster initialization failed: {e}")
                self.social_media_poster = None
        
        # Initialize modular components
        self.holiday_manager = HolidayManager()
        self.post_manager = PostManager()
        self.post_generator = PostGenerator(self.client)
        self.image_generator = ImageGenerator(self.client)
        
        # Daily post tracking
        self.daily_posts_generated = 0
        self.max_daily_posts = MAX_DAILY_POSTS
    
    def generate_post_with_image(self) -> Dict[str, Any]:
        """Generate a post with an accompanying image."""
        post = self.post_generator.generate_unique_post(self.post_manager, self.holiday_manager)
        
        # Check if it's a holiday post
        holiday_info = None
        if post.get('type') == 'holiday':
            holiday_info = {
                'name': post.get('holiday_name', ''),
                'type': post.get('holiday_type', ''),
                'key': post.get('holiday_key', '')
            }
        
        # If it's a blog promotion post, download the image from image_url
        if post.get('type') == 'blog_promotion' and post.get('image_url'):
            import requests
            import os
            from urllib.parse import urlparse
            image_url = post['image_url']
            # Download the image to the images directory
            images_dir = os.path.join(os.getcwd(), 'data', 'images')
            os.makedirs(images_dir, exist_ok=True)
            # Use the blog slug or a timestamp for the filename
            slug = post.get('blog_title', 'blog').replace(' ', '_').replace('/', '_')
            ext = os.path.splitext(urlparse(image_url).path)[1] or '.jpg'
            filename = f"blog_promotion_{slug}{ext}"
            image_path = os.path.join(images_dir, filename)
            try:
                resp = requests.get(image_url)
                if resp.status_code == 200:
                    with open(image_path, 'wb') as f:
                        f.write(resp.content)
                    post['image_filename'] = image_path
                    post['has_image'] = True
                else:
                    print(f"Failed to download blog image: {image_url}")
                    post['image_filename'] = None
                    post['has_image'] = False
            except Exception as e:
                print(f"Error downloading blog image: {e}")
                post['image_filename'] = None
                post['has_image'] = False
            return post
        
        # Otherwise, generate image based on post content
        image_filename = self.image_generator.generate_image(post['content'], post['type'], holiday_info)
        
        # Add image info to post
        post['image_filename'] = image_filename
        post['has_image'] = image_filename is not None
        
        return post
    
    def post_autonomously(self, post: Dict[str, Any]) -> Dict[str, Any]:
        """Automatically post content to Facebook only."""
        if not self.social_media_poster:
            return {
                'success': False,
                'error': 'Social media poster not available',
                'platforms': {}
            }
        
        try:
            print(f"Automatically posting to Facebook...")
            print(f"Content: {post.get('content', '')[:100]}...")
            if post.get('image_filename'):
                print(f"Image: {post.get('image_filename')}")
            
            # Use the autonomous poster to post to Facebook only
            results = self.social_media_poster.post_autonomously(post)
            
            return results
            
        except Exception as e:
            print(f"Error in autonomous posting: {e}")
            return {
                'success': False,
                'error': str(e),
                'platforms': {}
            }
    
    def daily_post(self):
        """Generate one content piece for the day (cron-friendly)."""
        print(f"\n=== Generating daily post for {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
        
        try:
            post = self.generate_post_with_image()
            
            if post is None:
                print("No post generated for today")
                return
            
            # Display the generated post
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] Generated post:")
            print(f"Type: {post['type']}")
            if post.get('type') == 'holiday':
                print(f"Holiday: {post.get('holiday_name', 'Unknown')}")
                print(f"Holiday Type: {post.get('holiday_type', 'Unknown')}")
            print(f"Content: {post['content']}")
            print(f"Hashtags: {' '.join(post['hashtags'])}")
            if post.get('has_image'):
                print(f"Image: {post.get('image_filename', 'Generated')}")
            else:
                print("No image generated")
            print("-" * 50)
            
            # Automatically post to Facebook
            if self.social_media_poster:
                print("Autonomous Facebook posting initiated...")
                posting_results = self.post_autonomously(post)
                
                if posting_results.get('overall_success'):
                    print("Successfully posted to Facebook!")
                    for platform, result in posting_results.get('platforms', {}).items():
                        if result.get('success'):
                            print(f"  {platform}: Posted successfully")
                        else:
                            print(f"  {platform}: {result.get('error', 'Unknown error')}")
                else:
                    print("Facebook posting failed:")
                    for platform, result in posting_results.get('platforms', {}).items():
                        if not result.get('success'):
                            print(f"  {platform}: {result.get('error', 'Unknown error')}")
            else:
                print("Facebook posting not configured - content generated but not posted")
            
            # Save current post to daily file
            daily_filename = self.post_manager.save_daily_post(post)
            
            print(f"Daily post generated and saved successfully!")
            print(f"Saved to: {daily_filename}")
            return post
            
        except Exception as e:
            print(f"Error generating daily post: {e}")
            # Generate fallback post
            fallback_post = self.post_generator.generate_fallback_post()
            return fallback_post

    def run_daily_cron(self):
        """Run the agent for cron - generates one post and exits."""
        print("Fishtown Web Design Daily Content Generator")
        print("=" * 50)
        print("Generating one daily post...")
        print("=" * 50)
        
        try:
            post = self.daily_post()
            print("Daily post generation completed successfully!")
            return post
        except Exception as e:
            print(f"Error in daily post generation: {e}")
            return None 