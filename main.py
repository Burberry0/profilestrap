import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import openai
import os
from dotenv import load_dotenv
from typing import List, Dict, Optional, Set
import logging
from datetime import datetime
import argparse
import re

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

# Common page patterns to look for
IMPORTANT_PAGE_PATTERNS = [
    r'about', r'company', r'team', r'leadership', r'history', r'mission', r'vision',
    r'services', r'solutions', r'products', r'offerings', r'what-we-do',
    r'contact', r'get-in-touch', r'connect', r'reach-out',
    r'work', r'portfolio', r'projects', r'case-studies', r'clients',
    r'approach', r'methodology', r'process', r'how-we-work',
    r'careers', r'jobs', r'join-us', r'opportunities',
    r'blog', r'news', r'insights', r'resources'
]

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

def get_organization_links(url: str, organization_name: str = None) -> List[str]:
    """Extract organization-specific links, excluding social media."""
    links = fetch_links(url)
    if not links:
        return []
    
    # If no organization name provided, extract from domain
    if not organization_name:
        organization_name = urlparse(url).netloc.replace('www.', '').split('.')[0]
    
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

def discover_important_pages(url: str, max_pages: int = 8) -> List[str]:
    """Auto-discover important pages based on common patterns and link analysis."""
    links = fetch_links(url)
    if not links:
        return []
    
    base_domain = urlparse(url).netloc
    important_pages = []
    
    # Filter internal links
    internal_links = []
    for link in links:
        parsed = urlparse(link)
        if parsed.netloc == base_domain or not parsed.netloc:
            path = parsed.path.strip('/')
            if path and path not in ['', '/']:
                internal_links.append(path)
    
    # Score pages based on importance patterns
    page_scores = {}
    for path in internal_links:
        score = 0
        path_lower = path.lower()
        
        # Check against important patterns
        for pattern in IMPORTANT_PAGE_PATTERNS:
            if re.search(pattern, path_lower):
                score += 1
        
        # Bonus for exact matches
        if any(exact in path_lower for exact in ['about', 'services', 'contact', 'work', 'team']):
            score += 2
        
        # Penalty for very long paths (likely not main pages)
        if len(path.split('/')) > 3:
            score -= 1
        
        if score > 0:
            page_scores[path] = score
    
    # Sort by score and return top pages
    sorted_pages = sorted(page_scores.items(), key=lambda x: x[1], reverse=True)
    important_pages = [page for page, score in sorted_pages[:max_pages]]
    
    logger.info(f"Discovered {len(important_pages)} important pages: {important_pages}")
    return important_pages

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

def scrape_company_pages(base_url: str, organization_name: str = None, max_pages: int = 8) -> Dict[str, Dict]:
    """Scrape content from important company pages with auto-discovery."""
    # Auto-discover important pages
    important_pages = discover_important_pages(base_url, max_pages=max_pages)
    
    # If no pages discovered, try some common defaults
    if not important_pages:
        important_pages = ["about", "services", "contact", "work", "team"]
    
    scraped_content = {}
    
    for page in important_pages:
        # Handle both relative and absolute URLs
        if page.startswith('http'):
            full_url = page
        else:
            full_url = f"{base_url.rstrip('/')}/{page.lstrip('/')}"
        
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

def generate_company_summary(scraped_content: Dict[str, Dict], company_url: str) -> str:
    """Generate a comprehensive company summary using AI or fallback to manual."""
    if not scraped_content:
        return "No content available for summarization."
    
    # Extract company name from URL
    company_name = urlparse(company_url).netloc.replace('www.', '').split('.')[0].title()
    
    # Combine content for AI analysis
    all_content = ""
    for page, info in scraped_content.items():
        all_content += f"\n\n--- {page.upper()} ---\n"
        all_content += info['content'][:MAX_CONTENT_LENGTH // len(scraped_content)]
    
    # AI summary prompt
    summary_prompt = f"""
Based on the following content from {company_name}'s website ({company_url}), create a comprehensive summary of their business profile. Focus on:

1. Company Overview & Mission
2. Years of Experience & Track Record  
3. Core Services & Expertise
4. Technology Stack & Approach
5. Target Market & Clientele
6. Notable Projects & Portfolio
7. Business Philosophy & Methodology
8. Geographic Presence & Team Structure
9. Key Differentiators & Competitive Advantages
10. Recent News & Updates

Content to analyze:
{all_content}

Please provide a professional, insightful summary that would be valuable for someone preparing for a business meeting with this company.
"""
    
    # Try AI first, fallback to manual
    ai_summary = call_openai_api(summary_prompt, max_tokens=1500)
    if ai_summary:
        return ai_summary
    
    logger.info("Falling back to manual summary generation")
    return generate_manual_summary(scraped_content, company_url)

def generate_manual_summary(scraped_content: Dict[str, Dict], company_url: str) -> str:
    """Generate a manual summary with improved structure."""
    company_name = urlparse(company_url).netloc.replace('www.', '').split('.')[0].title()
    
    summary = f"{company_name.upper()} - COMPANY PROFILE SUMMARY\n"
    summary += "=" * 60 + "\n\n"
    
    # Extract key information from scraped content
    about_content = scraped_content.get('about', {}).get('content', '')
    services_content = scraped_content.get('services', {}).get('content', '')
    work_content = scraped_content.get('work', {}).get('content', '')
    
    # Company Overview
    summary += "COMPANY OVERVIEW:\n"
    summary += f"- Website: {company_url}\n"
    summary += f"- Company: {company_name}\n"
    summary += "- Content analyzed from multiple pages\n"
    summary += f"- Total pages scraped: {len(scraped_content)}\n\n"
    
    # Available Information
    summary += "AVAILABLE INFORMATION:\n"
    for page, info in scraped_content.items():
        summary += f"- {page.title()}: {info['length']} characters\n"
    
    summary += "\n"
    
    # Content Previews
    summary += "CONTENT PREVIEWS:\n"
    for page, info in scraped_content.items():
        summary += f"\n{page.upper()}:\n"
        summary += f"{info['preview']}\n"
        summary += "-" * 40 + "\n"
    
    return summary

# ---- Main Function ----

def main():
    """Main function with command line argument support."""
    parser = argparse.ArgumentParser(description='ProfileStrap - Company Website Analysis Tool')
    parser.add_argument('url', help='Company website URL to analyze')
    parser.add_argument('--output', '-o', help='Output filename for summary (default: auto-generated)')
    parser.add_argument('--pages', '-p', type=int, default=8, help='Maximum number of pages to scrape (default: 8)')
    parser.add_argument('--no-ai', action='store_true', help='Skip AI summary generation')
    
    args = parser.parse_args()
    
    print("🔗 ProfileStrap - Company Website Analysis Tool")
    print("=" * 60)
    
    url = args.url
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    print(f"\n🌐 Analyzing: {url}")
    print("-" * 40)
    
    # Fetch and categorize links
    extracted_links = fetch_links(url)
    if not extracted_links:
        print("❌ No links found or error occurred")
        return
    
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
    print("✅ Link analysis completed!")

def analyze_company(url: str, output_file: str = None, max_pages: int = 8, use_ai: bool = True) -> str:
    """Analyze a company website and generate a summary."""
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    print(f"🔍 Scraping company pages from: {url}")
    
    # Scrape company pages
    content = scrape_company_pages(url)
    
    if not content:
        return "❌ No content could be scraped from the website."
    
    print(f"\n✅ Successfully scraped {len(content)} pages")
    
    # Generate summary
    if use_ai:
        print("🤖 Generating AI-powered company summary...")
        summary = generate_company_summary(content, url)
    else:
        print("📝 Generating manual summary...")
        summary = generate_manual_summary(content, url)
    
    # Save to file
    if not output_file:
        company_name = urlparse(url).netloc.replace('www.', '').split('.')[0]
        output_file = f"{company_name}_company_profile.txt"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print(f"\n✅ Company profile saved to: {output_file}")
    return summary

if __name__ == "__main__":
    main()
