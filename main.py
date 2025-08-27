import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import openai
import os
from dotenv import load_dotenv
from typing import List, Dict, Optional, Set
import logging
from datetime import datetime

# ---- Setup Logging ----
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ---- OpenAI Setup ----
def setup_openai():
    """Initialize OpenAI configuration with proper error handling."""
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.warning("OPENAI_API_KEY not found in environment variables")
        logger.info("Create a .env file with: OPENAI_API_KEY=your_key_here")
        return None
    
    try:
        openai.api_key = api_key
        # Test the API key
        client = openai.OpenAI(api_key=api_key)
        client.models.list()  # Simple API test
        logger.info("OpenAI API key configured successfully")
        return api_key
    except Exception as e:
        logger.error(f"Failed to configure OpenAI API: {e}")
        return None

# Initialize OpenAI
OPENAI_API_KEY = setup_openai()

# ---- Constants ----
SOCIAL_PLATFORMS = {
    'facebook.com', 'instagram.com', 'twitter.com', 'x.com', 
    'linkedin.com', 'youtube.com', 'tiktok.com', 'snapchat.com'
}

IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.ico', '.bmp', '.tiff'}

DEFAULT_TIMEOUT = 15
MAX_CONTENT_LENGTH = 8000  # For OpenAI token limits

# ---- Core Functions ----

def fetch_links(url: str, timeout: int = DEFAULT_TIMEOUT) -> List[str]:
    """Fetch links and paths from a webpage with improved error handling."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, timeout=timeout, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        links = set()

        # Extract href links
        for tag in soup.find_all("a", href=True):
            href = tag["href"]
            if href and href.strip():
                full_url = urljoin(url, href)
                links.add(full_url)

        # Extract images
        for img in soup.find_all("img", src=True):
            src = img["src"]
            if src and src.strip():
                full_url = urljoin(url, src)
                links.add(full_url)

        logger.info(f"Successfully extracted {len(links)} links from {url}")
        return list(links)
        
    except requests.exceptions.Timeout:
        logger.error(f"Timeout error fetching {url}")
        return []
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error fetching {url}: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error fetching {url}: {e}")
        return []

def categorize_links(links: List[str], base_url: str) -> Dict[str, List[str]]:
    """Categorize links into internal, external, and images."""
    base_domain = urlparse(base_url).netloc
    
    categorized = {
        'internal': [],
        'external': [],
        'images': [],
        'other': []
    }
    
    for link in links:
        parsed = urlparse(link)
        
        if any(link.lower().endswith(ext) for ext in IMAGE_EXTENSIONS):
            categorized['images'].append(link)
        elif parsed.netloc == base_domain or not parsed.netloc:
            categorized['internal'].append(link)
        elif parsed.netloc:
            categorized['external'].append(link)
        else:
            categorized['other'].append(link)
    
    return categorized

def get_all_links_array(url: str) -> List[str]:
    """Extract all links from a URL and return them as a clean array."""
    links = fetch_links(url)
    if not links:
        return []
    
    # Clean and deduplicate links
    clean_links = set()
    for link in links:
        parsed = urlparse(link)
        clean_link = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        clean_links.add(clean_link)
    
    return sorted(clean_links)

def get_organization_links(url: str, organization_name: str = "eightbitstudios") -> List[str]:
    """Extract organization-specific links, excluding social media."""
    links = fetch_links(url)
    if not links:
        return []
    
    filtered_links = []
    
    for link in links:
        if organization_name.lower() in link.lower():
            # Skip social media links
            if any(platform in link.lower() for platform in SOCIAL_PLATFORMS):
                continue
            
            # Clean the link
            parsed = urlparse(link)
            clean_link = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            if clean_link not in filtered_links:
                filtered_links.append(clean_link)
    
    return sorted(filtered_links)

def scrape_page_content(url: str, timeout: int = DEFAULT_TIMEOUT) -> Optional[str]:
    """Scrape text content from a specific page with improved content cleaning."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, timeout=timeout, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Remove unwanted elements
        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.decompose()
        
        # Get text content
        text = soup.get_text()
        
        # Improved text cleaning
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk and len(chunk) > 1)
        
        return text if text else None
        
    except Exception as e:
        logger.error(f"Error scraping {url}: {e}")
        return None

def scrape_organization_pages(base_url: str, organization_name: str = "eightbitstudios") -> Dict[str, Dict]:
    """Scrape content from specific organization pages with better error handling."""
    target_pages = [
        "about", "approach", "contact/general", "services",
        "services/ai-integration", "services/product-strategy", 
        "work", "services/startup-branding"
    ]
    
    scraped_content = {}
    
    for page in target_pages:
        full_url = f"{base_url}/{page}"
        logger.info(f"Scraping: {full_url}")
        
        content = scrape_page_content(full_url)
        if content:
            scraped_content[page] = {
                "url": full_url,
                "content": content,
                "preview": content[:500] + "..." if len(content) > 500 else content,
                "length": len(content),
                "scraped_at": datetime.now().isoformat()
            }
            logger.info(f"✅ Success - {len(content)} characters")
        else:
            logger.warning(f"❌ Failed to scrape {page}")
    
    return scraped_content

# ---- AI Functions ----

def call_openai_api(prompt: str, model: str = "gpt-4o-mini", max_tokens: int = 1000) -> Optional[str]:
    """Make OpenAI API call with proper error handling."""
    if not OPENAI_API_KEY:
        logger.warning("OpenAI API key not configured")
        return None
    
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        return None

def generate_experience_summary(scraped_content: Dict[str, Dict]) -> str:
    """Generate a comprehensive summary using AI or fallback to manual."""
    if not scraped_content:
        return "No content available for summarization."
    
    # Combine content for AI analysis
    all_content = ""
    for page, info in scraped_content.items():
        all_content += f"\n\n--- {page.upper()} ---\n"
        all_content += info['content'][:MAX_CONTENT_LENGTH // len(scraped_content)]
    
    # AI summary prompt
    summary_prompt = f"""
Based on the following content from Eight Bit Studios' website, create a comprehensive summary of their experience, expertise, and business profile. Focus on:

1. Company Overview & Mission
2. Years of Experience & Track Record  
3. Core Services & Expertise
4. Technology Stack & Approach
5. Target Market & Clientele
6. Notable Projects & Portfolio
7. Business Philosophy & Methodology
8. Geographic Presence & Team Structure

Content to analyze:
{all_content}
"""
    
    # Try AI first, fallback to manual
    ai_summary = call_openai_api(summary_prompt, max_tokens=1000)
    if ai_summary:
        return ai_summary
    
    logger.info("Falling back to manual summary generation")
    return generate_manual_summary(scraped_content)

def generate_manual_summary(scraped_content: Dict[str, Dict]) -> str:
    """Generate a manual summary with improved structure."""
    summary = "EIGHT BIT STUDIOS - EXPERIENCE SUMMARY\n"
    summary += "=" * 50 + "\n\n"
    
    # Extract key information
    about_content = scraped_content.get('about', {}).get('content', '')
    approach_content = scraped_content.get('approach', {}).get('content', '')
    
    # Company Overview
    summary += "COMPANY OVERVIEW:\n"
    summary += "- Founded: 2009\n"
    summary += "- Mission: Help non-technical founders launch AI-enabled MVPs faster\n"
    summary += "- Focus: AI app design & development for founders\n"
    summary += "- Philosophy: 'Functional Beats Fictional'\n\n"
    
    # Core Services
    summary += "CORE SERVICES:\n"
    summary += "- Flutter & Rails development\n"
    summary += "- UI/UX design\n"
    summary += "- AI integration\n"
    summary += "- Product strategy\n"
    summary += "- Startup branding\n"
    summary += "- Fractional CTO leadership\n"
    summary += "- MVP development\n\n"
    
    # Approach & Methodology
    summary += "APPROACH & METHODOLOGY:\n"
    summary += "- Feasibility First, Lean Always\n"
    summary += "- Start with working code, not concepts\n"
    summary += "- Solve tech challenges upfront\n"
    summary += "- Lean, modern studio model\n"
    summary += "- Move fast, cut fluff, build smart\n\n"
    
    # Geographic Presence
    summary += "GEOGRAPHIC PRESENCE:\n"
    summary += "- Local offices: Chicago + Dallas\n"
    summary += "- Remote work: Everywhere\n\n"
    
    # Target Market
    summary += "TARGET MARKET:\n"
    summary += "- Non-technical founders\n"
    summary += "- Startups needing AI-enabled MVPs\n"
    summary += "- Companies requiring technical expertise\n"
    summary += "- Founders Fleet program participants\n\n"
    
    # Portfolio Highlights
    summary += "PORTFOLIO HIGHLIGHTS:\n"
    summary += "- Grogo: Brain boosting screen breaks app\n"
    summary += "- RunBetter: Treadmill race training app\n"
    summary += "- Multiple successful app launches since 2009\n\n"
    
    # Business Model
    summary += "BUSINESS MODEL:\n"
    summary += "- Modular, founder-friendly services\n"
    summary += "- Project-based development\n"
    summary += "- Strategic partnerships\n"
    summary += "- Contractor-based team structure\n"
    
    return summary

# ---- Main Function ----

def main():
    """Main function with improved organization and error handling."""
    print("🔗 ProfileStrap - Enhanced Link Analysis & Content Scraping")
    print("=" * 60)
    
    # Test URLs
    test_urls = [
        "https://eightbitstudios.com",
    ]
    
    for url in test_urls:
        print(f"\n🌐 Analyzing: {url}")
        print("-" * 40)
        
        # Fetch and categorize links
        extracted_links = fetch_links(url)
        if not extracted_links:
            print("❌ No links found or error occurred")
            continue
        
        # Categorize links
        categorized = categorize_links(extracted_links, url)
        
        print(f"📊 Link Analysis Results:")
        print(f"  🏠 Internal links: {len(categorized['internal'])}")
        print(f"  🌐 External links: {len(categorized['external'])}")
        print(f"  🖼️  Images: {len(categorized['images'])}")
        print(f"  📄 Other: {len(categorized['other'])}")
        
        # Show samples
        for category, links in categorized.items():
            if links:
                print(f"\n{category.title()} (first 3):")
                for i, link in enumerate(links[:3], 1):
                    print(f"  {i}. {link}")
        
        print(f"\n{'='*60}")
    
    print("✅ Enhanced link analysis completed!")

if __name__ == "__main__":
    main()