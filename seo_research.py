import json
from typing import List, Dict
import time
from serp_crawl import get_serp_results
from meta_extraction import extract_meta

def save_results_to_file(results: List[Dict], filename: str = "seo_research_results.json"):
    """Save results to a JSON file for later analysis."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\n✓ Results saved to {filename}")
    except Exception as e:
        print(f"✗ Error saving results: {e}")

def main(seed_keyword: str, num_results: int = 10):
    """Main function to research a single keyword and extract meta data."""
    print(f"\nStarting SEO research for: '{seed_keyword}'")
    print("=" * 60)
    
    all_results = []
    successful_extractions = 0
    total_urls = 0
    
    print(f"\nStep 1: Getting search results for '{seed_keyword}'...")
    urls = get_serp_results(seed_keyword, num_results=num_results)
    
    if not urls:
        print(f"  ✗ No URLs found for '{seed_keyword}'")
        return []
        
    print(f"✓ Found {len(urls)} URLs for '{seed_keyword}'")
    
    print(f"\nStep 2: Extracting meta data from {len(urls)} URLs...")
    for j, url in enumerate(urls, 1):
        total_urls += 1
        
        meta = extract_meta(url)
        meta['keyword'] = seed_keyword  # Add the search keyword
        meta['rank'] = j  # Add ranking position
        all_results.append(meta)
        
        if meta['status'] == 'success':
            successful_extractions += 1
    
    # Display results summary
    print("\n" + "=" * 60)
    print("RESEARCH SUMMARY")
    print("=" * 60)
    print(f"Keyword: '{seed_keyword}'")
    print(f"Total URLs found: {total_urls}")
    print(f"Successful extractions: {successful_extractions}")
    print(f"Success rate: {(successful_extractions/total_urls*100):.1f}%" if total_urls > 0 else "N/A")
    
    # Display successful results
    if successful_extractions > 0:
        print("\nSUCCESSFUL EXTRACTIONS")
        print("-" * 40)
        for item in all_results:
            if item['status'] == 'success':
                print(f"\n🔸 Rank #{item['rank']}")
                print(f"   URL: {item['url']}")
                print(f"   Title: {item['title']}")
                print(f"   Description: {item['description'][:100]}...")
    else:
        print("\n No successful extractions found.")
        print("This might be due to:")
        print("- Network connectivity issues")
        print("- Websites blocking automated requests")
        print("- Invalid URLs in search results")
    
    # Save results to file
    if all_results:
        save_results_to_file(all_results)
    
    return all_results

if __name__ == "__main__":
    keyword="Python programming"
    try:
        print("🔧 SEO Research Tool Starting...")
        results = main(keyword, num_results=5)
        print(f"\n Process completed! Found {len(results)} total results.")
    except KeyboardInterrupt:
        print("\n Process interrupted by user.")
    except Exception as e:
        print(f"\n Unexpected error in main execution: {e}")
        import traceback
        traceback.print_exc()
