from dash import html
from dash import dcc
from src.utils.teamcolor import get_team_color

def create_vertical_timeline(season, match_summary_list):
    return html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H3([
                        f"{match['date']}"
                    ], className='date-item-1', style={
                        
                    }),
                    html.H3([
                        (f"Match {index+1}: {match['team_1']} VS {match['team_2']}").upper()
                    ], className='date-item-2', style={
                        
                    }),
                    html.H3([
                        f"{match['venue']}"
                    ], className='date-item-3', style={
                        
                    })
                ], className='date'),
                html.Div([
                    html.Div([
                        html.H4(f"{match['team_batting_first']}", className='name'),
                        html.H4(f"{match['team_batting_first_score']}", className='score')
                    ], className='team-score-1', style={
                        '--team-color': get_team_color(match['team_batting_first'])
                    }),
                    html.Div([
                        html.H4(f"{match['team_batting_second']}", className='name'),
                        html.H4(f"{match['team_batting_second_score']}", className='score')
                    ],className='team-score-2', style={
                        '--team-color': get_team_color(match['team_batting_second'])
                    }),
                ], className = 'team-score'),
                html.Div([
                    html.H4([
                        f"{match['winner']} won by {match['result_margin']} {match['result']}"
                    ], className='text-item-1'),
                    dcc.Link(
                    "VIEW MATCH DETAILS",
                    href=f"/match?season={season}&match={match['id']}",
                    refresh = True,
                    className='text-item-link'),
                    html.H4([
                        f"Player of the Match: {match['pom']}"
                    ], className='text-item-2')
                ], className='txt'),
                
            ], className='event', style={
                '--team-color': get_team_color(match['winner'])
            })
        ]) for index, match in enumerate(match_summary_list) if 'id' in match
    ], className='vtl')