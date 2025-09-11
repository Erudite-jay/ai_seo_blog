import requests
from bs4 import BeautifulSoup
import time
from typing import Dict

def extract_meta(url: str) -> Dict[str, str]:
    """Extract meta information from a URL with robust error handling."""
    result = {"url": url, "title": "Error", "description": "Error", "status": "failed"}
    
    print(f"    Extracting meta from: {url[:50]}...")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
        
        response = requests.get(url, timeout=10, headers=headers, allow_redirects=True)
        response.raise_for_status()
        
        # Check if content is HTML
        content_type = response.headers.get('content-type', '').lower()
        if 'html' not in content_type:
            result.update({
                "title": "Non-HTML Content",
                "description": f"Content type: {content_type}",
                "status": "skipped"
            })
            return result
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract title
        title = "No Title"
        if soup.title and soup.title.string:
            title = soup.title.string.strip()
        elif soup.find("h1"):
            title = soup.find("h1").get_text().strip()
        
        # Extract description with fallbacks
        description = "No Description"
        
        # Try meta description
        desc_tag = soup.find("meta", attrs={"name": "description"})
        if desc_tag and desc_tag.get('content'):
            description = desc_tag['content'].strip()
        else:
            # Try Open Graph description
            og_desc = soup.find("meta", attrs={"property": "og:description"})
            if og_desc and og_desc.get('content'):
                description = og_desc['content'].strip()
            else:
                # Fallback to first paragraph
                first_p = soup.find("p")
                if first_p:
                    description = first_p.get_text().strip()[:160] + "..."
        
        result.update({
            "title": title[:100],  # Limit title length
            "description": description[:300],  # Limit description length
            "status": "success"
        })
        
        print(f"    ✓ Success: {title[:30]}...")
        
        # Be respectful with delays
        time.sleep(0.5)
        
    except requests.RequestException as e:
        result["description"] = f"Request error: {str(e)}"
        print(f"    ✗ Request failed: {str(e)[:50]}")
    except Exception as e:
        result["description"] = f"Parsing error: {str(e)}"
        print(f"    ✗ Parse failed: {str(e)[:50]}")
    
    return result

if __name__ == "__main__":
    # Test the function
    test_url = "https://example.com"
    print(extract_meta(test_url))