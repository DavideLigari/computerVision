import cv2
import numpy as np


# Function to find optimal Canny edge parameters
def findOptimalCannyParams(image):
    best_params = (0, 0)  # (low_threshold, high_threshold)
    best_score = 0

    for low_threshold in range(50, 300, 10):
        for high_threshold in range(50, 300, 10):
            edge_image = cv2.Canny(image, low_threshold, high_threshold)
            # Implement a scoring method to evaluate edge quality
            score = evaluateEdgeQuality(edge_image)

            if score > best_score:
                best_score = score
                best_params = (low_threshold, high_threshold)

    print("best_params", best_params)
    return best_params


# Implement functions to evaluate edge quality and line detection quality
def evaluateEdgeQuality(edge_image):
    """Index based on the gradient magnitude of the edge"""
    # Calculate the gradient magnitude using the Sobel operator
    gradient_magnitude = cv2.Sobel(edge_image, cv2.CV_64F, 1, 1, ksize=3)

    # Apply a threshold to identify well-defined edges
    thresholded_edge_map = cv2.threshold(
        gradient_magnitude, 100, 255, cv2.THRESH_BINARY
    )[1]

    # Calculate the number of pixels in the thresholded edge map
    edge_clarity = np.sum(thresholded_edge_map == 255)

    return edge_clarity

    """index based on the lenght and strength of the edge"""
    # # Calculate the average edge strength (edge pixels' values)
    # avg_strength = np.mean(edge_image)

    # # Calculate the average edge length (total edge pixels)
    # avg_length = np.sum(edge_image) / 255  # Assuming edge pixels are binary (0 or 255)

    # # Calculate the geometric mean of avg_strength and avg_length
    # geometric_mean = np.sqrt(avg_strength * avg_length)

    # return geometric_mean
