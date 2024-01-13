"""
csv_data_manipulaltion.py

This file has general functions for manipulaiting data in csv files like melting columns into one.
"""

import pandas as pd
import numpy as np
from typing import Tuple


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
        replace_dots: True if want to replace '..' with zero
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

def process_fat_consumption_data(input_file, output_file='data/final/daily_per_capita_fat_supply_final.csv'):
    df = pd.read_csv(input_file)

    df.columns = ['Country Name', 'Country Code', 'Year' ,'Value']
    df['Series Name'] = 'Fat consumption per day per capita (grams)'

    df = df[['Country Name', 'Country Code', 'Series Name', 'Year', 'Value']]

    if output_file:
        df.to_csv(output_file, index=False)
        print(f"DataFrame saved to {output_file}")

    return df