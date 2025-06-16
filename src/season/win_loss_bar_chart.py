import plotly.graph_objects as go
import pandas as pd


# Define file paths for source files.
csv_file_path_deliveries = 'C:/Sayan/App-Statistical Probability Model/Sports/IPL/venv-mlmodel/ipl_complete_dataset_2008-2024/deliveries.csv'
csv_file_path_matches = 'C:/Sayan/App-Statistical Probability Model/Sports/IPL/venv-mlmodel/ipl_complete_dataset_2008-2024/matches.csv'

# Read the csv files into dataframes
deliveries = pd.read_csv(csv_file_path_deliveries)
matches = pd.read_csv(csv_file_path_matches)

replacements = {
    '2007/08' : '2008',
    '2009/10' : '2010',
    '2020/21' : '2020'
}

matches['season'] = matches['season'].replace(replacements)
matches['season'] = pd.to_numeric(matches['season'])


def create_sequential_team_charts(team_name, season_year, matches_df):
    """
    Create win/loss charts using sequential match numbers
    """
    # Filter data for the season and team
    season_data = matches_df[matches_df['season'] == season_year]
    team_data = season_data[
        (season_data['team1'] == team_name) | 
        (season_data['team2'] == team_name)
    ].copy()
    
    # Sort by date to maintain chronological order
    team_data = team_data.sort_values('date')
    
    # Add sequential match numbers
    team_data = team_data.reset_index(drop=True)
    team_data['match_number'] = range(1, len(team_data) + 1)
    
    # Function to get opponent team name
    def get_opponent(row, team):
        return row['team2'] if row['team1'] == team else row['team1']
    
    # Create labels with match number and opponent
    team_data['opponent'] = team_data.apply(lambda row: get_opponent(row, team_name), axis=1)
    team_data['match_label'] = team_data.apply(
        lambda row: f"M{row['match_number']}\nvs {row['opponent']}", axis=1
    )
    
    # Separate by result type
    margin_by_runs = team_data[team_data['result'] == 'runs'].copy()
    margin_by_wickets = team_data[team_data['result'] == 'wickets'].copy()
    
    # CHART 1: Wins and Losses by Runs
    fig_by_runs = go.Figure()
    
    if not margin_by_runs.empty:
        # Create colors and values for each match in chronological order
        colors = []
        y_values = []
        text_values = []
        
        for _, row in margin_by_runs.iterrows():
            if row['winner'] == team_name:
                colors.append('green')
                y_values.append(row['result_margin'])
                text_values.append(f"+{row['result_margin']}")
            else:
                colors.append('crimson')
                y_values.append(-row['result_margin'])  # Negative for losses
                text_values.append(f"-{row['result_margin']}")
        
        # Single trace to maintain chronological order
        fig_by_runs.add_trace(go.Bar(
            x=margin_by_runs['match_label'],
            y=y_values,
            marker_color=colors,
            text=text_values,
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Result: %{text} runs<extra></extra>',
            showlegend=False
        ))

        # Add invisible traces for legend
        fig_by_runs.add_trace(go.Bar(
            x=[None], y=[None],
            marker_color='green',
            name='Wins by Runs',
            showlegend=True
        ))

        fig_by_runs.add_trace(go.Bar(
            x=[None], y=[None],
            marker_color='crimson',
            name='Loss by Runs',
            showlegend=True
        ))
    
    fig_by_runs.update_layout(
        title=f'{team_name} - Season {season_year} Win/Loss (By Runs)',
        xaxis_title='Matches',
        yaxis_title='Victory Margin (Runs)',
        template='plotly_white',
        height=600,
        #width=max(1200, len(margin_by_runs) * 100),
        margin=dict(l=20, r=20, t=80, b=120),
        xaxis=dict(tickangle=45),
        showlegend=True,
        paper_bgcolor="LightSteelBlue"
    )
    
    # Add horizontal line at y=0
    fig_by_runs.add_hline(y=0, line_dash="solid", line_color="black", line_width=2)
    

    # CHART 2: Wins and Losses by Wickets
    fig_by_wickets = go.Figure()
    
    if not margin_by_wickets.empty:
        # Create colors and values for each match in chronological order
        colors = []
        y_values = []
        text_values = []
        
        for _, row in margin_by_wickets.iterrows():
            if row['winner'] == team_name:
                colors.append('green')
                y_values.append(row['result_margin'])
                text_values.append(f"+{row['result_margin']}")
            else:
                colors.append('crimson')
                y_values.append(-row['result_margin'])  # Negative for losses
                text_values.append(f"-{row['result_margin']}")
        
        fig_by_wickets.add_trace(go.Bar(
            x=margin_by_wickets['match_label'],
            y=y_values,
            marker_color=colors,
            text=text_values,
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Result: %{text} wickets<extra></extra>',
            showlegend=False
        ))

        # Add invisible traces for legend
        fig_by_wickets.add_trace(go.Bar(
            x=[None], y=[None],
            marker_color='green',
            name='Wins by Wickets',
            showlegend=True
        ))

        fig_by_wickets.add_trace(go.Bar(
            x=[None], y=[None],
            marker_color='crimson',
            name='Loss by Wickets',
            showlegend=True
        ))
    
    fig_by_wickets.update_layout(
        title=f'{team_name} - Season {season_year} Win/Loss (By Wickets)',
        xaxis_title='Matches',
        yaxis_title='Victory Margin (Wickets)',
        template='plotly_white',
        height=600,
        #width=max(1200, len(margin_by_wickets) * 100),
        margin=dict(l=20, r=20, t=80, b=120),
        xaxis=dict(tickangle=45),
        showlegend=True,
        paper_bgcolor="LightSteelBlue"
    )
    
    # Add horizontal line at y=0
    fig_by_wickets.add_hline(y=0, line_dash="solid", line_color="black", line_width=2)
    
    return fig_by_runs, fig_by_wickets