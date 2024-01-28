import pandas as pd

import sys
from pathlib import Path
# Add the parent directory to the sys.path (without this we cannot import constants or scripts)
print(Path.cwd())
sys.path.insert(0, str(Path.cwd()))
from src.plotting import plot_value_per_year_GER_HIC_GLO
from src.utils import generate_high_income_global_avg_index
from constants.countries import country_code_to_name

import matplotlib.pyplot as plt
from tueplots import bundles
from tueplots.constants.color import rgb

DATA_PATH = 'data/final'
OUTPUT_PATH = 'doc/IHD_germany_2024/fig'
alcohol_data_path = 'data/raw/alcohol_germany.csv'
fat_data_path = 'data/raw/daily_per_capita_fat_supply.csv'
health_data_path = f'{DATA_PATH}/oecd_healthSpending_final.csv'

df = pd.read_csv(alcohol_data_path)
df['Country'] = df['LOCATION'].apply(lambda x: country_code_to_name[x])
df = generate_high_income_global_avg_index(df, country_name_col='Country', country_code_col='LOCATION', year_col='TIME', value_cols=['Value'])

plt.rcParams.update(bundles.icml2022(column="full", ncols=2, nrows=1))
    
fig, ax = plt.subplots(1, 3)

plot_value_per_year_GER_HIC_GLO(df, ax=ax[0], value_column='Value', 
                                year_column='TIME', country_column='LOCATION', xlabel='Year', ylabel='Liters per capita',
                                title='Alcohol Consumption', legend=False, code=True)

df = pd.read_csv(fat_data_path)
df = generate_high_income_global_avg_index(df, country_name_col='Entity', country_code_col='LOCATION', year_col='Year', value_cols=['Total'])

plot_value_per_year_GER_HIC_GLO(df, ax=ax[1], value_column='Total', 
                                year_column='Year', country_column='Entity', xlabel='Year', ylabel='Fat supply per capita (g/day)',
                                title='Fat Consumption', legend=False, code=False)

df = pd.read_csv(health_data_path)
df = generate_high_income_global_avg_index(df, country_name_col='Country Name', country_code_col='Country Code', year_col='Year', value_cols=['Value'])

plot_value_per_year_GER_HIC_GLO(df, ax=ax[2], value_column='Value', 
                                year_column='Year', country_column='Country Name', xlabel='Year', ylabel='USD per capita',
                                title='Health Expenditure', legend=False, code=False)


labels = ['Global', 'High income', 'Germany']
linewidth = 5
handles = [plt.Line2D([], [], color=rgb.tue_blue, linewidth=linewidth),
        plt.Line2D([], [], color=rgb.tue_orange, linewidth=linewidth),
        plt.Line2D([], [], color=rgb.tue_red, linewidth=linewidth)]
        # plt.Line2D([], [], color=rgb.tue_gray, linewidth=1)]

# # plt.subplots_adjust(top=0.85)  # Adjust the top spacing for the suptitle
plt.suptitle('Factor Analysis')

# # Add the legend with 4 columns and 1 row
# # legend should be placed at the bottom of the figure, centered horizontally
# # under the subplots so it is visible
fig.legend(handles, labels, loc='upper right', ncol=3)
# # plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), shadow=True, ncol=2)

# # set x and y label for the whole figure
# # fig.text(0.5, -0.04, 'Year', ha='center', fontsize=16)
# # fig.text(-0.015, 0.5, 'Rate', va='center', rotation='vertical', fontsize=16)

plt.savefig(f'{OUTPUT_PATH}/fig_factor_analysis.pdf')
plt.savefig(f'{OUTPUT_PATH}/fig_factor_analysis.jpg')