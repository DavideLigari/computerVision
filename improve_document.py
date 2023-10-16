import cv2
import numpy as np

# This function has not been tested yet
# It's just a draft.


def improve_document(input_image_path):
    # Load the input image
    image = cv2.imread(input_image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding to find edges
    # Adaptive thresholding adjusts the threshold for each pixel based on its local neighborhood,
    # improving the detection of edges in varying lighting conditions.
    edges = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )

    # Find and draw contours around the edges
    # Contours are outlines of objects in an image, and finding them helps identify shapes and structures.
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours by area and keep the largest one
    # Selecting the largest contour is often used to isolate the main object or structure in an image.
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]

    # Perform rotation and perspective correction
    if len(contours) > 0:
        max_contour = contours[0]
        rect = cv2.minAreaRect(max_contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        # Calculate the dimensions and perspective transformation matrix
        width, height = int(rect[1][0]), int(rect[1][1])
        src_pts = np.float32(box)
        dst_pts = np.array(
            [[0, height - 1], [0, 0], [width - 1, 0], [width - 1, height - 1]],
            dtype="float32",
        )

        M = cv2.getPerspectiveTransform(src_pts, dst_pts)

        # Apply perspective transformation to correct the document's perspective
        warped = cv2.warpPerspective(image, M, (width, height))

        return warped

    return image


if __name__ == "__main__":
    input_image_path = "input_document.jpg"  # Replace with your input image path

    # Preprocess the image
    output_image = improve_document(input_image_path)

    # Display the processed image
    cv2.imshow("Processed Image", output_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Save the processed image
    cv2.imwrite("output_document.jpg", output_image)
