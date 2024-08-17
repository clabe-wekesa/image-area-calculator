import os
import cv2
import numpy as np
from pdf2image import convert_from_path
import click

def convert_pdf_to_image(pdf_path):
    """
    Converts a PDF file to a JPEG image.
    Returns the path to the converted image.
    """
    images = convert_from_path(pdf_path)
    # Assuming we're only dealing with single-page PDFs for simplicity
    if len(images) > 1:
        print("Warning: Multiple pages detected, only the first page will be processed.")
    image_path = f"{os.path.splitext(pdf_path)[0]}.jpg"
    images[0].save(image_path, 'JPEG')
    return image_path

@click.command()
@click.option('-i', '--image', required=True, help='Path to the input image or PDF.')
@click.option('-l', '--ref_length', required=True, type=float, help='The length of the reference object in centimeters.')
@click.option('-t', '--threshold_value', default=127, help='Threshold value for binarization (default=127).')
@click.option('-m', '--maxval', default=255, help='Maximum value for binary thresholding (default=255).')
@click.option('-a', '--area_threshold', default=200, help='Minimum contour area in pixels to consider (default=200).')
@click.option('-R', '--rotation_angle', default=0, help='Angle to rotate the image (default=0).')
@click.option('-o', '--output', default=None, help='Path to save the CSV file with contour areas (default=from input).')
def calculate_real_world_areas(image, ref_length, threshold_value, maxval, area_threshold, rotation_angle, output):
    """
    Calculate real-world areas of contours in an image using a reference object for scale.
    """

    # Check if the input file is a PDF and convert it to an image if necessary
    if image.lower().endswith('.pdf'):
        image = convert_pdf_to_image(image)

    # Derive the output image and CSV path from the input image name
    original_name = os.path.basename(image)
    base_name, _ = os.path.splitext(original_name)
    output_image_path = f"output_{original_name}"

    # Set the default CSV output path if not provided
    if output is None:
        output = f"{base_name}_areas.csv"

    # Global variable to store selected points
    points = []

    # Mouse callback function to capture two points
    def select_points(event, x, y, flags, param):
        nonlocal points
        if event == cv2.EVENT_LBUTTONDOWN:
            points.append((x, y))
            cv2.circle(img, (x, y), 2, (0, 0, 255), -1)
            cv2.imshow('img', img)
            if len(points) == 2:
                cv2.line(img, points[0], points[1], (0, 0, 255), 1)
                cv2.imshow('img', img)

    # Load the image
    img = cv2.imread(image)

    # Rotate the image if a rotation angle is provided
    if rotation_angle != 0:
        height, width = img.shape[:2]
        center = (width // 2, height // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, rotation_angle, 1.0)
        img = cv2.warpAffine(img, rotation_matrix, (width, height))

    # Display the image and set the mouse callback
    cv2.imshow('img', img)
    cv2.setMouseCallback('img', select_points)

    # Wait for two points to be selected
    cv2.waitKey(0)

    # Calculate the scale in pixels per centimeter
    if len(points) == 2:
        pixel_distance = np.linalg.norm(np.array(points[0]) - np.array(points[1]))
        pixels_per_cm = pixel_distance / ref_length
        print(f"Pixels per cm: {pixels_per_cm}")

        # Convert area in pixels to real-world area in cm²
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(img_gray, threshold_value, maxval, cv2.THRESH_BINARY_INV)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Open a CSV file to write contour areas
        with open(output, "w") as file:
            # Write CSV header
            file.write("Contour X,Contour Y,Area (cm²)\n")
            for cnt in contours:
                area_in_pixels = cv2.contourArea(cnt)
                if area_in_pixels > area_threshold:
                    real_area_cm2 = area_in_pixels / (pixels_per_cm ** 2)
                    x, y, w, h = cv2.boundingRect(cnt)
                    cv2.putText(img, f"{real_area_cm2:.2f} cm2", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                (0, 0, 255), 2)
                    file.write(f'{x},{y},{real_area_cm2:.2f}\n')
                    print(f"Contour at ({x}, {y}) - Area: {real_area_cm2:.2f} cm²")

        # Save the labeled image with the updated output path
        cv2.imwrite(output_image_path, img)

        # Display the final image with real-world areas
        cv2.imshow('img', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Please select exactly two points on the reference object.")

if __name__ == '__main__':
    calculate_real_world_areas()
