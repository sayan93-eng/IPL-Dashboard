import pandas as pd
import os
from src.utils.data_loader import load_matches_data, load_deliveries_data


# Read CSV files with correct paths
deliveries = load_deliveries_data()
matches = load_matches_data()

replacements = {
    '2007/08' : '2008',
    '2009/10' : '2010',
    '2020/21' : '2020'
}

matches['season'] = matches['season'].replace(replacements)
matches['season'] = pd.to_numeric(matches['season'])


############################################################# MATCHES LIST ########################################################################

def get_match_list_for_season(season) -> list:
    """
    Given the season like 2008, 2009, etc, the function returns a sequential list of all the matches in that season
    """
    matchlist = []
    matches_in_season = matches[matches['season'] == season]
    for index, match in matches_in_season.iterrows():
        team1 = match['team1']
        team2 = match['team2']
        date = match['date']
        matchlist.append({
            'label' : f"{team1} vs {team2} ({date})",
            'value' : match['id']
        })
    return matchlist


################################################################## MATCH SUMMARY ##################################################################

def get_match_summary_list(season):
    """
    For given season, returns a list of match_summary of each match.
    match_summary{
        id:
        date:
        venue:
        team_1:
        team_2:
        team_batting_first:
        team_batting_first_scorecard:{runs: , wickets: , overs: },
        team_batting_second:
        team_batting_second_scorecard:{runs: , wickets: , overs: },
        winning_team:
        margin:
        pom:    
    } 
    """
    season_data = matches[matches['season'] == season]

    summary_list = []

    for _, match in season_data.iterrows():
        match_summary = {}
        match_summary['id'] = match['id']
        match_summary['date'] = match['date']
        match_summary['venue'] = match['venue']
        match_summary['pom'] = match['player_of_match']
        match_summary['winner'] = match['winner']
        try:
            match_summary['result_margin'] = int(match['result_margin'])
        except ValueError:
            continue
        match_summary['result'] = match['result']
        team_1 = match['team1']
        team_2 = match['team2']
        match_summary['team_1'] = team_1
        match_summary['team_2'] = team_2
        
        if (match['toss_winner'] == team_1 and match['toss_decision'] == 'bat') or (match['toss_winner'] == team_2 and match['toss_decision'] == 'field'):
            match_summary['team_batting_first'] = team_1
            match_summary['team_batting_second'] = team_2
        else:
            match_summary['team_batting_first'] = team_2
            match_summary['team_batting_second'] = team_1
        
        # Calculate scorecard for team_batting_first
        team_batting_first_runs = int(match['target_runs'] - 1)
        team_batting_first_data = deliveries[(deliveries['match_id'] == match['id']) & (deliveries['inning'] == 1)]
        #team_batting_first_runs = team_batting_first_data['total_runs'].sum()
        team_batting_first_wickets = len(team_batting_first_data[team_batting_first_data['is_wicket'] == 1])
        # team_batting_first_overs
        team_batting_first_total_deliveries_faced = len(team_batting_first_data)
        team_batting_first_illegal_deliveries_faced = len(team_batting_first_data[
            (team_batting_first_data['extras_type'] == 'wides') | 
            (team_batting_first_data['extras_type'] == 'noballs')
        ])
        team_batting_first_legal_deliveries_faced = team_batting_first_total_deliveries_faced - team_batting_first_illegal_deliveries_faced
        team_batting_first_over_no = float(int(team_batting_first_legal_deliveries_faced/6))
        team_batting_first_ball_no = (float(team_batting_first_legal_deliveries_faced%6)/10)
        team_batting_first_overs = team_batting_first_over_no + team_batting_first_ball_no
        match_summary['team_batting_first_score'] = f"{team_batting_first_runs}/{team_batting_first_wickets}  ({team_batting_first_overs})"

        # Scorecard for team_batting_second
        team_batting_second_data = deliveries[(deliveries['match_id'] == match['id']) & (deliveries['inning'] == 2)]
        team_batting_second_runs = int(team_batting_second_data['total_runs'].sum())
        team_batting_second_wickets = len(team_batting_second_data[team_batting_second_data['is_wicket'] == 1])
        # team_batting_second_overs
        team_batting_second_total_deliveries_faced = len(team_batting_second_data)
        team_batting_second_illegal_deliveries_faced = len(team_batting_second_data[
            (team_batting_second_data['extras_type'] == 'wides') | 
            (team_batting_second_data['extras_type'] == 'noballs')
        ])
        team_batting_second_legal_deliveries_faced = team_batting_second_total_deliveries_faced - team_batting_second_illegal_deliveries_faced
        team_batting_second_over_no = float(int(team_batting_second_legal_deliveries_faced/6))
        team_batting_second_ball_no = (float(team_batting_second_legal_deliveries_faced%6)/10)
        team_batting_second_overs = team_batting_second_over_no + team_batting_second_ball_no
        match_summary['team_batting_second_score'] = f"{team_batting_second_runs}/{team_batting_second_wickets}  ({team_batting_second_overs})"

        summary_list.append(match_summary)

    return summary_list



################################################################## TEAM STATS ##################################################################

# Reference for team stats: https://nflstatsdashboard.pythonanywhere.com/
# https://plotly.com/examples/dashboards/
#https://mahmoud2227.pythonanywhere.com/

def get_team_stats(season, team):
    season_data = matches[matches['season'] == season]
    team_data = season_data[
    (season_data['team1'] == team) | 
    (season_data['team2'] == team)
    ]
    # Stats

    # Total number of matches played
    matches_played = len(team_data)

    # Number of matches won
    matches_won = len(team_data[team_data['winner'] == team])

    # Winning percent
    winning_percentage = float((matches_won/matches_played)*100)
    winning_percentage_round_off_two = f"{winning_percentage:.2f}"

    # Batting first data
    batting_first_data_1 = team_data[(team_data['toss_winner'] == team) & (team_data['toss_decision'] == 'bat')]
    batting_first_data_2 = team_data[(team_data['toss_winner'] != team) & (team_data['toss_decision'] == 'field')]

    batting_first = pd.concat([batting_first_data_1, batting_first_data_2], ignore_index=True)

    batting_first_highest_score = int(batting_first['target_runs'].max()) - 1
    batting_first_lowest_score = int(batting_first['target_runs'].min()) - 1

    # Batting second data
    batting_second_data_1 = team_data[(team_data['toss_winner'] == team) & (team_data['toss_decision'] == 'field')]
    batting_second_data_2 = team_data[(team_data['toss_winner'] != team) & (team_data['toss_decision'] == 'bat')]

    batting_second = pd.concat([batting_second_data_1, batting_second_data_2], ignore_index=True)
        # Get 'id' of the matches, reference these later in deliveries df
    match_ids = batting_second['id'].tolist()

    batting_second_score_list = []
    for match in match_ids:
        second_inning = deliveries[(deliveries['match_id'] == match) & (deliveries['inning'] == 2)]
        total_score = second_inning['total_runs'].sum()
        batting_second_score_list.append(total_score)
    
    batting_second_highest_score = max(batting_second_score_list)
    batting_second_lowest_score = min(batting_second_score_list)

    # Win Loss Form
    win_loss = []
    for _, match in team_data.iterrows():
        if match['winner'] == team:
            win_loss.append('W')
        else:
            win_loss.append('L')

    return {
        'Matches Played': matches_played,
        'Matches Won': matches_won,
        'Winning Percentage': winning_percentage_round_off_two,
        'Highest score batting first': batting_first_highest_score,
        'Lowest score batting first':batting_first_lowest_score,
        'Highest score batting second': batting_second_highest_score,
        'Lowest score batting second':batting_second_lowest_score,
        'Win Loss Form': win_loss
    }


################################################################## BATTER STATS ##################################################################


def get_batter_stats(season):
    season_data = matches[matches['season'] == season]

    # Get all match_ids in a season
    all_match_ids_in_a_season = season_data['id'].tolist()

    # Get all deliveries from all matches in season
    season_deliveries = deliveries[deliveries['match_id'].isin(all_match_ids_in_a_season)]

    # Get list of all batters who have batted at least 1 ball in the season
    batters_in_season = season_deliveries['batter'].unique().tolist()

    # Create an empty list to store the stats of every batter
    batter_stats_list = []

    # Process stats for each batter
    for batter in batters_in_season:

        # Initialize empty dict to store each batter stats
        batter_stats = {}

        # Get data for each batsman
        batsman_data = season_deliveries[season_deliveries['batter'] == batter]

        ### STATS ###
        # Name
        batter_stats['name'] = batsman_data['batter']

        # Number of Innings
        batter_stats['number_of_innings'] = len(batsman_data['match_id'].unique())

        # Total runs
        batter_stats['total_runs'] = batsman_data['batsman_runs'].sum()

        # Average
        batter_stats['batting_average'] = float(batter_stats['total_runs']/batter_stats['number_of_innings'])
        
        # Strike Rate
        total_balls_faced = len(batsman_data)
        illegal_balls_faced = len(batsman_data[
            (batsman_data['extras_type'] == 'wides') | 
            (batsman_data['extras_type'] == 'noballs')
        ])
        balls_faced = total_balls_faced - illegal_balls_faced
        batter_stats['strike_rate'] = (float(batter_stats['total_runs']/balls_faced))*100

        # Number of 4s
        batter_stats['number_of_4s'] = len(batsman_data[batsman_data['batsman_runs'] == 4])

        # Number of 6s
        batter_stats['number_of_6s'] = len(batsman_data[batsman_data['batsman_runs'] == 6])
        

        # Create a list of the individual scores of the batter
        scores_in_season = []
        current_match_id = None
        runs_in_innings = 0
        # Sort deliveries by match_id to ensure sequential processing
        batsman_data_sorted = batsman_data.sort_values('match_id')
        for _, delivery in batsman_data_sorted.iterrows():
            # Check if this is a new match
            if current_match_id != delivery['match_id']:
                # Store previous innings score (except for first iteration)
                if current_match_id is not None:
                    scores_in_season.append(runs_in_innings)
                # Reset for new match
                current_match_id = delivery['match_id']
                runs_in_innings = 0
            # Add runs for this delivery
            runs_in_innings += delivery['batsman_runs']
        # Store last innings score
        scores_in_season.append(runs_in_innings)


        # Highest Score
        batter_stats['highest_score'] = max(scores_in_season)

        # Number of 50s
        batter_stats['number_of_50s'] = len([score for score in scores_in_season if score >= 50 and score < 100])

        # Number of 100s
        batter_stats['number_of_100s'] = len([score for score in scores_in_season if score >= 100])

        # Add the stats dict to the list
        batter_stats_list.append(batter_stats)
    
    return batter_stats_list


################################################################## BOWLER STATS ##################################################################

def get_bowler_stats(season):
    season_data = matches[matches['season'] == season]

    # Get all match_ids in a season
    all_match_ids_in_a_season = season_data['id'].tolist()

    # Get all deliveries from all matches in season
    season_deliveries = deliveries[deliveries['match_id'].isin(all_match_ids_in_a_season)]

    # Get list of all bowlers who have bowled at least 1 ball in the season
    bowlers_in_season = season_deliveries['bowler'].unique().tolist()

    # Create an empty list to store the stats of every bowler
    bowler_stats_list = []

    # Process stat for each bowler
    for bowler in bowlers_in_season:

        # Initialize empty dict to store each bowler stats
        bowler_stats = {}

        # Get data for each bowler
        bowler_data =season_deliveries[season_deliveries['bowler'] == bowler]

        ### STATS ###
        # Name
        bowler_stats['name'] = bowler_data['bowler']
        
        # Number of Innings
        bowler_stats['number_of_innings'] = len(bowler_data['match_id'].unique())

        # Total wickets taken
        total_wickets = len(bowler_data[bowler_data['is_wicket'] == 1])
        run_out_wickets = len(bowler_data[bowler_data['dismissal_kind'] == 'run out'])
        bowler_stats['wickets_taken'] = total_wickets - run_out_wickets

        # Total runs conceded
        bowler_stats['runs_conceded'] = (bowler_data[bowler_data['extras_type'] != 'legbyes'])['total_runs'].sum()
        
        # Overs
        all_balls_bowled = len(bowler_data)
        illegal_balls_bowled = len(bowler_data[
            (bowler_data['extras_type'] == 'wides') | 
            (bowler_data['extras_type'] == 'noballs')
        ])
        legal_balls_bowled = all_balls_bowled - illegal_balls_bowled
        over_no = float(int(legal_balls_bowled/6))
        ball_no = (float(legal_balls_bowled%6)/10)
        bowler_stats['overs'] = over_no + ball_no

        # Average
        bowler_stats['average'] = float(bowler_stats['runs_conceded']/total_wickets)

        # Econ
        econ_over_no = float(int(legal_balls_bowled/6))
        econ_ball_no = float((legal_balls_bowled%6)/6)
        econ_over = econ_over_no + econ_ball_no
        bowler_stats['economy_rate'] = bowler_stats['runs_conceded']/econ_over

        # Strike Rate
        bowler_stats['strike_rate'] = float(legal_balls_bowled/total_wickets)

        # Dots
        bowler_stats['number_of_dots'] = len(bowler_data[bowler_data['total_runs'] == 0])


        # Create a list of indvidual bowling figures of the bowler
        bowling_figures = []
        current_match = None
        runs = 0
        wickets = 0
        bowler_data_sorted = bowler_data.sort_values('match_id')
        for _, delivery in bowler_data_sorted.iterrows():
            # Check if this is a new match
            if current_match != delivery['match_id']:
                if current_match is not None:
                    bowling_figures.append({wickets:runs})
                # Reset for new match
                current_match = delivery['match_id']
                runs = 0
                wickets = 0
            # Add runs excluding legbyes
            if delivery['extras_type'] != 'legbyes':
                runs += delivery['total_runs']
            # Add wiclets except run outs
            if delivery['is_wicket'] == 1 and delivery['dismissal_kind'] != 'run out':
                wickets +=1
        bowling_figures.append({wickets: runs})


        # Best bowling figure
        bowler_stats['best_bowling_figure'] = max(bowling_figures, key=lambda d: list(d.keys())[0])
    
        # Number of 3Ws
        bowler_stats['number_of_3Ws'] = sum(1 for d in bowling_figures if list(d.keys())[0] >= 3)

        # Number of 5Ws
        bowler_stats['number_of_5Ws'] = sum(1 for d in bowling_figures if list(d.keys())[0] >= 5)


        # Add to list
        bowler_stats_list.append(bowler_stats)
    
    return bowler_stats_list



####################################################################### POINTS TABLE #####################################################################

def calculate_points_table(season):
    pass

"""
NRR = (Total runs scored by team / Total overs faced by team) - (Total runs conceded or scored against team / Total overs bowled by team)
If a team chases a target successfully and wins, only the actual number of overs is counted.
But if a team is bowled out, the full quota of 20 overs is taken for NRR calculations.
Here's an example of an IPL 2025 match between Kolkata Knight Riders (KKR) and Sunrisers Hyderabad (SRH), which was played on April 3 at Eden Gardens. 

The scores read: KKR 200/6 in 20 overs and SRH 120/10 in 16.4 overs.

Here's how KKR's NRR is calculated for this particular match: (200/20) -  (120/20) = 4.00

Now, even though SRH faced just 16.4 overs, the full quota of 20 overs was considered during the calculation because they were bowled out.

However, if they had chased down the total in 19.1 overs, the calculation of 19.1 would have been used, not 20.
"""