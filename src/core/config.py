"""
Configuration module for the Autonomous Social Media Agent.
Contains company configuration, post categories, hashtags, and holiday definitions.
"""

# Company configuration
COMPANY_CONFIG = {
    "name": "Fishtown Web Design",
    "location": "Fishtown, Philadelphia",
    "services": [
        "Custom Website Design", "E-commerce Development",
        "SEO Optimization", "Website Maintenance", "Mobile-First Design",
        "Brand Identity Design", "Digital Marketing"
    ],
    "target_audience": [
        "Small businesses in Philadelphia", "Blue collar businesses, like, plumbers, electricians, and HVAC technicians.",
        "Professional services", "Startups and entrepreneurs", "Non-profit organizations"
    ],
    "brand_voice": "Professional yet approachable, creative, community-focused, tech-savvy but human, philly based",
    "content_guidelines": "IMPORTANT: Do not mention having a local office, physical workspace, or in-person meetings. We are a fully remote company serving the Philadelphia area. Focus on digital services, online collaboration, and virtual support for local businesses."
}

# Data directory configuration
DATA_DIRECTORY = "data/posts"
IMAGES_DIRECTORY = "data/images"

# Post type configurations - Easy to add new types here
# The system automatically uses all keys in this dictionary as post types
POST_TYPE_CONFIGS = {
    "web_design_tip": {
        "description": "Share a practical web design tip that small businesses can implement immediately. Make it actionable and valuable.",
        "image_prompt": "Flat design vector illustration in Canva style for a web design tip. Bold sans-serif text overlay, simple website and laptop icons, pastel background, lots of whitespace, clean and modern. Use #FECE87 and black as primary colors.",
        "hashtags": ["#WebDesign", "#UXDesign", "#WebsiteDesign", "#DigitalDesign"]
    },
    "industry_insight": {
        "description": "Share an insight about web design trends, digital marketing, or technology that affects small businesses.",
        "image_prompt": "Flat design vector illustration in Canva style for industry insight. Bold sans-serif text overlay, modern tech and web icons, pastel background, clean layout, lots of whitespace. Use #FECE87 and black as primary colors.",
        "hashtags": ["#DigitalMarketing", "#WebDesign", "#IndustryInsights", "#TechTrends"]
    },
    "behind_the_scenes": {
        "description": "Show the human side of web design - share something about the team, creative process, or digital workspace. Focus on collaboration, creativity, and the digital tools we use.",
        "image_prompt": "Flat design vector illustration in Canva style showing a creative workspace or team collaboration. Bold text overlay, simple icons, pastel background, clean and modern. Use #FECE87 and black as primary colors.",
        "hashtags": ["#BehindTheScenes", "#WebDesign", "#TeamWork", "#CreativeProcess"]
    },
    "local_community": {
        "description": "Connect with the Fishtown/Philadelphia community. Mention local events, businesses, or community initiatives.",
        "image_prompt": "Flat design vector illustration in Canva style representing the Fishtown/Philadelphia community. Community icons, local landmarks, bold text overlay, pastel background, clean layout. Use #FECE87 and black as primary colors.",
        "hashtags": ["#Fishtown", "#Philadelphia", "#LocalBusiness", "#Community"]
    },
    "tech_trends": {
        "description": "Discuss a relevant technology trend that small business owners should know about.",
        "image_prompt": "Flat design vector illustration in Canva style for tech trends. Modern technology icons, bold sans-serif text, pastel background, clean and minimalist. Use #FECE87 and black as primary colors.",
        "hashtags": ["#TechTrends", "#WebDesign", "#Innovation", "#DigitalTransformation"]
    },
    "business_tip": {
        "description": "Share a business tip related to digital presence, marketing, or online success.",
        "image_prompt": "Flat design vector illustration in Canva style for a business tip. Bold text overlay, business and marketing icons, pastel background, clean and professional. Use #FECE87 and black as primary colors.",
        "hashtags": ["#BusinessTips", "#SmallBusiness", "#DigitalMarketing", "#Entrepreneur"]
    },
    "holiday": {
        "description": "Celebrate holidays with posts that honor the significance while connecting to web design and local business success.",
        "image_prompt": "Flat design vector illustration in Canva style for a holiday celebration. Festive icons, bold text overlay, pastel background, clean and cheerful. Use #FECE87 and black as primary colors.",
        "hashtags": ["#Holiday", "#Celebration", "#WebDesign", "#LocalBusiness"]
    },
    "client_spotlight": {
        "description": "Share a success story about a client project, highlighting the results and impact on their business. Focus on local Philadelphia businesses when possible.",
        "image_prompt": "Flat design vector illustration in Canva style for a client spotlight. Business icons, success symbols, bold text overlay, pastel background, clean and modern. Use #FECE87 and black as primary colors.",
        "hashtags": ["#ClientSpotlight", "#SuccessStory", "#WebDesign", "#LocalBusiness"]
    },
    "seo_tips": {
        "description": "Share practical SEO tips and strategies that help small businesses improve their online visibility and search rankings.",
        "image_prompt": "Flat design vector illustration in Canva style for SEO tips. Search icons, graph/chart elements, bold text overlay, pastel background, clean and modern. Use #FECE87 and black as primary colors.",
        "hashtags": ["#SEO", "#SearchEngineOptimization", "#DigitalMarketing", "#WebDesign"]
    },
    "mobile_design": {
        "description": "Share insights about mobile-first design, responsive websites, and mobile user experience best practices.",
        "image_prompt": "Flat design vector illustration in Canva style for mobile design. Smartphone and tablet icons, responsive web elements, bold text overlay, pastel background, clean and modern. Use #FECE87 and black as primary colors.",
        "hashtags": ["#MobileDesign", "#ResponsiveDesign", "#UXDesign", "#MobileFirst"]
    },
    "blog_promotion": {
        "description": "Promote the latest blog post from Fishtown Web Design. Summarize the post and encourage followers to read more on the blog. Include the blog title, a short summary, and a link. Use the blog's featured image.",
        "image_prompt": "Flat design vector illustration in Canva style for a blog promotion. Blog and reading icons, bold text overlay, pastel background, clean and modern. Use #FECE87 and black as primary colors.",
        "hashtags": ["#Blog", "#WebDesignBlog", "#PhillyBusiness", "#FishtownWebDesign"]
    }
}

# Post categories - automatically generated from POST_TYPE_CONFIGS keys
POST_CATEGORIES = list(POST_TYPE_CONFIGS.keys())

# Hashtags
HASHTAGS = [
    "#FishtownWebDesign", "#PhillyWebDesign", "#WebDesign", "#DigitalMarketing",
    "#Philadelphia", "#SmallBusiness", "#WebDevelopment", "#UXDesign",
    "#LocalBusiness", "#Fishtown", "#PhillyBusiness", "#WebsiteDesign",
    "#DigitalAgency", "#Branding", "#SEO"
]

# Holiday definitions - Major US Holidays Only
HOLIDAYS = {
    "new_years_day": {"date": "01-01", "name": "New Year's Day", "type": "major"},
    "martin_luther_king_day": {"date": "01-15", "name": "Martin Luther King Jr. Day", "type": "major", "weekday": "monday"},
    "presidents_day": {"date": "02-19", "name": "Presidents' Day", "type": "major", "weekday": "monday"},
    "memorial_day": {"date": "05-27", "name": "Memorial Day", "type": "major", "weekday": "monday"},
    # "independence_day": {"date": "07-04", "name": "Independence Day", "type": "major"},
    "labor_day": {"date": "09-02", "name": "Labor Day", "type": "major", "weekday": "monday"},
    "columbus_day": {"date": "10-14", "name": "Columbus Day", "type": "major", "weekday": "monday"},
    "veterans_day": {"date": "11-11", "name": "Veterans Day", "type": "major"},
    "thanksgiving": {"date": "11-28", "name": "Thanksgiving", "type": "major", "weekday": "thursday"},
    "christmas": {"date": "12-25", "name": "Christmas", "type": "major"},
}

# Fallback posts for when API fails
FALLBACK_POSTS = [
    "💡 Quick web design tip: Make sure your website loads in under 3 seconds! Speed matters for both user experience and SEO. Need help optimizing your site? We're here to help! 🚀",
    "🌟 Client Spotlight: We recently helped a local Fishtown restaurant create a stunning website that increased their online orders by 40%! Great food + great website = happy customers! 🍕",
    "📊 Did you know? 57% of users won't recommend a business with a poorly designed mobile website. Mobile-first design isn't just a trend—it's essential! 📱",
    "🏘️ Love our Fishtown community! Supporting local businesses is what we're all about. What's your favorite local spot in the neighborhood? Share below! 👇",
    "🚀 The future of web design is here! AI-powered tools are revolutionizing how we create websites. But remember, human creativity and strategy still drive the best results! 🤖",
    "💼 Business tip: Your website is often the first impression potential customers have of your business. Make it count! Professional design builds trust and credibility. 🎯"
]

# Image generation settings
IMAGE_SETTINGS = {
    "size": "1024x1024",
    "quality": "hd",
    "style": "vivid",
    "max_tokens": 500,
    "temperature": 0.7
}

# Content similarity threshold
SIMILARITY_THRESHOLD = 0.3

# Daily post limits
MAX_DAILY_POSTS = 1
MAX_POST_GENERATION_ATTEMPTS = 5 