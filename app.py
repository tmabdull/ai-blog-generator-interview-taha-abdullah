from seo_fetcher import fetch_seo_data
from ai_generator import generate_blog_post

from flask import Flask, request, jsonify
import os

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import pytz

app = Flask(__name__)

# Main function to fetch SEO data and generate blog post
def generate_blog_post_for_keyword(keyword, save_to_file=False):
    seo_data = fetch_seo_data(keyword)
    
    if not seo_data or not seo_data[0]['is_data_found']:
        return None

    blog_content = generate_blog_post(keyword, seo_data[0])
    result = {
        "keyword": keyword,
        "seo_data": seo_data[0],
        "blog_post": blog_content
    }

    if save_to_file:
        filename = f"{POSTS_DIR}/blog_{keyword.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(blog_content)

    print(blog_content)
    return result

# ------------------------
# APScheduler configuration for running the job once per day
# ------------------------

# Constants
DAILY_KEYWORD = "wireless earbuds" # Predefined keyword for daily automation
POSTS_DIR = "./generated_posts" # Directory containing generated posts
os.makedirs(POSTS_DIR, exist_ok=True)

def scheduled_generate():
    generate_blog_post_for_keyword(DAILY_KEYWORD, save_to_file=True)

pacific_tz = pytz.timezone('America/Los_Angeles')
scheduler = BackgroundScheduler(timezone=pacific_tz)
scheduler.add_job(
    scheduled_generate, 
    trigger=IntervalTrigger(days=1, timezone=pacific_tz), 
    next_run_time=datetime.now(pacific_tz))
scheduler.start()

# ------------------------
# Flask App Routes
# ------------------------

@app.route('/generate', methods=['GET'])
def generate():
    """Generate a blog post for the given keyword."""
    try:
        keyword = request.args.get('keyword')
        if not keyword:
            return jsonify({"error": "Missing 'keyword' parameter"}), 400
        
        if not keyword.strip():
            return jsonify({"error": "Keyword cannot be empty"}), 400
            
        result = generate_blog_post_for_keyword(keyword)
        if not result:
            return jsonify({"error": "SEO data not found for keyword"}), 404
            
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": "Internal server error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=True)