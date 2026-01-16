import time
import random
import os

import google.generativeai as genai
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

from functools import wraps

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('x-api-key')
        if not api_key or not api_key.startswith("ux_test_"):
             return jsonify({"error": "Unauthorized. Invalid or missing API Key."}), 401
        return f(*args, **kwargs)
    return decorated_function

def mock_scan(url):
    """
    Simulates a professional UX audit with balanced Pros/Cons analysis.
    """
    time.sleep(2.0) 
    
    # Core Metrics
    categories = {
        "performance": random.randint(75, 98),
        "accessibility": random.randint(65, 90),
        "best_practices": random.randint(80, 100),
        "seo": random.randint(70, 95)
    }
    overall_score = int(sum(categories.values()) / 4)
    
    # Executive Summary Data
    summary_text = "Analysis complete. Optimization opportunities detected in Performance and Accessibility."
    
    # Try using Gemini for real summary if key exists
    if os.getenv("GEMINI_API_KEY") and "YOUR_GEMINI" not in os.getenv("GEMINI_API_KEY"):
        try:
            # Use 'gemini-1.5-flash' which is the current standard. 
            # If 404s persist, check if API Key has access to this model in Google AI Studio.
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"Write a professional 2-sentence executive summary for a UX audit with these scores: Performance {categories['performance']}, Accessibility {categories['accessibility']}, Best Practices {categories['best_practices']}, SEO {categories['seo']}. Tone: Strategic and direct."
            response = model.generate_content(prompt)
            summary_text = response.text.strip()
        except Exception as e:
            print(f"AI Summary Error: {e}")
            summary_text = "Standard Audit Complete: Analysis indicates solid performance metrics, though accessibility compliance requires attention. Recommended focus on color contrast and ARIA labels."

    strengths = [
        {
            "category": "Performance",
            "title": "Excellent Logical Paint",
            "description": "The Largest Contentful Paint (LCP) is under 1.2s, ensuring an immediate visual response for users."
        },
        {
            "category": "Design",
            "title": "Clear Visual Hierarchy",
            "description": "Heading structures (H1-H3) are correctly implemented, facilitating easy scanning of content."
        },
        {
            "category": "Security",
            "title": "HTTPS Enforced",
            "description": "All traffic is securely encrypted using modern TLS 1.3 protocols."
        },
        {
            "category": "Mobile",
            "title": "Responsive Viewport",
            "description": "The layout adapts fluidly to mobile viewports without horizontal scrolling."
        }
    ]

    weaknesses = [
        {
            "severity": "High",
            "title": "Insufficient Color Contrast",
            "description": "Primary text elements fall below the WCAG AA standard ratio of 4.5:1, impacting readability for low-vision users.",
            "recommendation": "Darken the text color to #334155 (Slate-700) or higher."
        },
        {
            "severity": "Medium",
            "title": "Missing Non-Text Alternatives",
            "description": "Several key navigation images lack 'alt' attributes, rendering them invisible to screen readers.",
            "recommendation": "Audit all <img> tags and apply descriptive alt text."
        },
        {
            "severity": "Medium",
            "title": "Unoptimized JavaScript Chunks",
            "description": "Large JS bundles are blocking the main thread for over 250ms, causing input delay.",
            "recommendation": "Implement code-splitting and defer non-critical scripts."
        },
        {
            "severity": "Low",
            "title": "Tap Targets Too Small",
            "description": "Mobile menu links have a hit area smaller than 48x48px, leading to potential 'fat finger' errors.",
            "recommendation": "Increase padding on .nav-link elements."
        }
    ]
    
    # Select random subset for variety
    active_strengths = random.sample(strengths, k=3)
    active_weaknesses = random.sample(weaknesses, k=3)
    
    result = {
        "url": url,
        "timestamp": time.strftime("%Y-%m-%d %H:%M UTC"),
        "score": overall_score,
        "categories": categories,
        "summary": summary_text,
        "strengths": active_strengths,
        "weaknesses": active_weaknesses
    }
    
    return result

@app.route('/')
def index():
    clerk_key = os.getenv("CLERK_PUBLISHABLE_KEY", "pk_test_placeholder")
    return render_template('index.html', clerk_key=clerk_key)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    url = data.get('url')
    if not url: return jsonify({"error": "URL required"}), 400
    return jsonify(mock_scan(url))

@app.route('/fix', methods=['POST'])
def fix_issue():
    # If API Key is missing, fallback to mock
    if not os.getenv("GEMINI_API_KEY") or "YOUR_GEMINI" in os.getenv("GEMINI_API_KEY"):
        time.sleep(1.0)
        return jsonify({
            "status": "success",
            "fix": "/* Mock Fix (Gemini Key Missing) */\n.nav-link {\n  padding: 12px 24px;\n}"
        })

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Provide a CSS fix for: 'Insufficient Color Contrast. Primary text elements fall below WCAG AA standard ratio of 4.5:1. Recommendation: Darken text color'. Return ONLY the CSS code block.")
        fix_code = response.text.replace('```css', '').replace('```', '').strip()
        return jsonify({"status": "success", "fix": fix_code})
    except Exception as e:
        print(f"AI Fix Error: {e}")
        # Fallback if AI fails so the UI doesn't break
        return jsonify({"status": "success", "fix": "/* AI Unavailable - Using Fallback */\n.text-element {\n  color: #1a1a1a; /* Darkened for contrast */\n}"})

# --- Public API v1 ---

@app.route('/api-docs')
def api_docs():
    return render_template('api_docs.html')

@app.route('/api/v1/health', methods=['GET'])
def api_health():
    return jsonify({"status": "healthy", "service": "UX Tester API", "version": "1.0.0"})

@app.route('/api/v1/scan', methods=['POST'])
@require_api_key
def api_scan():
    data = request.json
    url = data.get('url')
    if not url: return jsonify({"error": "URL required"}), 400
    
    # Reuse the internal logic
    result = mock_scan(url)
    return jsonify(result)

@app.route('/api/v1/fix', methods=['POST'])
@require_api_key
def api_fix():
    # Reuse the internal logic key check for Gemini, strictly speaking we are already auth'd by x-api-key
    # safely calling internal fix logic if refactored, but for now we'll duplicate the logic wrapper 
    # or just call the internal route logic if we extracted it. 
    # For simplicity and safety in this MVP, let's just re-implement the call or redirect.
    # Actually, let's extract the fix logic or just copy it for now to avoid breaking existing route.
    
    return fix_issue() # fix_issue uses request.json, so it works if data structure matches



# --- Monitoring System ---
MONITORED_SITES = [] # In-memory store: {url, status, score, last_check, history}

def check_monitored_sites():
    """Background task to check all monitored sites."""
    global MONITORED_SITES
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Running Background Monitor Check...")
    
    for site in MONITORED_SITES:
        try:
            # Perform a scan (using our internal logic)
            # For efficiency in this demo, we mock it or use the lightweight mock
            result = mock_scan(site['url'])
            
            # Update Status
            new_score = result['score']
            old_score = site.get('score', 0)
            
            status = 'Healthy'
            if new_score < 50: status = 'Critical'
            elif new_score < 70: status = 'Warning'
            
            # Update Site Record
            site['score'] = new_score
            site['status'] = status
            site['last_check'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Simple Alert Logic (Console for now)
            if new_score < old_score - 10:
                 print(f"ALERT: Score dropped for {site['url']} from {old_score} to {new_score}")
                 
        except Exception as e:
            print(f"Monitor Error for {site['url']}: {e}")
            site['status'] = 'Error'

# Start Scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(func=check_monitored_sites, trigger="interval", seconds=30)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

@app.route('/api/monitor', methods=['GET'])
def get_monitors():
    return jsonify(MONITORED_SITES)

@app.route('/api/monitor/add', methods=['POST'])
def add_monitor():
    data = request.json
    url = data.get('url')
    if not url: return jsonify({'error': 'URL required'}), 400
    
    # Check duplicate
    if any(s['url'] == url for s in MONITORED_SITES):
        return jsonify({'error': 'Already monitored'}), 400
        
    MONITORED_SITES.append({
        'url': url,
        'score': 0,
        'status': 'Pending',
        'last_check': 'Never'
    })
    
    # Trigger immediate check (async in real world, sync here for demo feel)
    # threading.Thread(target=check_monitored_sites).start() 
    return jsonify({'success': True})

@app.route('/api/monitor/remove', methods=['POST'])
def remove_monitor():
    data = request.json
    url = data.get('url')
    global MONITORED_SITES
    MONITORED_SITES = [s for s in MONITORED_SITES if s['url'] != url]
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=True)
