from flask import Flask, url_for, redirect, render_template
from src.home.home_dash import app as home_dash_app
from src.match.match_dash import app as match_dash_app
from src.season.season_dash import app as season_dash_app
from src.alltime.alltime_dash import app as alltime_dash_app


# Initialize Flask app
app = Flask(__name__,
            static_folder='src/assets',
            static_url_path='/assets')



# Root route redirects to home dash app
@app.route('/')
def index():
    # return the home dash application
    return home_dash_app.index()

@app.route('/match')
def match():
    # return the match dash application
    return match_dash_app.index()

@app.route('/season')
def season():
    # return the season dash application
    return season_dash_app.index()

@app.route('/alltime')
def alltime():
    # return the all-time dash application
    return alltime_dash_app.index()

# Register dash apps with Flask
# Initialize and register each Dash app with a unique name
home_dash_app.init_app(app)
match_dash_app.init_app(app)
season_dash_app.init_app(app)
alltime_dash_app.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)