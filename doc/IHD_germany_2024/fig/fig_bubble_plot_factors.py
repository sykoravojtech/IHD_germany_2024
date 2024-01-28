import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

sys.path.append('.')

# Add the parent directory to the sys.path (without this we cannot import constants or scripts)
from src.utils import get_iso3_gbd, generate_high_income_global_avg_index
from src.plotting import bubble_plot_factors_and_rates

RAW_DATA_PATH = 'data/raw/'
DATA_PATH = 'data/final/'
OUTPUT_PATH = 'doc/IHD_germany_2024/fig'
cvd_data_path = f'{DATA_PATH}/gbd_cardiovascular_allAges_final.csv'
YEAR_COLUMN_NAME = 'year'
VALUE_COLUMN_NAME = 'val'


df = pd.read_csv(cvd_data_path)
df = df[df.measure_name=='Deaths']
df['country_code'] = df['location_name'].map(get_iso3_gbd)

df = df[['location_name', 'country_code', 'year', 'val']]
df.columns = ['Country Name', 'Country Code', 'Year', 'IHD']


year_cols = [str(i) for i in range(1960, 2023)]

health_df = pd.read_csv(RAW_DATA_PATH+'/health_expenditure.csv')
health_df = health_df.melt(id_vars=['Country Name', 'Country Code'], value_vars=year_cols, var_name='Year', value_name='HealthInd')
health_df['Year'] = health_df['Year'].astype(int)
health_df = health_df.drop(['Country Name'], axis=1)
health_df = health_df.dropna()
health_df.dropna()['Country Code'].nunique()


fat_df = pd.read_csv(DATA_PATH+'/daily_per_capita_fat_supply_final.csv')
fat_df = fat_df.rename({'Value': 'Fat'}, axis=1).drop(['Country Name', 'Series Name'], axis=1)


alc_df = pd.read_csv(RAW_DATA_PATH+'/alcohol_germany.csv')
alc_df = alc_df[['LOCATION', 'TIME', 'Value']]
alc_df.columns = ['Country Code', 'Year', 'Alcohol']


age_df = pd.read_csv(RAW_DATA_PATH+'/median-age.csv')
age_df = age_df[['Code', 'Year', 'Median age - Sex: all - Age: all - Variant: estimates']]
age_df.columns = ['Country Code', 'Year', 'Age']


final_df = df.merge(health_df, on=['Country Code', 'Year'])
final_df = final_df.merge(alc_df, on=['Country Code', 'Year'])
final_df = final_df.merge(age_df, on=['Country Code', 'Year'])


mean_df = final_df.groupby(['Country Name', 'Country Code'])[['IHD', 'HealthInd', 'Alcohol', 'Age']].last().reset_index()

output_fig_path = OUTPUT_PATH + '/fig_bubble_plot_factors.pdf'
bubble_plot_factors_and_rates(mean_df, x_col='Alcohol', y_col='HealthInd', size_col='Age', hue_col='IHD',
                            x_label='Alcohol consumption (liters/day)', y_label='Health expenditure (\\% GDP)',
                            size_label='Median population age', hue_label='Death rate (deaths per 100,000 habitants)',
                            country_col='Country Name',
                            title='Effect of alcohol consumption, health expenditure and median age on ischemic heart disease death rate, averaged from 1990 to 2019',
                            output_path=output_fig_path)

output_fig_path = OUTPUT_PATH + '/fig_bubble_plot_factors.jpg'
plt.savefig(output_fig_path)




