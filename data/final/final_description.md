# File structure
- description.md describes each data folder with all these points
  - source (website)
  - brief description of what it includes
  - explanation of the columns
  
## wdi_AlcoholConsumption.csv
- https://databank.worldbank.org/source/world-development-indicators/
  - raw/wdi_tobaccoalcohol_population.csv
- Gives information about Total alcohol consumption per capita (liters of pure alcohol, projected estimates, 15+ years of age)
- Data is for all countries for the years 2000-2019
- Missing data was removed
- Columns: Country Name,Country Code,Series Name,Year,Value

## daily_per_capita_fat_supply.csv
- Gives information about daily fat consumption per capita
- Region-level data was removed
- Columns: Country Name,Country Code,Series Name,Year,Value

## share-of-adults-who-smoke.csv
- nothing changed
- original description in raw_description.md

## gbd_cardiovascularglobal.csv
- Downloaded from the Global Burden of Disease website
- Gives information about incidence and death number, percent and rate for all countries 1990-2019
- Columns: measure_id, measure_name, location_id, location_name, sex_id, sex_name, age_id, age_name, cause_id, cause_name, metric_id, metric_name, year, val, upper, lower