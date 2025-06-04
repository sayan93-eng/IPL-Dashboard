#!/usr/bin/env python3
"""
Railway-optimized IPL Dashboard
"""
import os
import sys
from flask import Flask, redirect, url_for, render_template_string
from src.home.home_dash import app as home_dash_app
from src.match.match_dash import app as match_dash_app
from src.season.season_dash import app as season_dash_app
from src.alltime.alltime_dash import app as alltime_dash_app

def check_data_files():
    """Check if required data files exist"""
    data_dir = os.path.join('data', 'ipl_complete_dataset_2008-2024')
    required_files = ['matches.csv', 'deliveries.csv']
    
    if not os.path.exists(data_dir):
        return False, f"Data directory not found: {data_dir}"
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(os.path.join(data_dir, file)):
            missing_files.append(file)
    
    if missing_files:
        return False, f"Missing data files: {', '.join(missing_files)}"
    
    return True, "All data files found"

def create_error_page(message):
    """Create an error page template"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>IPL Dashboard - Setup Required</title>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 50px; background: #f5f5f5; }}
            .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }}
            .error {{ color: #d32f2f; }}
            .solution {{ background: #e3f2fd; padding: 15px; border-left: 4px solid #2196f3; margin: 20px 0; }}
            .code {{ background: #f5f5f5; padding: 10px; font-family: monospace; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏏 IPL Dashboard</h1>
            <div class="error">
                <h2>⚠️ Setup Required</h2>
                <p><strong>Error:</strong> {message}</p>
            </div>
            
            <div class="solution">
                <h3>📥 Solution:</h3>
                <ol>
                    <li>Download the IPL dataset from <a href="https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020" target="_blank">Kaggle</a></li>
                    <li>Upload the CSV files to the data directory</li>
                    <li>Restart the application</li>
                </ol>
            </div>
            
            <p><strong>Note:</strong> This is a deployment on Railway. Data files need to be included in the repository.</p>
        </div>
    </body>
    </html>
    """

# Initialize Flask app
app = Flask(__name__,
            static_folder='src/assets',
            static_url_path='/assets')

# Get port from environment variable (Railway sets this)
port = int(os.environ.get('PORT', 5000))

# Check data files
data_check, message = check_data_files()

@app.route('/')
def index():
    """Root route"""
    if not data_check:
        return create_error_page(message)
    try:
        return home_dash_app.index()
    except Exception as e:
        return f"<h1>IPL Dashboard</h1><p>Error loading home: {str(e)}</p><p>Port: {port}</p>"

@app.route('/match')
def match():
    """Match analysis route"""
    if not data_check:
        return create_error_page(message)
    try:
        return match_dash_app.index()
    except Exception as e:
        return f"<h1>Match Analysis</h1><p>Error: {str(e)}</p>"

@app.route('/season')
def season():
    """Season statistics route"""
    if not data_check:
        return create_error_page(message)
    try:
        return season_dash_app.index()
    except Exception as e:
        return f"<h1>Season Statistics</h1><p>Error: {str(e)}</p>"

@app.route('/alltime')
def alltime():
    """All-time records route"""
    if not data_check:
        return create_error_page(message)
    try:
        return alltime_dash_app.index()
    except Exception as e:
        return f"<h1>All-time Records</h1><p>Error: {str(e)}</p>"

@app.route('/health')
def health_check():
    """Health check endpoint for Railway"""
    return {
        'status': 'healthy' if data_check else 'setup_required',
        'message': message,
        'data_files_found': data_check,
        'port': port,
        'environment': 'railway'
    }

# Initialize Dash apps only if data is available
if data_check:
    try:
        home_dash_app.init_app(app)
        match_dash_app.init_app(app)
        season_dash_app.init_app(app)
        alltime_dash_app.init_app(app)
        print("✅ All Dash applications initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing Dash apps: {e}")
        data_check = False

def main():
    """Main function to run the application"""
    print("🚂 IPL Dashboard starting on Railway...")
    print(f"🌐 Port: {port}")
    print(f"📊 Data check: {'✅ Passed' if data_check else '❌ Failed'}")
    
    if not data_check:
        print(f"⚠️  {message}")
    
    # Use 0.0.0.0 for Railway deployment
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == '__main__':
    main()