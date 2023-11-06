import numpy as np


def findOptimalCannyParams(image, sigma=0.22):
    """
    Compute optimal Canny edge detection parameters for a given image.

    Args:
       * image (numpy.ndarray): The input image for edge detection.
       * sigma (float): A parameter for adjusting the lower and upper Canny thresholds.

    Returns:
        int, int: The lower and upper Canny thresholds for edge detection.
    """
    # Compute the median of the single channel pixel intensities
    v = np.median(image)

    # Compute the lower and upper Canny thresholds using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))

    # Return the computed lower and upper thresholds
    return lower, upper
