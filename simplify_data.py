import numpy as np
import pandas as pd
import functions.reading as rd

# Get the dr8_id of the Bar galaxies from Table3.csv
csv_pd = pd.read_csv("data/Table3.csv")
dr8_ids = csv_pd["dr8_id"].to_numpy()

#wanted = ['8000_100878_5809', '8000_101095_2828', '8000_101965_2933', '8000_103001_2364', '8000_103072_3496']

# Open the parquet file
parq_data = rd.read_file("data/gz_desi_deep_learning_catalog_advanced.parquet")

wanted_rows, missing_rows = rd.get_rows(parq_data, dr8_ids)
wanted_rows.to_csv("galaxy_data/barred_galaxies.csv", index=False)
