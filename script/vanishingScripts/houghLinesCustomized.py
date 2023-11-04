import cv2
import numpy as np
from vanishingScripts.filterLines import filterLines


def multipleHoughTransform(image):
    """Perform multiple Hough Transforms with varying parameters to detect lines in the image.

    Args:
       * image (numpy.ndarray): The input image for line detection.

    Returns:
        list of numpy.ndarray: A list of detected lines, where each element is an array containing the line endpoints.
    """
    detectedLines = []

    # Loop over different sets of Hough Transform parameters
    for threshold in range(40, 100, 10):
        for minLineLength in range(10, 70, 10):
            for maxLineGap in range(2, 20, 2):
                # Apply the Hough Transform to detect lines in the image
                lines = cv2.HoughLinesP(
                    image,
                    1,  # rho (resolution of the accumulator)
                    np.pi / 180,  # theta (angular resolution of the accumulator)
                    threshold=threshold,  # threshold for line detection
                    minLineLength=minLineLength,  # minimum line length to consider
                    maxLineGap=maxLineGap,  # maximum allowed gap between line segments
                )

                if lines is not None:
                    # Filter and refine the detected lines (you may want to include this logic)
                    lines = filterLines(lines)
                    # Append the detected lines to the result list
                    detectedLines += lines

    return detectedLines
