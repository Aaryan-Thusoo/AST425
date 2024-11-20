####
# Functions obtained from GitHub Sandor: https://github.com/sandorkruk/DeCALS_south_images
####

from PIL import Image
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from astropy.io import fits
import wget
import numpy as np
import os

def make_png_from_fits(fits_loc, png_loc, png_size):
    '''
    Create png from multi-band fits
    Args:
        fits_loc (str): location of .fits to create png from
        png_loc (str): location to save png
    Returns:
        None
    '''
    try:
        img, hdr = fits.getdata(fits_loc, 0, header=True)
    except Exception:
        warnings.warn('Invalid fits at {}'.format(fits_loc))
    else:  # if no exception getting image

        # TODO wrap?

            # Set parameters for RGB image creation
        _scales = dict(
            g=(2, 0.008),
            r=(1, 0.014),
            z=(0, 0.019))
        _mnmx = (-0.5, 300)

        rgbimg = dr2_style_rgb(
            (img[0, :, :], img[1, :, :], img[2, :, :]),
            'grz',
            mnmx=_mnmx,
            arcsinh=1.,
            scales=_scales,
            desaturate=True)
        save_carefully_resized_png(png_loc, rgbimg, target_size=png_size)
        
def dr2_style_rgb(imgs, bands, mnmx=None, arcsinh=None, scales=None, desaturate=False):
    '''
    Given a list of image arrays in the given bands, returns a scaled RGB image.
    Originally written by Dustin Lang and used by Kyle Willett for DECALS DR1/DR2 Galaxy Zoo subjects
    Args:
        imgs (list): numpy arrays, all the same size, in nanomaggies
        bands (list): strings, eg, ['g','r','z']
        mnmx (min,max), values that will become black/white *after* scaling. Default is (-3,10)):
        arcsinh (bool): if True, use nonlinear scaling (as in SDSS)
        scales (str): Override preset band scaling. Dict of form {band: (plane index, scale divider)}
        desaturate (bool): If [default=False] desaturate pixels dominated by a single colour
    Returns:
        (np.array) of shape (H, W, 3) with values between 0 and 1 of pixel values for colour image
    '''

    bands = ''.join(bands)  # stick list of bands into single string

    # first number is index of that band
    # second number is scale divisor - divide pixel values by scale divisor for rgb pixel value
    grzscales = dict(
        g=(2, 0.0066),
        r=(1, 0.01385),
        z=(0, 0.025),
    )

    if scales is None:
        if bands == 'grz':
            scales = grzscales
        elif bands == 'urz':
            scales = dict(
                u=(2, 0.0066),
                r=(1, 0.01),
                z=(0, 0.025),
            )
        elif bands == 'gri':
            scales = dict(
                g=(2, 0.002),
                r=(1, 0.004),
                i=(0, 0.005),
            )
        else:
            scales = grzscales

    #  create blank matrix to work with
    h, w = imgs[0].shape
    rgb = np.zeros((h, w, 3), np.float32)

    # Copy each band matrix into the rgb image, dividing by band scale divisor to increase pixel values
    for im, band in zip(imgs, bands):
        plane, scale = scales[band]
        rgb[:, :, plane] = (im / scale).astype(np.float32)

    # TODO mnmx -> (min, max)
    # cut-off values for non-linear arcsinh map
    if mnmx is None:
        mn, mx = -3, 10
    else:
        mn, mx = mnmx

    if arcsinh is not None:
        # image rescaled by single-pixel not image-pixel, which means colours depend on brightness
        rgb = nonlinear_map(rgb, arcsinh=arcsinh)
        mn = nonlinear_map(mn, arcsinh=arcsinh)
        mx = nonlinear_map(mx, arcsinh=arcsinh)

    # lastly, rescale image to be between min and max
    rgb = (rgb - mn) / (mx - mn)

    # default False, but downloader sets True
    if desaturate:
        # optionally desaturate pixels that are dominated by a single
        # colour to avoid colourful speckled sky

        # reshape rgb from (h, w, 3) to (3, h, w)
        RGBim = np.array([rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]])
        a = RGBim.mean(axis=0)  # a is mean pixel value across all bands, (h, w) shape
        # putmask: given array and mask, set all mask=True values of array to new value
        np.putmask(a, a == 0.0, 1.0)  # set pixels with 0 mean value to mean of 1. Inplace?
        acube = np.resize(a, (3, h, w))  # copy mean value array (h,w) into 3 bands (3, h, w)
        bcube = (RGBim / acube) / 2.5  # bcube: divide image by mean-across-bands pixel value, and again by 2.5 (why?)
        mask = np.array(bcube)  # isn't bcube already an array?
        wt = np.max(mask, axis=0)  # maximum per pixel across bands of mean-band-normalised rescaled image
        # i.e largest relative deviation from mean
        np.putmask(wt, wt > 1.0, 1.0)  # clip largest allowed relative deviation to one (inplace?)
        wt = 1 - wt  # invert relative deviations
        wt = np.sin(wt*np.pi/2.0)  # non-linear rescaling of relative deviations
        temp = RGBim * wt + a*(1-wt) + a*(1-wt)**2 * RGBim  # multiply by weights in complicated fashion
        rgb = np.zeros((h, w, 3), np.float32)  # reset rgb to be blank
        for idx, im in enumerate((temp[0, :, :], temp[1, :, :], temp[2, :, :])):  # fill rgb with weight-rescaled rgb
            rgb[:, :, idx] = im

    clipped = np.clip(rgb, 0., 1.)  # set max/min to 0 and 1
    
    #print(clipped)

    return clipped

def nonlinear_map(x, arcsinh=1.):
    """
    Apply non-linear map to input matrix. Useful to rescale telescope pixels for viewing.
    Args:
        x (np.array): array to have map applied
        arcsinh (np.float):
    Returns:
        (np.array) array with map applied
    """
    return np.arcsinh(x * arcsinh)


def save_carefully_resized_png(png_loc, native_image, target_size):
    """
    # TODO
    Args:
        png_loc ():
        native_image ():
        target_size ():
    Returns:
    """
    native_pil_image = Image.fromarray(np.uint8(native_image * 255.), mode='RGB')
    nearest_image = native_pil_image.resize(size=(target_size, target_size), resample=Image.LANCZOS)
    nearest_image = nearest_image.transpose(Image.FLIP_TOP_BOTTOM)  # to align with north/east
    nearest_image.save(png_loc)


def create_image_directory(filepath = 'gal_images_DECaLS/'):
    if not os.path.exists(filepath):
        os.mkdir(filepath)


def plot_decals_image(ra,dec,images_dir = 'gal_images_DECaLS/',image_name = '',pixscale=0.15,bands='grz',width=424,height=424,final_size=424, origin = 'upper', fits_dir = '', delete_fits = False, flip_img = False, plot_img = True):
    '''
    Plots a DECaLS image based on ra,dec,pixscale

    if image_name is empty

    Can specify fits_dir if you want them to be on separate location than the png files.
    '''


    url = 'http://legacysurvey.org/viewer/fits-cutout?ra='+str(ra)+'&dec='+str(dec)+'&pixscale='+str(pixscale)+'&layer=dr8&bands='+str(bands)+'&width='+str(width)+'&height='+str(height)

    if image_name == '':
        image_name = 'gal_temp'

    if fits_dir != '':
        fits = wget.download(url,out=fits_dir+image_name+'.fits')
    else:
        fits = wget.download(url,out=images_dir+image_name+'.fits')
    png = images_dir+image_name+'.png'
    make_png_from_fits(fits, png, final_size)


    
    img = mpimg.imread(png)
    
    if flip_img:
        img = np.flip(img,0)

    #plot 
    if plot_img:
        
        plt.imshow(img, origin = origin)
        plt.xticks([])
        plt.yticks([])

    if delete_fits:
        if os.path.exists(fits):
            os.remove(fits)

    return img
