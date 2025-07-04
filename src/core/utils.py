#!/usr/bin/env python3
"""
Shared utilities for Fishtown Web Design Social Media Automation
"""

import os
import sys
from dotenv import load_dotenv

# Configure console for Unicode support on Windows
if sys.platform == 'win32':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')

def load_environment():
    """Load environment variables from .env file in config folder."""
    # Look for .env file in config folder
    config_env_path = os.path.join('config', '.env')
    if os.path.exists(config_env_path):
        load_dotenv(config_env_path)
    else:
        # Fallback to root directory for backward compatibility
        load_dotenv()

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import openai
        import schedule
        import dotenv
        return True
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Please install required packages with: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists with OpenAI API key."""
    # Check for .env file in config folder first, then root directory
    config_env_path = os.path.join('config', '.env')
    root_env_path = '.env'
    
    if not os.path.exists(config_env_path) and not os.path.exists(root_env_path):
        print(".env file not found!")
        print("Please create a .env file in the config folder with your OpenAI API key:")
        print("config/.env")
        print("OPENAI_API_KEY=your_api_key_here")
        return False
    
    load_environment()
    
    if not os.getenv("OPENAI_API_KEY"):
        print("OPENAI_API_KEY not found in .env file!")
        print("Please add your OpenAI API key to the .env file in the config folder:")
        print("config/.env")
        print("OPENAI_API_KEY=your_api_key_here")
        return False
    
    return True

def check_social_media_credentials():
    """Check if social media credentials are configured."""
    load_environment()
    
    facebook_token = os.getenv("FACEBOOK_ACCESS_TOKEN")
    facebook_page_id = os.getenv("FACEBOOK_PAGE_ID")
    instagram_id = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID")
    
    facebook_enabled = bool(facebook_token and facebook_page_id)
    instagram_enabled = bool(facebook_token and instagram_id)
    
    return {
        'facebook_enabled': facebook_enabled,
        'instagram_enabled': instagram_enabled,
        'facebook_token': facebook_token,
        'facebook_page_id': facebook_page_id,
        'instagram_id': instagram_id
    }

def validate_setup():
    """Validate the complete setup including dependencies and environment."""
    print("Validating setup...")
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    # Check environment
    if not check_env_file():
        return False
    
    # Check social media credentials
    credentials = check_social_media_credentials()
    
    print("All checks passed!")
    print(f"Facebook: {'Enabled' if credentials['facebook_enabled'] else 'Disabled'}")
    print(f"Instagram: {'Enabled' if credentials['instagram_enabled'] else 'Disabled'}")
    
    return True 