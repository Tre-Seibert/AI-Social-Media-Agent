#!/usr/bin/env python3
"""
Run script for the Autonomous Social Media Agent.
This script runs the daily post generation using the modular architecture.
"""

import sys
import traceback
from src.core.agent import AutonomousSocialMediaAgent


def main():
    """Main function to run the autonomous social media agent."""
    try:
        # Initialize the agent
        agent = AutonomousSocialMediaAgent()
        
        # Run the daily post generation
        result = agent.run_daily_cron()
        
        if result:
            print("✅ Agent completed successfully!")
            return 0
        else:
            print("❌ Agent failed to complete")
            return 1
            
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main()) 