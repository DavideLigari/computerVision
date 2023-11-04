import argparse
import sys
import cv2
import matplotlib.pyplot as plt
from vanishingScripts.readImage import readImage
from vanishingScripts.getLines import getLines
from vanishingScripts.getVanishingPoint import getVanishingPoint

if __name__ == "__main__":
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser(description="Vanishing Point Detection Script")

    # Required Arguments
    ap.add_argument(
        "-p",
        "--path",
        required=True,
        help="Path to the input image or a folder containing images for batch processing.",
    )
    ap.add_argument(
        "-t",
        "--tuning_method",
        required=True,
        choices=["Auto", "Manual"],
        help="Tuning method to use for line detection: 'Auto' or 'Manual'.",
    )

    # Optional Arguments for Manual Tuning
    ap.add_argument(
        "-l",
        "--lowThreshold",
        type=int,
        help="Low threshold for Canny Edge Detector. Required if tuning_method is 'Manual'.",
    )
    ap.add_argument(
        "-r",
        "--highThreshold",
        type=int,
        help="High threshold for Canny Edge Detector. Required if tuning_method is 'Manual'.",
    )
    ap.add_argument(
        "-a",
        "--theta",
        type=float,
        help="Theta for Hough Transform. Required if tuning_method is 'Manual'.",
    )
    ap.add_argument(
        "-d",
        "--threshold",
        type=int,
        help="Threshold for Hough Transform. Required if tuning_method is 'Manual'.",
    )
    ap.add_argument(
        "-m",
        "--minLineLength",
        type=float,
        help="Minimum line length for Hough Transform. Required if tuning_method is 'Manual'.",
    )
    ap.add_argument(
        "-g",
        "--maxLineGap",
        type=float,
        help="Maximum line gap for Hough Transform. Required if tuning_method is 'Manual'.",
    )

    # Optional Argument for Storing Results
    ap.add_argument(
        "-s",
        "--storingPath",
        help="Path for storing result images. It must contains also the filename and format. If not provided, result images will not be stored.",
    )

    args = vars(ap.parse_args())

    # Extract arguments
    img_path = args["path"]
    lowThreshold = args["lowThreshold"]
    highThreshold = args["highThreshold"]
    storingPath = args["storingPath"]
    theta = args["theta"]
    threshold = args["threshold"]
    minLineLength = args["minLineLength"]
    maxLineGap = args["maxLineGap"]
    tuning_method = args["tuning_method"]

    if tuning_method == "Manual" and not all(
        [lowThreshold, highThreshold, theta, threshold, minLineLength, maxLineGap]
    ):
        print(
            "When using 'Manual' tuning method, all manual tuning parameters are required."
        )
        sys.exit(1)

    images, imageNames = readImage(img_path)  # Reading all input images
    if tuning_method == "Auto":
        lowThreshold, highThreshold, theta, threshold, minLineLength, maxLineGap = (
            0,
            0,
            0,
            0,
            0,
            0,
        )

    for i in range(len(images)):
        image = images[i]

        # Getting the lines from the image
        lines = getLines(
            image,
            tuning_method=tuning_method,
            lowThreshold=float(lowThreshold),
            highThreshold=float(highThreshold),
            theta=float(theta),
            threshold=int(threshold),
            minLineLength=float(minLineLength),
            maxLineGap=float(maxLineGap),
        )

        # Get vanishing point
        vanishingPoint, vanishing_lines = getVanishingPoint(lines)

        # Checking if a vanishing point is found
        if vanishingPoint is None:
            print(
                "Vanishing Point not found. Possible reason is that not enough lines are found in the image for determination of vanishing point."
            )
            continue

        # Get only the most prominent lines
        if len(vanishing_lines) > 15:
            vanishing_lines = vanishing_lines[:15]

        # Drawing lines and vanishing point
        for line in vanishing_lines:
            cv2.line(image, (line[0], line[1]), (line[2], line[3]), (0, 255, 0), 2)

        cv2.circle(
            image, (int(vanishingPoint[0]), int(vanishingPoint[1])), 10, (0, 0, 255), -1
        )

        if storingPath:
            cv2.imwrite(storingPath, image)
        # Show the result image
        plt.figure(figsize=(20, 10))
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.title("Image with detected lines")
        plt.xticks([]), plt.yticks([])
        plt.axis("off")
        plt.show()
