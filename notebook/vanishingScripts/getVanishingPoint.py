import math
import random


# Function to calculate the intersection point of two lines
def calculate_intersection(line1, line2):
    """Calculate the intersection point of two lines.

    Args:
       * line1 (list): A list containing the parameters of the first line [x1, y1, x2, y2, m, c].
       * line2 (list): A list containing the parameters of the second line [x1, y1, x2, y2, m, c].

    Returns:
        tuple or None: A tuple containing the x and y coordinates of the intersection point if the lines are not parallel. None if the lines are parallel.
    """
    # Extract slope (m) and y-intercept (c) from each line
    m1, c1 = line1[4], line1[5]
    m2, c2 = line2[4], line2[5]

    # Check if the lines are not parallel (i.e., have different slopes)
    if m1 != m2:
        # Calculate the x and y coordinates of the intersection point
        x0 = (c1 - c2) / (m2 - m1)
        y0 = m1 * x0 + c1
        return x0, y0  # Return the intersection point coordinates
    else:
        return None  # Lines are parallel, no intersection point


# Function to count inliers (lines that are close to a given intersection point)
def count_inliers(lines, intersection, inlier_threshold):
    """Count inliers (lines close to a given intersection point).

    Args:
        lines (list): A list of lines, where each line is represented as [x1, y1, x2, y2, m, c].
        intersection (tuple): The x and y coordinates of the intersection point.
        inlier_threshold (float): The maximum distance allowed for a line to be considered an inlier.

    Returns:
        int: The number of inliers.
        list: A list of inlier lines, each represented as [x1, y1, x2, y2, m, c].
    """
    inlier_count = 0  # Initialize the inlier count to zero
    inlier_lines = []  # Create an empty list to store inlier lines

    # Iterate through each line
    for line in lines:
        # Extract slope (m) and y-intercept (c) of the line
        m, c = line[4], line[5]

        # Calculate the slope of the line perpendicular to the line being checked
        m_ = -1 / m

        # Calculate the y-intercept of the perpendicular line passing through the intersection point
        c_ = intersection[1] - m_ * intersection[0]

        # Calculate the x and y coordinates of the intersection point of the two lines
        x_ = (c - c_) / (m_ - m)
        y_ = m_ * x_ + c_

        # Calculate the distance between the line and the intersection point
        distance = math.sqrt((y_ - intersection[1]) ** 2 + (x_ - intersection[0]) ** 2)

        # Check if the distance is less than the inlier threshold
        if distance < inlier_threshold:
            inlier_count += 1  # Increment the inlier count
            inlier_lines.append(line)  # Add the line to the inlier lines list

    return inlier_count, inlier_lines  # Return the count and list of inlier lines


# Function to estimate the vanishing point using RANSAC (Random Sample Consensus)
def getVanishingPoint(lines, inlier_threshold=5, num_iterations=500):
    """Estimate the vanishing point using RANSAC.

    Args:
        lines (list): A list of lines, where each line is represented as [x1, y1, x2, y2, m, c].
        inlier_threshold (float): The maximum distance allowed for a line to be considered an inlier.
        num_iterations (int): The number of RANSAC iterations.

    Returns:
        tuple: A tuple containing the best estimated vanishing point (x, y coordinates) and associated vanishing lines.
    """
    best_vanishing_point = None  # Initialize the best vanishing point as None
    best_inlier_count = 0  # Initialize the best inlier count as zero
    vanishing_lines = []  # Create an empty list to store vanishing lines

    # Repeat the RANSAC process for the specified number of iterations
    for _ in range(num_iterations):
        # Randomly select two line indices
        sample_indices = random.sample(range(len(lines)), 2)
        line1, line2 = lines[sample_indices[0]], lines[sample_indices[1]]

        # Calculate the intersection point of the two selected lines
        intersection = calculate_intersection(line1, line2)

        # Skip if the lines are parallel (no intersection point)
        if intersection is None:
            continue

        # Count inliers and collect the corresponding inlier lines
        inlier_count, possible_lines = count_inliers(
            lines, intersection, inlier_threshold
        )

        # Check if the current intersection point has more inliers than the best found so far
        if inlier_count > best_inlier_count:
            best_inlier_count = inlier_count  # Update the best inlier count
            best_vanishing_point = intersection  # Update the best vanishing point
            vanishing_lines = possible_lines  # Update the list of vanishing lines

    return (
        best_vanishing_point,
        vanishing_lines,
    )  # Return the best vanishing point and associated lines
