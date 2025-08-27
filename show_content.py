#!/usr/bin/env python3
from main import scrape_organization_pages

def main():
    print("🔍 Scraping Eight Bit Studios pages...")
    content = scrape_organization_pages('https://eightbitstudios.com')
    
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