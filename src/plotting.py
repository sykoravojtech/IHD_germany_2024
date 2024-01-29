"""
plotting.py

This file has general functions for plotting data used in the project.
"""

from typing import List

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tueplots import bundles
from tueplots.constants.color import rgb
from matplotlib.colors import LinearSegmentedColormap


def plot_value_per_year_GER_HIC_GLO(df: pd.DataFrame, ax: plt.axes = None, value_column: str = "Value", year_column: str = "Year", 
                                    country_column: str = "Country Name", xticks: int = None, output_fig_path: str = None,
                                    xlabel: str = None, ylabel: str = None, title: str = None, legend: bool = True, code: bool = False
                                    ) -> None:
    """ 
    Plots the value of a column per year, with Germany, High-income countries and Global values highlighted.
    
    Args:
        df: dataframe, must have columns for value, year and country
        ax: axes to plot on, if None, creates a new figure
        value_column: column containing the values to plot
        year_column: column with years
        country_column: column with countries
        xticks: step size for year ticks, if None, ticks are not set
        output_fig_path: if given, saves the figure to this path
        xlabel: xlabel
        ylabel: ylabel
        title: title
        legend: if True, shows legend, if False, does not show legend
        code: if True, shows uses country codes instead of country names
    
    Returns:
        None
    """

    if ax is None:
        plt.rcParams.update(bundles.icml2022(column="half", ncols=1, nrows=2))
        _, ax = plt.subplots()

    if xticks is not None:
        # Set the x-axis ticks to show every 'xticks' years
        # Assuming 'Year' is an integer type column in df
        start_year = int(df[year_column].min())  # Find the minimum year in the dataset
        end_year = int(df[year_column].max())    # Find the maximum year in the dataset
        # print(f"{start_year=} {end_year=}")
        ax.set_xticks(range(start_year, end_year + 1, xticks))  # Set xticks to every 'xticks' years

    # Plotting lines
    FOREGROUND_LINEWIDTH = 2
    BACKGROUND_LINEWIDTH = 0.75
    BACKGROUND_ALPHA = 0.2
    for region in df[country_column].unique():
        curr_df = df[df[country_column] == region]
        ax.plot(curr_df[year_column], curr_df[value_column], color=rgb.tue_gray, linewidth=BACKGROUND_LINEWIDTH, alpha=BACKGROUND_ALPHA)
        
    for region in df[country_column].unique():
        curr_df = df[df[country_column] == region]
        if (region == 'Germany' and not code) or (region == 'DEU' and code):
            ax.plot(curr_df[year_column], curr_df[value_column], label=region, color=rgb.tue_red, linewidth=FOREGROUND_LINEWIDTH)
        elif (region == 'Global' and not code) or (region == 'GLB' and code):
            ax.plot(curr_df[year_column], curr_df[value_column], label=region, color=rgb.tue_blue, linewidth=FOREGROUND_LINEWIDTH)
        elif (region == 'High-income' and not code) or (region == 'HIC' and code):
            ax.plot(curr_df[year_column], curr_df[value_column], label=region, color=rgb.tue_orange, linewidth=FOREGROUND_LINEWIDTH)

    # Setting labels and titles
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    if title is not None:
        ax.set_title(title)
    
    ax.set_xlim([df[year_column].min(), df[year_column].max()])
    
    if legend:
        labels = ['Global', 'High income', 'Germany', "All countries"]
        handles = [plt.Line2D([], [], color=rgb.tue_blue, linewidth=FOREGROUND_LINEWIDTH),
                plt.Line2D([], [], color=rgb.tue_orange, linewidth=FOREGROUND_LINEWIDTH),
                plt.Line2D([], [], color=rgb.tue_red, linewidth=FOREGROUND_LINEWIDTH)]
                # plt.Line2D([], [], color='gray', linewidth=BACKGROUND_LINEWIDTH)]
        
        # Add the legend with 4 columns and 1 row
        plt.legend(handles, labels, loc='upper right', ncol=3)

    # Remove the border (spines) (GGPLOT was overridden)
    # ax.spines['top'].set_visible(False)
    # ax.spines['right'].set_visible(False)
    # ax.spines['bottom'].set_visible(False)
    # ax.spines['left'].set_visible(False)

    if output_fig_path:
        plt.savefig(output_fig_path)
        

def plot_comparison_GER_HIC_GLO(df: pd.DataFrame, value_column: str = "Value", year_column: str = "Year", 
                                country_column: str = "Country Name", indicator1: str = "Incidence", indicator2: str = "Deaths", 
                                indicator_column: str = "Measure" ,xticks: int = None, output_fig_path: str = None, 
                                xlabel: str = "xlabel", ylabel: str = "ylabel", title: str = "title"
                                ) -> None:
    """
    Uses the plot_value_per_year_GER_HIC_GLO function to plot three different visualizations of the same data.
    First one is for one indicator, second one is for the second indicator, third one is for the ratio of the two.
    
    Args:
        df: dataframe, must have columns for value, year and country
        value_column: column containing the values to plot
        year_column: column with years
        country_column: column with countries
        indicator1: label of first indicator
        indicator2: label of second indicator
        indicator_column: column with indicator labels
        xticks: step size for year ticks, if None, ticks are not set
        output_fig_path: if given, saves the figure to this path
        xlabel: xlabel
        ylabel: ylabel
        title: title
        
    Returns:
        None
    """
    
    plt.rcParams.update(bundles.icml2022(column="full", ncols=2, nrows=1))
    
    fig, ax = plt.subplots(1, 3)

    plot_value_per_year_GER_HIC_GLO(df[df[indicator_column] == indicator1], ax=ax[0], value_column=value_column, 
                                    year_column=year_column, country_column=country_column, xticks=xticks, xlabel=xlabel,
                                    ylabel=ylabel, title=indicator1, legend=False)
    plot_value_per_year_GER_HIC_GLO(df[df[indicator_column] == indicator2], ax=ax[1], value_column=value_column,
                                    year_column=year_column, country_column=country_column, xticks=xticks,
                                    xlabel=xlabel, title=indicator2, legend=False)
    
    # Step 1: Split the DataFrame into two DataFrames, one for each indicator
    deaths_df = df[df[indicator_column] == indicator2].rename(columns={value_column: value_column+"_1"})
    incidence_df = df[df[indicator_column] == indicator1].rename(columns={value_column: value_column+"_2"})

    # Step 2: Merge the DataFrames on 'year' and 'location_name'
    merged_df = pd.merge(deaths_df, incidence_df, on=[year_column, country_column])

    # Step 3: Calculate the ratio
    merged_df[value_column] = merged_df[value_column+"_1"] / merged_df[value_column+"_2"]

    # Step 4: Create the 'Ratio' measure_name and select relevant columns
    indicator_column_x = indicator_column + "_x"
    ratio_df = merged_df[[indicator_column_x, year_column, country_column, value_column]].copy()
    ratio_df[indicator_column_x] = 'Ratio'
    
    plot_value_per_year_GER_HIC_GLO(ratio_df, ax=ax[2], value_column=value_column, year_column=year_column, country_column=country_column,
                                    xticks=xticks, xlabel=xlabel,
                                    title=indicator2 + " / " + indicator1, legend=False)

    labels = ['Global', 'High income', 'Germany']
    linewidth = 5
    handles = [plt.Line2D([], [], color=rgb.tue_blue, linewidth=linewidth),
            plt.Line2D([], [], color=rgb.tue_orange, linewidth=linewidth),
            plt.Line2D([], [], color=rgb.tue_red, linewidth=linewidth)]
            # plt.Line2D([], [], color=rgb.tue_gray, linewidth=1)]

    # plt.subplots_adjust(top=0.85)  # Adjust the top spacing for the suptitle
    plt.suptitle(title)

    # Add the legend with 4 columns and 1 row
    # legend should be placed at the bottom of the figure, centered horizontally
    # under the subplots so it is visible
    fig.legend(handles, labels, loc='upper right', ncol=3)
    # plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), shadow=True, ncol=2)

    # set x and y label for the whole figure
    # fig.text(0.5, -0.04, 'Year', ha='center', fontsize=16)
    # fig.text(-0.015, 0.5, 'Rate', va='center', rotation='vertical', fontsize=16)

    if output_fig_path:
        plt.savefig(output_fig_path)


cmap_colors = [
    (0.0, rgb.tue_blue),
    (0.5, rgb.tue_orange),
    (1.0, rgb.tue_red)
]

# Create a colormap object
custom_cmap = LinearSegmentedColormap.from_list('custom_cmap', cmap_colors)


def bubble_plot_factors_and_rates(input_df:pd.DataFrame, x_col:str, y_col:str, size_col:str, hue_col:str, country_col:str,
                                x_label:str, y_label:str, size_label:str, hue_label:str,
                                title:str, output_path:str, 
                                white_list:List[str]=['Germany']):
    '''
    Make the bubble plots with 4 dimensions (x, y, bubble radius, hue)
    
    Args:
        input_df (pd.DataFrame): input dataframe contains 4 columns of values, 1 column for countries 
        x_col (str): name of the column in x dim
        y_col (str): name of the column in y dim
        size_col (str): name of the column in bubble size dim
        hue_col (str): name of the column in hue dim
        country_col (str): name of the column denoting country names
        x_label (str): label of x dim
        y_label (str): label of y dim
        size_label (str): label of bubble size dim
        hue_label (str): label of hue dim (color)
        title (str): title of the plot
        output_path (str): path to save the figure
        while_list (str): list of chosen countries the names of which to be displayed
    
    Returns:
        None
    '''
    df = input_df.copy()
    
    plt.rcParams.update(bundles.icml2022(column="full", ncols=2, nrows=1))
    
    # rescale for more distinguishible display
    df[size_col + '_rescaled'] = (df[size_col] - df[size_col].min() + 1) * 6 - 30

    # divide size values into size bins by percentile
    pct = [20, 60, 95]
    legend_sizes = np.percentile(df[size_col + '_rescaled'], pct) 
    def make_bin(x):
        if x < legend_sizes[0]:
                return legend_sizes[0]
        if x < legend_sizes[2]:
                return legend_sizes[1]
        return legend_sizes[2]
    df[size_col+'_bin'] = df[size_col + '_rescaled'].map(make_bin)

    scatter = plt.scatter(df[x_col], 
                        df[y_col], 
                        s=df[size_col+'_bin'],
                        alpha=0.4, c=df[hue_col], cmap=custom_cmap)

    # Add labels for the x and y axes
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    # Text position for countries
    annotation = {'Germany':[10, 10]}

    lookup = df.set_index(country_col)[hue_col].to_dict()

    blacklist = ['Iceland', 'South Africa', 'Croatia', 'United Kingdom', 'Brazil', 'Australia', 'Sweden',
                'Netherland', 'Argentina', 'Russian Federation', 'Lithuania', 'Bulgaria', 'Hungary', 'Luxembourg'
                ]
    
    for i, row in df.iterrows():
        size = 5
        if  row[country_col] in white_list:
                ann_point = annotation[row[country_col]]
                if row[country_col] in annotation:
                    plt.text(row[x_col]+1, 
                            row[y_col]+2500, 
                            s=row[country_col] + ': ' + str(round(lookup[row[country_col]])),
                            size=size, horizontalalignment='center',
                            verticalalignment='bottom')
                    plt.plot([row[x_col], row[x_col]+1], [row[y_col], row[y_col]+2500], color='gray', linewidth=0.5)
        elif row[country_col] not in blacklist:
            plt.text(row[x_col]-0.25, 
                    row[y_col]+0.5, 
                    s=row[country_col],
                    size=size)

    plt.scatter([12], [17], s=0.001)

    plt.colorbar(scatter, label=hue_label)

    legend_labels_int = [str(int(age)) for age in np.percentile(df[size_col], pct)]
    legend_labels = [None, None, None]
    legend_labels[0] = "under " + legend_labels_int[0]
    legend_labels[1] = "from " + legend_labels_int[0] + " to " + legend_labels_int[2]
    legend_labels[2] = "above " + legend_labels_int[2]

    # Create a list of legend entries
    legend_entries = [plt.scatter([], [], s=size, color='grey', label=label)
                    for label, size in zip(legend_labels, legend_sizes)]
    plt.legend(handles=legend_entries, title=size_label, ncol=3, loc='upper left')

    plt.title(title)

    plt.savefig(output_path)
    # plt.show()