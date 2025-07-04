# Refactored Social Media Automation

This project has been refactored from a monolithic `autonomous_agent.py` file into a modular architecture for better maintainability and organization.

## New File Structure

### Core Modules

1. **`config.py`** - Configuration and constants
   - Company configuration
   - Post categories and hashtags
   - Holiday definitions
   - Image generation settings
   - Fallback posts

2. **`holiday_manager.py`** - Holiday detection and management
   - Holiday detection logic
   - Weekday calculations (first, second, third, fourth, last)
   - Holiday-specific content generation
   - Holiday hashtags

3. **`post_manager.py`** - Post history and management
   - Post history loading/saving
   - Content similarity checking
   - Daily post file management
   - Post persistence

4. **`post_generator.py`** - Post content generation
   - OpenAI API integration for post generation
   - Prompt creation for different post types
   - Holiday post generation
   - Fallback post generation

5. **`image_generator.py`** - Image generation and management
   - DALL-E 3 integration
   - GPT-4o prompt enhancement
   - Image prompt creation for different post types
   - Image downloading and saving
   - Existing image checking

6. **`autonomous_agent_refactored.py`** - Main agent class (simplified)
   - Orchestrates all modules
   - Social media posting integration
   - Daily post workflow
   - Error handling

### Run Scripts

- **`run_agent_refactored.py`** - New run script using refactored agent
- **`run_agent.py`** - Original run script (still available)

## Benefits of Refactoring

1. **Modularity**: Each module has a single responsibility
2. **Maintainability**: Easier to find and fix issues
3. **Testability**: Individual modules can be tested separately
4. **Reusability**: Modules can be used independently
5. **Readability**: Smaller, focused files are easier to understand
6. **Scalability**: New features can be added to specific modules

## Usage

### Using the Refactored Version

```bash
# Run the refactored agent
python run_agent_refactored.py
```

### Using the Original Version (still available)

```bash
# Run the original agent
python run_agent.py
```

## Migration Guide

The refactored version maintains the same functionality as the original, but with better organization:

1. **Configuration**: All constants moved to `config.py`
2. **Holiday Logic**: Moved to `holiday_manager.py`
3. **Post Management**: Moved to `post_manager.py`
4. **Content Generation**: Moved to `post_generator.py`
5. **Image Generation**: Moved to `image_generator.py`
6. **Main Logic**: Simplified in `autonomous_agent_refactored.py`

## File Dependencies

```
autonomous_agent_refactored.py
├── config.py
├── holiday_manager.py
├── post_manager.py
├── post_generator.py
├── image_generator.py
├── utils.py
└── social_media_poster.py (optional)
```

## Testing Individual Modules

You can now test individual modules independently:

```python
# Test holiday detection
from holiday_manager import HolidayManager
holiday_mgr = HolidayManager()
holiday = holiday_mgr.check_if_holiday()

# Test post generation
from post_generator import PostGenerator
from openai import OpenAI
client = OpenAI()
post_gen = PostGenerator(client)

# Test image generation
from image_generator import ImageGenerator
img_gen = ImageGenerator(client)
```

## Configuration

All configuration is now centralized in `config.py`. To modify settings:

1. **Company Info**: Edit `COMPANY_CONFIG`
2. **Post Categories**: Edit `POST_CATEGORIES`
3. **Hashtags**: Edit `HASHTAGS`
4. **Holidays**: Edit `HOLIDAYS`
5. **Image Settings**: Edit `IMAGE_SETTINGS`

## Future Enhancements

With the modular structure, it's now easier to:

1. Add new post types
2. Implement new image generation models
3. Add support for additional social media platforms
4. Create unit tests for individual modules
5. Add new holiday detection logic
6. Implement caching mechanisms

## Backward Compatibility

The original `autonomous_agent.py` file is preserved, so existing scripts and cron jobs will continue to work. The refactored version provides the same API but with better internal organization. 