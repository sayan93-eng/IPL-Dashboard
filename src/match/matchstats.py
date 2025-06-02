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
        id = match['id']
        team1 = match['team1']
        team2 = match['team2']
        date = match['date']
        matchlist.append({
            'label' : f"{team1} vs {team2} ({date})",
            'value' : match['id']
        })
    return matchlist



################################################################ SCORECARD TABLE #############################################################

def get_batting_scorecard(match_id, inning_id):
    match_data = deliveries[deliveries['match_id'] == match_id]
    inning_data = match_data[match_data['inning'] == inning_id]
    batters = inning_data['batter'].unique()
    #bowlers = inning_data['bowler'].unique()
    batting_scorecard_list = []
    for batter in batters:
        batting_scorecard = {}
        batsman_df = inning_data[inning_data['batter'] == batter]
        runs_scored = 0
        legal_deliveries_faced = 0
        number_of_fours = 0
        number_of_sixes = 0
        dismissal_delivery = batsman_df[(batsman_df['is_wicket'] == 1)]
        fielder = dismissal_delivery['fielder'].iloc[0] if not dismissal_delivery.empty else ""
        dismissal_kind = dismissal_delivery['dismissal_kind'].iloc[0] if not dismissal_delivery.empty else ""
        bowler = dismissal_delivery['bowler'].iloc[0] if not dismissal_delivery.empty else ""

        for _, delivery in batsman_df.iterrows(): # check pandas way of doing this
            runs_scored += delivery['batsman_runs']
            if delivery['extras_type'] == 'wides' or delivery['extras_type'] == 'noballs':
                continue
            else:
                legal_deliveries_faced +=1
            
            if delivery['batsman_runs'] == 4:
                number_of_fours += 1
            elif delivery['batsman_runs'] == 6:
                number_of_sixes += 1
        try:
            strike_rate = float((runs_scored/legal_deliveries_faced)*100)
        except ZeroDivisionError:
            continue
        strike_rate_round_off_two_places = f"{strike_rate:.2f}"
        batting_scorecard['Batsman Name'] = batter
        batting_scorecard['Runs Scored'] = runs_scored
        batting_scorecard['Deliveries Faced'] = legal_deliveries_faced
        batting_scorecard['4s'] = number_of_fours
        batting_scorecard['6s'] = number_of_sixes
        batting_scorecard['Strike Rate'] = strike_rate_round_off_two_places
        if dismissal_kind == 'bowled':
            batting_scorecard['Dismissal Type'] = f"b {bowler}"
        elif dismissal_kind == 'lbw':
            batting_scorecard['Dismissal Type'] = f"lbw {bowler}"
        elif dismissal_kind == 'caught':
            batting_scorecard['Dismissal Type'] = f"c {fielder} b {bowler} "
        elif dismissal_kind == 'run out':
            batting_scorecard['Dismissal Type'] = f"run out {fielder}"
        elif dismissal_kind == 'stumped':
            batting_scorecard['Dismissal Type'] = f"b {bowler} stumped {fielder}"
        elif dismissal_kind == 'caught and bowled':
            batting_scorecard['Dismissal Type'] = f"c & b {bowler}"
        elif dismissal_kind == 'hit wicket':
            batting_scorecard['Dismissal Type'] = f"hit wicket"
        elif dismissal_kind == 'retired hurt':
            batting_scorecard['Dismissal Type'] = f"retired hurt"
        else:
            batting_scorecard['Dismissal Type'] = f"not out"
        
        batting_scorecard_list.append(batting_scorecard)
    
    
     
    return batting_scorecard_list

##################################################################### FINAL SCORE #######################################################

def get_final_score(match_id, inning_id):

    match_data = deliveries[deliveries['match_id'] == match_id]
    inning_data = match_data[match_data['inning'] == inning_id]
    # Calculate the final score e.g 165/9(20) or 135/10(16.2)

    # Calculate overs played bt the batting team
    total_deliveries_faced = len(inning_data)
    illegal_deliveries_faced = len(inning_data[
        (inning_data['extras_type'] == 'wides') | 
        (inning_data['extras_type'] == 'noballs')
    ])
    legal_deliveries_faced = total_deliveries_faced - illegal_deliveries_faced
    over_no = float(int(legal_deliveries_faced/6))
    ball_no = (float(legal_deliveries_faced%6)/10)
    overs = over_no + ball_no

    # Calculate total runs scored by the batting team
    total_runs = inning_data['total_runs'].sum()

    # Calculate no of wickets that have fallen
    wickets = len(inning_data[inning_data['is_wicket'] == 1])

    # Final score
    final_score = f"{total_runs}/{wickets}  ({overs})"

    return final_score
    

############################################################################### BOWLING SCORECARD #########################################################################


def get_bowling_scorecard(match_id, inning_id):
    match_data = deliveries[deliveries['match_id'] == match_id]
    inning_data = match_data[match_data['inning'] == inning_id]
    bowlers = inning_data['bowler'].unique()
    #bowler_data = inning_data_1[inning_data_1['bowler'] == 'T Natarajan']
    bowling_scorecard_list = []
    for bowler in bowlers:
        bowler_scorecard = {}
        bowler_data = inning_data[inning_data['bowler'] == bowler]
        legal_deliveries_bowled = 0
        runs_conceded = 0
        wickets_taken = 0
        number_of_dots = 0
        overs = 0.0
        economy_rate = 0.0
        
        for _, delivery in bowler_data.iterrows():
            bowler_scorecard = {}
            #print(delivery['total_runs'])
            if delivery['total_runs'] == 0:
                number_of_dots += 1
            else:
                if delivery['extras_type'] != 'legbyes':
                    runs_conceded += delivery['total_runs']

            if delivery['extras_type'] == 'wides' or delivery['extras_type'] == 'noballs':
                continue
            else:
                legal_deliveries_bowled += 1

            # Calculate overs to be displayed in scorecard
            over_no = float(int(legal_deliveries_bowled/6))
            ball_no = (float(legal_deliveries_bowled%6)/10)
            overs = over_no + ball_no
            
            # Calculate overs for calculating econ rate
            econ_over_no = float(int(legal_deliveries_bowled/6))
            econ_ball_no = float((legal_deliveries_bowled%6)/6)
            econ_over = econ_over_no + econ_ball_no
            economy_rate = runs_conceded/econ_over
            
            
            if delivery['is_wicket'] == 0:
                continue
            elif delivery['is_wicket'] and delivery['dismissal_kind'] != 'run out':

                wickets_taken += 1 
        
        economy_rate_round_off_two_places = f"{economy_rate:.2f}"
        bowler_scorecard['Bowler Name'] = bowler
        bowler_scorecard['Overs'] = overs
        bowler_scorecard['Runs Conceded'] = runs_conceded
        bowler_scorecard['Wickets'] = wickets_taken
        bowler_scorecard['Economy Rate'] = economy_rate_round_off_two_places
        #bowler_scorecard['Balls'] = legal_deliveries_bowled
        bowler_scorecard['Dots'] = number_of_dots

        bowling_scorecard_list.append(bowler_scorecard)
    
    return bowling_scorecard_list


################################################################ FALL OF WICKETS ###############################################################

def get_fall_of_wickets(match_id, inning_id):
    match_data =  deliveries[deliveries['match_id'] == match_id]
    inning_data = match_data[match_data['inning'] == inning_id]
    runs = 0
    wickets = 0
    fall_of_wickets = []
    for _, delivery in inning_data.iterrows():
        if delivery['is_wicket'] != 1:
            runs += delivery['total_runs']
        elif delivery['is_wicket'] == 1:
            fow = {}
            wickets += 1
            over = delivery['over']
            ball = delivery['ball']
            over_no = f"{over}.{ball}"
            batter = delivery['player_dismissed']
            bowler = delivery['bowler']
            score = f"{runs}/{wickets}"
            dismissal_kind = delivery['dismissal_kind']
            fow['score'] = score
            fow['over'] = over_no
            fow['batter'] = batter
            fow['bowler'] = bowler
            fow['dismissal_kind'] = dismissal_kind
            fall_of_wickets.append(fow)

    return fall_of_wickets


##################################################################### MATCH DETAILS TABLE ###########################################################

def get_match_details(match_id):
    match = {}
    match_details = matches[matches['id'] == match_id]
    season = match_details['season'].iloc[0]
    tournament = f"IPL Season {season}"
    venue = match_details['venue'].iloc[0]
    date = match_details['date'].iloc[0]
    toss_winner = match_details['toss_winner'].iloc[0]
    toss_decision = match_details['toss_decision'].iloc[0]
    toss_details = f"{toss_winner} won the toss and decided to {toss_decision}"
    umpires = match_details['umpire1'].iloc[0], match_details['umpire2'].iloc[0]
    player_of_match = match_details['player_of_match'].iloc[0]
    winner = match_details['winner'].iloc[0]
    result_margin = match_details['result_margin'].iloc[0]
    result_type = match_details['result'].iloc[0]
    result = ''
    if result_type == 'wickets':
        result = f"{winner} won by {result_margin} wickets"
    elif result_type == 'runs':
        result = f"{winner} won by {result_margin} runs"

    match['Tournament'] = tournament
    match['Date'] = date
    match['Venue'] = venue
    match['Toss Details'] = toss_details
    match['Umpires'] = umpires
    match['Result'] = result
    match['Player of the Match'] = player_of_match

    return match

################################################################ DATA FOR BAR PLOT #############################################################

def get_data_for_bar_plot(match_id, inning_id):
    match_data =  deliveries[deliveries['match_id'] == match_id]
    inning_data = match_data[match_data['inning'] == inning_id]

    runs_in_over_list = inning_data.groupby('over')['total_runs'].sum().tolist()
    wicket_overs_list = inning_data[inning_data['is_wicket'] == 1]['over'].tolist()

    return {
        'runs_in_over_list' : runs_in_over_list,
        'wicket_overs_list' : wicket_overs_list
    }

################################################################ DATA FOR LINE PLOT #############################################################

def get_data_for_line_plot(match_id, inning_id):
    match_data =  deliveries[deliveries['match_id'] == match_id]
    inning_data = match_data[match_data['inning'] == inning_id]

    total_runs_at_end_of_each_over_list = inning_data.groupby('over')['total_runs'].sum().cumsum().tolist()
    wicket_overs_list = inning_data[inning_data['is_wicket'] == 1]['over'].tolist()

    return {
        'total_runs_at_end_of_each_over_list' : total_runs_at_end_of_each_over_list,
        'wicket_overs_list' : wicket_overs_list
    }

################################################################ DATA FOR PIE CHART #############################################################

def get_data_for_pie_chart(match_id, inning_id):
    match_data =  deliveries[deliveries['match_id'] == match_id]
    inning_data = match_data[match_data['inning'] == inning_id]
    
    # runs_scored_in_1s_count = len(inning_data[inning_data['batsman_runs'] == 1])
    runs_scored_in_1s = len(inning_data[inning_data['batsman_runs'] == 1]) * 1
    runs_scored_in_2s = len(inning_data[inning_data['batsman_runs'] == 2]) * 2
    runs_scored_in_3s = len(inning_data[inning_data['batsman_runs'] == 3]) * 3
    runs_scored_in_4s = len(inning_data[inning_data['batsman_runs'] == 4]) * 4
    runs_scored_in_6s = len(inning_data[inning_data['batsman_runs'] == 6]) * 6
    runs_scored_extras = inning_data['extra_runs'].sum()

    return [runs_scored_in_1s, runs_scored_in_2s, runs_scored_in_3s, runs_scored_in_4s, runs_scored_in_6s, runs_scored_extras]


######################################################  PARTNERSHIP  DATA  ##################################################################

def get_partnership_data(match_id, inning_id):

    match_data =  deliveries[deliveries['match_id'] == match_id]
    inning_data = match_data[match_data['inning'] == inning_id]

    # Store the batter name in variables like batter1, batter2, ... batterpos, where pos is the position in which the batter came in to bat. 


    # Get df of all unique combinations of ['batter'] and ['non-striker'] in any order -> get all rows where batter=batter1 and non-striker=batter2 or batter=batter2 and non-striker=batter1

    # Create a mask to filter the dataframe 

    #mask = ((inning_data['batter'] == 'SC Ganguly') & (inning_data['non_striker'] == 'BB McCullum')) | 
        #((inning_data['batter'] == 'BB McCullum') & (inning_data['non_striker'] == 'SC Ganguly'))


    # Create a list of dataframes where each df is the partnership.
    # Iterate through the list, extract the info out from each df and add it to the final list.

    # Break up the entire innings df into partnership dfs.
    # Get all batter pairs in the innings.(all unique instances of batter and non_striker)
    #unique_combinations = df[['col1', 'col2']].drop_duplicates()
    all_pairs = inning_data[['batter', 'non_striker']].drop_duplicates()

    partnership_pair_list = []

    batter_1 = all_pairs['batter'].iloc[0]
    batter_2 = all_pairs['non_striker'].iloc[0]
    partnership_pair_list.append((batter_1, batter_2))

    # Track current batters
    current_batters = {batter_1, batter_2}
        
    for _, pair in all_pairs.iterrows():
        current_pair = {pair['batter'], pair['non_striker']}

        # If either batter is new (not in current_batters), we have a new partnership
        if current_pair.issubset(current_batters) is not True:
            # Find the continuing batter (common between current_batters and new pair)
            continuing_batter = current_batters.intersection(current_pair).pop() if current_batters.intersection(current_pair) else None
            new_batter = (current_pair - {continuing_batter}).pop() if continuing_batter else pair['batter']

        # Update current batters and add new partnership
            current_batters = {continuing_batter, new_batter} if continuing_batter else {pair['batter'], pair['non_striker']}
            partnership_pair_list.append(tuple(current_batters))





    partnership_data_list = []
    for pair in partnership_pair_list:
        partnership_data = {}
        partnership = inning_data[
        ((inning_data['batter'] == pair[0]) & (inning_data['non_striker'] == pair[1])) | 
        ((inning_data['batter'] == pair[1]) & (inning_data['non_striker'] == pair[0]))
        ]
        # Generate the data for batter1
        partnership_data['batter1'] = pair[0]
        partnership_data['batter1_runs'] = int(partnership[partnership['batter'] == partnership_data['batter1']]['batsman_runs'].sum())
        batter1_balls_total = int(len(partnership[partnership['batter'] == partnership_data['batter1']]))
        batter1_balls_illegal = int(len(partnership[
        (partnership['extras_type'] == 'wides') | (partnership['extras_type'] == 'noballs')]))
        partnership_data['batter1_balls'] = int(batter1_balls_total - batter1_balls_illegal)

        # Generate the data for batter2
        partnership_data['batter2'] = pair[1]
        partnership_data['batter2_runs'] = int(partnership[partnership['batter'] == partnership_data['batter2']]['batsman_runs'].sum())
        batter2_balls_total = int(len(partnership[partnership['batter'] == partnership_data['batter2']]))
        batter2_balls_illegal = int(len(partnership[
        (partnership['extras_type'] == 'wides') | (partnership['extras_type'] == 'noballs')]))
        partnership_data['batter2_balls'] = int(batter2_balls_total - batter2_balls_illegal)

        # Generate the data for extras
        partnership_data['extra_runs'] = int(partnership['extra_runs'].sum())
        # Generate the data for total runs
        partnership_data['total_runs'] = int(partnership['total_runs'].sum())
        # Generate the data for total balls
        partnership_data['all_balls'] = partnership_data['batter1_balls'] + partnership_data['batter2_balls']

        partnership_data_list.append(partnership_data)


    return partnership_data_list




"""
batter1 = partnership['batter'].iloc[0]
batter1_runs = partnership[partnership['batter'] == batter1]['batsman_runs'].sum()
batter1_balls_total = int(len(partnership[partnership['batter'] == batter1]))
batter1_balls_illegal = int(len(partnership[
    (partnership['extras_type'] == 'wides') | (partnership['extras_type'] == 'noballs')]))
batter1_balls = batter1_balls_total - batter1_balls_illegal







batter2 = partnership['non_striker'].iloc[0]

# At the start of each partnership, determine who is batter1 and who is batter2 by checking their index in all_batters.

total_runs = int(partnership['total_runs'].sum())

all_balls = int(len(partnership))

illegal_balls = int(len(partnership[
    (partnership['extras_type'] == 'wides') | (partnership['extras_type'] == 'noballs')]))

total_balls = all_balls - illegal_balls

print(all_balls)

print(
    {
    'batter1' : '', 
    'batter1_runs' : '', 
    'batter1_balls' : '', 
    'batter2' : '', 
    'batter2_runs' : '', 
    'batter2_balls' : '', 
    'extra_runs' : '',
    'total_runs' : total_runs,
    'total_balls' : total_balls
    }
    
)


partnership = {
    'batter1' : 'name',
    'batter1_runs' : '',
    'batter1_balls' : '',
    'batter1_balls' : '',
    'batter2_runs' : '',
    'batter2_balls' : '',
    'extra_runs' : '',
    'total_runs' : '',
    'total_balls' : ''
}
"""








# Edge case where batter comes in to bat as non_striker and the innings ends without batter facing any balls. In this case, all_nonstrikers will have 1 count more than all_batters.



