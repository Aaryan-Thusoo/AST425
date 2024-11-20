import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# galaxy_data = pd.read_csv("data/barred_galaxies.csv", delimiter=",")

def bulge_number(galaxy):
    columns = ["bulge-size_dominant_fraction", "bulge-size_large_fraction", "bulge-size_moderate_fraction",
                     "bulge-size_small_fraction", "bulge-size_none_fraction"]
    dom, large, mod, small, none = galaxy[columns[0]], galaxy[columns[1]], galaxy[columns[2]], galaxy[columns[3]], galaxy[columns[4]]
    return dom + 0.8*large + 0.5*mod + 0.2*small + 0.0*none

def spiral_confirmation(galaxy):
    return np.array(galaxy["has-spiral-arms_yes_fraction"] >= 0.5)

def spiral_tightness_number(galaxy):
    spiral_tightness_columns = ["spiral-winding_tight_fraction", "spiral-winding_medium_fraction",
                                "spiral-winding_loose_fraction"]
    tight, mod, loose = galaxy[spiral_tightness_columns[0]], galaxy[spiral_tightness_columns[1]], galaxy[spiral_tightness_columns[2]]
    return tight + 0.5*mod



