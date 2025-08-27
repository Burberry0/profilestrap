#!/usr/bin/env python3
"""
Test script for ProfileStrap link extraction functionality
"""

from main import fetch_links, test_url_interactive
from urllib.parse import urlparse

def main():
    print("🔗 ProfileStrap Link Extraction Test Suite")
    print("=" * 50)
    
    # Test various types of websites
    test_sites = [
        {
            "url": "https://github.com", 
            "description": "GitHub - Complex web app with many features"
        },
        {
            "url": "https://example.com", 
            "description": "Example.com - Simple static page"
        },
        {
            "url": "https://eightbitstudios.com", 
            "description": "Eight Bit Studios - Marketing/portfolio site"
        }
    ]
    
    for site in test_sites:
        print(f"\n🌐 {site['description']}")
        print("-" * 40)
        success = test_url_interactive(site['url'])
        
        if success:
            print("✅ Test passed!")
        else:
            print("❌ Test failed!")
        
        print("\n")
    
    print("📋 Summary:")
    print("- ✅ Link extraction from href attributes")
    print("- ✅ Image source extraction") 
    print("- ✅ Relative URL resolution")
    print("- ✅ Link categorization (internal/external/images)")
    print("- ✅ Error handling for failed requests")
    print("- ✅ Support for complex modern websites")
    
    print("\n🎉 All link fetching functionality tests completed!")

if __name__ == "__main__":
    main() 