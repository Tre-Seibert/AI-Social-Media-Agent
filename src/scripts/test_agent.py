#!/usr/bin/env python3
"""
Test script for the Autonomous Social Media Agent.
This script runs the agent without actually posting to social media platforms.
Useful for testing image generation, file saving, and content creation.
"""

import sys
import traceback
from datetime import datetime
from src.core.agent import AutonomousSocialMediaAgent


def test_agent_without_posting():
    """Test the agent without posting to social media."""
    try:
        print("🧪 Testing Autonomous Social Media Agent")
        print("=" * 50)
        print("This test will:")
        print("✅ Generate content")
        print("✅ Create images")
        print("✅ Save files to correct directories")
        print("❌ NOT post to social media")
        print("=" * 50)
        
        # Initialize the agent
        agent = AutonomousSocialMediaAgent()
        
        # Temporarily disable social media posting
        original_social_media_poster = agent.social_media_poster
        agent.social_media_poster = None
        
        print(f"\n📅 Test run for {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 50)
        
        # Generate a post with image
        print("🎯 Generating post with image...")
        post = agent.generate_post_with_image()
        
        if post is None:
            print("❌ No post generated")
            return False
        
        # Display the generated post
        print("\n📝 Generated Post Details:")
        print(f"Type: {post['type']}")
        if post.get('type') == 'holiday':
            print(f"Holiday: {post.get('holiday_name', 'Unknown')}")
            print(f"Holiday Type: {post.get('holiday_type', 'Unknown')}")
        print(f"Content: {post['content']}")
        print(f"Hashtags: {' '.join(post['hashtags'])}")
        
        if post.get('has_image'):
            print(f"✅ Image: {post.get('image_filename', 'Generated')}")
            
            # Check if image file exists (resolve the path)
            import os
            from src.core.config import IMAGES_DIRECTORY
            
            # Resolve the image path to check actual file location
            image_path = post.get('image_filename', '')
            if image_path.startswith('generated_images/'):
                actual_path = os.path.join(IMAGES_DIRECTORY, os.path.basename(image_path))
            else:
                actual_path = image_path
                
            if os.path.exists(actual_path):
                print(f"✅ Image file exists at: {actual_path}")
            else:
                print(f"❌ Image file not found at: {actual_path}")
        else:
            print("❌ No image generated")
        
        print("-" * 50)
        
        # Test file saving
        print("\n💾 Testing file saving...")
        daily_filename = agent.post_manager.save_daily_post(post)
        print(f"✅ Daily post saved to: {daily_filename}")
        
        # Check if files are in correct directories
        print("\n📁 Checking file locations...")
        
        # Check data/posts directory
        import os
        data_posts_dir = "data/posts"
        if os.path.exists(data_posts_dir):
            json_files = [f for f in os.listdir(data_posts_dir) if f.endswith('.json')]
            print(f"✅ Found {len(json_files)} JSON files in {data_posts_dir}")
            for file in json_files:
                print(f"   📄 {file}")
        else:
            print(f"❌ {data_posts_dir} directory not found")
        
        # Check data/images directory
        data_images_dir = "data/images"
        if os.path.exists(data_images_dir):
            image_files = [f for f in os.listdir(data_images_dir) if f.endswith('.png')]
            print(f"✅ Found {len(image_files)} image files in {data_images_dir}")
            # Show the most recent images
            recent_images = sorted(image_files)[-5:] if len(image_files) > 5 else image_files
            for file in recent_images:
                print(f"   🖼️  {file}")
        else:
            print(f"❌ {data_images_dir} directory not found")
        
        # Check for files in wrong locations
        print("\n🔍 Checking for files in wrong locations...")
        
        # Check root directory for JSON files
        root_json_files = [f for f in os.listdir('.') if f.endswith('.json')]
        if root_json_files:
            print(f"❌ Found {len(root_json_files)} JSON files in root directory:")
            for file in root_json_files:
                print(f"   📄 {file} (should be in data/posts/)")
        else:
            print("✅ No JSON files in root directory")
        
        # Check generated_images directory
        if os.path.exists("generated_images"):
            generated_images = [f for f in os.listdir("generated_images") if f.endswith('.png')]
            if generated_images:
                print(f"⚠️  Found {len(generated_images)} images in generated_images/ (should be in data/images/):")
                for file in generated_images:
                    print(f"   🖼️  {file}")
            else:
                print("✅ No images in generated_images/ directory")
        else:
            print("✅ No generated_images/ directory found")
        
        print("\n" + "=" * 50)
        print("✅ Test completed successfully!")
        print("📊 Summary:")
        print(f"   📝 Post generated: {'Yes' if post else 'No'}")
        print(f"   🖼️  Image generated: {'Yes' if post.get('has_image') else 'No'}")
        print(f"   💾 Files saved: {'Yes' if daily_filename else 'No'}")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        traceback.print_exc()
        return False


def main():
    """Main function to run the test."""
    try:
        success = test_agent_without_posting()
        return 0 if success else 1
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main()) 