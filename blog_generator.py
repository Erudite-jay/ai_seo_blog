import google.generativeai as genai
import time
from typing import Dict, Any
from dotenv import load_dotenv
import os
load_dotenv()


GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")

def configure_gemini(api_key: str):
    """Configure Gemini API with the provided key."""
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.0-flash')

def generate_blog_with_gemini(selected_result: Dict[Any, Any]) -> str:
    """Generate a comprehensive blog post using Gemini API based on selected research result."""

    try:
        # Configure Gemini
        model = configure_gemini(GEMINI_API_KEY)
        
        # Extract information from selected result
        url = selected_result.get('url', '')
        title = selected_result.get('title', '')
        description = selected_result.get('description', '')
        keyword = selected_result.get('keyword', '')
        
        
        # Create comprehensive prompt for blog generation
        prompt = f"""
        You are an expert content creator tasked with generating humanized, engaging blog content for Consultadd,
        a custom AI solutions company focused on tailored AI technologies.
        Your goal is to produce original, value-driven, and reader-focused blogs that feel like they are written by a thoughtful human expert, not an AI.

        RESEARCH DATA:
        - Target Keyword: {keyword}
        - Source URL: {url}
        - Page Title: {title}
        - Page Description: {description}

        BLOG POST REQUIREMENTS
        1. Purpose & User Intent: Make sure the blog fully satisfies the informational intent behind "{keyword}" and genuinely helps readers.

        CONTENT STRUCTURE:
        - Compelling Title (H1)
        - Introduction (2–3 engaging paragraphs)
        - Main Content with Multiple Sections (H2s and H3s)
        - Practical Tips/Examples
        - Conclusion with Call-to-Action
        - FAQ Section (optional but recommended)

        Page Quality:
        - Ensure originality — do not copy or spin the source material.
        Engagement:
        - Draft a long-form article (1500–2500 words).

        CONTENT GUIDELINES:
        Content Scope & Audience:
            1.Focus on topics relevant to SMBs exploring or adopting custom AI solutions, such as use cases, benefits, challenges, and best practices.
            2.Ensure the language and examples are inclusive and relatable even for readers outside SMBs, to avoid alienation.
            3.Topics should be research-backed, insightful, and aligned with Consultadd’s expertise.
        Tone & Style
            1.Write in the second person, directly addressing the reader as "you" and "your" to create a personal connection.
            2.Use a warm, empowering, conversational tone with simple, jargon-free language accessible to diverse readers.
            3.Incorporate storytelling elements such as customer anecdotes, metaphors, and subtle humor when appropriate.
            4.Vary sentence structure to keep the narrative fluid and engaging.
            5.Prioritize clarity and empathy, anticipating and answering reader questions and concerns.
        Keyword & SEO Guidelines
            1.Include Research Data naturally in titles, headings, and throughout the text without keyword stuffing.
            2.Use synonyms and related terms to enrich content and match varied search intents.
            3.Incorporate internal links to Consultadd’s(consultadd.com) key pages contextually.
            4.Write compelling meta titles and descriptions that summarize key blog points.
        Guardrails for Mentioning Consultadd
            1.When referring to Consultadd (consultadd.com), emphasize it as a trusted, experienced partner with over 13 years of industry presence, 150+ engineers, and 800+ satisfied clients without overt marketing.
            2.When mentioning other players, keep comparisons respectful and factual, without negative language.
            3.Focus on Consultadd’s unique value in tailoring AI solutions rapidly and accessibly, fitting the client’s pace and needs.
        Humanization Techniques
            1.Rewrite AI-generated drafts by replacing stiff or repetitive phrases with natural, idiomatic expressions.
            2.Add rhetorical questions to engage the reader (“Have you ever wondered…?”) and invite reflection.
            3.Use analogies and examples to clarify complex AI concepts simply.
            4.Include short personal asides or empathetic comments (“We understand that adopting AI can feel daunting…”).
            5.Avoid robotic or formulaic language and passive voice; prefer active, direct sentences.
            6.Edit to include slight variation in sentence length and transitions to improve flow.
        Structure & Formatting
            1.Open with a relatable hook addressing a common challenge or curiosity.
            2.Use clear headings/subheadings with keywords for easy navigation.
            3.End with actionable takeaways or thought-provoking insights.
            4.Embed real-world examples or hypothetical SMB scenarios for context.

        Please create a blog post that would rank well for "{keyword}" while providing trustworthy, comprehensive, and user-focused content. 
        Make sure to return:
            - The value of blog_content must contain valid HTML using <h1>, <h2>, <h3>, <p>, <ul>, <ol>, <blockquote>, <code>,<href> and <pre>.
            - Do NOT include ``` fences.
            - Do NOT include <!DOCTYPE>, <html>, <head>, or <body>.
            - Do NOT include Source URL or Domain in blog content.
        """
        
        print(f"Generating blog content for: {keyword}")
        print("This may take 30-60 seconds...")
        
        # Generate content using Gemini
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                top_p=0.8,
                top_k=40,
                max_output_tokens=4000,
            )
        )
        
        if response.text:
            print("Blog generated successfully!")
            return response.text
        else:
            raise Exception("No content generated by Gemini")
            
    except Exception as e:
        error_msg = f"Error generating blog with Gemini: {str(e)}"
        print(f"{error_msg}")