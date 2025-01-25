import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# basically just to have all shots mirrored on one side
# this isn't perfect bc some shots might be taken from across center ice, especially empty net goals
# but also the threshold will probably weed them out lmao
# i'm also stretching it to fit the image - it might not be real world accurate but it is good for display purposes
def do_math(x):
    if x <= 300:
        return round(x/300 * 322)
    else: 
        return round((x - 300)/300 * 322)

# get the data into a dataframe
# it is already nice and prepared for me!
# index_col=0 is because when i exported it, it ended up with an index already
# especially useful because this one doesn't have a column where all values are unique
pd_allshots = pd.read_csv("data/allshots_2024season.csv", index_col=0)
pd_goals = pd.read_csv("data/shotsgoals_2024season.csv", index_col=0)
pd_nongoals = pd.read_csv("data/shotsnongoals_2024season.csv", index_col=0)

# apply the do_math function with a lambda expression on each df
pd_allshots["x_location"] = pd_allshots["x_location"].map(lambda x: do_math(x))
pd_goals["x_location"] = pd_goals["x_location"].map(lambda x: do_math(x))
pd_nongoals["x_location"] = pd_nongoals["x_location"].map(lambda x: do_math(x))

print(pd_allshots["x_location"].max(axis=0))

# this just gives me the background picture
map_image = mpimg.imread("extra-resources/images/ht-ice-rink-2.png")

# set up the graph and make three subplots
fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(10, 4))

fig.suptitle("2024 Regular Season Shot Map", fontsize="x-large")

# go through each axes and set the size and the x/y ticks (remove them and the labels)
for i in range(3):
    axes[i].set_xticks([],[])
    axes[i].set_yticks([],[])

# graph it!
# ax is the plot, data/x/y are self explanatory, i want it filled in (heatmap look), coloured rainbow, 80% opacity with a threshold of 30%
# thresh explained here: https://seaborn.pydata.org/generated/seaborn.kdeplot.html
graph_allshots = sns.kdeplot(ax=axes[0], data=pd_allshots, x="x_location", y="y_location", fill=True, cmap="rainbow", alpha=0.8)
# show image with the image, aspect ratio is auto and order is -1 to send to back
graph_allshots.imshow(map_image,
                        aspect="equal",
                        zorder=-1
                    )
# give me a title :)
axes[0].set_title(f"All Shots: {len(pd_allshots)} data points")

# another graph
graph_goals = sns.kdeplot(ax=axes[1], data=pd_goals, x="x_location", y="y_location", fill=True, cmap="rainbow", alpha=0.8, thresh=0.2)
graph_goals.imshow(map_image,
                        aspect="equal",
                        zorder=-1
                    )
axes[1].set_title(f"All Goals: {len(pd_goals)} data points")

# and one last graph!
graph_nongoals = sns.kdeplot(ax=axes[2], data=pd_nongoals, x="x_location", y="y_location", fill=True, cmap="rainbow", alpha=0.8)
graph_nongoals.imshow(map_image,
                        aspect="equal",
                        zorder=-1
                    )
axes[2].set_title(f"All Non-Goals: {len(pd_nongoals)} data points")


plt.savefig(fname="shots-heatmap/shots-heatmap.png")
# i like how it looks with tight_layout, and then show it!
plt.tight_layout()
plt.show()


print(pd_goals)
