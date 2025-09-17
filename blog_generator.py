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


        CONTENT GUIDELINES DETAILS:
        1. Content Topic Relevance and Audience

            Focus on custom AI solutions for SMBs: practical AI adoption strategies, case studies, efficiency gains, cost benefits, AI trends impacting SMBs.
            Include industry best practices and broader AI adoption themes without alienating non-SMB readers, use inclusive language.
            Ensure content answers common SMB questions, industry pain points, and emerging opportunities with AI.

        2. Tone of Voice & Style

            Write in the second person to engage your reader directly. Use “you” and “your” throughout the blog to create a personal and immersive experience for the reader. Writing in second person places your audience at the center of the content, speaking directly to their needs, challenges, and goals. This approach makes your message feel like a one-on-one conversation rather than a distant lecture.
            Emulate warm, empowering, and conversational tone that reflects a human writer’s empathy and authority.
            Use simple, jargon-free language without assuming deep technical knowledge to engage diverse SMB readers.
            Incorporate storytelling: real-world examples, business narratives, customer success tales.
            Vary sentence structure to avoid robotic repetition; inject subtle personality and emotional cues (e.g., excitement, curiosity).

        3. Content Structure & Flow

            Use engaging headings and subheadings for easy scanning.
            Start with a hook or relatable pain point; conclude with a clear takeaway or actionable insight.
            Include mixed content types: statistics, anecdotes, FAQs, quotes, and analogies.
            Provide incremental learning by addressing basic to moderate complexity concepts gradually.

        4. Humanizing AI Content Techniques

            Edit AI drafts by rewriting phrases and sentences to sound natural and spontaneous.
            Add personal touches: use metaphors, rhetorical questions, and conversational asides.
            Avoid keyword stuffing; prioritize reader value over SEO tricks.
            Inject subtle humor or light emotional resonance when appropriate.

        5. Fact-Checking & Credibility

        Verify all facts, stats, data points with reputable sources before publishing.
        Attribute sources and include links where possible.
        Demonstrate experience and expertise by referencing Consultadd’s 13+ years, 150+ engineers, and proven case studies contextually in blogs.

        6. SEO and Discoverability

        Align topics and subtopics with keyword research relevant to AI solutions for SMBs.
        Use meaningful, descriptive headings including primary keywords naturally.
        Incorporate internal links to Consultadd’s landing pages, service descriptions, and related posts to guide readers down the funnel.
        Write compelling meta descriptions and engaging first 100 words to improve search ranking.

        7. Keyword Usage Strategy

        Use Keywords Thoughtfully and Naturally for SEO and Readability

            Research and prioritize relevant keywords aligned with Consultadd’s focus on custom AI solutions for SMBs, such as "custom AI solutions for small business," "AI adoption SMB," "rapid AI deployment," etc.
            Incorporate primary and secondary keywords strategically in key blog locations:
            Titles and subheadings
            Opening paragraph and conclusion
            Naturally spread in the body content without overuse
            Avoid keyword stuffing which harms readability and search rankings. Instead, use keywords in a way that sounds seamless and conversational.
            Use variations and synonyms of your keywords to capture a wider range of search queries and enrich the content. For example, use both "custom AI" and "tailored AI solutions."
            Maintain the human tone by prioritizing meaningful, helpful sentences over forced keyword placement. If a keyword disrupts the flow, rephrase the sentence or choose a related term.
            Leverage internal linking with keyword-rich anchor text to relevant Consultadd pages, enhancing SEO and guiding readers deeper into the content ecosystem.
            Focus on user intent: keywords should align with what your audience is genuinely searching for and reflect answers to their key challenges or questions, ensuring the content remains practical and audience-focused.

        8. Ethical and Transparent AI Use

            Be transparent internally about using AI tools for drafting but ensure human review and editing preserves authenticity.
            Avoid presenting AI as expert or authority; always highlight human oversight and expertise.
            Focus on value-driven, original insights, not generic AI regurgitation.

        ---

        Examples for Drafting Blog Topics 
        "Why Tailored AI, Not Off-the-Shelf, Matters for SMBs"
        "Stepwise Guide to Adopting AI for Small Businesses"
        "How Custom AI Solutions Boost SMB Productivity: Real Use Cases"
        "Breaking Down AI Jargon: What SMBs Really Need to Know"
        "AI Deployment in Weeks: How SMBs Can Stay Agile & Competitive"
        "Customer Success Story: AI-Powered Growth for a Local Retailer"
        "The Future of SMBs with Custom AI: Trends & Predictions for 2025"

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