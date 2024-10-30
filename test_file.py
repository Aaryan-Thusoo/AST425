import functions.reading as rd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# region Set up
galaxy_data = pd.read_csv("data/barred_galaxies.csv", delimiter=",")
kin_data = pd.read_csv("data/Table3.csv", delimiter=",")

# Split kin_data between fast and slow bars
slow_bars_kin_data = kin_data[kin_data["R"] > 1.4]
fast_bars_kin_data = kin_data[kin_data["R"] <= 1.4]

# ID for slow and fast bars
slow_bars_id = np.array(slow_bars_kin_data["dr8_id"])
fast_bars_id = np.array(fast_bars_kin_data["dr8_id"])

# All galaxy_data for slow and fast bars

slow_bars_galaxy_data, missing_slow = rd.get_rows(galaxy_data, slow_bars_id)
fast_bars_galaxy_data, missing_fast = rd.get_rows(galaxy_data, fast_bars_id)

save_dir = "plots/histograms/"

# endregion

# region Categories
categories = ["Bulge Intensity", "Spiral Tightness"]

bulge_columns = ["bulge-size_dominant_fraction", "bulge-size_large_fraction", "bulge-size_moderate_fraction",
                 "bulge-size_small_fraction", "bulge-size_none_fraction"]
bulge_column_types = ["Dominant", "Large", "Moderate", "Small", "No"]

spiral_tightness_columns = ["spiral-winding_tight_fraction", "spiral-winding_medium_fraction", "spiral-winding_loose_fraction"]
spiral_column_types = ["Tight", "Medium", "Loose"]

histogram_info = {"Bulge Intensity": ["bulge_intensity", bulge_columns, bulge_column_types],
                  "Spiral Tightness": ["spiral_tightness", spiral_tightness_columns, spiral_column_types]}

# endregion

for category in categories:

    file_name, column, column_type = histogram_info[category]

    print(f"====={category}=====")

    for col, type in zip(column, column_type):

        # region Plotting Histograms of Slow and Fast
        plt.figure()
        plt.hist(slow_bars_galaxy_data[col], range=(0, 1), density=True, label="Slow", bins=20, color="blue")
        plt.hist(fast_bars_galaxy_data[col], range=(0, 1), density=True, label="Fast", bins=20, alpha=0.5,
                 color="orange")
        plt.legend()
        plt.title(f"{type} {category} Size Fraction")
        plt.savefig(f"plots/histograms/{file_name}/{type}_bulge.png")
        # endregion

        # region Printing Statistics
        print(f"\t====={type.capitalize()} {category}=====")

        slow_median = np.median(slow_bars_galaxy_data[col])
        fast_median = np.median(fast_bars_galaxy_data[col])

        median_diff =  slow_median - fast_median
        median_percentage = median_diff / slow_median * 100
        print(f"\t\tMedian:"
              f"\n\t\t\tSlow: {slow_median}"
              f"\n\t\t\tFast: {fast_median}"
              f"\n\t\t\tDifference: {median_diff} ({median_percentage}%)\n")


        slow_mean = np.mean(slow_bars_galaxy_data[col])
        fast_mean = np.mean(fast_bars_galaxy_data[col])
        mean_diff = slow_mean - fast_mean
        mean_percentage = mean_diff / slow_mean * 100

        print(f"\t\tMean"
              f"\n\t\t\tSlow: {slow_mean}"
              f"\n\t\t\tFast: {fast_mean}"
              f"\n\t\t\tDifference: {mean_diff} ({mean_percentage}%)\n")

        slow_std = np.std(slow_bars_galaxy_data[col])
        fast_std = np.std(fast_bars_galaxy_data[col])
        std_diff = slow_std - fast_std
        std_percentage = std_diff / slow_std * 100

        print(f"\t\tStandard Deviation"
              f"\n\t\t\tSlow: {slow_std}"
              f"\n\t\t\tFast: {fast_std}"
              f"\n\t\t\tDifference: {std_diff} ({std_percentage}%)\n")

        slow_25 = np.percentile(slow_bars_galaxy_data[col], 25)
        fast_25 = np.percentile(fast_bars_galaxy_data[col], 25)
        diff_25 = slow_25 - fast_25
        percentage_25 = diff_25 / slow_25 * 100

        print(f"\t\t25th Percentile"
              f"\n\t\t\tSlow: {slow_25}"
              f"\n\t\t\tFast: {fast_25}"
              f"\n\t\t\tDifference: {diff_25} ({percentage_25}%)\n")

        slow_75 = np.percentile(slow_bars_galaxy_data[col], 75)
        fast_75 = np.percentile(fast_bars_galaxy_data[col], 75)
        diff_75 = slow_75 - fast_75
        percentage_75 = diff_75 / slow_75 * 100

        print(f"\t\t75th Percentile"
              f"\n\t\t\tSlow: {percentage_75}"
              f"\n\t\t\tFast: {percentage_75}"
              f"\n\t\t\tDifference: {diff_75} ({percentage_75}%)\n")
        # endregion
