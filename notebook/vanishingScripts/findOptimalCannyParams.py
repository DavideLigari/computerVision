# import the necessary packages
import numpy as np


def findOptimalCannyParams(image, sigma=0.22):
    # compute the median of the single channel pixel intensities
    v = np.median(image)
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    # return the edged image
    return lower, upper
