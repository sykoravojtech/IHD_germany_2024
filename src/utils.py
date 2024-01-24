"""
utils.py

This file has general utility functions.
"""

import pandas as pd
import pycountry
from  constants.countries import highincome_countries
from typing import List

def generate_high_income_global_avg_index(df: pd.DataFrame, country_name_col: str = "Country Name",
                                          country_code_col: str = "Country Code", year_col='Year',
                                          add_series_name: bool = False,
                                          value_cols: List[str] = ['Value']
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
    if year_col is not None:
        df_highincome = df[is_high_income].groupby('Year')[value_cols].mean().reset_index()
    else:
        df_highincome = df[is_high_income][value_cols].mean().to_frame().T
    if add_series_name:
        df_highincome['Series Name'] = df['Series Name'].iloc[0]
    df_highincome[country_name_col] = 'High-income'
    df_highincome[country_code_col] = 'HIC'

    if year_col is not None:
        df_global = df.groupby('Year')[value_cols].mean().reset_index()
    else:
        df_global = df[value_cols].mean().to_frame().T

    if add_series_name:
        df_global['Series Name'] = df['Series Name'].iloc[0]
    df_global[country_name_col] = 'Global'
    df_global[country_code_col] = 'GLB'

    df_final = pd.concat([df, df_highincome, df_global])
    return df_final


invalid_country_mapping_gbd = {
    'Venezuela (Bolivarian Republic of)': 'Venezuela',
    'Republic of Moldova': 'Moldova',
    'Taiwan (Province of China)': 'Taiwan',
    'United Republic of Tanzania': 'Tanzania',
    'Micronesia (Federated States of)': 'Micronesia, Federated States of',
    'Iran (Islamic Republic of)': 'Iran',
    'Republic of Korea': 'South Korea',
    'Democratic People\'s Republic of Korea': 'North Korea',
    'United States Virgin Islands': 'Virgin Islands, U.S.',
    'Micronesia': 'Federated States of Micronesia',
    'Turkey': 'Türkiye',
    'United States of America': 'United States',
    'Palestine': 'Palestine, State of',
    'Democratic Republic of the Congo': 'Congo, The Democratic Republic of the',
    'Bolivia (Plurinational State of)': 'Bolivia'
}

def get_iso3_gbd(country: str) -> str:
    '''
        Get the iso3 country code by country name for GBD data. Use a custom mapping for
        some countries with non-standard names

        Args:
            country (str): name of the country
        
        Returns:
            string of length 3 representing the country code or None if exception
    '''
    if country == 'Global':
        return 'GLB'
    elif country == 'High-income':
        return 'HIC'
    if country in invalid_country_mapping_gbd:
        country = invalid_country_mapping_gbd[country]
    try:
        return pycountry.countries.get(name=country).alpha_3
    except:
        try:
            return pycountry.countries.get(common_name=country).alpha_3
        except:
            return None

mapping_invalid_countries_wdi = {
    "Bahamas, The": "Bahamas",
    "Bolivia": "Bolivia, Plurinational State of",
    "Channel Islands": "Jersey",
    "Congo, Dem. Rep.": "Congo, The Democratic Republic of the",
    "Congo, Rep.": "Congo",
    "Cote d'Ivoire": "Côte d'Ivoire",
    "Curacao": "Curaçao",
    "Egypt, Arab Rep.": "Egypt",
    "Gambia, The": "Gambia",
    "Hong Kong SAR, China": "Hong Kong",
    "Iran, Islamic Rep.": "Iran, Islamic Republic of",
    "Korea, Dem. People\'s Rep.": "Korea, Democratic People\'s Republic of",
    "Korea, Rep.": "Korea, Republic of",
    "Lao PDR": "Lao People\'s Democratic Republic",
    "Macao SAR, China": "Macao",
    "Micronesia, Fed. Sts.": "Micronesia, Federated States of",
    "Moldova": "Moldova, Republic of",
    "St. Kitts and Nevis": "Saint Kitts and Nevis",
    "St. Lucia": "Saint Lucia",
    "St. Martin (French part)": "Saint Martin (French part)",
    "St. Vincent and the Grenadines": "Saint Vincent and the Grenadines",
    "Tanzania": "Tanzania, United Republic of",
    "Turkiye": "Türkiye",
    "Venezuela, RB": "Venezuela, Bolivarian Republic of",
    "Virgin Islands (U.S.)": "Virgin Islands, U.S.",
    "Yemen, Rep.": "Yemen"
}

def get_iso3_wdi(country_name: str) -> str:
    '''
        Get the iso3 country code by country name for GBD data. Use a custom mapping for
        some countries with non-standard names

        Args:
            country (str): name of the country
        
        Returns:
            string of length 3 representing the country code or None if exception
    '''
    if country_name in mapping_invalid_countries_wdi.keys():
        country_name = mapping_invalid_countries_wdi[country_name]
    try:
        return pycountry.countries.get(name=country_name).alpha_3
    except:
        try:
            return pycountry.countries.get(official_name=country_name).alpha_3
        except:
            return None


def min_max_scaler(series: pd.Series, ep:float=1e-8) -> pd.Series:
    '''
        Scale the series by substracting the min and divided by the difference
        between the max and the min

        Args:
            series (pd.Series): pandas column to be transformed
            ep (float): a small amount to avoid dividing by 0
        
        Returns:
            series (pd.Series): the transformed series 
    '''
    _min = series.min()
    _max = series.max()
    return (series-_min)/(_max-_min+ep)