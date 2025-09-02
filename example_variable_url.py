#!/usr/bin/env python3
"""
Example showing how to use scrape_company_pages with any variable URL
"""

from main import scrape_company_pages, discover_important_pages

def analyze_any_company(company_url, max_pages=5):
    """Analyze any company website with a variable URL"""
    
    print(f"🔍 Analyzing: {company_url}")
    
    # Step 1: Discover important pages
    important_pages = discover_important_pages(company_url, max_pages=max_pages)
    print(f"📄 Discovered {len(important_pages)} important pages: {important_pages}")
    
    # Step 2: Scrape content from those pages
    content = scrape_company_pages(company_url)
    print(f"✅ Successfully scraped {len(content)} pages")
    
    # Step 3: Show results
    print("\n" + "="*60)
    print("SCRAPED CONTENT SUMMARY:")
    print("="*60)
    
    for page, info in content.items():
        print(f"\n📄 {page.upper()}:")
        print(f"   URL: {info['url']}")
        print(f"   Length: {info['length']} characters")
        print(f"   Preview: {info['preview'][:150]}...")
    
    return content

def main():
    # Example 1: Use with a variable URL
    company_url = "https://stripe.com"  # You can change this to any URL
    content = analyze_any_company(company_url, max_pages=3)
    
    print(f"\n🎉 Analysis complete! Scraped {len(content)} pages from {company_url}")
    
    # Example 2: Use with different companies
    companies = [
        "https://openai.com",
        "https://github.com"
    ]
    
    for url in companies:
        print(f"\n{'='*60}")
        content = analyze_any_company(url, max_pages=2)
        print(f"✅ Completed analysis for {url}")

if __name__ == "__main__":
    main()
