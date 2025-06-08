import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def generate_blog_post(keyword: str, seo_metrics: dict) -> str:
    """
    Generates an SEO-optimized blog post using OpenAI's Responses API.

    Args:
        keyword: Target keyword for the blog post.
        seo_metrics: Dictionary containing SEO metrics.

    Returns:
        str: Generated blog post content with affiliate link placeholders.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"""
        Create a comprehensive blog post about {keyword} with these SEO considerations:
        - Search Volume: {seo_metrics.get('search_volume', 0)}
        - Keyword Difficulty: {seo_metrics.get('keyword_difficulty', 0)}/100
        - Avg CPC: ${seo_metrics.get('avg_cpc', 0):.2f}

        Structure:
        1. Engaging introduction
        2. 3-5 key points with subheadings
        3. Conclusion with call-to-action
        4. Insert 3 affiliate links using placeholders: {{AFF_LINK_1}}, {{AFF_LINK_2}}, {{AFF_LINK_3}}
        
        Tone: Professional yet approachable
        Word Count: 800-1000 words
        Include: Statistical data where appropriate
    """

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
            temperature=0.7,
            max_output_tokens=1300
        )

        return response.output_text
    
    except Exception as e:
        raise Exception(f"OpenAI Responses API error: {str(e)}")
