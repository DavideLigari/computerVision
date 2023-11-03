import math


def getVanishingPoint(Lines, inlier_threshold=10):
    best_vanishing_point = None
    best_inlier_count = 0
    vanishing_lines = []

    for i in range(len(Lines)):
        for j in range(i + 1, len(Lines)):
            line1 = Lines[i]
            line2 = Lines[j]

            m1, c1 = line1[4], line1[5]
            m2, c2 = line2[4], line2[5]

            if m1 != m2:
                # Calculate the intersection point
                x0 = (c1 - c2) / (m2 - m1)
                y0 = m1 * x0 + c1

                inlier_count = 0
                possible_lines = []

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

    return best_vanishing_point, vanishing_lines
