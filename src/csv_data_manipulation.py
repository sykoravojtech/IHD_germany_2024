"""
csv_data_manipulaltion.py

This file has general functions for manipulaiting data in csv files like melting columns into one.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple
from constants.countries import country_code_to_name

import sys
sys.path.append('.')

from src.utils import min_max_scaler, get_iso3_gbd

def melt_all_year_cols_into_one(input_file: str = None, df: pd.DataFrame = None, output_file: str = None, replace_dots: bool = False, 
                                remove_nan: bool = False, one_series: Tuple[str,str] = (), remove_cols: Tuple[str] = ()
                                ) -> pd.DataFrame:
    """
    Some datasets have one column for each year of data.
    This function changes the dataset so that there is one year column and one data column instead of columns for each year.

    Args:
        input_file: if no dataframe is given, the function will load the dataframe from this file
        output_file: if given, saves the dataframe to this file
        df: dataframe
        replace_dots: True if want to replace '..' with NaN
        remove_nan: removes all rows with NaN in Value column 
        one_series: (Column name, value name) - the rows of this value will be othe only ones that stay in the dataframe
        remove_cols: list of columns to remove

    Returns:
        The melted dataset 
    """
    
    if not df:
        if not input_file:
            print("No input file or dataframe given")
            return None
        else:
            print(f"Loading {input_file}")
            df = pd.read_csv(input_file)

    if remove_cols:
        print(f"Removing cols {remove_cols}")
        df.drop(remove_cols, axis=1, inplace=True)

    if one_series:
        print(f"Leaving only '{one_series[1]}' in '{one_series[0]}'")
        df = df[df[one_series[0]] == one_series[1]]

    # Correct the column names for the melting process
    year_columns = [col for col in df.columns if col.endswith(']')]
    # We'll use all columns except the year-specific columns as id_vars
    id_vars = [col for col in df.columns if col not in year_columns]

    # Melt the dataframe again with the corrected id_vars
    VALUE_COLUMN_NAME = "Value"
    YEAR_COLUMMN_NAME = "Year"
    melted_df = df.melt(id_vars=id_vars, 
                                    value_vars=year_columns, 
                                    var_name=YEAR_COLUMMN_NAME, 
                                    value_name=VALUE_COLUMN_NAME)

    # Extract the year number from the 'Year' column
    melted_df[YEAR_COLUMMN_NAME] = melted_df[YEAR_COLUMMN_NAME].str.extract('(\d{4})')

    if replace_dots:
        melted_df[VALUE_COLUMN_NAME] = melted_df[VALUE_COLUMN_NAME].replace("..", np.nan)
        melted_df[VALUE_COLUMN_NAME] = pd.to_numeric(melted_df[VALUE_COLUMN_NAME], errors='coerce')

    if remove_nan:
        melted_df.dropna(subset=[VALUE_COLUMN_NAME], inplace=True)

    if output_file:
        melted_df.to_csv(output_file, index=False)
        print(f"DataFrame saved to {output_file}")

    return melted_df

def process_fat_consumption_data(input_file:str, 
                                output_file:str='data/final/daily_per_capita_fat_supply_final.csv') -> pd.DataFrame:
    """
    Process global fat consumption data

    Args:
        input_file: path to the raw csv file
        output_file: path to save the processed data

    Returns:
        The final dataframe
    """
    df = pd.read_csv(input_file)

    df.columns = ['Country Name', 'Country Code', 'Year' ,'Value']
    df['Series Name'] = 'Fat consumption per day per capita (grams)'

    df = df[['Country Name', 'Country Code', 'Series Name', 'Year', 'Value']]

    if output_file:
        df.to_csv(output_file, index=False)
        

    return df


def process_IschemicHeartDisease_data(input_file: str = "data/raw/gbd_ischemicheartdiseaseglobal.csv", 
                            output_file: str = "data/final/gbd_IschemicHeartDisease_DeathsIncidence.csv"
                            ) -> pd.DataFrame:
    """
    Process global Ischemic Heart Disease data

    Args:
        input_file: 
        output_file: 

    Returns:
        final dataframe
    """
    df = pd.read_csv(input_file)
    df = df[df['age_name']=="All ages"].copy()
    df.drop(columns=['measure_id', 'location_id', 'sex_id', 'sex_name', 'metric_id', 'metric_name', 'age_id', 'age_name', 'cause_id'], inplace=True)
    df.rename(columns={'val': 'Value'}, inplace=True)
    if output_file:
        df.to_csv(output_file, index=False)
        print(f"DataFrame saved to {output_file}")
        
    return df


def process_OECD_data(input_file: str, output_file: str) -> pd.DataFrame:
    """
    Process OECD health indicator data. Get country names using country ISO 3 codes

    Args:
        input_file: path to the raw csv file
        output_file: path to save the processed data

    Returns:
        The final dataframe
    """
    df = pd.read_csv(input_file)
    df['NAME'] = df['LOCATION'].map(country_code_to_name)
    df = df[['NAME', 'LOCATION', 'INDICATOR', 'TIME', 'Value']]
    df.columns = ['Country Name', 'Country Code', 'Series Name', 'Year', 'Value']

    if output_file:
        df.to_csv(output_file, index=False)
        print(f"DataFrame saved to {output_file}")

    return df


def combine_OECD_health_indicators(input_file1:str, input_file2:str, output_file,
                                    show_after_scaling=True) -> pd.DataFrame:
    '''
        Combine 2 health care indicators to obtain a unified one by using non-weighted mean of scaled values
        
        Args:
            input_file1: path to the raw csv file 1
            input_file2: path to the raw csv file 2
            output_file: path to save the combined data
            show_after_scaling: whether to visualize the distributions of the 2 scaled factors
        
        Returns:
            The dataframe with the combined value column
    '''
    USED_COLS = ['Country Name', 'Country Code', 'Year', 'Value']
    healthSpending_df = pd.read_csv(input_file1)
    beds_df = pd.read_csv(input_file2)
    health_df = healthSpending_df[USED_COLS].merge(beds_df[USED_COLS], on=['Country Code', 'Country Name',  'Year'], suffixes=['HealthExp', 'Beds'])
    health_df['ValueHealthExpNorm'] = min_max_scaler(health_df['ValueHealthExp'])
    health_df['ValueBedsNorm'] = min_max_scaler(health_df['ValueBeds'])
    health_df['Value'] = (health_df['ValueHealthExpNorm'] + health_df['ValueBedsNorm'] ) / 2

    if show_after_scaling:
        plt.figure(figsize=(15,5))
        plt.subplot(1,3,1)
        plt.boxplot(health_df['ValueHealthExpNorm'], showfliers=False)
        plt.title('Health expenditure per capita in USD')
        plt.subplot(1,3,2)
        plt.boxplot(health_df['ValueBedsNorm'], showfliers=False)
        plt.title('Number of hospital beds per 1000 habitants')
        plt.subplot(1,3,3)
        plt.boxplot(health_df['Value'], showfliers=False)
        plt.title('Combined indicator')
        plt.show()

    health_df = health_df.drop(['ValueHealthExp', 'ValueHealthExpNorm', 'ValueBeds', 'ValueBedsNorm'], axis=1)
    health_df['Series Name'] = 'Combined Health Indicator'
    health_df = health_df[['Country Name', 'Country Code', 'Series Name', 'Year', 'Value']]
    if output_file:
        health_df.to_csv(output_file, index=False)
        print(f"DataFrame saved to {output_file}")
    return health_df


def process_cardiovascular_data(input_file: str, output_file1: str, output_file2: str) -> (pd.DataFrame, pd.DataFrame):
    """
    Process cardiovascular disease data from GBD. Get country names using country ISO 3 codes.
    Divide the data into 2 dataframes: one for all ages and one for age ranges.
    
    Args:
        input_file: path to the raw csv file
        output_file1: path to save the processed data for all ages
        output_file2: path to save the processed data for age ranges
    
    Returns:
        The final dataframes
    """
    
    input_df = pd.read_csv(input_file)
    input_df.drop(columns=['measure_id' ,'location_id', 'sex_id', 'sex_name', 'age_id', 'cause_id', 'metric_id', 'upper', 'lower', 'cause_name'], inplace=True)
    
    # measure_id,measure_name,location_id,location_name,sex_id,sex_name,age_id,age_name,cause_id,cause_name,metric_id,metric_name,year,val,upper,lower
    all_ages_df = input_df[input_df['age_name'] == 'All ages'].copy()
    all_ages_df.drop(columns=['age_name'], inplace=True)
    all_ages_df['Country Code'] = all_ages_df['location_name'].map(get_iso3_gbd)
    
    if output_file1:
        all_ages_df.to_csv(output_file1, index=False)
        print(f"DataFrame saved to {output_file1}")
    
    age_ranges_df = input_df[input_df['age_name'] != 'All Ages'].copy()
    age_ranges_df = age_ranges_df[(age_ranges_df['location_name'] == 'Global') | 
                                  (age_ranges_df['location_name'] == 'High-income') | 
                                  (age_ranges_df['location_name'] == 'Germany')] 
    
    if output_file2:
        age_ranges_df.to_csv(output_file2, index=False)
        print(f"DataFrame saved to {output_file2}")
    
    return all_ages_df, age_ranges_df
    
    