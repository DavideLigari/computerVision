from re import L
import cv2
import numpy as np
from vanishingScripts.filterLines import filterLines
from vanishingScripts.findOptimalCannyParams import findOptimalCannyParams
from vanishingScripts.findOptimalHoughParams import findOptimalHoughParams


def getLines(image):
    # Converting to grayscale
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Blurring image to reduce noise.
    blurGrayImage = cv2.GaussianBlur(grayImage, (5, 5), 1)

    # Generating Edge image
    lowTreshold, highTreshold = findOptimalCannyParams(blurGrayImage)
    edgeImage = cv2.Canny(blurGrayImage, lowTreshold, highTreshold)

    # Finding Lines in the image
    # threshold, minLineLenght, maxLineGap = findOptimalHoughParams(edgeImage)
    lines = cv2.HoughLinesP(
        edgeImage,
        1,
        np.pi / 180,
        threshold=50,
        minLineLength=10,
        maxLineGap=15,
    )
    # Check if lines found and exit if not.
    if lines is None:
        print("Not enough lines found in the image for Vanishing Point detection.")
        exit(0)

    # Filtering lines wrt angle
    filteredlines = filterLines(lines)

    return filteredlines
