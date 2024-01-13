"""
plotting.py

This file has general functions for plotting data used in the project.
"""

import pandas as pd
import matplotlib.pyplot as plt


def plot_value_per_year_GER_HIC_GLO(df: pd.DataFrame, ax: plt.axes = None, value_column: str = "Value", year_column: str = "Year", 
                                    country_column: str = "Country Name", xticks: int = None, output_fig_path: str = None,
                                    xlabel: str = "xlabel", ylabel: str = "ylabel", title: str = "title"
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
    
    Returns:
        None
    """

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))

    df = df.copy()
    plt.style.use('ggplot')

    # Explicitly set the face and edge color (GGPLOT was overridden)
    ax.set_facecolor('#f0f0f0')  # Light gray background color used in ggplot
    ax.grid(True, which='both', color='white', linestyle='-', linewidth=2)  # White grid lines

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
            ax.plot(curr_df[year_column], curr_df[value_column], label=region, color='red', linewidth=FOREGROUND_LINEWIDTH)
        elif region == 'Global':
            ax.plot(curr_df[year_column], curr_df[value_column], label=region, color='blue', linewidth=FOREGROUND_LINEWIDTH)
        elif region == 'High-income':
            ax.plot(curr_df[year_column], curr_df[value_column], label=region, color='green', linewidth=FOREGROUND_LINEWIDTH)
        else:
            ax.plot(curr_df[year_column], curr_df[value_column], color="gray", linewidth=BACKGROUND_LINEWIDTH, alpha=BACKGROUND_ALPHA)

    # Setting labels and titles
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    labels = ['Global', 'High income', 'Germany', "All countries"]
    handles = [plt.Line2D([], [], color='blue', linewidth=FOREGROUND_LINEWIDTH),
            plt.Line2D([], [], color='green', linewidth=FOREGROUND_LINEWIDTH),
            plt.Line2D([], [], color='red', linewidth=FOREGROUND_LINEWIDTH),
            plt.Line2D([], [], color='gray', linewidth=BACKGROUND_LINEWIDTH)]
    
    # Add the legend with 3 columns and 1 row
    plt.legend(handles, labels, bbox_to_anchor=(0.5, -0.12), loc='upper center', ncol=4)

    # Remove the border (spines) (GGPLOT was overridden)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    plt.tight_layout()

    if output_fig_path:
        plt.savefig(output_fig_path)