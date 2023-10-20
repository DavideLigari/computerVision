# Document Scanning and Enhancement Project

This Python-based project aims to develop an application that can take a picture of a document, detect its edges, and transform it into a neatly cropped and perspective-corrected scanned image. Additionally, the project includes functionality to enhance the text quality of scanned documents by removing noise, correcting skew, and improving readability.

## Project Overview

Document scanning and enhancement play a crucial role in digitizing physical documents, improving document readability, and preparing documents for archiving or further processing. This project combines computer vision and image processing techniques to achieve these goals.

## Features

1. **Document Edge Detection and Cropping**:
   - The application can take an input image of a document.
   - It converts the image to grayscale, applies Gaussian blur to reduce noise, and utilizes Canny edge detection to identify document edges.
   - The largest contour in the edge-detected image is assumed to be the document, and it is cropped from the input image.
   - The cropped document is saved as a separate image file.

2. **Document Enhancement**:
   - The application loads the cropped document.
   - It converts the document to grayscale and applies thresholding to enhance text visibility.
   - The skew of the document is automatically corrected (deskewed).
   - The enhanced document is saved as a separate image file.

## Dependencies

- Python 3.x
- OpenCV (opencv-python)

## Usage

1. Clone this repository to your local machine:

```bash
git clone https://github.com/your-username/document-scanning-and-enhancement.git
```

2. Install the required dependencies:

```bash
pip install opencv-python
```

3. Run the document scanning and enhancement application:

```bash
python scan_and_enhance.py
```

Replace `'scan_and_enhance.py'` with the name of the Python script containing the code provided in this repository.

4. Follow the on-screen instructions to provide the input image and observe the resulting cropped and enhanced document.

## License

This project is licensed under the [APACHE 2.0 License](https://github.com/AndreaAlberti07/Computer-Vision-Project/blob/main/LICENSE).

