import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import cv2 as cv
import argparse
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import os

# Your program logic functions (you can include them here or import them)
# Loss function
def get_loss(num, bin, thresh, tuning_method, under_tuning, over_tuning):
    """
    Calculate a loss function based on the provided parameters.

    Args:
        num (array): Histogram values.
        bin (array): Bin values of the histogram.
        thresh (int): Threshold value for binarization.
        tuning_method (str): Tuning method ('Auto' or 'Manual').
        under_tuning (float): Tuning value for pixels under the threshold.
        over_tuning (float): Tuning value for pixels over the threshold.

    Returns:
        float: The computed loss value.
    """
    bin = bin[:-1]

    # distance if the pixel is under the threshold
    dist_under_thresh = bin[:thresh]
    # distance if the pixel is over the threshold
    dist_over_thresh = 256 - bin[thresh:]

    # Tune according to 'skewness' and value inserted by the user
    if tuning_method == "Auto":
        weighted = bin * num
        m = np.sum(weighted) / np.sum(num)
        tuning = np.abs(m - 128)

        if m > (256 / 2 + 20):
            tuned_dist_under_thresh = dist_under_thresh
            tuned_dist_over_thresh = dist_over_thresh + tuning
        elif m < (256 / 2 - 20):
            tuned_dist_under_thresh = dist_under_thresh + tuning
            tuned_dist_over_thresh = dist_over_thresh
        else:
            tuned_dist_under_thresh = dist_under_thresh
            tuned_dist_over_thresh = dist_over_thresh

    else:
        tuned_dist_under_thresh = dist_under_thresh + int(under_tuning)
        tuned_dist_over_thresh = dist_over_thresh + int(over_tuning)

    # concatenate the two parts
    dist_mat = np.concatenate((tuned_dist_under_thresh, tuned_dist_over_thresh))
    loss = np.sum(num * dist_mat)  # Loss function
    return loss


def get_best_thresh(
    num, bin, tuning_method="Auto", under_tuning=None, over_tuning=None, show_loss=False
):
    """
    Find the best threshold value for binarization based on the provided parameters.

    Args:
    num (array): Histogram values.
    bin (array): Bin values of the histogram.
    tuning_method (str): Tuning method ('Auto' or 'Manual').
    under_tuning (float): Tuning value for pixels under the threshold (only for 'Manual' tuning).
    over_tuning (float): Tuning value for pixels over the threshold (only for 'Manual' tuning).
    show_loss (bool): Whether to plot the loss function.

    Returns:
    int: The best threshold value.
    float: The minimum loss value.
    list: List of loss values for each threshold.
    """
    loss_list = []

    if tuning_method == "Manual":
        if under_tuning is None or over_tuning is None:
            print("Please insert values for tuning")
            return
    else:
        weighted = bin[:-1] * num
        m = np.sum(weighted) / np.sum(num)
        if m > (256 / 2 + 10):
            under_over = "over"
        else:
            under_over = "under"
        print(f"Tuning parameter (128 - mean): {np.abs(m - 128)} --> {under_over}")

    for i in range(1, 255):
        loss = get_loss(num, bin, i, tuning_method, under_tuning, over_tuning)
        loss_list.append(loss)
    min_loss = np.min(loss_list)
    best_thresh = np.argmin(loss_list)
    if show_loss:
        plt.figure()
        plt.plot(loss_list)
        plt.title("Loss function")

    return best_thresh, min_loss, loss_list


def apply_thresh(img_gray, thresh, show_img=False):
    """
    Apply thresholding to a grayscale image.

    Args:
    img_gray (array): Grayscale input image.
    thresh (int): Threshold value for binarization.
    show_img (bool): Whether to display the binarized image.

    Returns:
    array: Binarized image.
    """
    img_bin = img_gray > thresh  # Mask
    if show_img:
        plt.figure()
        plt.imshow(img_bin, cmap="gray")
        plt.title("Binarized"), plt.xticks([]), plt.yticks([])
    return img_bin


# ------------------------ MAIN ------------------------#

# Function to execute your program
def run_program():
    img_path = img_path_entry.get()
    tuning_method = tuning_method_var.get()
    under_tuning = under_tuning_entry.get()
    over_tuning = over_tuning_entry.get()
    storing_path = storing_path_entry.get()
    show_all = show_all_var.get()

    # Input validation
    if not os.path.exists(img_path):
        messagebox.showerror("Error", "Input image path does not exist.")
        return

    # Run your program (add the program logic here)
    try:
        # Load image
        img = cv.imread(img_path, cv.IMREAD_COLOR)

        # Convert to grayscale
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        # Compute the histogram
        num, bin = np.histogram(img_gray.ravel(), 256, [0, 256])

        # Get and apply the best threshold
        best_thresh, min_loss, losses = get_best_thresh(
        num, bin, tuning_method, under_tuning, over_tuning, show_loss=False
        )
        img_bin = apply_thresh(img_gray, best_thresh, show_img=False)

        print("The best threshold is: ", best_thresh)
        print("The minimum loss is: ", min_loss)

        # Binarization with Otsu's method
        img_otsu = cv.threshold(img_gray, 0, 255, cv.THRESH_OTSU)[1]

        if show_all == "True":
            # Show the results
            # Histogram and Loss
            fig, axs = plt.subplots(1, 2, figsize=(10, 5))
            plt.subplots_adjust(wspace=0.02)  # You can adjust the value as needed

            axs[0].set_title("Histogram")
            axs[0].plot(num)
            axs[1].set_title("Loss function")
            axs[1].plot(losses)
            fig.text(0.5, 0.01, "Pixel values", ha="center", fontsize=12)

            # Images comparison
            fig, axs = plt.subplots(1, 3, figsize=(15, 10))

            # Plot the original image in the first subplot
            axs[0].imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
            axs[0].set_title("Original")
            axs[0].set_xticks([]), axs[0].set_yticks([])

            # Plot the binarized image in the second subplot
            axs[1].imshow(img_bin, cmap="gray")
            axs[1].set_title("Binarized")
            axs[1].set_xticks([]), axs[1].set_yticks([])

            # Plot the Otsu image in the third subplot
            axs[2].imshow(img_otsu, cmap="gray")
            axs[2].set_title("Otsu")
            axs[2].set_xticks([]), axs[2].set_yticks([])

            # Show the plots
            plt.show()

        # Save the binarized image
        # Check if the file already exists
        if storing_path:
            if os.path.exists(storing_path):
                print(
                        f"Warning: The file {storing_path} already exists. Skipping save operation."
                )
        else:
                # Convert it to 0 and 255
                img_bin = (img_bin * 255).astype(np.uint8)

                # Save the binary image as a JPEG file
                cv.imwrite(storing_path, img_bin)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main application window
app = tk.Tk()
app.title("Binarization Program GUI")

# Create and configure GUI elements
# Input image path
img_path_label = tk.Label(app, text="Input Image Path:")
img_path_label.pack()
img_path_entry = tk.Entry(app)
img_path_entry.pack()

# Browse button for selecting an image
def browse_image():
    img_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.ppm *.pgm")])
    img_path_entry.delete(0, tk.END)
    img_path_entry.insert(0, img_path)

browse_button = tk.Button(app, text="Browse", command=browse_image)
browse_button.pack()

# Tuning method (Auto or Manual)
tuning_method_label = tk.Label(app, text="Tuning Method:")
tuning_method_label.pack()
tuning_method_var = tk.StringVar(value="Auto")  # Default to Auto
tuning_method_auto_radio = tk.Radiobutton(app, text="Auto", variable=tuning_method_var, value="Auto")
tuning_method_manual_radio = tk.Radiobutton(app, text="Manual", variable=tuning_method_var, value="Manual")
tuning_method_auto_radio.pack()
tuning_method_manual_radio.pack()

# Under Tuning
under_tuning_label = tk.Label(app, text="Under Tuning (Manual):")
under_tuning_label.pack()
under_tuning_entry = tk.Entry(app)
under_tuning_entry.pack()

# Over Tuning
over_tuning_label = tk.Label(app, text="Over Tuning (Manual):")
over_tuning_label.pack()
over_tuning_entry = tk.Entry(app)
over_tuning_entry.pack()

# Storing Path
storing_path_label = tk.Label(app, text="Storing Path:")
storing_path_label.pack()
storing_path_entry = tk.Entry(app)
storing_path_entry.pack()

# Show All (True or False)
show_all_label = tk.Label(app, text="Show All (True or False):")
show_all_label.pack()
show_all_var = tk.StringVar(value="False")  # Default to False
show_all_true_radio = tk.Radiobutton(app, text="True", variable=show_all_var, value="True")
show_all_false_radio = tk.Radiobutton(app, text="False", variable=show_all_var, value="False")
show_all_true_radio.pack()
show_all_false_radio.pack()

# Button to run the program
run_button = tk.Button(app, text="Run Program", command=run_program)
run_button.pack()

# Text widget to display results
result_text = tk.Text(app, height=10, width=50)
result_text.pack()

# Start the Tkinter main loop
app.mainloop()
