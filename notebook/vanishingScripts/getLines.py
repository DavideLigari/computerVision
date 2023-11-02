import cv2
import numpy as np
from vanishingScripts.filterLines import filterLines
from vanishingScripts.findOptimalCannyParams import findOptimalCannyParams
from vanishingScripts.findOptimalHoughParams import findOptimalHoughParams


def getLines(Image):
    # Converting to grayscale
    GrayImage = cv2.cvtColor(Image, cv2.COLOR_BGR2GRAY)

    # Blurring image to reduce noise.
    BlurGrayImage = cv2.GaussianBlur(GrayImage, (5, 5), 1)

    # Generating Edge image
    lowTreshold, highTreshold = findOptimalCannyParams(BlurGrayImage)
    EdgeImage = cv2.Canny(BlurGrayImage, lowTreshold, highTreshold)

    # Finding Lines in the image
    # threshold, minLineLenght, maxLineGap = findOptimalHoughParams(EdgeImage)
    Lines = cv2.HoughLinesP(
        EdgeImage,
        1,
        np.pi / 180,
        threshold=50,
        minLineLength=10,
        maxLineGap=15,
    )
    # Check if lines found and exit if not.
    if Lines is None:
        print("Not enough lines found in the image for Vanishing Point detection.")
        exit(0)

    # Filtering Lines wrt angle
    FilteredLines = filterLines(Lines)

    return FilteredLines
