from urllib.parse import urlparse, parse_qs
import os
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
from .matchstats import get_match_list_for_season, get_batting_scorecard, get_partnership_data, get_final_score, get_bowling_scorecard, get_fall_of_wickets, get_data_for_bar_plot, get_data_for_line_plot, get_data_for_pie_chart, get_match_details
from src.components.navbar import create_navbar, create_footer
from src.components.styles import TAB_STYLE, TAB_SELECTED_STYLE, PAGE_CONTAINER_STYLE, FALL_OF_WICKET_CARD_STYLE, BAR_SECTION_STYLE, BATTER_BAR_STYLE, INFO_SECTION_STYLE, LIST_ITEM_STYLE
from src.utils.data_loader import load_matches_data, load_deliveries_data
"""
4 dcc tabs :  Scorecard, Innings progression and fall of wickets by bar plot, Innings progression and fall of wickets using line/worm plot, Runs Distribution pie chart. Each of these will have individual tabs to switch between the two innings, except for the worm plot which will have a single tab for both innings.

"""

################################ CONSTANTS ################################


############################### HELPER FUNCTIONS ##########################

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

def calculate_percentage(part, total):
    """Calculate percentage safely handling zero division"""
    try:
        return (part/total) * 100 if total > 0 else 0
    except ZeroDivisionError:
        return 0

"""
def get_color_based_on_runs(color, runs):

    # Extract RGB values from the base color string
    rgb = color.replace('rgb(', '').replace(')', '').split(',')
    r = int(rgb[0])
    g = int(rgb[1])
    b = int(rgb[2])


    # Calculate gradient factors
    if runs < 5:
        factor = 0.2  # Very light
    elif runs < 10:
        factor = 0.4  # Light
    elif runs < 15:
        factor = 0.6  # Medium
    elif runs < 20:
        factor = 0.8  # Dark
    else:
        factor = 1.0  # Full color
    
    # Calculate new RGB values based on the factor
    new_r = int(r * factor)
    new_g = int(g * factor)
    new_b = int(b * factor)

    # Return the new color in RGB format
    return f'rgb({new_r}, {new_g}, {new_b})'
"""


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
    url_base_pathname='/match/',
    assets_folder= os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets'),
    external_stylesheets=['https://cdn.jsdelivr.net/npm/bootstrap@5.3.6/dist/css/bootstrap.min.css'],
    suppress_callback_exceptions=True 
)



"""
dcc.Dropdown(
        id='season-dropdown',
        options=[{'label': str(season), 'value': season} for season in season_list],
        value=2023,
        clearable=False
    )
"""
#app.config.external_stylesheets = ['https://cdn.jsdelivr.net/npm/bootstrap@5.3.6/dist/css/bootstrap.min.css']


###############################################################################   LAYOUT   ############################################################################################


# Define the layout of the app
app.layout = html.Div([
            dcc.Location(id='url', refresh=True),

            html.Div(children=[

            html.Div([
                create_navbar()
            ], className='navbar'),

            html.Div([

                html.Div([
                    html.H1("Match Statistics Dashboard")   
                    ], className='row text-center my-4 mx-auto'
                ),


                html.Div([

                    html.P([
                        'The Match Dashboard enables detailed match analysis through an intuitive interface. Users can select specific matches using season and match dropdowns to access comprehensive scorecards displaying batting and bowling statistics along with partnership details. The ball-by-ball tab provides granular analysis of each over, including run progression and key events, while the wagon wheel visualization illustrates shot distribution and scoring patterns throughout the innings.'
                    ], style={
                        'margin':'0',
                        'line-height':'1.5'
                    })
                    ], className='row my-4 text-left mx-auto', style={
                    'backgroundColor' :'black',
                    'color':'white',
                    'padding': '20px',  # Single value for equal padding
                }),

                html.Div(
                    children=[
                        html.Div([
                            dcc.Dropdown(
                                id='season-dropdown',
                                placeholder = 'Select the IPL season',
                                options=[{'label': str(season), 'value': season} for season in season_list],
                                clearable=True
                            ),
                        ],className='col-md-6 text-center'),
                        html.Div([
                            dcc.Dropdown(
                                id='match-dropdown',
                                placeholder = 'Select the match',
                                options=[],
                                value=None,
                                clearable=True
                            )
                        ], className='col-md-6 text-center')
                    ], className='row my-5 mx-auto', style={ 
                        'padding':'20px',
                        'marginBottom':'0'
                    }
                ),
                
            
                

                
                # Div for tabs and their content
                # This will be hidden by default and shown when a match is selected
                # Row has to be immediate parents of coloumn
                html.Div(
                id='tabs-container',
                className= 'row my-0 mx-auto', style={
                        'display':'none',
                        'marginTop':'0'
                    },
                children=[
                    html.Div([  # Outer wrapper
                        dcc.Tabs(  # Main tabs component
                            id='tabs',
                            value='scorecard',
                            children=[
                                
                                dcc.Tab(  # Scorecard tab
                                    label='Scorecard',
                                    value='scorecard',
                                    style=TAB_STYLE,
                                    selected_style = TAB_SELECTED_STYLE,
                                    children=[
                                        html.Div([
                                            dcc.Tabs(  # Innings tabs for scorecard
                                                id='scorecard-tabs',
                                                value='inning1',
                                                style = {
                                                    'width':'100%',
                                                    'margin':'20px auto'
                                                },
                                                children=[
                                                    dcc.Tab(label='Inning 1', value='inning1', style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
                                                    dcc.Tab(label='Inning 2', value='inning2', style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE)
                                                ],
                                            )
                                        ]), 
                                    ],
                                ),
                                
                                
                                
                                
                                dcc.Tab(  # Bar Plot tab
                                    label='Innings Progression (Bar Plot)',
                                    value='bar-plot',
                                    style=TAB_STYLE,
                                    selected_style = TAB_SELECTED_STYLE, 
                                    children=[
                                        html.Div([
                                            dcc.Tabs(  # Innings tabs for bar plot
                                                id='bar-plot-tabs',
                                                value='inning1',
                                                style = {
                                                    'width':'100%',
                                                    'margin':'20px auto'
                                                },
                                                children=[
                                                    dcc.Tab(label='Inning 1', value='inning1', style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
                                                    dcc.Tab(label='Inning 2', value='inning2', style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE)
                                                ],
                                            )
                                        ])
                                        
                                    ],  
                                ),
                                

                                dcc.Tab(  # Line Plot tab
                                    label='Innings Progression (Line Plot)',
                                    value='line-plot',
                                    style=TAB_STYLE,
                                    selected_style= TAB_SELECTED_STYLE 
                                ),
                                
                                dcc.Tab(  # Pie Chart tab
                                    label='Runs Distribution (Pie Chart)',
                                    value='pie-chart',
                                    style=TAB_STYLE,
                                    selected_style = TAB_SELECTED_STYLE, 
                                    children=[
                                        html.Div([
                                            dcc.Tabs(  # Innings tabs for pie chart
                                                id='pie-chart-tabs',
                                                value='inning1',
                                                style = {
                                                    'width':'100%',
                                                    'margin':'20px auto'
                                                },
                                                children=[
                                                    dcc.Tab(label='Inning 1', value='inning1', style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE), 
                                                    dcc.Tab(label='Inning 2', value='inning2', style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE)
                                                ],
                                            )
                                        ])
                                    ],  
                                )# End of pie chart tab

                            ],
                        )
                    ]),

                    ],
                ),
                # End of tabs container

                # Content area for selected tab
                html.Div(id='tabs-content', children=[], className='row my-5 mx-auto', style={
                    'display':'none',  # Initially hidden
                    
                })

            ], className='container-fluid', 
            style= PAGE_CONTAINER_STYLE
            ),

            html.Div([
                create_footer()
            ], className='footer')

        ], className='wrapper')
    ])

##############################################################################    END OF LAYOUT   ############################################################################################

@app.callback(
    [Output('season-dropdown', 'value'),
     Output('match-dropdown', 'options'),
     Output('match-dropdown', 'value')],
    [Input('url', 'search')],
    prevent_initial_call=False  # Allow initial call
)

def update_dropdowns_from_url(search):
    if not search:
        return None, [], None
    
    # Parse query parameters
    parsed = parse_qs(search.replace('?', ''))
    season = int(parsed.get('season', [None])[0]) if parsed.get('season') else None
    match = int(parsed.get('match', [None])[0]) if parsed.get('match') else None
    
    if not season:
        return None, [], None
    
    # Get match options for the season
    matchlist = get_match_list_for_season(season)
    options = [{'label': match['label'], 'value': match['value']} for match in matchlist]
    
    return season, options, match


@app.callback(
    Output('url', 'search'),
    [Input('season-dropdown', 'value'),
     Input('match-dropdown', 'value')],
    prevent_initial_call=True
)
def update_url(selected_season, selected_match):
    if selected_season and selected_match:
        return f'?season={selected_season}&match={selected_match}'
    elif selected_season:
        return f'?season={selected_season}'
    return ''


# Callback to update the content of the tabs based on selected match
@app.callback(
    Output('tabs-content', 'children'),
    [Input('match-dropdown', 'value'),
     Input('tabs', 'value'),
     Input('scorecard-tabs', 'value'),
     Input('bar-plot-tabs', 'value'),
     Input('pie-chart-tabs', 'value')]
)



def update_tab_content(selected_match, selected_tab, scorecard_tab, bar_plot_tab, pie_chart_tab):
    if selected_match is None:
        return []

    # Get the match ID and inning ID
    match_id = selected_match
    match_deliveries = deliveries[deliveries['match_id'] == match_id]
    team_batting_first = match_deliveries[match_deliveries['inning'] == 1]['batting_team'].iloc[0]
    team_batting_second = match_deliveries[match_deliveries['inning'] == 2]['batting_team'].iloc[0]

    # Assign the color to the teams. This color will be used to represent the team in the bar and line plots.
    team_batting_first_color = get_team_color(team_batting_first)
    team_batting_second_color = get_team_color(team_batting_second)


    ################################################################### SCORECARD TABLE ################################################################
    # Add partnership stats using stacked bar chart.
    # Update the batting scorecard to show extras, and total score at the end of innings e.g 165/9(20) or 135/10(16.2)
    # Update the bowling scorecard to show the fall of wickets like so:
        # 5/1(0.4), 25/2(3.2), ...
    # Add a match details table at the bottom for misc stuff like date, venue, mom, umpires, etc
    if selected_tab == 'scorecard':
        inning_id = 1 if scorecard_tab == 'inning1' else 2
        batting_scorecard = get_batting_scorecard(match_id, inning_id)
        batting_scorecard_df = pd.DataFrame(batting_scorecard)
        bowling_scorecard = get_bowling_scorecard(match_id, inning_id)
        bowling_scorecard_df = pd.DataFrame(bowling_scorecard)
        batting_team = team_batting_first if inning_id == 1 else team_batting_second
        bowling_team = team_batting_second if inning_id == 1 else team_batting_first

        # Get final_score
        final_score = get_final_score(match_id, inning_id)

        # Get the fall of wickets
        fall_of_wickets = get_fall_of_wickets(match_id, inning_id)

        # Get match details table
        match_table = get_match_details(match_id)
             
        # Generate batting scorecard table
        # For batting scorecard
        fig_batting_scorecard = go.Figure(data=[go.Table(
            header=dict(
                values=list(batting_scorecard_df.columns),
                fill_color=team_batting_first_color if inning_id == 1 else team_batting_second_color,
                align='center',
                # Content vertical alignment
                font=dict(size=16, color='white'),
                height=30  # Set fixed header height
            ),
            cells=dict(
                values=[
                    batting_scorecard_df['Batsman Name'], 
                    batting_scorecard_df['Runs Scored'], 
                    batting_scorecard_df['Deliveries Faced'], 
                    batting_scorecard_df['4s'], 
                    batting_scorecard_df['6s'], 
                    batting_scorecard_df['Strike Rate'], 
                    batting_scorecard_df['Dismissal Type']
                ],
                fill_color= [[
                    'palegreen' if batting_scorecard_df['Dismissal Type'][i] == 'not out' else 'lavender'
                    for i in range(len(batting_scorecard_df))
                ]],
                align='center',
                font = dict(
                    size = 14,
                    color = 'grey'
                ),
                height=30  # Set fixed cell height
            )
        )], layout=go.Layout(
            margin=dict(l=0, r=0, t=0, b=0),
            height=len(batting_scorecard_df) * 30 + 30,  # Calculate total height based on rows
            autosize=True
        ))

        

        fig_bowling_scorecard = go.Figure(data=[go.Table(
            header=dict(
                values=list(bowling_scorecard_df.columns),
                fill_color=team_batting_first_color if inning_id == 2 else team_batting_second_color,
                align='center',
                font=dict(size=16, color='white'),  
                # Bold font

                height=30  # Set fixed header height
            ),
            cells=dict(
                values=[
                    bowling_scorecard_df['Bowler Name'], 
                    bowling_scorecard_df['Overs'], 
                    bowling_scorecard_df['Runs Conceded'], 
                    bowling_scorecard_df['Wickets'], 
                    bowling_scorecard_df['Economy Rate'], 
                    bowling_scorecard_df['Dots']
                ],
                fill_color='lavender',
                align='center',
                font = dict(
                    size = 14,
                    color = 'grey'
                ),
                height=30  # Set fixed cell height
            )
        )], layout=go.Layout(
            margin=dict(l=0, r=0, t=0, b=0),
            height=len(bowling_scorecard_df) * 30 + 30,  # Calculate total height based on rows
            autosize=True
        ))

        # Generate list of partnership data
        partnership_data = get_partnership_data(match_id, inning_id)
        max_partnership = max(p['batter1_runs'] + p['batter2_runs'] + p['extra_runs'] for p in partnership_data)

        return [
            html.Div(children=[
                html.Div([
                    html.H2(f"Batting: {batting_team} - {final_score}")
                ], className='batting-header',
                style={
                    '--batting-team-color': team_batting_first_color if inning_id == 1 else team_batting_second_color
                }),
                html.Div([
                    dcc.Graph(figure=fig_batting_scorecard)
                ], className = 'batting-scorecard',
                style={
                    '--batting-team-color': team_batting_first_color if inning_id == 1 else team_batting_second_color
                }),  
                # Partership container
                html.Div([
                    html.Ul([
                        html.Li([
                            # First row - Partnership bar
                            html.Div([
                                html.Div([
                                    # Batter 1 bar, only show if batter1_runs > 0
                                    *([html.Div(
                                        style={
                                            **BATTER_BAR_STYLE,
                                            'backgroundColor': '#1f77b4',
                                            'width': f"{calculate_percentage(p['batter1_runs'], p['batter1_runs'] + p['batter2_runs'] + p['extra_runs'])}%",
                                        }
                                    )] if p['batter1_runs'] > 0 else []),
                                    # Extras bar, only show if extras > 0
                                    *([html.Div(
                                        style={
                                            **BATTER_BAR_STYLE,
                                            'backgroundColor': '#2ca02c',
                                            'width': f"{calculate_percentage(p['extra_runs'], p['batter1_runs'] + p['batter2_runs'] + p['extra_runs'])}%",
                                        }
                                    )] if p['extra_runs'] > 0 else []),
                                    # Batter 2 bar
                                    *([html.Div(
                                        style={
                                            **BATTER_BAR_STYLE,
                                            'backgroundColor': '#ff7f0e',
                                            'width': f"{calculate_percentage(p['batter2_runs'], p['batter1_runs'] + p['batter2_runs'] + p['extra_runs'])}%",
                                        }
                                    )] if p['batter2_runs'] > 0 else [])
                                ], style={
                                    **BAR_SECTION_STYLE,
                                    'width': f"{calculate_percentage(p['batter1_runs'] + p['batter2_runs'] + p['extra_runs'], max_partnership)}%",
                                })
                            ], style={'width': '100%', 'backgroundColor': '#eee', 'borderRadius': '4px', 'padding': '10px'}),
            
                            # Second row - Partnership Total;
                            html.Div([
                                html.Div(f"Partnership {i+1} Total: {p['batter1_runs'] + p['batter2_runs'] + p['extra_runs']} runs", 
                                        style={'fontWeight': 'bold', 'textAlign': 'center', 'color':'white'})
                            ], style={'textAlign': 'center', 'marginTop': '10px'}),

                            # Third row - Partnership info
                            html.Div([
                                html.Div(f"{p['batter1']}: {p['batter1_runs']}", style={'color':'#1f77b4'}),
                                html.Div(f"Extras: {p['extra_runs']}" if p['extra_runs'] > 0 else "", style={'color': '#2ca02c'}),
                                html.Div(f"{p['batter2']}: {p['batter2_runs']}", style={'color':'#ff7f0e'})
                            ], style=INFO_SECTION_STYLE)
                        ], style=LIST_ITEM_STYLE)
                        for i, p in enumerate(partnership_data)
                    ], style={'padding': '0', 'margin': '0'})
                                ], className='partnership-container',
                                style={
                                    '--team-color': team_batting_first_color if inning_id == 1 else team_batting_second_color
                                })

            ], className='row my-4 batting-container',
                style={
                    '--batting-team-color': team_batting_first_color if inning_id == 1 else team_batting_second_color
                }),

            html.Div(children=[
                html.Div([
                    html.H2(f"Bowling: {bowling_team}")
                ], className='bowling-header',
                style= {
                    '--bowling-team-color': team_batting_first_color if inning_id == 2 else team_batting_second_color
                }),

                html.Div([
                    dcc.Graph(figure=fig_bowling_scorecard)
                ], className = 'bowling-scorecard',
                style = {
                    '--bowling-team-color': team_batting_first_color if inning_id == 2 else team_batting_second_color
                }),

                html.Div([
                # Card deck container
                    html.Div([
                        # Create a card for each fall of wicket
                        *[html.Div([  # Using list unpacking for multiple cards
                            html.Div([
                                html.Div([  # Card body Front
                                    html.Div([
                                        html.P(f"Wicket: {index + 1}"),
                                        html.P(f"Score: {wicket['score']}"),
                                        html.P(f"Over: {wicket['over']}")
                                    ], className='card-text')
                                ], className='card-body card-front',
                                style={
                                    'alignSelf':'center'
                                }),

                                html.Div([  # Card body Back
                                    html.Div([
                                        html.P(f"Batsman: {wicket['batter']}"),
                                        html.P(f"Bowler: {wicket['bowler']}"),
                                        html.P(f"Dismissal: {wicket['dismissal_kind']}")
                                    ], className='card-text')
                                ], className='card-body card-back',
                                style={
                                    'alignSelf':'center'
                                })
                            ], className='card-inner'),
                        ], className='card',
                        id = f'wicket-card-{index}', 
                        style={
                            **FALL_OF_WICKET_CARD_STYLE,
                            'transition': 'all 0.2s ease-in-out',
                            '--team-color': team_batting_first_color if inning_id == 2 else team_batting_second_color  # Add CSS variable
                            }) for index, wicket in enumerate(fall_of_wickets)]
                    ], className='card-deck',
                    style={
                        '--team-color': team_batting_first_color if inning_id == 2 else team_batting_second_color  # Add CSS variable
                    })
                ], className='card-deck-container',
                style={
                    '--team-color': team_batting_first_color if inning_id == 2 else team_batting_second_color  # Add CSS variable
                })
            ], className='row my-8 bowling-container', style={
                    '--bowling-team-color': team_batting_first_color if inning_id == 2 else team_batting_second_color
            })
        ]
    

    ################################################################ BAR PLOT ###############################################
    # Vertical bar plot where x = overs, y = runs in that over. Those overs which have wickets will have symbol/s(1 or more wickets) on top of that bar.
    # The bars are offset by 1 over. Will need to fix this. e.g runs and wickets from 0.0 to 0.6 will be added to the 1st bar, and xtick for the bar will be 1.

    # Replace ONLY the bar plot section (elif selected_tab == 'bar-plot':) in your callback with this:

    elif selected_tab == 'bar-plot':
        try:
            inning_id = 1 if bar_plot_tab == 'inning1' else 2
            batting_team = team_batting_first if inning_id == 1 else team_batting_second

            # Generate the data
            bar_data = get_data_for_bar_plot(match_id, inning_id)
            runs_in_over = bar_data['runs_in_over_list']
            wicket_overs = bar_data['wicket_overs_list']

            # Ensure we have data and create proper x-axis
            if not runs_in_over:
                return [html.Div("No bar plot data available", style={'color': 'white', 'padding': '20px'})]

            # Create x-axis based on actual data length, not fixed 1-20
            x_values = list(range(1, len(runs_in_over) + 1))

            # Generate the figure
            bar_plot_innings_by_over = go.Figure(
                data=go.Bar(
                    x=x_values,  # Use actual data length instead of fixed range
                    y=runs_in_over,
                    name=f"{batting_team}",
                    width=0.6,  # Increased width for better visibility
                    marker=dict(
                        color=team_batting_first_color if inning_id == 1 else team_batting_second_color,
                        line=dict(width=1, color='black')
                    )
                )
            )

            # Update layout
            bar_plot_innings_by_over.update_layout(
                margin=dict(l=50, r=50, t=50, b=50, pad=4),
                paper_bgcolor="LightSteelBlue",
                title=f"Innings Progression: {batting_team}",
                xaxis=dict(
                    title="Overs",
                    tickmode='linear',
                    tick0=1,
                    dtick=1,
                    range=[0.5, len(runs_in_over) + 0.5]  # Dynamic range based on data
                ),
                yaxis=dict(title="Runs"),
                showlegend=True
            )

            # Add wicket markers only if we have wicket data
            if wicket_overs:
                marker = dict(
                    color='red',
                    size=20,
                    symbol='circle',
                    line=dict(color='black', width=1)
                )

                # Get unique overs where wickets fell
                unique_wicket_overs = list(set(wicket_overs))

                # Add markers for each wicket
                for over in unique_wicket_overs:
                    # Ensure the over is within our data range
                    if over <= len(runs_in_over):
                        wickets_in_over = wicket_overs.count(over)
                        
                        for w in range(wickets_in_over):
                            base_offset = 2
                            spacing = 3
                            y_offset = base_offset + (w * spacing)
                            
                            bar_plot_innings_by_over.add_trace(
                                go.Scatter(
                                    x=[over],
                                    y=[runs_in_over[over-1] + y_offset],
                                    mode='markers',
                                    marker=marker,
                                    showlegend=False,
                                    hovertemplate="Wicket<extra></extra>"
                                )
                            )

            return [
                html.Div([
                    dcc.Graph(figure=bar_plot_innings_by_over)
                ], className='row my-4 bar-plot-container', style={
                    '--team-color': team_batting_first_color if inning_id == 1 else team_batting_second_color 
                }),
            ]
        
        except Exception as e:
            # More detailed error reporting
            import traceback
            error_details = traceback.format_exc()
            return [html.Div([
                html.H3("Bar Plot Error", style={'color': 'red'}),
                html.P(f"Error: {str(e)}", style={'color': 'white'}),
                html.Pre(error_details, style={'color': 'white', 'fontSize': '12px', 'overflow': 'auto'})
            ], style={'padding': '20px'})]
    

    ############################################################### LINE PLOT #######################################################
    # Add 1 each to the wicket_overs_list to cover edge cases where wicket/s have fallen in the 1st over(0.1 to 0.6). Current behavior is wickets fallen in 1st over are displayed on the y-axis.
    # Add more info to the wicket markers: batsman who is out, dismissal type and bowler and fielder involved.

    elif selected_tab == 'line-plot':

        # Generate data for both teams
        team_batting_first_total_runs_at_end_of_each_over_list = get_data_for_line_plot(match_id, 1)['total_runs_at_end_of_each_over_list']
        team_batting_second_total_runs_at_end_of_each_over_list = get_data_for_line_plot(match_id, 2)['total_runs_at_end_of_each_over_list']
        team_batting_first_wicket_overs_list = get_data_for_line_plot(match_id, 1)['wicket_overs_list']
        team_batting_second_wicket_overs_list = get_data_for_line_plot(match_id, 2)['wicket_overs_list']
        inning_data_1 = match_deliveries[match_deliveries['inning'] == 1]
        inning_data_1['over'] += 1
        inning_data_2 = match_deliveries[match_deliveries['inning'] == 2]
        inning_data_2['over'] += 1 
        team_batting_first_max_overs = int(inning_data_1['over'].max())
        team_batting_second_max_overs = int(inning_data_2['over'].max())

        team_batting_first_overs_list = [i for i in range(1, team_batting_first_max_overs + 1)]
        team_batting_second_overs_list = [i for i in range(1, team_batting_second_max_overs + 1)]

        x_axis_1 = [0] + team_batting_first_overs_list
        x_axis_2 = [0] + team_batting_second_overs_list
        y_axis_1 = [0] + team_batting_first_total_runs_at_end_of_each_over_list
        y_axis_2 = [0] + team_batting_second_total_runs_at_end_of_each_over_list

        line_plot_innings = go.Figure()

        # Add the first team's line plot
        line_plot_innings.add_trace(go.Scatter(
            x=x_axis_1,
            y=y_axis_1,
            mode='lines',
            name=team_batting_first,
            line=dict(color=team_batting_first_color),
            marker=dict(size=10)
        ))

        # Add the second team's line plot
        line_plot_innings.add_trace(go.Scatter(
            x=x_axis_2,
            y=y_axis_2,
            mode='lines',
            name=team_batting_second,
            line=dict(color=team_batting_second_color),
            marker=dict(size=10)
        ))

        # Update layout
        line_plot_innings.update_layout(
            #autosize = False,
            #width = 2000,
            #height = 500,
            margin = dict(
                l = 50,
                r = 50,
                t = 50,
                b = 50,
                pad = 4
            ),
            paper_bgcolor = "LightSteelBlue",
            xaxis=dict(
                title='Overs',
                range=[0, max(team_batting_first_max_overs, team_batting_second_max_overs) + 1],
                showgrid=True,
                zeroline=True,
                zerolinewidth=2,
                fixedrange = True,  # Prevents x-axis from moving
                dtick=1,
                tickmode='array',
                ticktext=[''] + [str(i) for i in range(1, max(team_batting_first_max_overs, team_batting_second_max_overs) + 1)],  # Empty string for 0
                tickvals=[i for i in range(0, max(team_batting_first_max_overs, team_batting_second_max_overs) + 1)]
            ),
            yaxis=dict(
                title='Runs',
                range=[0, max(max(team_batting_first_total_runs_at_end_of_each_over_list), max(team_batting_second_total_runs_at_end_of_each_over_list)) * 1.1],
                showgrid=True,
                zeroline=True,
                zerolinewidth=2,
                fixedrange = True,  # Prevents y-axis from moving
                dtick = 25,
                tickmode='array',
                ticktext=[''] + [str(i) for i in range(25, max(max(team_batting_first_total_runs_at_end_of_each_over_list), max(team_batting_second_total_runs_at_end_of_each_over_list)) + 60, 25)],  # Empty string for 0
                tickvals=[i for i in range(0, max(max(team_batting_first_total_runs_at_end_of_each_over_list), max(team_batting_second_total_runs_at_end_of_each_over_list)) + 60, 25)]
            ),
            title=f"Match Progress - {team_batting_first} vs {team_batting_second}",
            showlegend=True
            #hovermode='x unified'
        )


        # Create marker design
        marker = dict(
            color='red',
            size=10,
            symbol='circle',
            line=dict(
                color='black',
                width=1
            )
        )


        # Add wicket markers for team batting first.
        # Get unique overs where wickets fell
        team_batting_first_unique_wicket_overs = list(set(team_batting_first_wicket_overs_list))

        # Add markers for each wicket
        for over in team_batting_first_unique_wicket_overs:

            # Count how many wickets fell in this over
            wickets_in_over = team_batting_first_wicket_overs_list.count(over)

            # Add a marker for each wicket
            for w in range(wickets_in_over):
                base_offset = 1
                spacing = 3
                y_offset = base_offset + (w * spacing)  # Adjust spacing between markers
                line_plot_innings.add_trace(
                    go.Scatter(
                        x=[over],
                        y=[team_batting_first_total_runs_at_end_of_each_over_list[over-1] + y_offset],
                        mode='markers',
                        marker=marker,
                        #name=f'W{w+1}' if wickets_in_over > 1 else 'Wicket',
                        showlegend=False
                    )
                )
        
        # Add wicket markers for team batting second.
        # Get unique overs where wickets fell
        team_batting_second_unique_wicket_overs = list(set(team_batting_second_wicket_overs_list))

        # Add markers for each wicket
        for over in team_batting_second_unique_wicket_overs:

            # Count how many wickets fell in this over
            wickets_in_over = team_batting_second_wicket_overs_list.count(over)

            # Add a marker for each wicket
            for w in range(wickets_in_over):
                base_offset = 1
                spacing = 3
                y_offset = base_offset + (w * spacing)  # Adjust spacing between markers
                line_plot_innings.add_trace(
                    go.Scatter(
                        x=[over],
                        y=[team_batting_second_total_runs_at_end_of_each_over_list[over-1] + y_offset],
                        mode='markers',
                        marker=marker,
                        #name=f'W{w+1}' if wickets_in_over > 1 else 'Wicket',
                        showlegend=False
                    )
                )

        # Return the figure
        return [
            html.Div([
                dcc.Graph(figure=line_plot_innings)
            ], className='row my-4 line-plot-container', style={
                '--batting-team-color': team_batting_first_color,
                '--bowling-team-color': team_batting_second_color
            }),
        ]

    ################################################################# RUNS DISTRIBUTION PIE CHART ##################################################################
    elif selected_tab == 'pie-chart':
        # Placeholder for pie chart
        inning_id = 1 if pie_chart_tab == 'inning1' else 2
        batting_team = team_batting_first if inning_id == 1 else team_batting_second
        bowling_team = team_batting_second if inning_id == 1 else team_batting_first
        # Get the runs distribution data
        runs_distribution = get_data_for_pie_chart(match_id, inning_id)
        # Create the pie chart figure
        fig_pie_chart = go.Figure(
            data=[
                go.Pie(
                    labels=['1s', '2s', '3s', '4s', '6s', 'Extras'],
                    values=runs_distribution,
                    textinfo='value',
                    textposition='inside',
                    hovertemplate="%{label}: %{value} runs<br>%{percent}<extra></extra>",
                    marker=dict(colors=[
                        'rgb(255, 99, 132)',  # Red for 1s
                        'rgb(54, 162, 235)',  # Blue for 2s
                        'rgb(255, 206, 86)',  # Yellow for 3s
                        'rgb(75, 192, 192)',  # Green for 4s
                        'rgb(153, 102, 255)', # Purple for 6s
                        'rgb(255, 159, 64)'   # Orange for extras
                    ])
            )],
            layout=(
                go.Layout(
                    title = f"Runs Distribution: {batting_team}",
                    paper_bgcolor="LightSteelBlue",
                    uniformtext_minsize=12,
                    uniformtext_mode='hide',
                    margin = dict(
                    l = 50,
                    r = 50,
                    t = 50,
                    b = 50,
                    pad = 4
                    ),
                )
            )
        )
        

        return html.Div([
            dcc.Graph(figure=fig_pie_chart)
        ], className='row my-4 pie-chart-container', style={
            '--team-color': team_batting_first_color if inning_id == 1 else team_batting_second_color
        })

    else:
        return html.Div("Invalid Tab Selected")



# Callback to update the tabs visibility based on selected match
@app.callback(
    [Output('tabs-container', 'style'),
     Output('tabs-content', 'style')],
    [Input('season-dropdown', 'value'),
     Input('match-dropdown', 'value'),
     Input('tabs', 'value')]  # Add tabs value as input
)


def toggle_tabs_visibility(season, match, selected_tab):
    if not season or not match:
        # Hide both if no season/match selected
        return {'display': 'none'}, {'display': 'none'}
    
    # Show tabs container always when match is selected
    tabs_container_style = {
                        'display': 'block'
                    }
    
    # Show content only when a tab is selected
    tabs_content_style = {
        'display': 'block' if selected_tab else 'none',
        'padding': '20px'
    }
    
    return tabs_container_style, tabs_content_style




if __name__ == '__main__':
    app.run(debug=True)