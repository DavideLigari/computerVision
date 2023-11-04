import cv2

# Custom functions
from vanishingScripts.findOptimalCannyParams import findOptimalCannyParams
from vanishingScripts.houghLinesCustomized import multipleHoughTransform
from vanishingScripts.filterLines import filterLines


def getLines(
    image,
    tuning_method,
    lowThreshold=float(0),
    highThreshold=float(0),
    theta=float(0),
    threshold=0,
    minLineLength=float(0),
    maxLineGap=float(0),
):
    """Detect lines in an input image using the provided parameters and tuning method.

    Args:
       * image (numpy.ndarray): The input color image.
       * tuning_method (str): The tuning method for parameter selection ('Auto' or 'Manual').
       * lowThreshold (float): Low threshold for Canny edge detection.
       * highThreshold (float): High threshold for Canny edge detection.
       * theta (float): Theta for Hough Transform.
       * threshold (int): Threshold for Hough Transform.
       * minLineLength (float): Minimum line length for Hough Transform.
       * maxLineGap (float): Maximum line gap for Hough Transform.

    Returns:
        list of numpy.ndarray: A list of detected lines, where each element is an array containing the line endpoints.
    """

    # Converting the input color image to grayscale
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Blurring the grayscale image to reduce noise
    blurGrayImage = cv2.GaussianBlur(grayImage, (5, 5), 1)

    # Initially, set the 'edgeImage' to 'blurGrayImage'
    edgeImage = blurGrayImage

    lines = []

    # Check the 'tuning_method' to determine the path to follow
    if tuning_method == "Auto":
        # Auto mode for parameter tuning

        # Find optimal Canny edge detection parameters
        lowTreshold, highTreshold = findOptimalCannyParams(blurGrayImage)

        print(
            "Optimal low threshold : ",
            lowTreshold,
            " Optimal high threshold : ",
            highTreshold,
        )

        # Apply Canny edge detection using the optimal thresholds
        edgeImage = cv2.Canny(blurGrayImage, lowTreshold, highTreshold)

        # Detect lines using a custom Hough Transform method for multiple orientations
        lines = multipleHoughTransform(edgeImage)
    else:
        # Manual mode for parameter tuning

        # Apply Canny edge detection with user-defined thresholds
        edgeImage = cv2.Canny(blurGrayImage, lowThreshold, highThreshold)

        # Detect lines using OpenCV's Hough Transform
        lines = cv2.HoughLinesP(
            edgeImage,
            1,
            theta,
            threshold=threshold,
            minLineLength=minLineLength,
            maxLineGap=maxLineGap,
        )

        # Apply a custom line filter to retain only relevant lines
        lines = filterLines(lines)

    return lines
