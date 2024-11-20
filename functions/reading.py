import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def read_file(filename, num_rows=None):
    if num_rows is None:
        return pd.read_parquet(filename, engine='pyarrow')
    else:
        return pd.read_parquet(filename).head(num_rows)


def slow_and_fast_setup():
    galaxy_data = pd.read_csv("data/barred_galaxies.csv", delimiter=",")
    kin_data = pd.read_csv("data/Table3.csv", delimiter=",")

    # Split kin_data between fast and slow bars
    slow_bars_kin_data = kin_data[kin_data["R"] > 1.4]
    fast_bars_kin_data = kin_data[kin_data["R"] <= 1.4]

    # ID for slow and fast bars
    slow_bars_id = np.array(slow_bars_kin_data["dr8_id"])
    fast_bars_id = np.array(fast_bars_kin_data["dr8_id"])

    # All galaxy_data for slow and fast bars

    slow_bars_galaxy_data, missing_slow = get_rows(galaxy_data, slow_bars_id)
    fast_bars_galaxy_data, missing_fast = get_rows(galaxy_data, fast_bars_id)

    return slow_bars_galaxy_data, fast_bars_galaxy_data

def get_rows(data, rows):
    # Get the matching rows 
    matching_rows = data[data['dr8_id'].isin(rows)]

    # Find the rows that were not found
    found_ids = set(matching_rows['dr8_id'])
    missing_ids = [row for row in rows if row not in found_ids]

    return matching_rows, missing_ids


def features_or_disk(data):
    return np.array([data["smooth-or-featured_smooth_fraction"],
                     data["smooth-or-featured_featured-or-disk_fraction"],
                     data["smooth-or-featured_artifact_fraction"]])

def edge_on_off(data):
    return np.array([data["disk-edge-on_yes_fraction"],
                     data["disk-edge-on_no_fraction"]])

def bar_strength(data):
    return np.array([data["bar_strong_fraction"],
                     data["bar_weak_fraction"],
                     data["bar_no_fraction"]])


def fraction_histogram(data, column, bins="sturges", range=(0, 1), axes_info=("TITLE", "X LABEL", "Y LABEL"),
                       savename=None):
    plt.figure()

    title, xlabel, ylabel = axes_info
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.hist(data[column], bins=bins, range=range)

    # Save the plot if savename is provided
    if savename:
        plt.savefig(savename)
    plt.show()
