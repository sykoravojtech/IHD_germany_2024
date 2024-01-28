import pandas as pd
import matplotlib.pyplot as plt

import sys
from pathlib import Path
# Add the parent directory to the sys.path (without this we cannot import constants or scripts)
print(Path.cwd())
sys.path.insert(0, str(Path.cwd()))
from src.plotting import plot_comparison_GER_HIC_GLO

DATA_PATH = 'data/final'
OUTPUT_PATH = 'doc/IHD_germany_2024/fig'
cvd_data_path = f'{DATA_PATH}/gbd_cardiovascular_allAges_final.csv'
YEAR_COLUMN_NAME = 'year'
VALUE_COLUMN_NAME = 'val'

df = pd.read_csv(cvd_data_path)
df = df[df['metric_name'] == 'Rate']

plot_comparison_GER_HIC_GLO(df=df, year_column=YEAR_COLUMN_NAME, value_column=VALUE_COLUMN_NAME, output_fig_path=f'{OUTPUT_PATH}/fig_cardiovascular_disease_rate.pdf',
                            title='Cardiovascular disease rate', country_column='location_name', indicator1='Incidence', 
                            indicator2='Deaths', indicator_column='measure_name', xlabel='Year', ylabel='Rate per 100,000')

plt.savefig(f'{OUTPUT_PATH}/fig_cardiovascular_disease_rate.jpg')