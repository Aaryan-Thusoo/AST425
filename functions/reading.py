import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def read_file(filename, num_rows=None):
    if num_rows is None:
        return pd.read_parquet(filename, engine='pyarrow')
    else:
        return pd.read_parquet(filename).head(num_rows)

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
