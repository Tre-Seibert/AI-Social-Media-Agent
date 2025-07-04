"""
Image Generator module for creating images using DALL-E 3.
Handles image generation, prompt enhancement, and image management.
"""

import os
import random
import hashlib
from datetime import datetime
from typing import Dict, Any, Optional
from PIL import Image
import requests
from io import BytesIO
from openai import OpenAI
from ..core.config import IMAGE_SETTINGS, IMAGES_DIRECTORY, POST_TYPE_CONFIGS


class ImageGenerator:
    """Generates images using DALL-E 3 and manages image storage."""
    
    def __init__(self, client: OpenAI):
        self.client = client
    
    def generate_image_prompt(self, post_content: str, post_type: str, holiday_info: Dict[str, Any] | None = None) -> str:
        """Generate a specific, detailed image prompt based on the actual post content."""
        
        # If it's a holiday post, use holiday-specific image generation
        if post_type == "holiday" and holiday_info:
            quality_settings = "high quality, professional photography, clean composition, no text, no words, no letters, minimalist design"
            return self.create_holiday_image_prompt(holiday_info, quality_settings)
        
        # Extract key elements from the post content
        content_lower = post_content.lower()
        
        # Create a focused, specific prompt based on post type and content
        prompt = self.create_focused_image_prompt(post_content, post_type, content_lower)
        
        return prompt
    
    def create_focused_image_prompt(self, post_content: str, post_type: str, content_lower: str) -> str:
        """Create a focused, specific image prompt using configuration."""
        
        # Base quality settings
        quality_settings = "high quality, professional photography, clean composition, no text, no words, no letters, minimalist design"
        
        # Get post type configuration
        post_config = POST_TYPE_CONFIGS.get(post_type, {})
        base_image_prompt = post_config.get('image_prompt', 
            f"Professional photograph of a modern laptop displaying a clean, minimalist website design. Clean composition with professional web design elements.")
        
        # For holiday posts, use special handling
        if post_type == "holiday":
            return self.create_holiday_image_prompt(post_content, quality_settings)
        
        # For other post types, use the configured image prompt
        return f"{base_image_prompt} {quality_settings}. Perfect for social media."
    
    def create_holiday_image_prompt(self, holiday_info: Dict[str, Any], quality_settings: str) -> str:
        """Create a specific image prompt for holiday posts."""
        holiday_name = holiday_info['name']
        
        if "independence" in holiday_name.lower() or "july" in holiday_name.lower():
            return f"Professional photograph of American flag with modern web design elements subtly integrated. Clean, patriotic composition with red, white, and blue color scheme. {quality_settings}. Perfect for social media."
        elif "christmas" in holiday_name.lower():
            return f"Professional photograph of festive holiday decorations with modern web design elements subtly integrated. Clean, warm composition with holiday colors. {quality_settings}. Perfect for social media."
        elif "thanksgiving" in holiday_name.lower():
            return f"Professional photograph of warm, welcoming Thanksgiving elements with modern web design concepts subtly integrated. Clean, cozy composition with autumn colors. {quality_settings}. Perfect for social media."
        else:
            return f"Professional photograph of celebration elements with modern web design concepts subtly integrated. Clean, festive composition. {quality_settings}. Perfect for social media."
    
    def check_existing_images(self, post_type: str, content: str) -> Optional[str]:
        """Check if we already have an image for similar content."""
        try:
            # Create a simple hash of the content to check for similarity
            content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
            
            # Look for existing images with similar content hash
            if os.path.exists(IMAGES_DIRECTORY):
                for filename in os.listdir(IMAGES_DIRECTORY):
                    if filename.endswith(".png") and content_hash in filename:
                        full_path = os.path.join(IMAGES_DIRECTORY, filename)
                        if os.path.exists(full_path):
                            print(f"🔄 Found existing image for similar content: {filename}")
                            return full_path
            return None
        except Exception as e:
            print(f"❌ Error checking existing images: {e}")
            return None
    
    def generate_image(self, post_content: str, post_type: str, holiday_info: Dict[str, Any] | None = None) -> Optional[str]:
        """Generate an image using DALL-E 3 with base prompts."""
        try:
            # First check if we already have an image for similar content
            existing_image = self.check_existing_images(post_type, post_content)
            if existing_image:
                print(f"🔄 Using existing image: {existing_image}")
                return existing_image
            
            # Generate the base image prompt
            base_prompt = self.generate_image_prompt(post_content, post_type, holiday_info)
            
            print(f"🎨 Generating image for post type: {post_type}")
            print(f"📝 Image prompt: {base_prompt}")
            print(f"📄 Post content preview: {post_content[:100]}...")
            
            # Use DALL-E 3 with the base prompt
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=base_prompt,
                size=IMAGE_SETTINGS["size"],
                quality=IMAGE_SETTINGS["quality"],
                n=1,
                style=IMAGE_SETTINGS["style"]
            )
            
            if response and response.data:
                image_url = response.data[0].url
                
                # Download and save the image
                if image_url:
                    image_filename = self.download_and_save_image(image_url, post_type)
                    
                    print(f"✅ Image generated successfully: {image_filename}")
                    return image_filename
                else:
                    print("❌ No image URL received from DALL-E 3")
                    return None
            else:
                print("❌ No image data received from DALL-E 3")
                return None
                
        except Exception as e:
            print(f"❌ Error generating image: {e}")
            return None
    
    def download_and_save_image(self, image_url: str, post_type: str) -> Optional[str]:
        """Download image from URL and save it locally."""
        try:
            # Create images directory if it doesn't exist
            os.makedirs(IMAGES_DIRECTORY, exist_ok=True)
            
            # Generate filename with content hash for uniqueness
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            # Use a combination of timestamp and random component for uniqueness
            random_suffix = random.randint(1000, 9999)
            filename = os.path.join(IMAGES_DIRECTORY, f"{post_type}_{timestamp}_{random_suffix}.png")
            
            # Download image
            response = requests.get(image_url)
            response.raise_for_status()
            
            # Open and save image
            image = Image.open(BytesIO(response.content))
            image.save(filename, "PNG")
            
            print(f"💾 Image saved to: {filename}")
            # Return the path in the format expected by the rest of the system (generated_images/filename.png)
            relative_path = f"generated_images/{os.path.basename(filename)}"
            return relative_path
            
        except Exception as e:
            print(f"❌ Error downloading/saving image: {e}")
            return None 