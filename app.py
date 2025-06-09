from flask import Flask, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import os

from seo_fetcher import fetch_seo_data
from ai_generator import generate_blog_post

app = Flask(__name__)

# Predefined keyword for daily automation
DAILY_KEYWORD = "wireless earbuds"

# Directory to save daily generated posts
OUTPUT_DIR = "./generated_posts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_blog_post_for_keyword(keyword, save_to_file=False):
    seo_data = fetch_seo_data(keyword)
    print("SEO Data:", seo_data[0]) # TODO: Rm
    if not seo_data or not seo_data[0]['is_data_found']:
        print("^ SEO Data not found")
        return None

    blog_content = generate_blog_post(keyword, seo_data[0])
    result = {
        "keyword": keyword,
        "seo_data": seo_data[0],
        "blog_post": blog_content
    }

    if save_to_file:
        filename = f"{OUTPUT_DIR}/blog_{keyword.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(blog_content)
    return result

@app.route('/get_blog_post', methods=['GET'])
def get_blog_post():
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({"error": "Missing 'keyword' parameter"}), 400
    result = generate_blog_post_for_keyword(keyword)
    if not result:
        return jsonify({"error": "SEO data not found for keyword"}), 404
    return jsonify(result)

# Using APScheduler to run the job once per day
def scheduled_generate():
    generate_blog_post_for_keyword(DAILY_KEYWORD, save_to_file=True)

scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_generate, 'interval', days=1, next_run_time=datetime.now())
scheduler.start()

if __name__ == '__main__':
    app.run(debug=True)