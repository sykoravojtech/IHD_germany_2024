import pandas as pd
from  constants.countries import highincome_countries

def generate_high_income_global_avg_index(df):
    is_high_income = df['Country Name'].isin(highincome_countries)
    df_highincome = df[is_high_income].groupby('Year')['Value'].mean().reset_index()
    df_highincome['Series Name'] = df['Series Name'].iloc[0]
    df_highincome['Country Name'] = 'High-income'
    df_highincome['Country Code'] = 'HIC'

    df_global = df.groupby('Year')['Value'].mean().reset_index()
    df_global['Series Name'] = df['Series Name'].iloc[0]
    df_global['Country Name'] = 'Global'
    df_global['Country Code'] = 'GLB'

    df_final = pd.concat([df, df_highincome, df_global])
    return df_final