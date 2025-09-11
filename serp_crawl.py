from typing import List
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
load_dotenv()


GOOGLE_CX=os.getenv("GOOGLE_CX")
GOOGLE_SERP=os.getenv("GOOGLE_SERP")

def get_serp_results(query: str, num_results: int = 10) -> List[str]:
    """
    Get search results using Google Custom Search JSON API.
    You need a Google API key + Custom Search Engine ID (cx).
    """
    print(f"  Searching Google for: '{query}'")
    api_key = GOOGLE_SERP   
    cx = GOOGLE_CX         

    try:
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=query, cx=cx, num=num_results).execute()

        urls = []
        if 'items' in res:
            for item in res['items']:
                urls.append(item['link'])

        print(f"  Found {len(urls)} URLs")
        return urls

    except Exception as e:
        print(f"  Error getting Google SERP results for '{query}': {e}")
        return []

if __name__ == "__main__":
    query = "seo tools"
    results = get_serp_results(query)
    print(f"SERP results for '{query}': {results}")
