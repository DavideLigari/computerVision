from re import L
import cv2
import numpy as np
from vanishingScripts.filterLines import filterLines
from vanishingScripts.findOptimalCannyParams import findOptimalCannyParams
from vanishingScripts.findOptimalHoughParams import findOptimalHoughParams
import matplotlib.pyplot as plt


def getLines(image):
    # Converting to grayscale
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Blurring image to reduce noise.
    blurGrayImage = cv2.GaussianBlur(grayImage, (5, 5), 1)

    # Generating Edge image
    lowTreshold, highTreshold = findOptimalCannyParams(blurGrayImage)
    print("lowTreshold, highTreshold", lowTreshold, highTreshold)
    edgeImage = cv2.Canny(blurGrayImage, lowTreshold, highTreshold)
    plt.figure(figsize=(10, 10))
    plt.imshow(edgeImage, cmap="gray")
    plt.show()

    # Finding Lines in the image
    # threshold, minLineLenght, maxLineGap = findOptimalHoughParams(edgeImage)
    lines = cv2.HoughLinesP(
        edgeImage,
        1,
        np.pi / 180,
        threshold=50,
        minLineLength=60,
        maxLineGap=15,
    )
    # Check if lines found and exit if not.
    if lines is None:
        print("Not enough lines found in the image for Vanishing Point detection.")
        exit(0)

    # Filtering lines wrt angle
    filteredlines = filterLines(lines)

    return filteredlines
