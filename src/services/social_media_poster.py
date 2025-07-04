#!/usr/bin/env python3
"""
Fishtown Web Design Autonomous Social Media Poster
Automatically posts generated content to Facebook and Instagram
"""

import os
import json
import time
import requests
import hashlib
from datetime import datetime
from typing import Dict, Any, Optional
import logging
from ..core.utils import load_environment, check_social_media_credentials, validate_setup
from ..core.config import DATA_DIRECTORY, IMAGES_DIRECTORY

# Configure logging
import sys

# Create handlers
file_handler = logging.FileHandler(os.path.join('data', 'logs', 'social_media.log'), encoding='utf-8')
console_handler = logging.StreamHandler(sys.stdout)

# Set encoding for console handler to handle Unicode on Windows
if sys.platform == 'win32':
    # On Windows, use utf-8 encoding for console output
    console_handler.setStream(sys.stdout)
    # Force UTF-8 encoding for the console
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[file_handler, console_handler]
)
logger = logging.getLogger(__name__)

def resolve_image_path(image_path: str) -> str:
    """Resolve image path to the correct directory."""
    if not image_path:
        return image_path
    
    # If the path starts with generated_images/, look in the IMAGES_DIRECTORY
    if image_path.startswith('generated_images/'):
        filename = os.path.basename(image_path)
        return os.path.join(IMAGES_DIRECTORY, filename)
    
    return image_path

class AutonomousSocialMediaPoster:
    def __init__(self):
        """Initialize the autonomous social media poster."""
        # Load environment using shared utility
        load_environment()
        
        # Get credentials using shared utility
        credentials = check_social_media_credentials()
        
        self.access_token = credentials['facebook_token']
        self.page_id = credentials['facebook_page_id']
        self.instagram_business_account_id = credentials['instagram_id']
        
        # Check if Facebook is configured
        self.facebook_enabled = credentials['facebook_enabled']
        
        # Check if Instagram is configured (requires both Facebook access token and Instagram business account ID)
        self.instagram_enabled = credentials['instagram_enabled']
        
        if not self.facebook_enabled and not self.instagram_enabled:
            logger.warning("No social media credentials configured - posting disabled")
            return
        
        self.base_url = "https://graph.facebook.com/v18.0"
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        })
        
        # Rate limiting
        self.last_post_time = 0
        self.min_post_interval = 60  # Minimum 60 seconds between posts
        
        # Track uploaded images to prevent duplicates
        self.uploaded_images: Dict[str, Dict[str, str]] = self.load_uploaded_images()
        
        # Clean up old upload tracking data (older than 3 days)
        self.cleanup_old_uploads(days_old=3)
        
        logger.info(f"Social media poster initialized - Facebook: {self.facebook_enabled}, Instagram: {self.instagram_enabled}")
    
    def load_uploaded_images(self) -> Dict[str, Dict[str, str]]:
        """Load previously uploaded image hashes to prevent duplicates."""
        uploaded_images_path = os.path.join(DATA_DIRECTORY, 'uploaded_images.json')
        try:
            with open(uploaded_images_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def save_uploaded_images(self):
        """Save uploaded image hashes to file."""
        uploaded_images_path = os.path.join(DATA_DIRECTORY, 'uploaded_images.json')
        # Ensure directory exists
        os.makedirs(DATA_DIRECTORY, exist_ok=True)
        with open(uploaded_images_path, 'w') as f:
            json.dump(self.uploaded_images, f, indent=2)
    
    def get_image_hash(self, image_path: str) -> str:
        """Generate a hash for an image file to detect duplicates."""
        try:
            with open(image_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception as e:
            logger.error(f"Error generating image hash: {e}")
            return ""
    
    def is_image_already_uploaded(self, image_path: str) -> bool:
        """Check if an image has already been uploaded to Facebook."""
        resolved_path = resolve_image_path(image_path)
        if not image_path or not os.path.exists(resolved_path):
            return False
        
        image_hash = self.get_image_hash(resolved_path)
        return image_hash in self.uploaded_images
    
    def mark_image_as_uploaded(self, image_path: str, media_id: str):
        """Mark an image as uploaded to prevent future duplicates."""
        resolved_path = resolve_image_path(image_path)
        if not image_path or not os.path.exists(resolved_path):
            return
        
        image_hash = self.get_image_hash(resolved_path)
        if image_hash:
            self.uploaded_images[image_hash] = {
                'media_id': media_id,
                'uploaded_at': datetime.now().isoformat(),
                'image_path': image_path
            }
            self.save_uploaded_images()
    
    def cleanup_old_uploads(self, days_old: int = 7):
        """Clean up old upload tracking data to prevent issues with similar images."""
        try:
            cutoff_date = datetime.now().timestamp() - (days_old * 24 * 60 * 60)
            cleaned_count = 0
            
            for hash_key, data in list(self.uploaded_images.items()):
                try:
                    upload_time = datetime.fromisoformat(data['uploaded_at']).timestamp()
                    if upload_time < cutoff_date:
                        del self.uploaded_images[hash_key]
                        cleaned_count += 1
                except (ValueError, KeyError):
                    # Remove invalid entries
                    del self.uploaded_images[hash_key]
                    cleaned_count += 1
            
            if cleaned_count > 0:
                self.save_uploaded_images()
                logger.info(f"Cleaned up {cleaned_count} old upload tracking entries")
                
        except Exception as e:
            logger.error(f"Error cleaning up old uploads: {e}")
    
    def post_autonomously(self, post_data: Dict[str, Any]) -> Dict[str, Any]:
        """Automatically post content to Facebook and Instagram."""
        results = {
            'timestamp': datetime.now().isoformat(),
            'platforms': {},
            'overall_success': False
        }
        
        content = post_data.get('full_post', post_data.get('content', ''))
        image_path = post_data.get('image_filename')
        
        logger.info(f"Autonomous posting initiated for post type: {post_data.get('type', 'unknown')}")
        logger.info(f"Content: {content[:100]}{'...' if len(content) > 100 else ''}")
        if image_path:
            logger.info(f"Image: {image_path}")
        
        # Post to Facebook if enabled
        if self.facebook_enabled:
            fb_result = self._post_to_facebook(content, image_path)
            results['platforms']['facebook'] = fb_result
            
            if fb_result.get('success'):
                if fb_result.get('has_image', False):
                    logger.info("Facebook: Posted photo with caption successfully")
                else:
                    logger.info("Facebook: Posted text-only status successfully")
            else:
                logger.error(f"Facebook: {fb_result.get('error', 'Unknown error')}")
        else:
            logger.warning("Facebook posting is disabled")
            results['platforms']['facebook'] = {
                'success': False,
                'error': 'Facebook posting is disabled',
                'platform': 'facebook'
            }
        
        # Post to Instagram if enabled
        if self.instagram_enabled:
            # Get Facebook post ID if Facebook posting was successful and had an image
            facebook_post_id = None
            if (self.facebook_enabled and 
                results['platforms'].get('facebook', {}).get('success') and 
                results['platforms']['facebook'].get('has_image')):
                facebook_post_id = results['platforms']['facebook'].get('post_id')
            
            ig_result = self._post_to_instagram(content, image_path, facebook_post_id)
            results['platforms']['instagram'] = ig_result
            
            if ig_result.get('success'):
                if ig_result.get('has_image', False):
                    logger.info("Instagram: Posted photo with caption successfully")
                else:
                    logger.info("Instagram: Posted text-only status successfully")
            else:
                logger.error(f"Instagram: {ig_result.get('error', 'Unknown error')}")
        else:
            logger.warning("Instagram posting is disabled")
            results['platforms']['instagram'] = {
                'success': False,
                'error': 'Instagram posting is disabled',
                'platform': 'instagram'
            }
        
        # Determine overall success
        results['overall_success'] = any(
            result.get('success', False) 
            for result in results['platforms'].values()
        )
        
        # Log final results
        if results['overall_success']:
            logger.info("Posting completed successfully!")
        else:
            logger.error("Posting failed on all platforms")
        
        # Log results to file
        self._log_posting_results(post_data, results)
        
        return results
    
    def _post_to_facebook(self, content: str, image_path: Optional[str] = None) -> Dict[str, Any]:
        """Post to Facebook Page."""
        try:
            self._respect_rate_limits()
            
            # First, verify we can access the page
            page_info = self._verify_page_access()
            if not page_info.get('success'):
                return page_info
            
            # Get page access token
            page_access_token = self._get_page_access_token()
            if not page_access_token:
                return {
                    'success': False,
                    'error': 'Failed to get page access token. Check your permissions.',
                    'platform': 'facebook'
                }
            
            # If we have an image, post as a photo with caption
            resolved_image_path = resolve_image_path(image_path)
            if image_path and os.path.exists(resolved_image_path):
                return self._post_photo_with_caption(content, resolved_image_path, page_access_token)
            else:
                # Post as text-only status
                return self._post_text_only(content, page_access_token)
        
        except Exception as e:
            logger.error(f"Error posting to Facebook: {e}")
            return {
                'success': False,
                'error': str(e),
                'platform': 'facebook'
            }
    
    def _post_photo_with_caption(self, content: str, image_path: str, page_access_token: str) -> Dict[str, Any]:
        """Post a photo with caption using the /photos endpoint."""
        try:
            with open(image_path, 'rb') as image_file:
                files = {'source': image_file}
                data = {
                    'message': content,
                    'access_token': page_access_token
                }
                
                response = requests.post(
                    f"{self.base_url}/{self.page_id}/photos",
                    files=files,
                    data=data
                )
            
            if response.status_code == 200:
                result = response.json()
                post_id = result.get('id')
                logger.info(f"Posted photo with caption to Facebook: {post_id}")
                
                # Mark image as uploaded to prevent future duplicates
                self.mark_image_as_uploaded(image_path, post_id)
                
                self.last_post_time = time.time()
                return {
                    'success': True,
                    'post_id': post_id,
                    'platform': 'facebook',
                    'has_image': True
                }
            elif response.status_code == 400 and "duplicate" in response.text.lower():
                logger.warning(f"Facebook detected duplicate image: {image_path}")
                # Mark as uploaded to prevent future attempts
                self.mark_image_as_uploaded(image_path, "duplicate_detected")
                # Try posting as text-only
                return self._post_text_only(content, page_access_token)
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                logger.error(f"Facebook photo posting failed: {error_msg}")
                return {
                    'success': False,
                    'error': error_msg,
                    'platform': 'facebook'
                }
        
        except Exception as e:
            logger.error(f"Error posting photo to Facebook: {e}")
            return {
                'success': False,
                'error': str(e),
                'platform': 'facebook'
            }
    
    def _post_text_only(self, content: str, page_access_token: str) -> Dict[str, Any]:
        """Post text-only status using the /feed endpoint."""
        try:
            post_data = {
                'message': content,
                'access_token': page_access_token
            }
            
            response = self.session.post(
                f"{self.base_url}/{self.page_id}/feed",
                data=post_data
            )
            
            if response.status_code == 200:
                result = response.json()
                post_id = result.get('id')
                logger.info(f"Posted text-only status to Facebook: {post_id}")
                
                self.last_post_time = time.time()
                return {
                    'success': True,
                    'post_id': post_id,
                    'platform': 'facebook',
                    'has_image': False
                }
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                logger.error(f"Facebook text posting failed: {error_msg}")
                return {
                    'success': False,
                    'error': error_msg,
                    'platform': 'facebook'
                }
        
        except Exception as e:
            logger.error(f"Error posting text to Facebook: {e}")
            return {
                'success': False,
                'error': str(e),
                'platform': 'facebook'
            }
    
    def _verify_page_access(self) -> Dict[str, Any]:
        """Verify that we can access the specified page."""
        try:
            response = self.session.get(
                f"{self.base_url}/{self.page_id}",
                params={'fields': 'id,name,category'}
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Page access verified: {data.get('name', 'Unknown')}")
                return {
                    'success': True,
                    'page_name': data.get('name'),
                    'page_category': data.get('category')
                }
            else:
                error_msg = f"Page access failed: {response.status_code} - {response.text}"
                logger.error(f"{error_msg}")
                
                if "does not exist" in response.text:
                    error_msg += "\nThe page ID might be incorrect. Use 'me/accounts' to find your pages."
                elif "permissions" in response.text:
                    error_msg += "\nCheck your access token permissions."
                
                return {
                    'success': False,
                    'error': error_msg
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f"Error verifying page access: {e}"
            }
    
    def _get_page_access_token(self) -> Optional[str]:
        """Get the page-specific access token."""
        try:
            response = self.session.get(
                f"{self.base_url}/{self.page_id}",
                params={'fields': 'access_token'}
            )
            
            if response.status_code == 200:
                data = response.json()
                page_token = data.get('access_token')
                if page_token:
                    logger.info("Retrieved page access token")
                    return page_token
                else:
                    logger.error("No page access token in response")
                    return None
            else:
                logger.error(f"Failed to get page access token: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting page access token: {e}")
            return None
    
    def _post_to_instagram(self, content: str, image_path: Optional[str] = None, facebook_post_id: Optional[str] = None) -> Dict[str, Any]:
        """Post to Instagram Business Account."""
        try:
            self._respect_rate_limits()
            
            # Verify Instagram business account access
            ig_info = self._verify_instagram_access()
            if not ig_info.get('success'):
                return ig_info
            
            # Instagram requires images for posts, so if no image, we can't post
            resolved_image_path = resolve_image_path(image_path)
            if not image_path or not os.path.exists(resolved_image_path):
                return {
                    'success': False,
                    'error': 'Instagram requires an image for posts. No image provided.',
                    'platform': 'instagram'
                }
            
            # Post photo to Instagram
            return self._post_photo_to_instagram(content, resolved_image_path, facebook_post_id)
        
        except Exception as e:
            logger.error(f"Error posting to Instagram: {e}")
            return {
                'success': False,
                'error': str(e),
                'platform': 'instagram'
            }
    
    def _verify_instagram_access(self) -> Dict[str, Any]:
        """Verify that we can access the Instagram business account."""
        try:
            response = self.session.get(
                f"{self.base_url}/{self.instagram_business_account_id}",
                params={'fields': 'id,username,media_count'}
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Instagram access verified: @{data.get('username', 'Unknown')}")
                return {
                    'success': True,
                    'username': data.get('username'),
                    'media_count': data.get('media_count')
                }
            else:
                error_msg = f"Instagram access failed: {response.status_code} - {response.text}"
                logger.error(f"{error_msg}")
                
                if "does not exist" in response.text:
                    error_msg += "\nThe Instagram business account ID might be incorrect."
                elif "permissions" in response.text:
                    error_msg += "\nCheck your access token permissions for Instagram."
                
                return {
                    'success': False,
                    'error': error_msg
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f"Error verifying Instagram access: {e}"
            }
    
    def _post_photo_to_instagram(self, content: str, image_path: str, facebook_post_id: Optional[str] = None) -> Dict[str, Any]:
        """Post a photo to Instagram using the /media endpoint."""
        try:
            # Step 1: Get image URL from Facebook post if available, otherwise upload image
            image_url = None
            
            if facebook_post_id:
                # Try to get the image URL from the existing Facebook post
                page_access_token = self._get_page_access_token()
                if page_access_token:
                    post_response = requests.get(
                        f"{self.base_url}/{facebook_post_id}",
                        params={
                            'fields': 'images,picture',
                            'access_token': page_access_token
                        }
                    )
                    
                    if post_response.status_code == 200:
                        post_data = post_response.json()
                        logger.info(f"Facebook post data: {post_data}")
                        
                        if 'images' in post_data and post_data['images']:
                            image_url = post_data['images'][0].get('source')
                        elif 'picture' in post_data:
                            image_url = post_data['picture']
                        
                        if image_url:
                            logger.info(f"Retrieved image URL from Facebook post: {image_url}")
            
            # If we couldn't get the URL from Facebook post, upload the image
            if not image_url:
                logger.info("Uploading image to Facebook to get URL for Instagram")
                # Upload image to Facebook page to get a URL (without creating a post)
                page_access_token = self._get_page_access_token()
                if not page_access_token:
                    return {
                        'success': False,
                        'error': 'Failed to get page access token for image upload',
                        'platform': 'instagram'
                    }
                
                with open(image_path, 'rb') as image_file:
                    files = {'source': image_file}
                    data = {
                        'access_token': page_access_token,
                        'published': 'false'  # Don't create a post, just upload the image
                    }
                    
                    upload_response = requests.post(
                        f"{self.base_url}/{self.page_id}/photos",
                        files=files,
                        data=data
                    )
                
                if upload_response.status_code != 200:
                    error_msg = f"Failed to upload image for Instagram: {upload_response.status_code} - {upload_response.text}"
                    logger.error(f"{error_msg}")
                    return {
                        'success': False,
                        'error': error_msg,
                        'platform': 'instagram'
                    }
                
                upload_result = upload_response.json()
                
                # Debug: Log the full response to understand the structure
                logger.info(f"Facebook upload response: {upload_result}")
                
                # Try different ways to get the image URL from Facebook response
                # Method 1: Check if there's a direct 'images' field
                if 'images' in upload_result and upload_result['images']:
                    image_url = upload_result['images'][0].get('source')
                
                # Method 2: Check if there's a 'picture' field
                if not image_url and 'picture' in upload_result:
                    image_url = upload_result['picture']
                
                # Method 3: Try to get the URL from the post ID
                if not image_url and 'id' in upload_result:
                    # Get the post details to extract image URL
                    post_id = upload_result['id']
                    post_response = requests.get(
                        f"{self.base_url}/{post_id}",
                        params={
                            'fields': 'images,picture',
                            'access_token': page_access_token
                        }
                    )
                    
                    if post_response.status_code == 200:
                        post_data = post_response.json()
                        # logger.info(f"🔍 Post data: {post_data}")
                        
                        if 'images' in post_data and post_data['images']:
                            image_url = post_data['images'][0].get('source')
                        elif 'picture' in post_data:
                            image_url = post_data['picture']
                
                if not image_url:
                    error_msg = f"No image URL returned from Facebook upload. Response: {upload_result}"
                    logger.error(f"{error_msg}")
                    return {
                        'success': False,
                        'error': error_msg,
                        'platform': 'instagram'
                    }
                
                logger.info(f"Uploaded image for Instagram: {image_url}")
            
            # Step 2: Create media container with image_url
            media_data = {
                'image_url': image_url,
                'caption': content,
                'access_token': self.access_token
            }
            
            response = requests.post(
                f"{self.base_url}/{self.instagram_business_account_id}/media",
                data=media_data
            )
            
            if response.status_code == 200:
                result = response.json()
                media_id = result.get('id')
                
                if media_id:
                    logger.info(f"Created Instagram media container: {media_id}")
                    
                    # Step 3: Publish the media
                    publish_data = {
                        'creation_id': media_id,
                        'access_token': self.access_token
                    }
                    
                    publish_response = requests.post(
                        f"{self.base_url}/{self.instagram_business_account_id}/media_publish",
                        data=publish_data
                    )
                    
                    if publish_response.status_code == 200:
                        publish_result = publish_response.json()
                        post_id = publish_result.get('id')
                        logger.info(f"Published Instagram post: {post_id}")
                        
                        # Mark image as uploaded to prevent future duplicates
                        self.mark_image_as_uploaded(image_path, post_id)
                        
                        self.last_post_time = time.time()
                        return {
                            'success': True,
                            'post_id': post_id,
                            'media_id': media_id,
                            'platform': 'instagram',
                            'has_image': True
                        }
                    else:
                        error_msg = f"Instagram publish failed: {publish_response.status_code} - {publish_response.text}"
                        logger.error(f"{error_msg}")
                        return {
                            'success': False,
                            'error': error_msg,
                            'platform': 'instagram'
                        }
                else:
                    error_msg = "No media ID returned from Instagram"
                    logger.error(f"{error_msg}")
                    return {
                        'success': False,
                        'error': error_msg,
                        'platform': 'instagram'
                    }
            else:
                error_msg = f"Instagram media creation failed: {response.status_code} - {response.text}"
                logger.error(f"{error_msg}")
                return {
                    'success': False,
                    'error': error_msg,
                    'platform': 'instagram'
                }
        
        except Exception as e:
            logger.error(f"Error posting photo to Instagram: {e}")
            return {
                'success': False,
                'error': str(e),
                'platform': 'instagram'
            }
    
    def _respect_rate_limits(self):
        """Ensure we don't exceed platform rate limits."""
        current_time = time.time()
        time_since_last_post = current_time - self.last_post_time
        
        if time_since_last_post < self.min_post_interval:
            sleep_time = self.min_post_interval - time_since_last_post
            logger.info(f"Rate limiting: waiting {sleep_time:.1f} seconds")
            time.sleep(sleep_time)
    
    def _log_posting_results(self, post_data: Dict[str, Any], results: Dict[str, Any]):
        """Log posting results to posting_log.json."""
        try:
            posting_log_path = os.path.join(DATA_DIRECTORY, 'posting_log.json')
            
            # Ensure directory exists
            os.makedirs(DATA_DIRECTORY, exist_ok=True)
            
            # Load existing log
            try:
                with open(posting_log_path, 'r') as f:
                    posting_log = json.load(f)
            except FileNotFoundError:
                posting_log = []
            
            # Add new entry
            log_entry = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'post_id': post_data.get('id', 'unknown'),
                'content': post_data.get('full_post', post_data.get('content', '')),
                'type': post_data.get('type', 'unknown'),
                'has_image': post_data.get('has_image', False),
                'image_filename': post_data.get('image_filename'),
                'posting_results': results
            }
            
            posting_log.append(log_entry)
            
            # Save updated log
            with open(posting_log_path, 'w') as f:
                json.dump(posting_log, f, indent=2)
            
            logger.info(f"Posting results logged: {results.get('overall_success', False)}")
            
        except Exception as e:
            logger.error(f"Error logging posting results: {e}") 