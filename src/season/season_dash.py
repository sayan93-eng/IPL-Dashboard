import os
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
from .seasonstats import get_match_list_for_season, get_match_summary_list, get_team_stats, get_batter_stats, get_bowler_stats, get_player_team_in_season
from src.components.navbar import create_navbar, create_footer
from src.components.styles import TAB_STYLE, TAB_SELECTED_STYLE, PAGE_CONTAINER_STYLE
from src.components.season_vertical_timeline import create_vertical_timeline
from src.utils.data_loader import load_matches_data, load_deliveries_data

############################################################# HELPER FUNCTIONS  ##############################################

def get_team_color(team):

    # Switch cases for all teams, name = team name, value = colour
    team_colors = {
        'Chennai Super Kings': 'rgb(255, 255, 0)',  # Yellow
        'Delhi Capitals': 'rgb(255, 0, 0)',  # Red
        'Delhi Daredevils': 'rgb(255, 0, 0)', # Red
        'Deccan Chargers' : 'rgb(255, 215, 0)',  # Gold
        'Gujarat Lions' : 'rgb(255, 145, 15)', # Orange
        'Gujarat Titans' : 'rgb(37, 73, 166)', # Dark Navy Blue
        'Kings XI Punjab' : 'rgb(223, 62, 62)', # Red shade
        'Kochi Tuskers Kerala' : 'rgb(255, 168, 0)', # shade of orange
        'Kolkata Knight Riders' : 'rgb(158, 0 ,255)', # Dark purple
        'Lucknow Super Giants' : 'rgb(80, 251, 249)', # Light blue-green
        'Mumbai Indians'  : 'rgb(0, 66, 255)', # Dark blue
        'Pune Warriors' : 'rgb(86, 207, 255)', # light blue
        'Punjab Kings' : 'rgb(223, 62, 62)', # Red shade,
        'Rajasthan Royals' : 'rgb(255, 106, 248)', # light pink
        'Rising Pune Supergiant' : 'rgb(177, 145, 191)', # Dark pink
        'Rising Pune Supergiants' : 'rgb(177, 145, 191)', # Dark pink',
        'Royal Challengers Bangalore' : 'rgb(197, 0, 0)', # Dark Maroon
        'Royal Challengers Bengaluru' : 'rgb(197, 0, 0)', # Dark Maroon
        'Sunrisers Hyderabad' : 'rgb(255, 123, 0)', # Dark orange
    }

    # Get the color for the team
    color = team_colors.get(team, 'rgb(0, 0, 0)')  # Default to black if team not found

    return color


# Read CSV files with correct paths
deliveries = load_deliveries_data()
matches = load_matches_data()

# Normalize the season column values in matches.
replacements = {
    '2007/08' : '2008',
    '2009/10' : '2010',
    '2020/21' : '2020'
}

matches['season'] = matches['season'].replace(replacements)
matches['season'] = pd.to_numeric(matches['season'])

# Generate and store list of seasons for dropdown display.
season_list = list(range(2008,2025))

# Initialize the dash app
app = dash.Dash(
    __name__,
    url_base_pathname='/season/',
    assets_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets'),
    external_stylesheets=['https://cdn.jsdelivr.net/npm/bootstrap@5.3.6/dist/css/bootstrap.min.css'],
    suppress_callback_exceptions=True
)

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

        # Teams dropdown container (only for Teams tab)
        html.Div(
            id='teams-dropdown-container',
            children=[
                html.Div([
                    dcc.Dropdown(
                        id='teams-dropdown',
                        options=[],  # Will be populated based on season
                        placeholder='Select a team to view detailed stats',
                        value=None,
                        clearable=True
                    )
                ], className='col-md-6 mx-auto')
            ],
            className='row my-3 mx-auto',
            style={'display': 'none', 'padding': '20px'}
        ),

        # Players dropdown container (only for Players tab)
        html.Div(
            id='players-dropdown-container',
            children=[
                html.Div([
                    dcc.Dropdown(
                        id='player-type-dropdown',
                        options=[
                            {'label': 'Batters', 'value': 'batters'},
                            {'label': 'Bowlers', 'value': 'bowlers'}
                        ],
                        placeholder='Select player type',
                        value=None,
                        clearable=False
                    )
                ], className='col-md-6 mx-auto'),
            ],
            className='row my-3 mx-auto',
            style={'display': 'none', 'padding': '20px'}
        ),

        # Tabs content container
        html.Div(
            id='tabs-content',
            children=[],
            className='row my-5 mx-auto',
            style={'display': 'none'}
        ),

    ], className='container-fluid', style=PAGE_CONTAINER_STYLE),

    html.Div([
        create_footer()
    ], className='footer')

], className='wrapper')

#################################################################################### CALLBACKS #############################################################################################

# Callback to make the tabs container visible once season is selected
@app.callback(
    Output('tabs-container', 'style'),
    [Input('season-dropdown', 'value')]
)
def update_tabs_visibility(selected_season):
    if not selected_season:
        return {'display': 'none'}
    return {'display': 'block'}

# Callback to show appropriate dropdowns based on selected tab
@app.callback(
    [Output('teams-dropdown-container', 'style'),
     Output('players-dropdown-container', 'style'),
     Output('teams-dropdown', 'options')],
    [Input('tabs', 'value'),
     Input('season-dropdown', 'value')]
)
def update_dropdown_containers(selected_tab, selected_season):
    teams_style = {'display': 'none'}
    players_style = {'display': 'none'}
    teams_options = []

    
    if selected_season:
        # Get teams for the selected season
        season_matches = matches[matches['season'] == selected_season]
        teams = sorted(list(set(season_matches['team1'].tolist() + season_matches['team2'].tolist())))
        teams_options = [{'label': team, 'value': team} for team in teams]
        
        if selected_tab == 'teams':
            teams_style = {'display': 'flex', 'padding': '20px'}
        elif selected_tab == 'players':
            players_style = {'display': 'flex', 'padding': '20px'}
    
    return teams_style, players_style, teams_options

# Callback to show/hide content and populate it based on selections
@app.callback(
    [Output('tabs-content', 'children'),
     Output('tabs-content', 'style')],
    [Input('tabs', 'value'),
     Input('season-dropdown', 'value'),
     Input('teams-dropdown', 'value'),
     Input('player-type-dropdown', 'value')]
)
def render_content(selected_tab, selected_season, selected_team, player_type):
    if not selected_season:
        return [], {'display': 'none'}
    
    content_style = {'display': 'block'}
    
    if selected_tab == 'matches':
        match_summary_list = get_match_summary_list(selected_season)
        content = html.Div([
            html.Div([
                html.H2(f'Matches in Season {selected_season}'),
            ], className='matches-header'),
            
            html.Div([
                create_vertical_timeline(selected_season, match_summary_list)
            ], className='matches-list')
        ], className='row my-4 mx-auto matches-container')
        
        return content, content_style
    
    elif selected_tab == 'teams':
        if selected_team:
            # Show detailed stats for the selected team
            team_stats = get_team_stats(selected_season, selected_team)
            teamcolor = get_team_color(selected_team)
            content = html.Div([
                html.H2(f'{selected_team} - Season {selected_season}', style={
                    '--team-color':teamcolor
                }),
                
                html.Div([
                    html.Div([
                        html.Table([
                            html.Tbody([
                                html.Tr([
                                    html.Td('Matches Played:', style={'color': 'white', 'padding': '10px', 'fontWeight': 'bold'}),
                                    html.Td(f"{team_stats['Matches Played']}", style={'color': 'white', 'padding': '10px'})
                                ]),
                                html.Tr([
                                    html.Td('Matches Won:', style={'color': 'white', 'padding': '10px', 'fontWeight': 'bold'}),
                                    html.Td(f"{team_stats['Matches Won']}", style={'color': 'white', 'padding': '10px'})
                                ]),
                                html.Tr([
                                    html.Td('Winning Percentage:', style={'color': 'white', 'padding': '10px', 'fontWeight': 'bold'}),
                                    html.Td(f"{team_stats['Winning Percentage']}%", style={'color': 'white', 'padding': '10px'})
                                ]),
                                html.Tr([
                                    html.Td('Highest Score (Batting First):', style={'color': 'white', 'padding': '10px', 'fontWeight': 'bold'}),
                                    html.Td(f"{team_stats['Highest score batting first']}", style={'color': 'white', 'padding': '10px'})
                                ]),
                                html.Tr([
                                    html.Td('Highest Score (Batting Second):', style={'color': 'white', 'padding': '10px', 'fontWeight': 'bold'}),
                                    html.Td(f"{team_stats['Highest score batting second']}", style={'color': 'white', 'padding': '10px'})
                                ])
                            ])
                        ], style={'width': '100%'})
                    ], className='col-md-6'),
                    
                    html.Div([
                        html.H4('Recent Form', style={'color': '#24d5ec', 'marginBottom': '20px'}),
                        html.Div([
                            html.Span(result, style={
                                'display': 'inline-block',
                                'width': '30px',
                                'height': '30px',
                                'borderRadius': '50%',
                                'backgroundColor': '#4CAF50' if result == 'W' else '#f44336',
                                'color': 'white',
                                'textAlign': 'center',
                                'lineHeight': '30px',
                                'margin': '5px',
                                'fontWeight': 'bold'
                            }) for result in team_stats['Win Loss Form'][-10:]  # Show last 10 matches
                        ])
                    ], className='col-md-6')
                ], className='row')
            ], className='team-container', style={
                '--team-color': teamcolor
            })
            
            return content, content_style
        """
        else:
            # Show all teams in the season
            season_matches = matches[matches['season'] == selected_season]
            teams = sorted(list(set(season_matches['team1'].tolist() + season_matches['team2'].tolist())))
            
            content = html.Div([
                html.H2(f'Teams in Season {selected_season}', 
                       style={'color': 'white', 'textAlign': 'center', 'marginBottom': '30px'}),
                html.P('Select a team from the dropdown above to view detailed statistics.', 
                       style={'color': '#24d5ec', 'textAlign': 'center', 'marginBottom': '30px'}),
                html.Div([
                    html.Div([
                        html.H4(team, style={'color': 'white', 'textAlign': 'center', 'padding': '20px'})
                    ], className='col-md-3 my-2', style={
                        'backgroundColor': 'rgba(36, 213, 236, 0.1)',
                        'borderRadius': '8px',
                        'margin': '10px',
                        'border': '1px solid #24d5ec'
                    }) for team in teams
                ], className='row justify-content-center')
            ], style={'padding': '20px'})
            
            return content, content_style
        """
        
    
    elif selected_tab == 'players':
        """
        if not player_type:
            content = html.Div([
                html.H3("Please select a player type from the dropdown above to view statistics", 
                       style={'color': 'white', 'textAlign': 'center'})
            ])
            return content, content_style
        """
        
        
        if player_type == 'batters':
            batter_stats = get_batter_stats(selected_season)
            
            # Create a table of top batters
            sorted_batters = sorted(batter_stats, key=lambda x: x['total_runs'], reverse=True)[:20]
            


            content = html.Div([
                html.H2(f'Top Batters - Season {selected_season}'),
                html.Div([
                    html.Table([
                        html.Thead([
                            html.Tr([
                                html.Th('Rank', style={'color': 'white', 'padding': '10px', 'borderBottom': '2px solid #24d5ec'}),
                                html.Th('Batter', style={'color': 'white', 'padding': '10px', 'borderBottom': '2px solid #24d5ec'}),
                                html.Th('Innings', style={'color': 'white', 'padding': '10px', 'borderBottom': '2px solid #24d5ec'}),
                                html.Th('Runs', style={'color': 'white', 'padding': '10px', 'borderBottom': '2px solid #24d5ec'}),
                                html.Th('Average', style={'color': 'white', 'padding': '10px', 'borderBottom': '2px solid #24d5ec'}),
                                html.Th('Strike Rate', style={'color': 'white', 'padding': '10px', 'borderBottom': '2px solid #24d5ec'}),
                                html.Th('50s', style={'color': 'white', 'padding': '10px', 'borderBottom': '2px solid #24d5ec'}),
                                html.Th('100s', style={'color': 'white', 'padding': '10px', 'borderBottom': '2px solid #24d5ec'})
                            ])
                        ]),
                        html.Tbody([
                            html.Tr([
                                html.Td(f"{i+1}", style={'color': 'white', 'padding': '8px', 'borderBottom': '1px solid #333'}),
                                html.Td(f"{batter['name'].iloc[0] if hasattr(batter['name'], 'iloc') else batter['name']} ({get_player_team_in_season(batter['name'].iloc[0], selected_season)})",
                                        className='batter-name', 
                                        style={
                                            '--team-color':get_team_color(get_player_team_in_season(batter['name'].iloc[0] if hasattr(batter['name'], 'iloc') else batter['name'], selected_season)),
                                        }),
                                html.Td(f"{batter['number_of_innings']}", style={'color': 'white', 'padding': '8px', 'borderBottom': '1px solid #333'}),
                                html.Td(f"{batter['total_runs']}", style={'color': 'white', 'padding': '8px', 'borderBottom': '1px solid #333'}),
                                html.Td(f"{batter['batting_average']:.2f}", style={'color': 'white', 'padding': '8px', 'borderBottom': '1px solid #333'}),
                                html.Td(f"{batter['strike_rate']:.2f}", style={'color': 'white', 'padding': '8px', 'borderBottom': '1px solid #333'}),
                                html.Td(f"{batter['number_of_50s']}", style={'color': 'white', 'padding': '8px', 'borderBottom': '1px solid #333'}),
                                html.Td(f"{batter['number_of_100s']}", style={'color': 'white', 'padding': '8px', 'borderBottom': '1px solid #333'})
                            ]) for i, batter in enumerate(sorted_batters)
                        ])
                    ], style={'width': '100%', 'borderCollapse': 'collapse'})
                ], style={'backgroundColor': 'black', 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0px -10px 5px #24d5ec, 0 1px 2px #24d5ec','marginTop':'50px'})
            ], className='batters-container')
            
            return content, content_style
        
        elif player_type == 'bowlers':
            bowler_stats = get_bowler_stats(selected_season)
            
            # Create a table of top bowlers
            sorted_bowlers = sorted(bowler_stats, key=lambda x: x['wickets_taken'], reverse=True)[:20]
            
            content = html.Div([
                html.H2(f'Top Bowlers - Season {selected_season}'),
                html.Div([
                    html.Table([
                        html.Thead([
                            html.Tr([
                                html.Th('Rank', style={'color': 'white', 'padding': '10px', 'borderBottom': '2px solid #24d5ec'}),
                                html.Th('Player', style={'color': 'white', 'padding': '10px', 'borderBottom': '2px solid #24d5ec'}),
                                html.Th('Innings', style={'color': 'white', 'padding': '10px', 'borderBottom': '2px solid #24d5ec'}),
                                html.Th('Wickets', style={'color': 'white', 'padding': '10px', 'borderBottom': '2px solid #24d5ec'}),
                                html.Th('Overs', style={'color': 'white', 'padding': '10px', 'borderBottom': '2px solid #24d5ec'}),
                                html.Th('Average', style={'color': 'white', 'padding': '10px', 'borderBottom': '2px solid #24d5ec'}),
                                html.Th('Economy', style={'color': 'white', 'padding': '10px', 'borderBottom': '2px solid #24d5ec'}),
                                html.Th('Strike Rate', style={'color': 'white', 'padding': '10px', 'borderBottom': '2px solid #24d5ec'})
                            ])
                        ]),
                        html.Tbody([
                            html.Tr([
                                html.Td(f"{i+1}", style={'color': 'white', 'padding': '8px', 'borderBottom': '1px solid #333'}),
                                html.Td(f"{bowler['name'].iloc[0] if hasattr(bowler['name'], 'iloc') else bowler['name']} ({get_player_team_in_season(bowler['name'].iloc[0], selected_season)})",
                                        className='bowler-name', 
                                        style={ 
                                            '--team-color':get_team_color(get_player_team_in_season(bowler['name'].iloc[0] if hasattr(bowler['name'], 'iloc') else bowler['name'], selected_season)),
                                        }),
                                html.Td(f"{bowler['number_of_innings']}", style={'color': 'white', 'padding': '8px', 'borderBottom': '1px solid #333'}),
                                html.Td(f"{bowler['wickets_taken']}", style={'color': 'white', 'padding': '8px', 'borderBottom': '1px solid #333'}),
                                html.Td(f"{bowler['overs']:.1f}", style={'color': 'white', 'padding': '8px', 'borderBottom': '1px solid #333'}),
                                html.Td(f"{bowler['average']:.2f}", style={'color': 'white', 'padding': '8px', 'borderBottom': '1px solid #333'}),
                                html.Td(f"{bowler['economy_rate']:.2f}", style={'color': 'white', 'padding': '8px', 'borderBottom': '1px solid #333'}),
                                html.Td(f"{bowler['strike_rate']:.2f}", style={'color': 'white', 'padding': '8px', 'borderBottom': '1px solid #333'})
                            ]) for i, bowler in enumerate(sorted_bowlers)
                        ])
                    ], style={'width': '100%', 'borderCollapse': 'collapse'})
                ], style={'backgroundColor': 'black', 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0px -10px 5px #24d5ec, 0 1px 2px #24d5ec', 'marginTop':'50px'})
            ], className='bowlers-container')
            
            return content, content_style

    return [], {'display': 'none'}

if __name__ == '__main__':
    app.run(debug=True)