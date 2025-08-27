#!/usr/bin/env python3
from main import scrape_organization_pages, generate_experience_summary

def main():
    print("🔍 Scraping Eight Bit Studios pages...")
    content = scrape_organization_pages('https://eightbitstudios.com')
    
    print("\n" + "="*80)
    print("GENERATING EXPERIENCE SUMMARY...")
    print("="*80)
    
    # Generate the summary
    summary = generate_experience_summary(content)
    
    print("\n" + "="*80)
    print("EXPERIENCE SUMMARY:")
    print("="*80)
    print(summary)
    
    # Save summary to file
    with open('eightbitstudios_experience_summary.txt', 'w') as f:
        f.write(summary)
    
    print(f"\n✅ Summary saved to: eightbitstudios_experience_summary.txt")

if __name__ == "__main__":
    main() 