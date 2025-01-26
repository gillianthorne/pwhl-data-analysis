import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import datetime

# basically just to have all shots mirrored on one side
# this isn't perfect bc some shots might be taken from across center ice, especially empty net goals
# but also the threshold will probably weed them out lmao
# i'm also stretching it to fit the image - it might not be real world accurate but it is good for display purposes
def do_math(x):
    if x <= 300:
        return round(x/300 * 322)
    else: 
        return round((x - 300)/300 * 322)
    
df_goals = pd.read_csv("data/allshots_2024season.csv", index_col=0)

print(df_goals["goalie_id"].unique())

# this just makes it easier but i really should set up a csv with the active players
goalie_names = {
    64: "Campbell",
    28: "Desbiens",
    59: "Maschmeyer",
    6: "Frankel",
    22: "Hensley",
    41: "Levy",
    85: "Chuli",
    155: "Schroeder",
    70: "Howe",
    123: "Rooney",
    19: "Soderberg",
    48: "Abstreiter",
    154: "Post"
}

goalies_dict = {}
goalies = df_goals["goalie_id"].unique()
for goalie in goalies:
    goalies_dict[goalie] = df_goals[df_goals["goalie_id"]==goalie]
    goalies_dict[goalie].loc[:, "x_location"] = goalies_dict[goalie].loc[:, "x_location"].map(lambda x: do_math(x))

print(len(goalies_dict))

# this just gives me the background picture
map_image = mpimg.imread("extra-resources/images/ht-ice-rink-2.png")

fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(10, 7))

fig.suptitle("2024 Regular Season Shot Map Per Goalie", fontsize="x-large")

# go through each axes and set the size and the x/y ticks (remove them and the labels)
keys = list(goalies_dict.keys())
print(keys)
for i in range(len(goalies_dict)-4):
    if i <= 2:
        x_row = 0
    elif i <= 5:
        x_row = 1
    elif i <= 8:
        x_row = 2
    elif i <= 11:
        x_row = 3
    else:
        x_row = 4

    if i in [0, 3, 6, 9]:
        y_col = 0
    elif i in [1, 4, 7, 10, 12]:
        y_col = 1
    else:
        y_col = 2
    axes[x_row, y_col].set_xticks([],[])
    axes[x_row, y_col].set_yticks([],[])
    # print(goalies_dict[keys[i]].mode(axis=0, numeric_only=True))

    sns.kdeplot(ax=axes[x_row, y_col], data=goalies_dict[keys[i]], x="x_location", y="y_location", 
                cmap="rainbow", fill=True, alpha=0.8, thresh=0.1)\
                    .imshow(map_image, aspect="equal", zorder=-1)
    axes[x_row, y_col].set_title(f"{goalie_names[keys[i]]}: {len(goalies_dict[keys[i]])}")

# plt.tight_layout()
plt.savefig(f"images/goalie-shots-{round(datetime.datetime.today().timestamp())}.png")
# plt.show()
print(round(datetime.datetime.today().timestamp()))