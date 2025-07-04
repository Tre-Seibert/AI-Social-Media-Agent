# Social Media Automation Platform

A professional social media automation platform for Fishtown Web Design that generates and posts content across multiple platforms using AI-powered content generation.

## 🚀 Features

- **AI-Powered Content Generation**: Uses OpenAI's GPT models to create engaging social media posts
- **Automated Image Generation**: Creates custom images using DALL-E 3 for each post
- **Multi-Platform Posting**: Supports Facebook and Instagram (expandable)
- **Holiday-Aware Content**: Automatically detects holidays and generates relevant content
- **Content Diversity**: Generates different types of posts (tech trends, business tips, portfolio showcases, etc.)
- **Duplicate Prevention**: Ensures content variety by checking post history
- **Scheduled Posting**: Automated daily posting with configurable schedules

## 📁 Project Structure

```
social-media-automation/
├── src/                          # Source code
│   ├── core/                     # Core application logic
│   │   ├── __init__.py
│   │   ├── agent.py              # Main automation agent
│   │   ├── config.py             # Configuration management
│   │   └── utils.py              # Utility functions
│   ├── services/                 # Business logic services
│   │   ├── __init__.py
│   │   ├── holiday_manager.py    # Holiday detection and management
│   │   ├── post_manager.py       # Post history and management
│   │   ├── post_generator.py     # Content generation service
│   │   ├── image_generator.py    # Image generation service
│   │   └── social_media_poster.py # Social media platform integration
│   └── scripts/                  # Executable scripts
│       ├── __init__.py
│       └── run_agent.py          # Main execution script
├── data/                         # Data storage
│   ├── posts/                    # Post history and daily posts
│   ├── images/                   # Generated images
│   └── logs/                     # Application logs
├── config/                       # Configuration files
│   ├── .env.example              # Environment variables template
│   └── settings.yaml             # Application settings
├── docs/                         # Documentation
│   ├── api.md
│   ├── deployment.md
│   └── troubleshooting.md
├── requirements.txt              # Python dependencies
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd social-media-automation
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp config/.env.example config/.env
   # Edit config/.env with your API keys and configuration
   ```

5. **Run the application**
   ```bash
   python src/scripts/run_agent.py
   ```

## ⚙️ Configuration

### Environment Variables

Create a `config/.env` file with the following variables:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Facebook Configuration
FACEBOOK_ACCESS_TOKEN=your_facebook_access_token
FACEBOOK_PAGE_ID=your_facebook_page_id

# Instagram Configuration (optional)
INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_PASSWORD=your_instagram_password

# Application Settings
LOG_LEVEL=INFO
POSTING_SCHEDULE=daily
```

### Application Settings

Edit `config/settings.yaml` to customize:

- Company information
- Post categories and hashtags
- Holiday definitions
- Image generation settings
- Posting schedules

## 📖 Usage

### Basic Usage

```python
from src.core.agent import SocialMediaAgent

# Initialize the agent
agent = SocialMediaAgent()

# Generate and post content
agent.run_daily_posting()
```

### Advanced Usage

```python
from src.services.post_generator import PostGenerator
from src.services.image_generator import ImageGenerator

# Generate custom content
post_gen = PostGenerator()
content = post_gen.generate_post("tech_trends")

# Generate custom image
img_gen = ImageGenerator()
image_path = img_gen.generate_image("tech_trends", content)
```

## 🧪 Testing

Run the test suite:

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run specific test modules
pytest tests/test_services/
pytest tests/test_core/
```

## 📊 Monitoring

The application generates logs in `data/logs/`:

- `social_media.log` - Main application logs
- `posting_log.json` - Detailed posting history
- `post_history.json` - Complete post history

## 🔧 Development

### Adding New Post Types

1. Add category to `config/settings.yaml`
2. Update prompts in `src/services/post_generator.py`
3. Add image prompts in `src/services/image_generator.py`

### Adding New Social Media Platforms

1. Create new service in `src/services/`
2. Implement posting interface
3. Update `src/services/social_media_poster.py`

## 🚀 Deployment

### Local Deployment

```bash
# Run with logging
python src/scripts/run_agent.py --log-level DEBUG

# Run scheduled posting
python src/scripts/run_agent.py --schedule
```

### Production Deployment

1. Set up environment variables
2. Configure logging
3. Set up monitoring
4. Use process manager (PM2, systemd, etc.)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

- Check the documentation in `docs/`
- Review the troubleshooting guide
- Open an issue on GitHub

## 🔄 Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and updates. 