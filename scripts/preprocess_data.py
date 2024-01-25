import pandas as pd

import sys
sys.path.append('.')
from src.csv_data_manipulation import (melt_all_year_cols_into_one, process_fat_consumption_data,
                 process_IschemicHeartDisease_data, process_OECD_data,
                 combine_OECD_health_indicators, process_cardiovascular_data)

# ============= Alcohol consumption data =============
INPUT_FILE = "data/raw/wdi_tobaccoalcohol_population.csv"
OUTPUT_FILE = "data/final/wdi_AlcoholConsumption.csv"

alcohol_df = melt_all_year_cols_into_one(
    input_file = INPUT_FILE, 
    output_file = OUTPUT_FILE,
    replace_dots = True,
    remove_nan = True,
    one_series = ("Series Name", "Total alcohol consumption per capita (liters of pure alcohol, projected estimates, 15+ years of age)"),
    remove_cols = ["Series Code"])
# =====================================================

# ================ Fat consumption data ===============
INPUT_FILE = "data/raw/daily_per_capita_fat_supply.csv"
OUTPUT_FILE = "data/final/daily_per_capita_fat_supply_final.csv"

fat_df = process_fat_consumption_data(INPUT_FILE, OUTPUT_FILE)
# ======================================================

# =========== GDB ischemic heart disease data ==========
INPUT_FILE = "data/raw/gbd_ischemicheartdiseaseglobal.csv"
OUTPUT_FILE = "data/final/gbd_IschemicHeartDisease_DeathsIncidence.csv"

IHD_df = process_IschemicHeartDisease_data(INPUT_FILE, OUTPUT_FILE)
# ======================================================


# ============= OECD health care data ===========
INPUT_FILE_1 = "data/raw/oecd_healthSpending.csv"
OUTPUT_FILE_1 = "data/final/oecd_healthSpending_final.csv"

INPUT_FILE_2 = "data/raw/oecd_hospitalBeds.csv"
OUTPUT_FILE_2 = "data/final/oecd_hospitalBeds_final.csv"

OUTPUT_COMBINED = "data/final/oecd_combined_final.csv"

process_OECD_data(INPUT_FILE_1, OUTPUT_FILE_1)

process_OECD_data(INPUT_FILE_2, OUTPUT_FILE_2)

# combine the above 2 health care factors
# - first standardize each factor
# - average them together to form a unified health care indicator
combine_OECD_health_indicators(OUTPUT_FILE_1, OUTPUT_FILE_2, OUTPUT_COMBINED, show_after_scaling=False)
# ======================================================


# ============= GBD cardiovascular disease data ===========
INPUT_FILE = "data/raw/gbd_cardiovascular.csv"
OUTPUT_FILE1 = "data/final/gbd_cardiovascular_allAges_final.csv"
OUTPUT_FILE_2 = "data/final/gbd_cardiovascular_ageRanges_final.csv"

process_cardiovascular_data(INPUT_FILE, OUTPUT_FILE1, OUTPUT_FILE_2)
# ==========================================================