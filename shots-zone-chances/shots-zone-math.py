import pandas as pd

shots = pd.read_csv("data/shots_hometeam_2024season.csv")

print(shots.head())

# distance from net:
# let's say the net is at (585, 150)
# max x = 588, max y = 298

# distance between 2 points is (x2 - x1)/(y2 - y1)
# we are going to let x2 and 72 be 585 and 150, respectively

# sql:
# SELECT games.id, goalie.name, shots.goalie_id, shots.period, shots.x_location, shots.y_location, IF(player_teams.team_id = games.home_team_id, 1, 0) AS is_home 
# FROM shots 
# JOIN players 
# AS goalie 
# ON shots.goalie_id = goalie.id 
# JOIN games ON shots.game_id = games.id 
# JOIN player_teams 
# ON goalie.id = player_teams.player_id 
# AND player_teams.start_date != "0000-00-00"
# WHERE games.season = 1;

def do_math(x):
    if x <= 300:
        return round(x/300 * 322)
    else: 
        return round((x - 300)/300 * 322)

print(shots.head())

shots["x_location"].loc[:, "x_location"] = shots["x_location"][(shots["period"] == 2) & (shots["is_home"] == 1)].map(lambda x: do_math())

print(shots.head())