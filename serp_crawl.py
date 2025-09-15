from typing import List
from googleapiclient.discovery import build
from dotenv import load_dotenv
from urllib.parse import urlparse
import os

load_dotenv()

GOOGLE_CX = os.getenv("GOOGLE_CX")
GOOGLE_SERP = os.getenv("GOOGLE_SERP")

def get_domain(url: str) -> str:
    """Extract domain from URL."""
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain
    except:
        return url

def get_serp_results(query: str, num_results: int = 10) -> List[str]:
    """
    Get search results using Google Custom Search JSON API with unique domain filtering.
    You need a Google API key + Custom Search Engine ID (cx).
    """
    print(f"  Searching Google for: '{query}'")
    api_key = GOOGLE_SERP   
    cx = GOOGLE_CX         

    try:
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=query, cx=cx, num=num_results).execute()

        urls = []
        seen_domains = set() 
        
        if 'items' in res:
            for item in res['items']:
                url = item['link']
                domain = get_domain(url)
                
                if domain not in seen_domains:
                    urls.append(url)
                    seen_domains.add(domain)

        print(f"  Found {len(urls)} unique domain URLs")
        return urls

    except Exception as e:
        print(f"  Error getting Google SERP results for '{query}': {e}")
        return []

if __name__ == "__main__":
    query = "seo tools"
    results = get_serp_results(query)
    print(f"\nSERP results for '{query}' (unique domains only):")
    for i, url in enumerate(results, 1):
        domain = get_domain(url)
        print(f"  {i}. {domain} - {url}")