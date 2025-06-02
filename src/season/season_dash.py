import os
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
from .seasonstats import get_match_list_for_season, get_match_summary_list, get_team_stats, get_batter_stats, get_bowler_stats
from src.components.navbar import create_navbar, create_footer
from src.components.styles import TAB_STYLE, TAB_SELECTED_STYLE, PAGE_CONTAINER_STYLE
from src.components.season_vertical_timeline import create_vertical_timeline
from src.utils.data_loader import load_matches_data, load_deliveries_data
"""
User selects the season from dropdown. Once season is selected, below tabs are displayed, with matches tab the default.
3 tabs: Matches | Teams | Players

Matches : Will have a list of summary of all the matches in the season(get_match_summary_list). Each record will have a breif scorecard, winning team and margin & motm player name with score/bowler scorecard. Each record will link to the corresponding match scorecard.

Teams: List of all teams participating in the season. Some kind of graph(sanky) to show all the teams > 4 teams that moved to qualifier stage > 2 teams final > winner.
Points table. Each team will link to team page with detailed stats. 
Other graphs displaying the different metrics of each team using get_team_stats.
Choose a color scheme for the teams. 
# Points table calculation
Each team plays the other teams 2 times(h+a) in the league stage. Every team will play the same number of matches in the league stage.
If the number of actual league matches played is less than expected as above, those will be counted as cancelled due to rain and both teams will get 1 point.


Players: Select batter or bowler > selected player stats and graphs.
"""


import os


# Read CSV files with correct paths
deliveries = load_deliveries_data()
matches = load_matches_data()


# Normalize the season coloumn values in matches.
replacements = {
    '2007/08' : '2008',
    '2009/10' : '2010',
    '2020/21' : '2020'
}

matches['season'] = matches['season'].replace(replacements)
matches['season'] = pd.to_numeric(matches['season'])


# Generate and store list of seasons for dropdown ddisplay.
season_list = list(range(2008,2025))


# Initialize the dash app
app = dash.Dash(
    __name__,
    url_base_pathname='/season/',
    assets_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets'),
    external_stylesheets=['https://cdn.jsdelivr.net/npm/bootstrap@5.3.6/dist/css/bootstrap.min.css'],
    suppress_callback_exceptions=True
)


"""
In Dash, setting suppress_callback_exceptions=True allows the app to run without raising errors for callbacks associated with components that are not present in the initial layout. This is useful for dynamically generated components, but it's generally advised to avoid using it to ensure better error handling and app structure.
in this app, nav and footer are created by functions, and these elemtns are not prsent during intial app layout structure.
"""

#################################################################################### APP LAYOUT #############################################################################################

# App Layout
app.layout = html.Div(children=[

    html.Div([
        create_navbar()
    ], className='navbar'),

    html.Div([

        html.Div([
            html.H1('Season Statistics Dashboard'),
        ], className='row text-center my-4 mx-auto'),

        html.Div([
                    html.P([
                        "In the Season Dashboard, users can explore season-wide statistics by selecting specific IPL seasons. The overview section presents the points table and team rankings, while the teams tab breaks down team-wise performance including net run rates and head-to-head records. The matches section offers a chronological view of all matches in the selected season, with each match entry linking directly to detailed statistics and summaries."
                    ], style={
                        'margin':'0',
                        'line-height':'1.5'
                    })
                    ], className='row my-4 mx-auto', style={
                    'backgroundColor' :  'black',
                    'color':'white',
                    'padding': '20px'
                    }),
        
        html.Div([
            dcc.Dropdown(
            id = 'season-dropdown',
            options=[{'label': str(season), 'value': season} for season in season_list],
            value=None,
            clearable=False,
            placeholder='Select the IPL season'
            )
        ], className='row my-5 mx-auto text-center', style={
            'padding':'20px'
        }),
        
        

        # Div container for selection tabs
        html.Div(
            id = 'tabs-container',
            style= {'display':'none'},
            children=[
                dcc.Tabs(id='tabs', value='matches', children=[
                    dcc.Tab(label='Matches', value='matches', style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
                    dcc.Tab(label='Teams', value='teams', style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
                    dcc.Tab(label='Players', value='players', style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE)
                ])
            ], className='row my-5 mx-auto'
        ),

        # Tabs content container
        html.Div(
            id='tabs-content',
            # This will be populated based on the selected tab
            children=[],
            className='row my-5 mx-auto',
            style={'display': 'none'}  # Initially hidden
        ),

    ], className='container-fluid', style=PAGE_CONTAINER_STYLE),

    html.Div([
        create_footer()
    ], className='footer')

], className='wrapper')

                


#################################################################################### APP LAYOUT ENDS #############################################################################################


# Callback to make the tabs container & children tabs visible once season is selected
@app.callback(
    [Output('tabs-container', 'style'),
    Output('tabs-content', 'style')],
    [Input('season-dropdown', 'value'),
     Input('tabs', 'value')]
)


def update_tabs_visibility(selected_season, selected_tab):
    if not selected_season:
        return {'display': 'none'}, {'display': 'none'}
    
    # Show tabs container when season is selected
    tabs_container_style = {'display': 'block'}
    
    # Show content only when both season and tab are selected
    tabs_content_style = {'display': 'block' if selected_tab else 'none'}
    
    return tabs_container_style, tabs_content_style


# Add this callback after your existing callbacks
@app.callback(
    Output('tabs-content', 'children'),
    [Input('tabs', 'value'),
     Input('season-dropdown', 'value')]
)

def render_content(selected_tab, selected_season):
    if not selected_season:
        return []
    
    if selected_tab == 'matches':
        match_summary_list = get_match_summary_list(selected_season)
        return html.Div([

                html.Div([
                    html.H2(f'Matches in Season {selected_season}'),
                ], className='matches-header'),
                
                html.Div([
                    create_vertical_timeline(selected_season, match_summary_list)
                ], className='matches-list')
        ], className='row my-4 mx-auto matches-container')
    
    elif selected_tab == 'teams':
        return html.Div([html.H3("Teams content coming soon...")])
    
    elif selected_tab == 'players':
        return html.Div([html.H3("Players content coming soon...")])


# Each match in the matches tab will link to the corresponding match scorecard in match_dash.py


if __name__ == '__main__':
    app.run(debug=True)