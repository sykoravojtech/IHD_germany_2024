"""
utils.py

This file has general utility functions.
"""

import pandas as pd
from  constants.countries import highincome_countries

def generate_high_income_global_avg_index(df: pd.DataFrame, country_name_col: str = "Country Name",
                                          country_code_col: str = "Country Code", add_series_name: bool = False,
                                          value_col: str = "Value"
                                          ) -> pd.DataFrame:
    """
    Calculates average value for all countries combined and all high-income countries combined.
    Then adds it to the end of the DataFrame.

    Args:
        df: dataframe, must have columns for value, year and country
        country_col_name: label of column with country names
        country_code_col: label for column with country codes
        add_series_name: true if we want to add the series name
    
    Returns:
        DataFrame with all averages added.
    """
    is_high_income = df[country_name_col].isin(highincome_countries)
    df_highincome = df[is_high_income].groupby('Year')[value_col].mean().reset_index()
    if add_series_name:
        df_highincome['Series Name'] = df['Series Name'].iloc[0]
    df_highincome[country_name_col] = 'High-income'
    df_highincome[country_code_col] = 'HIC'

    df_global = df.groupby('Year')[value_col].mean().reset_index()
    if add_series_name:
        df_global['Series Name'] = df['Series Name'].iloc[0]
    df_global[country_name_col] = 'Global'
    df_global[country_code_col] = 'GLB'

    df_final = pd.concat([df, df_highincome, df_global])
    return df_final
