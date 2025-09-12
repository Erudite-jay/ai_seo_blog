from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime
import threading
import time
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from seo_research import main
from blog_generator import generate_blog_with_gemini

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this' 

# Global variables to track research progress
research_status = {
    'running': False,
    'progress': '',
    'completed': False,
    'results': []
}

@app.route('/')
def index():
    """Main page with keyword input."""
    return render_template('index.html')

@app.route('/start_research', methods=['POST'])
def start_research():
    """Start SEO research in background."""
    global research_status
    
    if research_status['running']:
        return jsonify({'error': 'Research already running'}), 400
    
    data = request.get_json()
    keyword = data.get('keyword', '').strip()
    num_results = int(data.get('num_results', 10))
    
    if not keyword:
        return jsonify({'error': 'Keyword is required'}), 400
    
    # Reset status
    research_status = {
        'running': True,
        'progress': 'Starting research...',
        'completed': False,
        'results': [],
        'keyword': keyword
    }
    
    # Start research in background thread
    thread = threading.Thread(
        target=run_research, 
        args=(keyword, num_results)
    )
    thread.daemon = True
    thread.start()
    
    return jsonify({'message': 'Research started', 'status': 'running'})

def run_research(keyword, num_results):
    """Run SEO research in background thread."""
    global research_status
    
    try:
        research_status['progress'] = f'Researching keyword: {keyword}...'
        results = main(keyword, num_results)
        
        research_status['results'] = results
        research_status['completed'] = True
        research_status['progress'] = f'Completed! Found {len(results)} results.'
        
        # Save results to session file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'results_{keyword.replace(" ", "_")}_{timestamp}.json'
        
        with open(f'static/results/{filename}', 'w') as f:
            json.dump({
                'keyword': keyword,
                'timestamp': timestamp,
                'results': results
            }, f, indent=2)
            
        research_status['filename'] = filename
        
    except Exception as e:
        research_status['progress'] = f'Error: {str(e)}'
        research_status['results'] = []
        research_status['completed'] = True
    
    research_status['running'] = False

@app.route('/research_status')
def get_research_status():
    """Get current research status."""
    return jsonify(research_status)

@app.route('/results')
def show_results():
    """Show research results page."""
    if not research_status.get('completed'):
        return render_template('waiting.html')
    
    return render_template('results.html', 
                         keyword=research_status.get('keyword', ''),
                         results=research_status.get('results', []))

@app.route('/generate_blog', methods=['POST'])
def generate_blog():
    """Generate blog using Gemini API."""
    try:
        data = request.get_json()
        selected_result = data.get('selected_result')

        
        if not selected_result:
            return jsonify({'error': 'Missing selected result or API key'}), 400
        
        # Generate blog using Gemini
        blog_content = generate_blog_with_gemini(selected_result)
        
        # Save generated blog
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'blog_{timestamp}.json'
        
        os.makedirs('static/blogs', exist_ok=True)
        with open(f'static/blogs/{filename}', 'w') as f:
            json.dump({
                'source_result': selected_result,
                'blog_content': blog_content,
                'generated_at': timestamp
            }, f, indent=2)
        
        return jsonify({
            'success': True,
            'blog_content': blog_content,
            'filename': filename
        })
        
    except Exception as e:
        return jsonify({'error': f'Blog generation failed: {str(e)}'}), 500

@app.route('/blog/<filename>')
def view_blog(filename):
    """View generated blog."""
    try:
        with open(f'static/blogs/{filename}', 'r') as f:
            blog_data = json.load(f)
        return render_template('blog.html', blog_data=blog_data)
    except FileNotFoundError:
        return "Blog not found", 404

if __name__ == '__main__':
    os.makedirs('static/results', exist_ok=True)
    os.makedirs('static/blogs', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    print("Starting SEO Research Web Interface...")
    print("Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5001)
