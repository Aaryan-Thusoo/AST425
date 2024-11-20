import scipy.stats
import numpy as np
import pandas as pd
import scipy.stats as scs
from functions import reading as rd


def pval_to_sigma(pval):
    '''
    https://en.wikipedia.org/wiki/68%E2%80%9395%E2%80%9399.7_rule
    https://en.wikipedia.org/wiki/Standard_score

    Alternative: np.sqrt(2)*(special.erfinv(1-pval))
    '''

    temp = (1 - pval + 1) / 2
    sigma = scs.norm.ppf(temp)
    return sigma

# Set up
slow_bars_galaxy_data, fast_bars_galaxy_data = rd.slow_and_fast_setup()

# region Categories
categories = ["Bulge Intensity", "Spiral Tightness", "Spiral Confirmation"]

bulge_columns = ["bulge-size_dominant_fraction", "bulge-size_large_fraction", "bulge-size_moderate_fraction",
                 "bulge-size_small_fraction", "bulge-size_none_fraction"]
bulge_column_types = ["Dominant", "Large", "Moderate", "Small", "No"]

spiral_tightness_columns = ["spiral-winding_tight_fraction", "spiral-winding_medium_fraction", "spiral-winding_loose_fraction"]
spiral_column_types = ["Tight", "Medium", "Loose"]

spiral_confirmation_columns = ["has-spiral-arms_yes_fraction", "has-spiral-arms_no_fraction"]
spiral_confirmation_types = ["Yes", "No"]

columns_info = {"Spiral Confirmation": ["spiral_confirmation", spiral_confirmation_columns, spiral_confirmation_types],
                  "Bulge Intensity": ["bulge_intensity", bulge_columns, bulge_column_types],
                  "Spiral Tightness": ["spiral_tightness", spiral_tightness_columns, spiral_column_types]}

# endregion

for category in categories:

    file_name, column, column_type = columns_info[category]

    print(f"====={category}=====")

    for col, type in zip(column, column_type):

        stat, crit_val, p_val = scs.anderson_ksamp([slow_bars_galaxy_data[col], fast_bars_galaxy_data[col]])

        print(f"\tFor {type} {category} the p-value between slow and fast distributions is: {pval_to_sigma(p_val):.5} sigma\n")


