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