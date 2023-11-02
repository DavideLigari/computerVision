#!/bin/bash

# Define the list of image file names
image_files=(
    "1img.tif"
    "2img.webp"
    "3img.jpeg"
    "5img.jpeg"
    "6img.jpg"
    "7img.jpg"
    "8img.png"
    "9img.tif"
    "10img.jpg"
    "11img.jpg"
    "12img.tif"
    "13img.jpg"
    "14img.jpg"
    "15img.tif"
    "16img.tif"
    "17img.tif"
    "18img.tif"
    "19img.jpeg"
    "20img.tif"
    "21img.tif"
    "22img.png"
    "23img.tif"
    "24img.tif"
    "25img.tif"
    "26img.tif"
    "27img.jpg"
    "28img.tif"
    "29img.jpeg"
    "30img.png"
    "31img.tif"
    "32img.tif"
    "33img.tif"
)

# Loop through the image files and execute the command
for image_file in "${image_files[@]}"; do
    python binarization.py -i "Images/$image_file" -t 'Auto' -s "Images/tested/${image_file}_binarized.jpeg" -show_all False
done
