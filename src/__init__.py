"""
Social Media Automation Platform
A professional social media automation platform for Fishtown Web Design.
"""

__version__ = "1.0.0"
__author__ = "Fishtown Web Design"
__description__ = "AI-powered social media automation platform"

# Main classes to expose
from .core.agent import AutonomousSocialMediaAgent

# Convenience imports for common use cases
__all__ = [
    "AutonomousSocialMediaAgent",
] 