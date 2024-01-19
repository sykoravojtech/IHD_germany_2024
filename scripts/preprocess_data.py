import pandas as pd

import sys
sys.path.append('.')
from src import melt_all_year_cols_into_one, process_fat_consumption_data, process_IschemicHeartDisease_data

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
