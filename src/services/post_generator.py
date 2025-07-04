"""
Post Generator module for creating social media posts.
Handles content generation, prompts, and post formatting.
"""

import random
from datetime import datetime
from typing import Dict, Any, List
from openai import OpenAI
from ..core.config import (
    COMPANY_CONFIG, POST_CATEGORIES, HASHTAGS, FALLBACK_POSTS,
    MAX_POST_GENERATION_ATTEMPTS, POST_TYPE_CONFIGS
)
import requests


class PostGenerator:
    """Generates social media posts using OpenAI API."""
    
    def __init__(self, client: OpenAI):
        self.client = client
    
    def generate_unique_post(self, post_manager, holiday_manager) -> Dict[str, Any]:
        """Generate a unique post that hasn't been used recently."""
        # First check if today is a holiday
        holiday_info = holiday_manager.check_if_holiday()
        
        if holiday_info:
            print(f"🎉 Today is {holiday_info['name']}! Generating holiday-themed post...")
            post = self.generate_holiday_post(holiday_info)
            if post is None:
                print("❌ Failed to generate holiday post, falling back to regular post...")
                # Continue to regular post generation below
            else:
                post['generated_at'] = datetime.now().isoformat()
                post['id'] = f"holiday_post_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                post_manager.add_post(post)
                return post
        
        # If not a holiday, check if today is Monday for blog promotion
        today = datetime.now()
        if today.weekday() == 4:  # Monday is 0
            try:
                # Fetch the latest blog post from Strapi
                url = 'http://127.0.0.1:1337/api/posts?populate=featuredImage&sort=publishedDate:desc&pagination[limit]=1&publicationState=live'
                response = requests.get(url)
                data = response.json()
                posts = data.get('data', [])
                if posts:
                    post_data = posts[0]
                    title = post_data.get('title', 'Our Latest Blog Post')
                    summary = post_data.get('summary') or post_data.get('content', '')[:180] + '...'
                    slug = post_data.get('slug', '')
                    link = f"https://fishtownwebdesign.com/blog/{slug}" if slug else "https://fishtownwebdesign.com/blog"
                    # Get featured image
                    featured_image = post_data.get('featuredImage')
                    image_url = None
                    if featured_image:
                        # Prefer medium, then small, then default
                        formats = featured_image.get('formats', {})
                        if 'medium' in formats:
                            image_url = 'https://fishtownwebdesign.com' + formats['medium']['url']
                        elif 'small' in formats:
                            image_url = 'https://fishtownwebdesign.com' + formats['small']['url']
                        else:
                            image_url = 'https://fishtownwebdesign.com' + featured_image.get('url', '')
                    # Compose the social post
                    hashtags = POST_TYPE_CONFIGS['blog_promotion']['hashtags']
                    content = f"Check out our latest blog post: {title}\n\n{summary}\n\nRead more: {link}"
                    post = {
                        "type": "blog_promotion",
                        "content": content,
                        "hashtags": hashtags,
                        "full_post": f"{content}\n\n{' '.join(hashtags)}",
                        "image_url": image_url,
                        "blog_link": link,
                        "blog_title": title
                    }
                    post['generated_at'] = datetime.now().isoformat()
                    post['id'] = f"blog_promotion_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    post_manager.add_post(post)
                    return post
                else:
                    print("No new blog post found for this week. Skipping blog promotion post.")
                    return None
            except Exception as e:
                print(f"Error fetching latest blog post from Strapi: {e}")
                return None
        
        # If not a holiday and not Monday, generate regular post
        attempts = 0
        
        while attempts < MAX_POST_GENERATION_ATTEMPTS:
            post_type = random.choice(POST_CATEGORIES)
            post = self.generate_post_content(post_type)
            
            # Check if this content is too similar to recent posts
            if not post_manager.is_content_similar(post['content']):
                post['generated_at'] = datetime.now().isoformat()
                post['id'] = f"post_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                post_manager.add_post(post)
                return post
            
            attempts += 1
        
        # If all attempts fail, generate a fallback post
        return self.generate_fallback_post()
    
    def generate_post_content(self, post_type: str) -> Dict[str, Any]:
        """Generate post content using OpenAI."""
        prompt = self.create_prompt(post_type)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert social media manager for Fishtown Web Design. Generate ONE SINGLE engaging, authentic post that showcases web design expertise while being helpful to the local Philadelphia business community. Keep the post under 200 words and include relevant emojis. IMPORTANT: Generate only ONE post, not multiple numbered posts. Do not use numbers like '1)', '2)', '3)' in your response."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=250,
                temperature=0.8
            )
            
            # Check if response and content exist
            if (response and response.choices and 
                len(response.choices) > 0 and 
                response.choices[0].message and 
                response.choices[0].message.content):
                
                content = response.choices[0].message.content.strip()
                
                # Clean up content to ensure only one post
                # Remove any numbered posts (1), 2), 3), etc.)
                lines = content.split('\n')
                cleaned_lines = []
                for line in lines:
                    line = line.strip()
                    # Skip lines that start with numbers followed by ) or .
                    if line and not (line[0].isdigit() and len(line) > 1 and line[1] in [')', '.']):
                        cleaned_lines.append(line)
                
                # Join the cleaned lines
                content = '\n'.join(cleaned_lines).strip()
                
                # Get hashtags from post type config, fall back to general hashtags
                post_config = POST_TYPE_CONFIGS.get(post_type, {})
                type_hashtags = post_config.get('hashtags', [])
                
                if type_hashtags:
                    # Use post type specific hashtags + some general hashtags
                    hashtags = type_hashtags + random.sample(HASHTAGS, 3)
                else:
                    hashtags = random.sample(HASHTAGS, 6)
                
                return {
                    "type": post_type,
                    "content": content,
                    "hashtags": hashtags,
                    "full_post": f"{content}\n\n{' '.join(hashtags)}"
                }
            else:
                print("Warning: Empty response from OpenAI API")
                return self.generate_fallback_post()
            
        except Exception as e:
            print(f"Error generating post: {e}")
            return self.generate_fallback_post()
    
    def create_prompt(self, post_type: str) -> str:
        """Create specific prompt for post type using configuration."""
        base_context = f"""
        Company: {COMPANY_CONFIG['name']}
        Location: {COMPANY_CONFIG['location']}
        Services: {', '.join(COMPANY_CONFIG['services'])}
        Target Audience: {', '.join(COMPANY_CONFIG['target_audience'])}
        Brand Voice: {COMPANY_CONFIG['brand_voice']}
        
        Generate a {post_type.replace('_', ' ')} post that is engaging, authentic, and relevant to local Philadelphia businesses.
        """
        
        # Get post type configuration
        post_config = POST_TYPE_CONFIGS.get(post_type, {})
        description = post_config.get('description', f"Generate a {post_type.replace('_', ' ')} post.")
        
        return base_context + f"\n\n{description}"
    
    def generate_holiday_post(self, holiday_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a holiday-specific post."""
        holiday_name = holiday_info['name']
        holiday_type = holiday_info['type']
        
        # Create holiday-specific prompt
        holiday_prompt = self.create_holiday_prompt(holiday_info)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are an expert social media manager for Fishtown Web Design. Today is {holiday_name}. Generate ONE SINGLE engaging, authentic holiday post that celebrates {holiday_name} while being relevant to web design and local Philadelphia businesses. Keep the post under 200 words and include relevant emojis. IMPORTANT: Generate only ONE post, not multiple numbered posts. Do not use numbers like '1)', '2)', '3)' in your response."
                    },
                    {
                        "role": "user",
                        "content": holiday_prompt
                    }
                ],
                max_tokens=250,
                temperature=0.8
            )
            
            # Check if response and content exist
            if (response and response.choices and 
                len(response.choices) > 0 and 
                response.choices[0].message and 
                response.choices[0].message.content):
                
                content = response.choices[0].message.content.strip()
                
                # Clean up content to ensure only one post
                lines = content.split('\n')
                cleaned_lines = []
                for line in lines:
                    line = line.strip()
                    # Skip lines that start with numbers followed by ) or .
                    if line and not (line[0].isdigit() and len(line) > 1 and line[1] in [')', '.']):
                        cleaned_lines.append(line)
                
                # Join the cleaned lines
                content = '\n'.join(cleaned_lines).strip()
                
                # Add holiday-specific hashtags
                from .holiday_manager import HolidayManager
                holiday_manager = HolidayManager()
                holiday_hashtags = holiday_manager.get_holiday_hashtags(holiday_info)
                hashtags = random.sample(HASHTAGS, 4) + holiday_hashtags
                
                return {
                    "type": "holiday",
                    "holiday_name": holiday_name,
                    "holiday_type": holiday_type,
                    "content": content,
                    "hashtags": hashtags,
                    "full_post": f"{content}\n\n{' '.join(hashtags)}"
                }
            else:
                print("Warning: Empty response from OpenAI API for holiday post")
                print("Falling back to regular post generation...")
                return None
            
        except Exception as e:
            print(f"Error generating holiday post: {e}")
            print("Falling back to regular post generation...")
            return None
    
    def create_holiday_prompt(self, holiday_info: Dict[str, Any]) -> str:
        """Create a specific prompt for holiday posts."""
        holiday_name = holiday_info['name']
        
        base_context = f"""
        Company: {COMPANY_CONFIG['name']}
        Location: {COMPANY_CONFIG['location']}
        Services: {', '.join(COMPANY_CONFIG['services'])}
        Target Audience: {', '.join(COMPANY_CONFIG['target_audience'])}
        Brand Voice: {COMPANY_CONFIG['brand_voice']}
        
        Today is {holiday_name}. Generate a holiday-themed post that celebrates this special day while being relevant to web design and local Philadelphia businesses.
        """
        
        return base_context + f"\n\nCelebrate {holiday_name} with a post that honors the significance of this national holiday while connecting it to web design and local business success."
    
    def generate_fallback_post(self) -> Dict[str, Any]:
        """Generate fallback post if API fails."""
        content = random.choice(FALLBACK_POSTS)
        hashtags = random.sample(HASHTAGS, 6)
        
        return {
            "type": "fallback",
            "content": content,
            "hashtags": hashtags,
            "full_post": f"{content}\n\n{' '.join(hashtags)}",
            "generated_at": datetime.now().isoformat(),
            "id": f"fallback_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        } 