import cv2
import numpy as np
from vanishingScripts.filterLines import filterLines
import random


def multipleHoughTransform(image):
    """Perform multiple Hough Transforms with varying parameters to detect lines in the image."""
    detectedLines = []

    for threshold in range(40, 100, 10):
        for minLineLength in range(10, 70, 10):
            for maxLineGap in range(2, 20, 2):
                lines = cv2.HoughLinesP(
                    image,
                    1,
                    np.pi / 180,
                    threshold=threshold,
                    minLineLength=minLineLength,
                    maxLineGap=maxLineGap,
                )

                if lines is not None:
                    lines = filterLines(lines)
                    detectedLines += lines

    return detectedLines
