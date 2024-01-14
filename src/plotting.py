"""
plotting.py

This file has general functions for plotting data used in the project.
"""

import pandas as pd
import matplotlib.pyplot as plt
from tueplots import bundles
from tueplots.constants.color import rgb

plt.rcParams.update(bundles.beamer_moml())
plt.rcParams.update({"figure.dpi": 200})
plt.rcParams['font.family'] = 'DejaVu Sans'


def plot_value_per_year_GER_HIC_GLO(df: pd.DataFrame, ax: plt.axes = None, value_column: str = "Value", year_column: str = "Year", 
                                    country_column: str = "Country Name", xticks: int = None, output_fig_path: str = None,
                                    xlabel: str = "xlabel", ylabel: str = "ylabel", title: str = "title", legend: bool = True
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
    
    Returns:
        None
    """

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    df = df.copy()

    # Explicitly set the face and edge color (GGPLOT was overridden)
    # ax.set_facecolor('#f0f0f0')  # Light gray background color used in ggplot
    # ax.grid(True, which='both', color='white', linestyle='-', linewidth=2)  # White grid lines

    if xticks is not None:
        # Set the x-axis ticks to show every 'xticks' years
        # Assuming 'Year' is an integer type column in df
        start_year = int(df[year_column].min())  # Find the minimum year in the dataset
        end_year = int(df[year_column].max())    # Find the maximum year in the dataset
        # print(f"{start_year=} {end_year=}")
        ax.set_xticks(range(start_year, end_year + 1, xticks))  # Set xticks to every 'xticks' years

    # Plotting lines
    FOREGROUND_LINEWIDTH = 5
    BACKGROUND_LINEWIDTH = 1
    BACKGROUND_ALPHA = 0.3
    for region in df[country_column].unique():
        curr_df = df[df[country_column] == region]
        if region == 'Germany':
            ax.plot(curr_df[year_column], curr_df[value_column], label=region, color=rgb.tue_red, linewidth=FOREGROUND_LINEWIDTH)
        elif region == 'Global':
            ax.plot(curr_df[year_column], curr_df[value_column], label=region, color=rgb.tue_blue, linewidth=FOREGROUND_LINEWIDTH)
        elif region == 'High-income':
            ax.plot(curr_df[year_column], curr_df[value_column], label=region, color=rgb.tue_green, linewidth=FOREGROUND_LINEWIDTH)
        else:
            ax.plot(curr_df[year_column], curr_df[value_column], color=rgb.tue_gray, linewidth=BACKGROUND_LINEWIDTH, alpha=BACKGROUND_ALPHA)

    # Setting labels and titles
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    
    ax.set_xlim([df[year_column].min(), df[year_column].max()])
    
    if legend:
        labels = ['Global', 'High income', 'Germany', "All countries"]
        handles = [plt.Line2D([], [], color='blue', linewidth=FOREGROUND_LINEWIDTH),
                plt.Line2D([], [], color='green', linewidth=FOREGROUND_LINEWIDTH),
                plt.Line2D([], [], color='red', linewidth=FOREGROUND_LINEWIDTH),
                plt.Line2D([], [], color='gray', linewidth=BACKGROUND_LINEWIDTH)]
        
        # Add the legend with 4 columns and 1 row
        plt.legend(handles, labels, bbox_to_anchor=(0.5, -0.12), loc='upper center', ncol=4)

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
    
    fig, ax = plt.subplots(1, 3, figsize=(18, 6))

    plot_value_per_year_GER_HIC_GLO(df[df[indicator_column] == indicator1], ax=ax[0], value_column=value_column, 
                                    year_column=year_column, country_column=country_column, xticks=xticks, xlabel=xlabel,
                                    ylabel=ylabel, title=title + " " + indicator1, legend=False)
    plot_value_per_year_GER_HIC_GLO(df[df[indicator_column] == indicator2], ax=ax[1], value_column=value_column,
                                    year_column=year_column, country_column=country_column, xticks=xticks, xlabel=xlabel,
                                    ylabel=ylabel, title=title + " " + indicator2, legend=False)
    df = df.copy()
    df['Ratio'] = df[df[indicator_column] == indicator1][value_column].values / df[df[indicator_column] == indicator2][value_column].values
    plot_value_per_year_GER_HIC_GLO(df, ax=ax[2], value_column='Ratio', year_column=year_column, country_column=country_column,
                                    xticks=xticks, xlabel=xlabel, ylabel=ylabel, 
                                    title=title + " " + indicator1 + " / " + indicator2, legend=False)

    labels = ['Global', 'High income', 'Germany']
    handles = [plt.Line2D([], [], color=rgb.tue_blue, linewidth=5),
            plt.Line2D([], [], color=rgb.tue_green, linewidth=5),
            plt.Line2D([], [], color=rgb.tue_red, linewidth=5),
            plt.Line2D([], [], color=rgb.tue_gray, linewidth=1)]

    # plt.subplots_adjust(top=0.85)  # Adjust the top spacing for the suptitle
    plt.suptitle(title, fontsize=16, y=1.05)

    # Add the legend with 4 columns and 1 row
    # legend should be placed at the bottom of the figure, centered horizontally
    # under the subplots so it is visible
    fig.legend(handles, labels, loc='upper right', ncol=4, fontsize=12, bbox_to_anchor=(0.99, 1.075))
    # set x and y label for the whole figure
    fig.text(0.5, -0.04, 'Year', ha='center', fontsize=16)
    fig.text(-0.015, 0.5, 'Rate', va='center', rotation='vertical', fontsize=16)

    if output_fig_path:
        plt.savefig(output_fig_path)