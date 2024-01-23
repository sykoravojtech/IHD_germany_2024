# File structure
- description.md describes each data folder with all these points
  - source (website)
  - brief description of what it includes
  - explanation of the columns
  
## wdi_tobaccoalcohol_population.csv
- https://databank.worldbank.org/source/world-development-indicators/
  - Country
    - select all
  - Series
    - Check "Series Name" column
  - Time
    - select all
- Gives information about tobacco use, alcohol consumption per capita, and percept of male and female population in age groups split by 5 year periods. There is also total population of males, of females, and combined.
- Data is for all countries for the years 1990-2019
- There is missing data and it is written as two dots '..'

## daily_per_capita_fat_supply.csv
- http://www.fao.org/faostat/en/#data/FBS
- The downloaded data is processed by "Our World in Data" website, and contains this information
  - Entity: Country or Region
  - Code: Country Code
  - Year
  - Total | 00002901 || Food available for consumption | 0684pc || grams of fat per day per capita: grams of consumed fat per day per capita
- Data is for all countries for the years 1961-2020
- There are also records of regions such as: Africa' 'Africa (FAO)' 'Americas (FAO)' 'Asia' 'Asia (FAO)', etc (to be dropped, we only analyze at country level)

## share-of-adults-who-smoke.csv
- Data source: World Health Organization (via World Bank)
  - https://ourworldindata.org/smoking
- The downloaded data is processed by "Our World in Data" website, and contains this information
  - Entity: Country or Region
  - Code: Country Code
  - Year
  - Prevalence of current tobacco use (% of adults)

## alcohol_germany.csv
- https://data.oecd.org/healthrisk/alcohol-consumption.htm
- Definition of Alcohol consumption
  - Alcohol consumption is defined as annual sales of pure alcohol in litres per person aged 15 years and older. Alcohol use is associated with numerous harmful health and social consequences, including an increased risk of a range of cancers, stroke and liver cirrhosis. Alcohol also contributes to death and disability through accidents and injuries, assault, violence, homicide and suicide. This indicator is measured in litres per capita (people aged 15 years and older).

## smoking_germany.csv
- https://data.oecd.org/healthrisk/daily-smokers.htm
- Daily smokers are defined as the population aged 15 years and over who are reporting to smoke every day. Smoking is a major risk factor for at least two of the leading causes of premature mortality - circulatory disease and cancer, increasing the risk of heart attack, stroke, lung cancer, and cancers of the larynx and mouth. In addition, smoking is an important contributing factor for respiratory diseases. This indicator is presented as a total and per gender and is measured as a percentage of the population considered (total, men or women) aged 15 years and over.

## oecd_healthSpending.csv
- https://data.oecd.org/healthres/health-spending.htm
- Health spending measures the final consumption of health care goods and services (i.e. current health expenditure) including personal health care (curative care, rehabilitative care, long-term care, ancillary services and medical goods) and collective services (prevention and public health services as well as health administration), but excluding spending on investments. Health care is financed through a mix of financing arrangements including government spending and compulsory health insurance (“Government/compulsory”) as well as voluntary health insurance and private funds such as households’ out-of-pocket payments, NGOs and private corporations (“Voluntary”). This indicator is presented as a total and by type of financing (“Government/compulsory”, “Voluntary”, “Out-of-pocket”) and is measured as a share of GDP, as a share of total health spending and in USD per capita (using economy-wide PPPs).
- Total, US dollars/capita, 1970 – 2022

## oecd_hospitalBeds.csv
- https://data.oecd.org/healtheqt/hospital-beds.htm
- This indicator provides a measure of the resources available for delivering services to inpatients in hospitals in terms of number of beds that are maintained, staffed and immediately available for use. Total hospital beds include curative (or acute) care beds, rehabilitative care beds, long-term care beds and other beds in hospitals. The indicator is presented as a total and for curative care and psychiatric care. It is measured in number of beds per 1 000 inhabitants.
- Total, Per 1 000 inhabitants, 1991 – 2022

## median-age.csv
- https://ourworldindata.org/grapher/median-age?tab=table&time=earliest..2020