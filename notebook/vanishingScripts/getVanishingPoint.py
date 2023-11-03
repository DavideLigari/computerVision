import math
import random


def getVanishingPoint(Lines, max_iterations=10000, inlier_threshold=10):
    """TO CHANGE: This function is used to find the vanishing point of a set of lines.
    The idea is to find the intersection point of all possible pairs of lines.
    and for each intersection point, count the number of lines that are close to it.
    The intersection point with the highest number of inliers is the vanishing point and
    the lines that are close to it are the vanishing lines."""
    best_vanishing_point = None
    best_inlier_count = 0
    vanishing_lines = []

    for _ in range(max_iterations):
        # Randomly sample two lines
        sample_lines = random.sample(Lines, 2)
        m1, c1 = sample_lines[0][4], sample_lines[0][5]
        m2, c2 = sample_lines[1][4], sample_lines[1][5]
        possible_lines = []
        if m1 != m2:
            # Calculate the intersection point
            x0 = (c1 - c2) / (m2 - m1)
            y0 = m1 * x0 + c1

            inlier_count = 0

            # Count inliers (lines that are close to the intersection point)
            for line in Lines:
                m, c = line[4], line[5]
                m_ = -1 / m
                c_ = y0 - m_ * x0

                x_ = (c - c_) / (m_ - m)
                y_ = m_ * x_ + c_

                distance = math.sqrt((y_ - y0) ** 2 + (x_ - x0) ** 2)

                if distance < inlier_threshold:
                    inlier_count += 1
                    possible_lines.append(line)

            if inlier_count > best_inlier_count:
                best_inlier_count = inlier_count
                best_vanishing_point = [x0, y0]
                vanishing_lines = possible_lines
                vanishing_lines += sample_lines

    return best_vanishing_point, vanishing_lines
