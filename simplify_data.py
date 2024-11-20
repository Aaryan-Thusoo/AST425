import numpy as np
import pandas as pd
import functions.reading as rd
from functions.numbering import spiral_confirmation

# Get the dr8_id of the Bar galaxies from Table3.csv
csv_pd = pd.read_csv("data/Table3.csv")
dr8_ids = csv_pd["dr8_id"].to_numpy()

# Open the parquet file
"""parq_data = rd.read_file("data/gz_desi_deep_learning_catalog_advanced.parquet")

wanted_rows, missing_rows = rd.get_rows(parq_data, dr8_ids)
wanted_rows.to_csv("galaxy_data/barred_galaxies.csv", index=False)"""

# region Looking for galaxies with confirmed spiral arms

wanted_rows = pd.read_csv("data/barred_galaxies.csv")

confirmed_spirals = spiral_confirmation(wanted_rows)

