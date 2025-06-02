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



def get_all_batters():
    all_batters = deliveries['batter'].unique().tolist()
    return all_batters

def get_all_bowlers():
    all_bowlers = deliveries['bowler'].unique().tolist()
    return all_bowlers


def get_seasons_teams(player):
    player_data = deliveries[deliveries['batter'] == player]
    teams = player_data['batting_team'].unique().tolist()
    matches_played = player_data['match_id'].unique().tolist()
    all_seasons = list(range(2008, 2025))
    seasons_played = []
    for season in all_seasons:
        matches_played_in_season = list(set(matches_played) & set(matches[matches['season'] == season]['id'].tolist()))
        if len(matches_played_in_season) > 0:
            seasons_played.append(season)
    
    return {
        'teams': teams,
        'seasons': seasons_played
    }


#print(get_seasons_teams('JJ Bumrah'))

#print(len(matches[matches['season'] == 2008]['id'].tolist()))

def get_batter_vs_bowler_stats(batter, bowler):

    batter_bowler = deliveries[(deliveries['batter'] == batter) & (deliveries['bowler'] == bowler)]

    all_deliveries = len(batter_bowler)
    illegal_deliveries = len(batter_bowler[
                (batter_bowler['extras_type'] == 'wides') | 
                (batter_bowler['extras_type'] == 'noballs')
            ])
    legal_deliveries = all_deliveries - illegal_deliveries

    runs = batter_bowler['batsman_runs'].sum()

    outs = len(batter_bowler[batter_bowler['is_wicket'] == 1])

    dots = len(batter_bowler[batter_bowler['total_runs'] == 0])

    fours = len(batter_bowler[batter_bowler['batsman_runs'] == 4])

    sixes = len(batter_bowler[batter_bowler['batsman_runs'] == 6])

    batter_avg = float(runs/outs)

    batter_strikerate = float((runs/legal_deliveries)*100)

    bowler_avg = float(runs/outs)

    econ_over_no = float(int(legal_deliveries/6))
    econ_ball_no = float((legal_deliveries%6)/6)
    econ_over = econ_over_no + econ_ball_no
    over = float("{:.1f}".format(econ_over))
    bowler_econ = float(runs/over)

    number_of_matches = batter_bowler['match_id'].unique().tolist()

    return {
        'matches': number_of_matches,
        'balls': legal_deliveries,
        'runs': runs,
        'dots': dots,
        'outs': outs,
        'fours': fours,
        'sixes': sixes,
        'strikerate': batter_strikerate,
        'econrate': bowler_econ
    }


def get_batter_career_stats(batter):
    batter_data = deliveries[deliveries['batter'] == batter]
    matches_played = int(len(batter_data['match_id'].unique().tolist()))

    if matches_played > 0:
        runs = int(batter_data['batsman_runs'].sum())
        outs = int(len(batter_data[batter_data['is_wicket'] == 1]))


        # Generate list of all scores sequentially for career
        scores_in_career = []
        current_match_id = None
        runs_in_innings = 0
        # Sort deliveries by match_id to ensure sequential processing
        batter_data_sorted = batter_data.sort_values('match_id')
        for _, delivery in batter_data_sorted.iterrows():
            # Check if this is a new match
            if current_match_id != delivery['match_id']:
                # Store previous innings score (except for first iteration)
                if current_match_id is not None:
                    scores_in_career.append(runs_in_innings)
                # Reset for new match
                current_match_id = delivery['match_id']
                runs_in_innings = 0
            # Add runs for this delivery
            runs_in_innings += delivery['batsman_runs']
        # Store last innings score
        scores_in_career.append(runs_in_innings)

        highest_score = max(scores_in_career)

        try:
            avg = float("{:.2f}".format(runs/outs))
        except ZeroDivisionError:
            avg = 'NA'

        all_deliveries = len(batter_data)
        illegal_deliveries = len(batter_data[
                    (batter_data['extras_type'] == 'wides') | 
                    (batter_data['extras_type'] == 'noballs')
                ])
        legal_deliveries = all_deliveries - illegal_deliveries
        
        try:
            strike_rate = round((runs/legal_deliveries)*100, 2)
        except ZeroDivisionError:
            strike_rate = 0.0

        number_of_50s = len([score for score in scores_in_career if score >= 50 and score < 100])

        number_of_100s = len([score for score in scores_in_career if score >= 100])

        number_of_4s = len(batter_data[batter_data['batsman_runs'] == 4])

        number_of_6s = len(batter_data[batter_data['batsman_runs'] == 6])

        return{
            'matches':matches_played,
            'runs':runs,
            'highest_score': highest_score,
            'average': avg,
            'strike_rate': strike_rate,
            '100s': number_of_100s,
            '50s' : number_of_50s,
            '4s': number_of_4s,
            '6s': number_of_6s

        }
    
    return None


def get_bowler_career_stats(bowler):
    bowler_data = deliveries[deliveries['bowler'] == bowler]
    matches_played = len(bowler_data['match_id'].unique().tolist())
    
    if matches_played > 0:
        # WICKETS
        total_wickets = len(bowler_data[bowler_data['is_wicket'] == 1])
        run_out_wickets = len(bowler_data[bowler_data['dismissal_kind'] == 'run out'])
        wickets = total_wickets - run_out_wickets

        runs_conceded = (bowler_data[bowler_data['extras_type'] != 'legbyes'])['total_runs'].sum()

        try:
            avg = float("{:.2f}".format(runs_conceded/wickets))
        except ZeroDivisionError:
            avg = 'NA'


        # Overs
        all_balls_bowled = len(bowler_data)
        illegal_balls_bowled = len(bowler_data[
            (bowler_data['extras_type'] == 'wides') | 
            (bowler_data['extras_type'] == 'noballs')
        ])
        legal_balls_bowled = all_balls_bowled - illegal_balls_bowled
        over_no = float(int(legal_balls_bowled/6))
        ball_no = (float(legal_balls_bowled%6)/10)
        overs = over_no + ball_no

        dots = len(bowler_data[bowler_data['total_runs'] == 0])

        try:
            dot_percentage = float("{:.2f}".format((dots/legal_balls_bowled)*100))
        except ZeroDivisionError:
            dot_percentage = 'NA'

        econ_over_no = float(int(legal_balls_bowled/6))
        econ_ball_no = float((legal_balls_bowled%6)/6)
        econ_over = econ_over_no + econ_ball_no

        try:
            econ_rate = float("{:.2f}".format(runs_conceded/econ_over))
        except ZeroDivisionError:
            econ_rate = 'NA'

        try:
            strike_rate = float("{:.2f}".format(legal_balls_bowled/total_wickets))
        except ZeroDivisionError:
            strike_rate = 'NA'


    
        # Create a list of indvidual bowling figures of the bowler
        career_bowling_figures = []
        current_match = None
        runs = 0
        wickets_in_innings = 0
        bowler_data_sorted = bowler_data.sort_values('match_id')
        for _, delivery in bowler_data_sorted.iterrows():
            # Check if this is a new match
            if current_match != delivery['match_id']:
                if current_match is not None:
                    career_bowling_figures.append({wickets_in_innings:runs})
                # Reset for new match
                current_match = delivery['match_id']
                runs = 0
                wickets_in_innings = 0
            # Add runs excluding legbyes
            if delivery['extras_type'] != 'legbyes':
                runs += delivery['total_runs']
            # Add wiclets except run outs
            if delivery['is_wicket'] == 1 and delivery['dismissal_kind'] != 'run out':
                wickets_in_innings +=1
        career_bowling_figures.append({wickets_in_innings: runs})

        best_bowling_figure = max(career_bowling_figures, key=lambda d: list(d.keys())[0])

        number_of_3Ws = sum(1 for d in career_bowling_figures if list(d.keys())[0] >= 3)

        number_of_5Ws = sum(1 for d in career_bowling_figures if list(d.keys())[0] >= 5)

        return {
            'matches': matches_played,
            'wickets': wickets,
            'overs': overs,
            'dot_ball_percentage': dot_percentage,
            'best_bowling_figure' : best_bowling_figure,
            'average': avg,
            'economy_rate': econ_rate,
            'strike_rate': strike_rate,
            '3Ws' : number_of_3Ws,
            '5Ws' : number_of_5Ws
        }
    
    return None








