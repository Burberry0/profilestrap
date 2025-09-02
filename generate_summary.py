#!/usr/bin/env python3
import argparse
from main import analyze_company

def main():
    parser = argparse.ArgumentParser(description='Generate company profile summary from any website')
    parser.add_argument('url', help='Company website URL to analyze')
    parser.add_argument('--output', '-o', help='Output filename for summary (default: auto-generated)')
    parser.add_argument('--pages', '-p', type=int, default=8, help='Maximum number of pages to scrape (default: 8)')
    parser.add_argument('--no-ai', action='store_true', help='Skip AI summary generation')
    
    args = parser.parse_args()
    
    print("🔍 ProfileStrap - Company Analysis Tool")
    print("=" * 50)
    
    # Analyze the company
    summary = analyze_company(
        url=args.url,
        output_file=args.output,
        max_pages=args.pages,
        use_ai=not args.no_ai
    )
    
    print("\n" + "="*80)
    print("COMPANY PROFILE SUMMARY:")
    print("="*80)
    print(summary)

if __name__ == "__main__":
    main()
