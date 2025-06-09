from seo_fetcher import fetch_seo_data
from ai_generator import generate_blog_post

from flask import Flask, request, jsonify
import os

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import pytz

from flask_cors import CORS
import sys

# Vercel config
sys.path.append(os.path.dirname(__file__)) # Add the api directory to Python path
app = Flask(__name__)
CORS(app)

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

# Below routes are used to display blogs on the frontend
@app.route('/posts', methods=['GET'])
def get_posts():
    """Return a list of markdown filenames in generated_posts directory (for frontend)."""
    try:
        # Ensure the posts directory exists
        if not os.path.exists(POSTS_DIR):
            os.makedirs(POSTS_DIR, exist_ok=True)
            return jsonify({"files": []})
        
        # Get all .md files from the directory
        files = [f for f in os.listdir(POSTS_DIR) if f.endswith('.md')]
        files.sort(reverse=True)  # Most recent first
        
        return jsonify({"files": files})
        
    except Exception as e:
        return jsonify({"error": "Unable to access posts directory"}), 500

@app.route('/posts/<filename>', methods=['GET'])
def get_post_content(filename):
    """Return the raw markdown content for a given file (for frontend)."""
    try:
        # Basic security: ensure filename is safe
        if not filename.endswith('.md'):
            return jsonify({"error": "Invalid file type. Only .md files are allowed"}), 400
            
        if '..' in filename or '/' in filename or '\\' in filename:
            return jsonify({"error": "Invalid filename"}), 400
        
        file_path = os.path.join(POSTS_DIR, filename)
        
        # Check if file exists
        if not os.path.exists(file_path):
            return jsonify({"error": "File not found"}), 404
            
        # Read and return file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        return content, 200, {'Content-Type': 'text/plain; charset=utf-8'}
        
    except Exception as e:
        return jsonify({"error": "Internal server error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=True)