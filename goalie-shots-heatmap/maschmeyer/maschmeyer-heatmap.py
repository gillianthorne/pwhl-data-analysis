import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

# basically just to have all shots mirrored on one side
# this isn't perfect bc some shots might be taken from across center ice, especially empty net goals
# but also the threshold will probably weed them out lmao
# i'm also stretching it to fit the image - it might not be real world accurate but it is good for display purposes
def do_math(x):
    if x <= 300:
        return round(x/300 * 322)
    else: 
        return round((x - 300)/300 * 322)
    
# load the csv files of shots/goals, filter so it's just maschmeyer
df_shots = pd.read_csv("data/allshots_2024season.csv", index_col=0)
df_shots = df_shots[df_shots["goalie_id"] == 59]

df_saves = pd.read_csv("data/shotsnongoals_2024season.csv", index_col=0)
df_saves = df_saves[df_saves["goalie_id"] == 59]

df_goals = pd.read_csv("data/shotsgoals_2024season.csv", index_col=0)
df_goals = df_goals[df_goals["goalie_id"] == 59]

# do the math!
df_shots["x_location"] = df_shots.loc[:, "x_location"].map(lambda x: do_math(x))
df_saves["x_location"] = df_saves.loc[:, "x_location"].map(lambda x: do_math(x))
df_goals["x_location"] = df_goals.loc[:, "x_location"].map(lambda x: do_math(x))

# this just gives me the background picture
map_image = mpimg.imread("extra-resources/images/ht-ice-rink-2.png")

fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(10, 3))

fig.suptitle("Emerance Maschmeyer Shots, Saves and Goals")

# graph it!
shots_graph = sns.kdeplot(ax=axes[0], data=df_shots, x="x_location", y="y_location", fill=True, cmap="rainbow", alpha=0.8, thresh=0.07)
shots_graph.imshow(map_image, aspect="equal", zorder=-1)
axes[0].set_title("Shots Faced")

saves_graph = sns.kdeplot(ax=axes[1], data=df_saves, x="x_location", y="y_location", fill=True, cmap="rainbow", alpha=0.8, thresh=0.07)
saves_graph.imshow(map_image, aspect="equal", zorder=-1)
axes[1].set_title("Saves")

goals_graph = sns.kdeplot(ax=axes[2], data=df_goals, x="x_location", y="y_location", fill=True, cmap="rainbow", alpha=0.8, thresh=0.3)
goals_graph.imshow(map_image, aspect="equal", zorder=-1)
axes[2].set_title("Goals Allowed")

plt.tight_layout()
plt.savefig("images/maschhmeyer-heatmap.png")
plt.show()