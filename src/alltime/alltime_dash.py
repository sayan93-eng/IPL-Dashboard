import os
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
from src.components.navbar import create_navbar, create_footer
from src.components.styles import TAB_STYLE, TAB_SELECTED_STYLE, PAGE_CONTAINER_STYLE
from .alltimestats import get_all_batters, get_all_bowlers, get_batter_vs_bowler_stats, get_bowler_career_stats, get_batter_career_stats, get_seasons_teams, get_fielding_stats, get_misc_stats


"""
TEAMS || PLAYERS
Stats for teams and players
Search bar where users can enter the name of the player or the team and get alltime stats for the player/team.
Will show all time records

Players
all-time highest individual score
all-time best individual bowling figures(most wicktes, if tie then lowest econ)
all-time-most runs
all-time-most wickets
Number of 100s
Number of 50s
Highest average
Highest strike rate
Lowest econ rate


Teams
Total matches played
Matches won
Matches lost
Win %
Home record
Away record
Best season(not necesarily the season winner)
Worst season
most runs scored(top 20)
most wickets taken(top 20) 

Player(Batter) vs (Bowler)
Two search bars side by side, user types in and selects from dropdown.
Number of Matches where the two faced each other
Deliveries
Runs
Outs
Batter Average, Strike Rate
Bowler Average, Econ,
Compare against their own avg across thier ipl careers and show if they overperform or underperform.
"""

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



all_batters = get_all_batters()
all_bowlers = get_all_bowlers()

app = dash.Dash(
    __name__,
    url_base_pathname='/alltime/',
    assets_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets'),
    external_stylesheets=['https://cdn.jsdelivr.net/npm/bootstrap@5.3.6/dist/css/bootstrap.min.css'],
)


app.layout = html.Div(children=[

    html.Div([
        create_navbar()
    ], className='navbar'),

    html.Div([
        html.Div([
            html.H1("Alltime Statistics Dashboard")   
            ], className='row text-center my-4 mx-auto'),

        
        html.Div([
                html.P([
                    "The All-time Records Dashboard features comprehensive historical IPL statistics through three main sections. The records tab allows users to search and view any player's complete career statistics. In the head-to-head section, users can select any batter-bowler combination to analyze their complete matchup history, with performance metrics highlighted using color-coded indicators. The teams section showcases franchise achievements and historical rankings throughout IPL history."
                ], style={
                    'margin':'0',
                    'line-height':'1.5'
                })
                ], className='row my-4 mx-auto', style={
                'backgroundColor' : 'black',
                'color':'white',
                'padding': '20px'
                }),
        

        html.Div(
            id='tabs-container',
            children=[
                dcc.Tabs(id='tabs', value='players-tabs', children=[
                    dcc.Tab(
                        label='Players', 
                        value='players', 
                        style=TAB_STYLE, 
                        selected_style=TAB_SELECTED_STYLE,
                        children=[
                            html.Div([
                                dcc.Tabs(
                                    id = 'players-tabs',
                                    value = 'players-records',
                                    style = {
                                        'width':'100%',
                                        'margin':'20px auto'
                                    },
                                    children=[
                                        dcc.Tab(label='Records', value='players-records', style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
                                        dcc.Tab(label='Head-to-Head', value='players-headtohead', style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE)
                                    ]
                                )
                            ])
                        ]
                    ),
                        
                    dcc.Tab(
                        label='Teams', 
                        value='teams', 
                        style=TAB_STYLE, 
                        selected_style=TAB_SELECTED_STYLE,
                        children=[
                            html.Div([
                                dcc.Tabs(
                                    id = 'teams-tabs',
                                    value = 'teams-records',
                                    style = {
                                        'width':'100%',
                                        'margin':'20px auto'
                                    },
                                    children=[
                                        dcc.Tab(label='Records', value='teams-records', style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
                                        dcc.Tab(label='Head-to-Head', value='teams-headtohead', style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE)
                                    ]
                                )
                            ])
                        ]
                    )
                ])
            ], className='row my-5 mx-auto'
        ),

        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='player-dropdown',
                    options=[{'label': player, 'value': player} 
                            for player in list(set(all_batters + all_bowlers))],  # Remove duplicates
                    placeholder='Select player',
                    value=None,
                    searchable=True,
                    clearable=True
                )
            ], className='col-md-6 mx-auto text-center')
        ], id='player-records-container', className='row my-5 mx-auto', style={'display': 'none'}),

        html.Div([

            # Batter search bar
            html.Div([
                dcc.Dropdown(
                    id='batter-dropdown',
                    options=[{'label': batter, 'value': batter} for batter in all_batters],
                    placeholder='Select batter',
                    #style={'width': '100%', 'backgroundColor': 'white', 'color': 'black'},
                    value=None,
                    searchable=True,
                    clearable=True
                )
            ], className='col-md-6 text-center', 
            #style={'width': '45%', 'display': 'inline-block', 'marginRight': '5%'}
            ),
            
            # Bowler search bar
            html.Div([
                dcc.Dropdown(
                    id='bowler-dropdown',
                    options=[{'label': bowler, 'value': bowler} for bowler in all_bowlers],
                    placeholder='Select bowler',
                    #style={'width': '100%', 'backgroundColor': 'white', 'color': 'black'},
                    value=None,
                    searchable=True,
                    clearable=True
                )
            ], className='col-md-6 text-center', 
            #style={'width': '45%', 'display': 'inline-block'}
            )

        ], id = 'dropdowns-container', className='row my-5 mx-auto', style={'display': 'none'}),

        html.Div(id='stats-output-container',
                 children = [],
                 className='row my-5 mx-auto',
                 style={'display':'none'}
                ),

    ], className='container-fluid' , style=PAGE_CONTAINER_STYLE),

    html.Div([
        create_footer()
    ], className='footer')

], className='wrapper')

########################################################## END OF LAYOUT #################################################

@app.callback(
    Output('player-records-container', 'style'),
    [Input('tabs', 'value'),
     Input('players-tabs', 'value')]
)
def toggle_player_dropdown(selected_tab, selected_player_tab):
    if selected_tab == 'players' and selected_player_tab == 'players-records':
        return {'display': 'flex',
                'padding': '20px'
                }
    return {'display': 'none'}


@app.callback(
    Output('stats-output-container', 'children'),
    Output('stats-output-container', 'style'),
    [Input('tabs', 'value'),
     Input('players-tabs', 'value'),
     Input('player-dropdown', 'value'),
     Input('batter-dropdown', 'value'),
     Input('bowler-dropdown', 'value')]
)

def update_stats(selected_tab, selected_player_tab, selected_player, selected_batter, selected_bowler):

    # For players records tab
    if selected_tab == 'players' and selected_player_tab == 'players-records':
        if not selected_player:
            return [], {'display': 'none'}

        batting_stats = get_batter_career_stats(selected_player) or {}
        bowling_stats = get_bowler_career_stats(selected_player) or {}

        # Default values for stats
        default_batting = {
            'matches': 'N/A',
            'runs': 'N/A', 
            'average': 0,
            'strike_rate': 0,
            'highest_score': 'N/A',
            '50s': 'N/A',
            '100s': 'N/A',
            '4s': 'N/A',
            '6s': 'N/A'
        }

        default_bowling = {
            'matches': 'N/A',
            'wickets': 'N/A',
            'overs': 'N/A',
            'dot_ball_percentage': 0,
            'best_bowling_figure': 'N/A',
            'average': 0,
            'economy_rate': 0,
            'strike_rate': 0,
            '3Ws': 'N/A',
            '5Ws': 'N/A'
        }

        # Merge with defaults
        batting_stats = {**default_batting, **batting_stats}
        bowling_stats = {**default_bowling, **bowling_stats}


        # Get fielding stats
        fielding_stats = get_fielding_stats(selected_player)

        # Get MOM stats
        pom_stats = get_misc_stats(selected_player)

        misc_stats = get_seasons_teams(selected_player)
        last_team_played = ''
        if len(misc_stats['teams']) > 1:
            last_team_played = misc_stats['teams'][-1]
        elif len(misc_stats['teams']) == 1:
            last_team_played = misc_stats['teams'][0]

        return html.Div([
            html.H2(
                f"IPL Career: {selected_player}", 
                   className='stats-header'
            ),

            # Batting Stats
            html.Div([
                html.H4("Batting"),
                html.Div([
                    html.Div([
                        html.H5("Innings", className='metric'),
                        html.H5("Runs", className='metric'),
                        html.H5("Average", className='metric'),
                        html.H5("Strike Rate", className='metric'),
                        html.H5("Highest Score", className='metric'),
                        html.H5("50s", className='metric'),
                        html.H5("100s", className='metric'),
                        html.H5("4s", className='metric'),
                        html.H5("6s", className='metric')
                    ], className='stats-metric'),

                    html.Div([
                        html.H5(f"{batting_stats['matches']}", className='value'),
                        html.H5(f"{batting_stats['runs']}", className='value'),
                        html.H5(f"{batting_stats['average']}", className='value'),
                        html.H5(f"{batting_stats['strike_rate']}", className='value'),
                        html.H5(f"{batting_stats['highest_score']}", className='value'),
                        html.H5(f"{batting_stats['50s']}", className='value'),
                        html.H5(f"{batting_stats['100s']}", className='value'),
                        html.H5(f"{batting_stats['4s']}", className='value'),
                        html.H5(f"{batting_stats['6s']}", className='value')
                    ], className='stats-value'),
                ], className='stats-box')
            ], className='batting-stats-container'),

            # Bowling Stats
            html.Div([
                html.H4("Bowling", className='mb-3'),
                html.Div([
                    html.Div([
                        html.H5("Innings", className='metric'),
                        html.H5("Wickets", className='metric'),
                        html.H5("Overs", className='metric'),
                        html.H5("Dot Ball %", className='metric'),
                        html.H5("Best Bowling Figure", className='metric'),
                        html.H5("Average", className='metric'),
                        html.H5("Economy", className='metric'),
                        html.H5("Strike Rate", className='metric'),
                        html.H5("3Ws", className='metric'),
                        html.H5("5Ws", className='metric')
                    ], className='stats-metric'),

                    html.Div([
                        html.H5(f"{bowling_stats['matches']}", className='value'),
                        html.H5(f"{bowling_stats['wickets']}", className='value'),
                        html.H5(f"{bowling_stats['overs']}", className='value'),
                        html.H5(f"{bowling_stats['dot_ball_percentage']}", className='value'),
                        html.H5(f"{bowling_stats['best_bowling_figure']}", className='value'),
                        html.H5(f"{bowling_stats['average']}", className='value'),
                        html.H5(f"{bowling_stats['economy_rate']}", className='value'),
                        html.H5(f"{bowling_stats['strike_rate']}", className='value'),
                        html.H5(f"{bowling_stats['3Ws']}", className='value'),
                        html.H5(f"{bowling_stats['5Ws']}", className='value'),
                    ], className='stats-value'),
                ], className='stats-box')
            ], className='bowling-stats-container'),

            html.Div([
                html.H4("Fielding", className='mb-3'),
                html.Div([
                    html.Div([
                        html.H5("Catches", className='metric'),
                        html.H5("Run Outs", className='metric'),
                        html.H5("Stumpings", className='metric')
                    ], className='stats-metric'),
                    html.Div([
                        html.H5(f"{fielding_stats['Catches']}", className='value'),
                        html.H5(f"{fielding_stats['Run Outs']}", className='value'),
                        html.H5(f"{fielding_stats['Stumped']}", className='value')
                    ], className='stats-value')
                ], className='stats-box')
            ], className='fielding-stats-container'),

            html.Div([
                html.H4("Misc", className='mb-3'),
                html.Div([
                    html.Div([
                        html.H5("Seasons", className='metric'),
                        html.H5("Teams", className='metric'),
                        html.H5("Player of Match Awards", className='metric'),
                        html.H5("Last Player of Match", className='metric')
                    ], className='stats-metric'),
                    html.Div([
                        html.H5(', '.join(map(str, misc_stats['seasons'])), className='value'),
                        html.H5(', '.join(map(str, misc_stats['teams'])), className='value'),
                        html.H5(f"{pom_stats['POM Awards']}", className='value'),
                        html.H5(f"{pom_stats['Last POM']}", className='value'),
                    ], className='stats-value')
                ], className='stats-box')
            ],className='misc-stats-container')

        ], className='stats-container', style={
            '--team-color': get_team_color(last_team_played)
        }), {'display': 'block'}
    

    # For players head to head tab
    if selected_tab == 'players' and selected_player_tab == 'players-headtohead':

        if not selected_batter or not selected_bowler:
            return [], {'display': 'none'}
        

        stats = get_batter_vs_bowler_stats(selected_batter, selected_bowler)
        batter_career = get_batter_career_stats(selected_batter) or {}
        bowler_career = get_bowler_career_stats(selected_bowler) or {}

        career_strike_rate = batter_career.get('strike_rate', 0)
        career_economy_rate = bowler_career.get('economy_rate', 0)

         # Calculate border colors based on performance
        strike_rate_border = 'rgb(0, 255, 0)' if stats['strikerate'] > career_strike_rate else 'rgb(255, 0, 0)'
        economy_rate_border = 'rgb(0, 255, 0)' if stats['econrate'] < career_economy_rate else 'rgb(255, 0, 0)'

        return html.Div([

            html.Div([
                html.H2(f"{selected_batter} vs {selected_bowler}")
                ], style={'textAlign': 'center', 
                          'color': 'white', 
                          'padding':'15px',
                          'marginTop':'0px',
                          'borderBottom':'2px solid #24d5ec',
                          'fontFamily':['Impact', 'Haettenschweiler', 'Arial Narrow Bold', 'sans-serif'],
                    }),
            
            html.Div([
                html.Div([
                    html.Div([
                        html.H5("Matches", className='metric'),
                        html.H5("Balls", className='metric'),
                        html.H5("Runs", className='metric'),
                        html.H5("Dots", className='metric'),
                        html.H5("Dismissals", className='metric'),
                        html.H5("4s", className='metric'),
                        html.H5("6s", className='metric'),
                        html.H5("Strike Rate", className='metric'),
                        html.H5("Economy Rate", className='metric')
                    ], className='metrics', style={'flex': 1,
                              'display':'flex',
                              'flexDirection':'column'  
                              }),

                    html.Div([
                        html.H5(f"{len(stats['matches'])}", className='value'),
                        html.H5(f"{stats['balls']}", className='value'),
                        html.H5(f"{stats['runs']}", className='value'),
                        html.H5(f"{stats['dots']}", className='value'),
                        html.H5(f"{stats['outs']}", className='value'),
                        html.H5(f"{stats['fours']}", className='value'),
                        html.H5(f"{stats['sixes']}", className='value'),
                        html.H5(f"{stats['strikerate']}", className='value', style={
                            'boxShadow': f'0 0 10px {strike_rate_border}',
                            'borderRadius': '4px'
                            
                        }),
                        html.H5(f"{stats['econrate']}", className='value', style={
                            'boxShadow': f'0 0 10px {economy_rate_border}',
                            'borderRadius': '4px'
                            
                        })
                    ], className='values', style={'flex': 1,
                              'display':'flex',
                              'flexDirection':'column'
                              }),
                ], className='box', style={ 
                    'display': 'flex',
                    'justifyContent': 'space-between',
                    'padding': '40px',
                    'borderRadius': '4px',
                    'margin':'20px 0',
                    'backgroundColor':'rgba(36, 213, 236, 0.1)'
                })
            
            ]),
        ], style={
            'padding':'20px',
            'margin':'20px 40px 20px 10px',
            'borderRadius':'8px',
            'backgroundColor':'black',
            'color':'white',
            'boxShadow':'0px -10px 10px #24d5ec, 0 10px 10px #24d5ec'


        }), {'display':'block'}


    # If no valid tab combination is selected
    return [], {'display': 'none'}


@app.callback(
    Output('dropdowns-container', 'style'),
    [Input('tabs', 'value'),
     Input('players-tabs', 'value')]
)
def toggle_dropdowns(selected_tab, selected_player_tab):
    if selected_tab == 'players' and selected_player_tab == 'players-headtohead':
        return {'display': 'flex',
                'padding':'20px',
                'margin':'0'
                }
    return {'display': 'none'}






if __name__ == '__main__':
    app.run(debug=True)