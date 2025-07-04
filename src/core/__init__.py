"""
Core application logic for the Social Media Automation Platform.
Contains the main agent, configuration, and utility functions.
"""

from .agent import AutonomousSocialMediaAgent
from .config import (
    COMPANY_CONFIG, 
    POST_CATEGORIES, 
    POST_TYPE_CONFIGS,
    HASHTAGS, 
    HOLIDAYS, 
    IMAGE_SETTINGS,
    MAX_DAILY_POSTS,
    SIMILARITY_THRESHOLD,
    FALLBACK_POSTS,
    MAX_POST_GENERATION_ATTEMPTS
)
from .utils import (
    load_environment,
    check_social_media_credentials,
    validate_setup
)

__all__ = [
    "AutonomousSocialMediaAgent",
    "COMPANY_CONFIG",
    "POST_CATEGORIES", 
    "POST_TYPE_CONFIGS",
    "HASHTAGS",
    "HOLIDAYS",
    "IMAGE_SETTINGS",
    "MAX_DAILY_POSTS",
    "SIMILARITY_THRESHOLD",
    "FALLBACK_POSTS",
    "MAX_POST_GENERATION_ATTEMPTS",
    "load_environment",
    "check_social_media_credentials",
    "validate_setup"
] 