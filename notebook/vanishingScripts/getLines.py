from re import L
import cv2
import numpy as np
from vanishingScripts.findOptimalCannyParams import findOptimalCannyParams
from vanishingScripts.findOptimalHoughParams import findOptimalHoughParams
import matplotlib.pyplot as plt
from vanishingScripts.houghLinesCustomized import multipleHoughTransform


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
    lines = multipleHoughTransform(edgeImage)

    return lines
