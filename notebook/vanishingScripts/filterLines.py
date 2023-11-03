import math

# Threshold by which lines will be rejected wrt the horizontal
REJECT_DEGREE_TH = 6.0


def filterLines(lines):
    finalLines = []

    for line in lines:
        [[x1, y1, x2, y2]] = line

        # Calculating equation of the line: y = mx + c
        if x1 != x2:
            m = (y2 - y1) / (x2 - x1)
        else:
            m = 100000000
        c = y2 - m * x2
        # theta will contain values between -90 -> +90.
        theta = math.degrees(math.atan(m))

        # Rejecting lines of slope near to 0 degree or 90 degree and storing others
        if REJECT_DEGREE_TH <= abs(theta) <= (90 - REJECT_DEGREE_TH):
            l = math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)  # length of the line
            finalLines.append([x1, y1, x2, y2, m, c, l])

    # Removing extra lines
    # (we might get many lines, so we are going to take only longest 15 lines
    # for further computation because more than this number of lines will only
    # contribute towards slowing down of our algo.)
    if len(finalLines) > 5:
        finalLines = sorted(finalLines, key=lambda x: x[-1], reverse=True)
        finalLines = finalLines[:15]

    return finalLines
