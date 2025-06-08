from ai_generator import generate_blog_post
from seo_fetcher import fetch_seo_metrics

seo_data = fetch_seo_metrics("wireless earbuds")
blog_content = generate_blog_post("wireless earbuds", seo_data)
print(blog_content)
