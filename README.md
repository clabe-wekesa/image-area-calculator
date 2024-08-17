# Image Area Calculator

This Python application provides a tool for calculating the real-world areas of contours in an image using a known object in the image for scaling. The application is built with OpenCV for image processing and includes functionality for converting PDF files to images if needed. Users can easily calculate areas in square centimeters by simply selecting points on an object of known length in the image.

### Purpose of the Package

The Image Area Calculator offers a straightforward solution for anyone needing to measure areas in images accurately. Whether you're working with scanned documents, photos, or any other images containing measurable objects, this tool allows you to calculate areas in real-world units (cm²) by referencing a known object in the image. The package supports image files directly and can also convert PDF files to images for processing.

### Features

- Automatically converts single-page PDF files to JPEG images for processing.
- Allows users to select two points on a reference object in the image to calculate the scale, then calculates and displays areas of contours in the image in square centimeters (cm²).
- Supports rotating images by a specified angle to correct the orientation before processing.
- Exports the calculated areas and contour coordinates to a CSV file for further analysis.
- Displays the image with calculated areas overlaid directly on the contours, making it easy to visualize the results.

### Installation Instructions

**1. Python Environment**  
Requires [Python 3](https://www.python.org/) environment. Ensure you have it installed on your computer.

```shell
pip install image-area-calculator
```
**2. Additional Dependencies**  
The application uses the following libraries, which will be automatically installed via pip:
- Click (for handling command-line options and arguments)
- OpenCV (for image processing)
- pdf2image (for PDF to image conversion)
- NumPy (for numerical calculations)

### Usage
After installation, you can use the tool directly from the command line. For example:

```shell
calculate-areas --image 'path/to/image.jpg' \
                 --ref_length 5 \
                 --threshold_value 127 \
                 --maxval 255 \
                 --area_threshold 200 \
                 --rotation_angle 90 \
                 --output 'output_areas.csv'
```

Command-Line Options
- `-i, --image`: Path to the input image or PDF file. This is required.
- `-l, --ref_length`: The length of the reference object in centimeters. This is required to calculate the scale.
- `-t, --threshold_value`: The threshold value for binarization (default is 127). Adjust if needed for better contour detection.
- `-m, --maxval`: The maximum value for binary thresholding (default is 255).
- `-a, --area_threshold`: Minimum contour area in pixels to consider (default is 200). Adjust to filter out smaller contours.
- `-R, --rotation_angle`: Angle to rotate the image in degrees (default is 0). Use this if the image needs to be rotated.
- `-o, --output`: Path to save the CSV file with contour areas (default is derived from the image name).  

### Acknowledgment
1The development of this application draws upon various Python libraries, particularly OpenCV for image processing and pdf2image for handling PDF files. These tools are critical for enabling the image manipulation and analysis capabilities of this package.

### Author
[Dr. Clabe Wekesa](https://www.ice.mpg.de/246268/group-members) 
