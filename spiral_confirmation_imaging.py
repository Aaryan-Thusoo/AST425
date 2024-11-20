import pandas as pd
import wget
from astropy.io import fits
import matplotlib.pyplot as plt
from astropy.visualization import ZScaleInterval
import numpy as np
import os
from matplotlib.colors import LogNorm

def get_image_fits(galaxy, pixscale, bands, width, height):

    ra, dec = galaxy["ra"], galaxy["dec"]

    url = 'http://legacysurvey.org/viewer/fits-cutout?ra=' + str(ra) + '&dec=' + str(dec) + '&pixscale=' + str(
        pixscale) + '&layer=dr8&bands=' + str(bands) + '&width=' + str(width) + '&height=' + str(height)

    filename = "data/fits/" + galaxy["dr8_id"] + ".fits"

    # Download the file if it does not exist
    print("Downloading...")
    wget.download(url, out=filename)
    print("\nDownload complete.")

    return filename


def imaging_fits(file, frac_range):

    hdul = fits.open(file)
    header, data = hdul[0].header, hdul[0].data

    zscale = ZScaleInterval()
    vmin, vmax = zscale.get_limits(data)

    vmin = np.percentile(data, 0.1)  # 1st percentile
    vmax = np.percentile(data, 99) # 99th percentile

    plt.figure()
    plt.title(f"{file[10:-5]} {frac_range}")

    plt.imshow(data, origin='lower', cmap='gray', vmin=vmin, vmax=vmax)
    plt.show()


def get_galaxies_in_spiral_confirmation_range(galaxies, frac_min, frac_max):

    return galaxies[(galaxies["has-spiral-arms_yes_fraction"] >= frac_min) & (galaxies["has-spiral-arms_yes_fraction"] <= frac_max)]

if __name__ == "__main__":

    galaxy_data = pd.read_csv("data/barred_galaxies.csv")

    fraction_ranges = [(0.0, 0.2), (0.2, 0.3), (0.3, 0.4), (0.4, 0.5)]
    for f_range in fraction_ranges[0:1]:

        g_range = get_galaxies_in_spiral_confirmation_range(galaxy_data, f_range[0], f_range[1])

        g_range.reset_index(drop=False, inplace=True)

        for i in range(0, len(g_range[0:1])):
            file = get_image_fits(g_range.iloc[i], pixscale=0.262, width=100, height=100, bands="r")
            imaging_fits(file, f_range)
