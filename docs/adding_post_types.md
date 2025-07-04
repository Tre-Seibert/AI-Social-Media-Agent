# Adding New Post Types

Adding new post types is now **super simple**! Just edit the `POST_TYPE_CONFIGS` in `src/core/config.py`.

## How to Add a New Post Type

### Step 1: Edit the Config File

Open `src/core/config.py` and add your new post type to the `POST_TYPE_CONFIGS` dictionary:

```python
POST_TYPE_CONFIGS = {
    # ... existing post types ...
    
    "your_new_type": {
        "description": "Your description here - what kind of posts to generate",
        "image_prompt": "Your image prompt here - what kind of image to create",
        "hashtags": ["#YourHashtag1", "#YourHashtag2", "#YourHashtag3"]
    }
}
```

### Step 2: That's It!

The system automatically:
- ✅ Uses your new post type for content generation
- ✅ Creates images using your image prompt
- ✅ Uses your hashtags when relevant
- ✅ No other changes needed!

## Quick Examples

### Add E-commerce Tips
```python
"ecommerce_tips": {
    "description": "Share practical e-commerce website optimization tips for online stores",
    "image_prompt": "Professional photograph of a modern e-commerce website interface on a laptop, showing product listings and shopping cart elements",
    "hashtags": ["#Ecommerce", "#OnlineStore", "#WebDesign", "#DigitalMarketing"]
}
```

### Add Accessibility Tips
```python
"accessibility_tips": {
    "description": "Share web accessibility best practices and inclusive design tips",
    "image_prompt": "Professional photograph of inclusive design elements and accessibility features on a modern website interface",
    "hashtags": ["#Accessibility", "#InclusiveDesign", "#WebDesign", "#UXDesign"]
}
```

### Add WordPress Tips
```python
"wordpress_tips": {
    "description": "Share WordPress optimization and customization tips for small businesses",
    "image_prompt": "Professional photograph of WordPress dashboard and website customization tools on a laptop",
    "hashtags": ["#WordPress", "#WebDesign", "#CMS", "#DigitalMarketing"]
}
```

## Configuration Options

Each post type can have:

- **description**: Tells the AI what kind of content to generate
- **image_prompt**: Tells the AI what kind of image to create  
- **hashtags**: Specific hashtags for this post type (optional)

## Tips for Good Configurations

### Descriptions
- Be specific about the type of content
- Mention your target audience
- Include tone/style guidance

### Image Prompts
- Start with "Professional photograph of..."
- Be specific about what to show
- Include style guidance like "clean, minimalist"

### Hashtags
- Use 3-4 relevant hashtags
- Mix specific and general hashtags
- Keep them relevant to your business

## Testing Your New Post Type

After adding to config, run your agent:

```bash
python src/scripts/run_agent.py
```

The system will automatically start generating posts of your new type! 🚀

## Why This Approach is Better

✅ **One File**: Only edit `config.py`  
✅ **No Code Changes**: No need to modify multiple files  
✅ **No Imports**: No need to update imports  
✅ **Automatic**: System detects new types automatically  
✅ **Flexible**: Each type can have custom everything  
✅ **Simple**: Just add to the dictionary and you're done! 