import google.generativeai as genai
from typing import List, Dict

def generate_seo_suggestions(blog_content: str, model, num_options: int = 3) -> str:
    """
    Generate SEO suggestions (slug, meta title, meta description) for given blog content.
    Returns HTML formatted suggestions.
    """
    prompt = f"""
    Based on the following blog content, suggest {num_options} SEO-optimized options.
    For each option, provide:
    - URL Slug (short, hyphen-separated, lowercase)
    - Meta Title (under 60 characters, compelling and keyword-rich)
    - Meta Description (under 160 characters, engaging with call-to-action)

    Blog content:
    {blog_content[:1000]}...

    Format your response as clean HTML using only these tags: <h4>, <p>, <strong>, <ul>, <li>, <code>
    Structure each option clearly with:
    <h4>Option [number]</h4>
    <ul>
        <li><strong>URL Slug:</strong> <code>your-slug-here</code></li>
        <li><strong>Meta Title:</strong> Your compelling title here</li>
        <li><strong>Meta Description:</strong> Your engaging description here</li>
    </ul>

    Do NOT include:
    - ``` code fences
    - <!DOCTYPE>, <html>, <head>, or <body> tags
    - Any explanatory text outside the structure
    - Line breaks between options
    """

    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=800,
            )
        )

        if not response.text:
            return "<p>No SEO suggestions could be generated.</p>"

        # Clean up the response
        seo_html = response.text.strip()
        
        # Remove any markdown code fences if they appear
        seo_html = seo_html.replace("```html", "").replace("```", "").strip()
        
        return seo_html

    except Exception as e:
        return f"<p><strong>Error generating SEO suggestions:</strong> {str(e)}</p>"