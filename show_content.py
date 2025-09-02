#!/usr/bin/env python3
import argparse
from main import scrape_company_pages, discover_important_pages

def main():
    parser = argparse.ArgumentParser(description='Show scraped content from any company website')
    parser.add_argument('url', help='Company website URL to scrape')
    parser.add_argument('--pages', '-p', type=int, default=8, help='Maximum number of pages to scrape (default: 8)')
    
    args = parser.parse_args()
    
    url = args.url
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    print(f"🔍 Scraping {url} pages...")
    
    # First discover pages with the specified limit
    important_pages = discover_important_pages(url, max_pages=args.pages)
    print(f"Discovered {len(important_pages)} pages: {important_pages}")
    
    # Then scrape content from those pages
    content = scrape_company_pages(url)
    
    print("\n" + "="*80)
    print("CONTENT PREVIEWS:")
    print("="*80)
    
    for page, info in content.items():
        print(f"\n🔍 {page.upper()}:")
        print("-" * 40)
        print(f"URL: {info['url']}")
        print(f"Length: {info['length']} characters")
        print(f"Preview: {info['preview']}")
        print("-" * 40)

if __name__ == "__main__":
    main()
