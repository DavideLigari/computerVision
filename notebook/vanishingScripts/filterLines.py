import math

# Threshold by which lines will be rejected wrt the horizontal
REJECT_DEGREE_TH = 6.0


# Function to filter and process lines
def filterLines(lines):
    """
    Filter and process lines based on slope and length.

    Args:
       * lines (list of numpy.ndarray): List of detected lines, where each element is an array containing line endpoints.

    Returns:
        list of numpy.ndarray: Filtered and processed lines.
    """
    finalLines = []  # Initialize an empty list to store the filtered lines

    for line in lines:
        [[x1, y1, x2, y2]] = line[:3]

        # Calculating the equation of the line: y = mx + c
        if x1 != x2:
            m = (y2 - y1) / (x2 - x1)  # Calculate the slope (m) of the line
        else:
            m = 100000000  # A very large value to represent vertical lines
        c = y2 - m * x2  # Calculate the y-intercept (c) of the line

        # Calculate the angle (theta) of the line with respect to the horizontal
        # Theta will contain values between -90 degrees to +90 degrees.
        theta = math.degrees(math.atan(m))

        # Rejecting lines of slope near to 0 degree or 90 degrees and storing others
        # Lines with slopes close to 0 or 90 degrees are rejected as they are considered horizontal or vertical lines.
        if REJECT_DEGREE_TH <= abs(theta) <= (90 - REJECT_DEGREE_TH):
            l = math.sqrt(
                (y2 - y1) ** 2 + (x2 - x1) ** 2
            )  # Calculate the length of the line

            notParallel = True
            for line2 in finalLines:
                if line2[4] == m:
                    notParallel = False
            # Check if a line with the same slope (parallel) already exists in finalLines
            if notParallel:
                finalLines.append(
                    [x1, y1, x2, y2, m, c, l]
                )  # Store the line's endpoints, slope, intercept, and length

    # Removing extra lines
    # We might get many lines, so we are going to take only the longest 10 lines
    # for further computation because more than this number of lines will only contribute towards slowing down the algorithm.
    if len(finalLines) > 10:
        finalLines = sorted(
            finalLines, key=lambda x: x[-1], reverse=True
        )  # Sort lines by length in descending order
        finalLines = finalLines[:10]  # Keep only the top 10 longest lines

    return finalLines
