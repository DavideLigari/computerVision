import os
import cv2


def readImage(InputImagePath):
    """Read images from a file or a folder and return them as a list.

    Args:
       * InputImagePath (str): The path to the input image file or folder.

    Returns:
       * list of numpy.ndarray: A list of images.
       * list of str: A list of image names.
    """

    Images = []  # Input Images will be stored in this list.
    ImageNames = []  # Names of input images will be stored in this list.

    # Checking if path is of a file or folder.
    if os.path.isfile(InputImagePath):  # If the path is of a file.
        InputImage = cv2.imread(InputImagePath, cv2.IMREAD_COLOR)  # Reading the image.

        # Checking if the image is read.
        if InputImage is None:
            print("Image not read. Provide a correct path")
            exit()

        Images.append(InputImage)  # Storing the image.
        ImageNames.append(os.path.basename(InputImagePath))  # Storing the image's name.

    # If the path is of a folder containing images.
    elif os.path.isdir(InputImagePath):
        # Getting all image names present inside the folder.
        for ImageName in os.listdir(InputImagePath):
            # Reading images one by one.
            InputImage = cv2.imread(InputImagePath + "/" + ImageName)

            Images.append(InputImage)  # Storing images.
            ImageNames.append(ImageName)  # Storing image names.

    # If it is neither a file nor a folder (Invalid Path).
    else:
        print("\nEnter a valid Image Path.\n")
        exit()

    return Images, ImageNames
