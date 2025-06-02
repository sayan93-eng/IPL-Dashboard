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