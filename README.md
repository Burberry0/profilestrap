# 🔗 ProfileStrap

**AI-Powered Website Analysis & Content Scraping Tool**

ProfileStrap is a sophisticated Python tool that automatically scrapes websites, extracts links, and generates comprehensive business summaries using AI. Perfect for market research, competitive analysis, and business intelligence gathering.

## ✨ Features

### 🌐 **Web Scraping & Analysis**
- **Intelligent Link Extraction** - Automatically discovers all links, images, and resources
- **Content Scraping** - Extracts clean, readable text from web pages
- **Link Categorization** - Organizes links into internal, external, images, and other types
- **Organization Filtering** - Focuses on company-specific content while excluding social media

### 🤖 **AI-Powered Summarization**
- **OpenAI Integration** - Uses GPT-4o-mini for intelligent content analysis
- **Business Intelligence** - Generates comprehensive company experience summaries
- **Smart Fallbacks** - Manual summary generation if AI is unavailable
- **Structured Analysis** - Covers company overview, services, approach, and more

### 🛠️ **Technical Capabilities**
- **Professional Logging** - Comprehensive logging with different levels
- **Error Handling** - Robust error handling with graceful fallbacks
- **Type Safety** - Full Python type hints for better code quality
- **Modular Design** - Clean, maintainable, and extensible architecture

## 🚀 Quick Start

### 1. **Installation**
```bash
# Clone the repository
git clone https://github.com/yourusername/profilestrap.git
cd profilestrap

# Install dependencies
pip install -r requirements.txt
```

### 2. **Configuration**
```bash
# Create .env file with your OpenAI API key
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

### 3. **Basic Usage**
```python
from main import scrape_organization_pages, generate_experience_summary

# Scrape a company's website
content = scrape_organization_pages('https://example.com')

# Generate AI-powered summary
summary = generate_experience_summary(content)
print(summary)
```

### 4. **Command Line Usage**
```bash
# Analyze links from a website
python main.py

# Generate comprehensive business summary
python generate_summary.py

# Test link extraction
python test_links.py
```

## 📋 Requirements

- **Python 3.8+**
- **OpenAI API Key** (for AI summarization)
- **Internet Connection** (for web scraping)

### Dependencies
```
requests>=2.25.0
beautifulsoup4>=4.9.0
openai>=1.0.0
python-dotenv>=0.19.0
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in your project root:

```env
OPENAI_API_KEY=sk-your-openai-api-key-here
```

### Customization
Modify constants in `main.py`:
```python
SOCIAL_PLATFORMS = {'facebook.com', 'instagram.com', ...}
IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', ...}
DEFAULT_TIMEOUT = 15
MAX_CONTENT_LENGTH = 8000
```

## 📊 Example Output

### Link Analysis
```
📊 Link Analysis Results:
  🏠 Internal links: 23
  🌐 External links: 10
  🖼️  Images: 48
  📄 Other: 0
```

### AI-Generated Summary
```
### Comprehensive Summary of Eight Bit Studios

#### 1. Company Overview & Mission
Eight Bit Studios is a specialized design and development firm focused on creating AI-driven applications for founders...

#### 2. Years of Experience & Track Record
Founded in 2009, Eight Bit Studios boasts over a decade of experience in the mobile and web app development space...
```

## 🏗️ Architecture

### Core Modules
- **`main.py`** - Main application with all core functionality
- **`generate_summary.py`** - AI summary generation script
- **`test_links.py`** - Link testing and validation script
- **`show_content.py`** - Content preview and analysis script

### Key Functions
- **`fetch_links()`** - Web scraping and link extraction
- **`scrape_organization_pages()`** - Multi-page content scraping
- **`generate_experience_summary()`** - AI-powered business analysis
- **`categorize_links()`** - Intelligent link organization

## 🔒 Security & Privacy

- **API Key Protection** - Uses environment variables for sensitive data
- **Git Ignore** - Prevents accidental commit of sensitive files
- **Rate Limiting** - Respectful web scraping with configurable timeouts
- **User Agent** - Professional headers to avoid blocking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** - For providing the AI summarization capabilities
- **BeautifulSoup** - For robust HTML parsing
- **Requests** - For reliable HTTP operations

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/profilestrap/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/profilestrap/discussions)
- **Wiki**: [Project Wiki](https://github.com/yourusername/profilestrap/wiki)

---

**Made with ❤️ for business intelligence and market research** 