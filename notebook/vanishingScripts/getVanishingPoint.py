import math
import random


def calculate_intersection(line1, line2):
    m1, c1 = line1[4], line1[5]
    m2, c2 = line2[4], line2[5]

    if m1 != m2:
        x0 = (c1 - c2) / (m2 - m1)
        y0 = m1 * x0 + c1
        return x0, y0
    return None


def count_inliers(lines, intersection, inlier_threshold):
    inlier_count = 0
    inlier_lines = []

    for line in lines:
        m, c = line[4], line[5]
        m_ = -1 / m
        c_ = intersection[1] - m_ * intersection[0]

        x_ = (c - c_) / (m_ - m)
        y_ = m_ * x_ + c_

        distance = math.sqrt((y_ - intersection[1]) ** 2 + (x_ - intersection[0]) ** 2)

        if distance < inlier_threshold:
            inlier_count += 1
            inlier_lines.append(line)

    return inlier_count, inlier_lines


def getVanishingPoint(lines, inlier_threshold=10, num_iterations=1000):
    best_vanishing_point = None
    best_inlier_count = 0
    vanishing_lines = []

    for _ in range(num_iterations):
        sample_indices = random.sample(range(len(lines)), 2)
        line1, line2 = lines[sample_indices[0]], lines[sample_indices[1]]
        intersection = calculate_intersection(line1, line2)

        if intersection is None:
            continue

        inlier_count, possible_lines = count_inliers(
            lines, intersection, inlier_threshold
        )

        if inlier_count > best_inlier_count:
            best_inlier_count = inlier_count
            best_vanishing_point = intersection
            vanishing_lines = possible_lines

    return best_vanishing_point, vanishing_lines
