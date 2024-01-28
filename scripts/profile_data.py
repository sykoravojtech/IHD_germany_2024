# %%
import os
import sys
from sys import platform
from pathlib import Path

import pandas as pd
import numpy as np
import seaborn as sns

# Add the parent directory to the sys.path (without this we cannot import constants or scripts)
sys.path.insert(0, '.')
from src.plotting import plot_comparison_GER_HIC_GLO
from constants.countries import highincome_countries
from src.utils import get_iso3_gbd

# %%
import matplotlib.pyplot as plt 

from tueplots import bundles
plt.rcParams.update(bundles.icml2022(column="full", ncols=1, nrows=1))

# %%
# if platform == 'darwin': # macos
#     print('mac os')
#     os.environ["PATH"] += os.pathsep + '/Library/TeX/texbin'

# %%
RAW_DATA_PATH = 'data/raw'
DATA_PATH = 'data/final'
OUTPUT_PATH = 'doc/IHD_germany_2024/fig'
cvd_data_path = f'{DATA_PATH}/gbd_cardiovascular_allAges_final.csv'
YEAR_COLUMN_NAME = 'year'
VALUE_COLUMN_NAME = 'val'

official_range = range(1990, 2020)

# %% [markdown]
# ## Load Data

# %%
df = pd.read_csv(cvd_data_path)
df = df[(df.measure_name=='Incidence') & (df['metric_name'] == 'Rate')]
df['country_code'] = df['location_name'].map(get_iso3_gbd)
df

# %%
df = df[['location_name', 'country_code', 'year', 'val']]
df.columns = ['Country Name', 'Country Code', 'Year', 'IHD']

# %%
print('======= GDB data ========')

# %%
print('Number of countries:', df['Country Code'].nunique())

# %%
print('GBD data year range:', df.Year.min(), df.Year.max())

# %%
print("Percentage missing data: ", df['IHD'].isna().mean())

# %% [markdown]
# ## Healthcare expenditure

# %%
year_cols = [str(i) for i in range(1960, 2023)]

# %%
health_df = pd.read_csv(f'{RAW_DATA_PATH}/health_expenditure.csv')
health_df = health_df.melt(id_vars=['Country Name', 'Country Code'], value_vars=year_cols, var_name='Year', value_name='HealthInd')
health_df['Year'] = health_df['Year'].astype(int)
health_df = health_df.drop(['Country Name'], axis=1)
# health_df = health_df.dropna()

# %%
print('======= Healthcare expenditure data ========')

# %%
print('Healthcare expenditure data year range:', health_df.Year.min(), health_df.Year.max())

# %%
print('Number of countries:', health_df['Country Code'].nunique())

# %%
print('% missing data:', health_df.HealthInd.isnull().mean())

# %%
print('% missing data from 1990 - 2019:', health_df[health_df.Year.isin(official_range)].HealthInd.isnull().mean())

# %% [markdown]
# ### GBD

# %%
global_burden_diseases = pd.read_csv(f'{RAW_DATA_PATH}/gbd_ischemicheartdiseaseglobal.csv')

# %%
print('======= IHD data ========')

# %%
gbd = global_burden_diseases[global_burden_diseases.measure_name == 'Deaths']

# %%
gbd.groupby('location_name').year.nunique().min()

# %%
print('IHD data year range:', gbd.year.min(), gbd.year.max())

# %%
print('Number of countries:', gbd['location_name'].nunique())

# %%
gbd.head()

# %%
print('% missing data:', gbd.val.isnull().mean())

# %%
# global_burden_diseases.isnull().mean()

# %% [markdown]
# ## Fat

# %%
def count_countries(series):
    print('Number of countries:', series.nunique())

def year_range(series):
    print('year range:', series.min(), series.max())

def count_missing(series):
    print('% missing data:', series.isnull().mean())

# %%
fat_df = pd.read_csv(DATA_PATH+'/daily_per_capita_fat_supply_final.csv')
fat_df = fat_df.rename({'Value': 'Fat'}, axis=1).drop(['Country Name', 'Series Name'], axis=1)

# %%
print('======= Fat consumption data ========')

# %%
count_countries(fat_df['Country Code'])
year_range(fat_df['Year'])
count_missing(fat_df[fat_df.Year.isin(official_range)]['Fat'])

# %%
fat_df

# %%


# %% [markdown]
# ## Alcohol

# %%
alc_df = pd.read_csv(f'{RAW_DATA_PATH}/alcohol_germany.csv')
alc_df = alc_df.rename({'Value': 'Alcohol'}, axis=1)
alc_df

# %%
print('======= Alcohol consumption data ========')

# %%
count_countries(alc_df['LOCATION'])
year_range(alc_df['TIME'])
count_missing(alc_df[alc_df.TIME.isin(official_range)]['Alcohol'])
alc_df[alc_df.TIME.isin(official_range)]['TIME'].unique()

# %% [markdown]
# ## Age

# %%
age_df = pd.read_csv(f'{RAW_DATA_PATH}/median-age.csv')
age_df = age_df[['Code', 'Year', 'Median age - Sex: all - Age: all - Variant: estimates']]
age_df.columns = ['Country Code', 'Year', 'Age']

# %%
print('======= Age data ========')

# %%
count_countries(age_df['Country Code'])
year_range(age_df['Year'])
count_missing(age_df[age_df.Year.isin(official_range)]['Age'])



