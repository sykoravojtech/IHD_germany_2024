import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
import os
from tueplots import bundles
from tueplots.constants.color import rgb

DATA_PATH = "../../../data/raw/"

# Create a linear segmented colormap
custom_cmap = LinearSegmentedColormap.from_list("tue_red_blue", [rgb.tue_red, rgb.tue_blue])
n_colors = 11  # You can adjust the number of colors in the palette
custom_colors = [custom_cmap(i / n_colors) for i in range(n_colors)]
tue_RB_palette = sns.color_palette(custom_colors)

# load csv data
cvd_data = pd.read_csv(DATA_PATH + "GBD_CVD_specific.csv")

# preprocess data & sort - get only germany, get only death rate, combine male and female numbers
ONLY_GERMANY = True
new_filtered_data = cvd_data[(cvd_data['metric'] == 'Rate') & (cvd_data['measure'] == 'Deaths')]
if ONLY_GERMANY:
    new_filtered_data = new_filtered_data[new_filtered_data['location'] == 'Germany']
new_impact_data = new_filtered_data.groupby('cause')['val'].sum().sort_values(ascending=False)

# bar plot
plt.rcParams.update(bundles.icml2022(column="half", ncols=2, nrows=1))
plt.rcParams["figure.figsize"] = (plt.rcParams["figure.figsize"][0], plt.rcParams["figure.figsize"][1]*2)
barplot = sns.barplot(x=new_impact_data.values, y=new_impact_data.index, palette=tue_RB_palette, orient='h')

# Remove the y-axis labels
plt.yticks([])

# Get the two largest cause indices for conditional labeling
top_two_indices = new_impact_data.nlargest(2).index

# Customize y-axis labels, placing them inside the bars for the top two causes and higher outside for the others
for i, bar in enumerate(barplot.patches):
    cause = new_impact_data.index[i]
    label_y_pos = bar.get_y() + bar.get_height() / 2

    if cause in top_two_indices:
        # Label inside the bar for top two causes
        label_x_pos = bar.get_width()*0.7   # Slightly inside the end of the bar
        label_color = 'white'
        ha_alignment = 'right'
    else:
        # Label outside the bar for other causes, to the right of the bar
        label_x_pos = bar.get_width() + (max(new_impact_data.values) * 0.01)  # Slightly outside the bar
        label_color = 'black'
        ha_alignment = 'left'

    plt.text(label_x_pos, label_y_pos,
             cause,
             va='center',
             ha=ha_alignment,
             color=label_color)
    
plt.title('Impact of Different Cardiovascular Diseases')
plt.xlabel('Death rate')
plt.ylabel('Cause of death')

plt.savefig("fig_ImpactOfDifferentCVDs.pdf")