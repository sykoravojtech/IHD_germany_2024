import pandas as pd
from sklearn.preprocessing import StandardScaler
from pathlib import Path
import sys
import seaborn as sns
import matplotlib.pyplot as plt

from tueplots import bundles
from tueplots.constants.color import rgb

from pathlib import Path
# Add the parent directory to the sys.path (without this we cannot import constants or scripts)
print(Path.cwd())
sys.path.insert(0, str(Path.cwd()))

from src.utils import get_iso3_gbd

DATA_PATH = "data/final/"
DATA_PATH_RAW = "data/raw/"
OUTPUT_PATH = 'doc/IHD_germany_2024/fig'

ihd_df = pd.read_csv(DATA_PATH + "gbd_IschemicHeartDisease_DeathsIncidence.csv")
ihd_df.rename(columns={'year': 'Year'}, inplace=True)
ihd_df = ihd_df[ihd_df['measure_name'] == 'Deaths']
ihd_df['Country Code'] = ihd_df['location_name'].apply(get_iso3_gbd)

fat_df = pd.read_csv(DATA_PATH + "daily_per_capita_fat_supply_final.csv")
fat_df = fat_df[(fat_df['Year'] >= 1990) & (fat_df['Year'] <= 2019)]

alcohol_df = pd.read_csv(DATA_PATH_RAW + "alcohol_germany.csv")
alcohol_df = alcohol_df[(alcohol_df["TIME"] >= 1990) & (alcohol_df["TIME"] <= 2019)]

healthSpending_df = pd.read_csv(DATA_PATH_RAW + "oecd_healthSpending.csv")

medianAge_df = pd.read_csv(DATA_PATH_RAW + "median-age.csv")
medianAge_df = medianAge_df[(medianAge_df['Year'] >= 1990) & (medianAge_df['Year'] <= 2019)]
medianAge_df.drop(columns=['Median age - Sex: all - Age: all - Variant: medium'], inplace=True)
medianAge_df.rename(columns={'Median age - Sex: all - Age: all - Variant: estimates': 'Median Age'}, inplace=True)

def add_alcohol(combined_df):
    alcohol_df_renamed = alcohol_df.rename(columns={'Value': 'Alcohol', "TIME": "Year", "LOCATION": "Country Code"})
    combined_df = combined_df.merge(alcohol_df_renamed[['Alcohol', 'Year', 'Country Code']], on=['Year', 'Country Code'], how='left')
    return combined_df

def add_fat(combined_df):
    fat_df_renamed = fat_df.rename(columns={'Value': 'Fat'})
    combined_df = combined_df.merge(fat_df_renamed[['Fat', 'Year', 'Country Code']], on=['Country Code', 'Year'], how='left')
    return combined_df

def add_healthSpending(combined_df):
    healthSpending_df_renamed = healthSpending_df.rename(columns={'Value': 'Health expenditure', 'TIME': 'Year', 'LOCATION': 'Country Code'})
    combined_df = combined_df.merge(healthSpending_df_renamed[['Health expenditure', 'Year', 'Country Code']], on=['Year', 'Country Code'], how='left')
    return combined_df

def add_medianAge(combined_df):
    medianAge_df_renamed = medianAge_df.rename(columns={'Code': 'Country Code'})
    combined_df = combined_df.merge(medianAge_df_renamed[['Median Age', 'Year', 'Country Code']], on=['Year', 'Country Code'], how='left')
    return combined_df

combined_df = ihd_df[['Value', 'Year', 'Country Code']].copy()
# combined_df = combined_df[combined_df['Country Code'].isin(country_codes)]
combined_df.rename(columns={"Value":'Death Rate'}, inplace=True)

independents = [add_medianAge, add_fat, add_alcohol, add_healthSpending]
for func in independents:
    combined_df = func(combined_df)  
    combined_df.dropna(inplace=True)
    
combined_df.dropna(inplace=True)
combined_df.drop(columns=['Year', 'Country Code'], inplace=True)
combined_df.reset_index(drop=True, inplace=True)

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Prepare the data for modeling
X = combined_df.drop('Death Rate', axis=1)  # independent variables
y = combined_df['Death Rate']  # dependent variable

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a pipeline with preprocessing and model
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('rf', RandomForestRegressor(random_state=42))
])

# Define a grid of hyperparameters to search
param_grid = {
    'rf__n_estimators': [100, 200, 300],
    'rf__max_depth': [None, 10, 20, 30],
    # Add other parameters here
}

# Use GridSearchCV to find the best parameters
grid_search = GridSearchCV(pipeline, param_grid, cv=5, n_jobs=-1, scoring='neg_mean_squared_error')
grid_search.fit(X_train, y_train)

# Get the best model
best_model = grid_search.best_estimator_

# Predict and evaluate using the best model
rf_pred = best_model.predict(X_test)
rf_mse = mean_squared_error(y_test, rf_pred)
rf_r2 = r2_score(y_test, rf_pred)

# Feature importances
importances = best_model.named_steps['rf'].feature_importances_
feature_names = X_train.columns
forest_importances = pd.Series(importances, index=feature_names).sort_values(ascending=False)

import shap
from tueplots import figsizes
from shap.plots import beeswarm
import numpy as np
import matplotlib.cm as cm
from shap.plots.colors import red_blue

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

# Standardize the data
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

plt.rcParams.update(bundles.icml2022(column="full", ncols=1, nrows=2))


X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns)

# Assuming best_model is your trained RandomForestRegressor from GridSearchCV
explainer = shap.TreeExplainer(best_model.named_steps['rf'])
shap_values = explainer(X_train_scaled)

beeswarm(shap_values, show=False, plot_size = figsizes.icml2022_full()['figure.figsize'], color_bar=False)

plt.rcParams.update(bundles.icml2022(column="full", ncols=1, nrows=2))
# ax.set_title('SHAP values summary')
# Formatting the plot
num_features = X_train_scaled.shape[1]
feature_order = np.argsort(np.sum(np.abs(explainer.shap_values(X_train_scaled)), axis=0))
plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=False  # labels along the bottom edge are off
)
plt.gca().spines['right'].set_visible(True)
plt.gca().spines['top'].set_visible(True)
plt.gca().spines['left'].set_visible(True)
plt.yticks([])
plt.yticks(range(num_features))
plt.title('SHAP values summary', fontsize=14)
plt.gca().set_xlabel('SHAP value (impact on model output)')
plt.grid(True, axis='x', linestyle='--', alpha=0.5)
       
m = cm.ScalarMappable(cmap=red_blue)
m.set_array([0, 1])
cb = plt.colorbar(m, ax=plt.gca(), ticks=[0, 1], aspect=20)
cb.set_ticklabels(['Low', 'High'], fontsize=9)
cb.set_label('Feature Value', labelpad=0, fontsize=11)
cb.ax.tick_params(length=0)
cb.set_alpha(1)
cb.outline.set_visible(False)
plt.savefig(f'{OUTPUT_PATH}/fig_shap_values_summary.pdf')
plt.savefig(f'{OUTPUT_PATH}/fig_shap_values_summary.jpg')

