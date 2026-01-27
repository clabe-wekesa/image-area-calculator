import os
import cv2
import numpy as np
from pdf2image import convert_from_path
import click

from .viewer_scroll import select_two_points


# --------------------------------------------------
# PDF → temporary image conversion
# --------------------------------------------------
def convert_pdf_to_image(pdf_path):
    """
    Converts a PDF file to a temporary JPEG image.
    Returns the path to the converted image.
    """
    images = convert_from_path(pdf_path)
    if len(images) > 1:
        print("Warning: Multiple pages detected, only the first page is used.")

    image_path = f"{os.path.splitext(pdf_path)[0]}__tmp.jpg"
    images[0].save(image_path, "JPEG")
    return image_path


# --------------------------------------------------
# CLI
# --------------------------------------------------
@click.command()
@click.option("-i", "--image", required=True, help="Path to input image or PDF.")
@click.option("-l", "--ref_length", required=True, type=float,
              help="Reference object length in centimeters.")
@click.option("-t", "--threshold_value", default=127,
              help="Threshold value (default=127).")
@click.option("-m", "--maxval", default=255,
              help="Max value for thresholding (default=255).")
@click.option("-a", "--area_threshold", default=200,
              help="Minimum contour area in pixels.")
@click.option("-R", "--rotation_angle", default=0,
              help="Rotation angle in degrees.")
@click.option("-o", "--output", default=None,
              help="CSV output filename (default: <basename>_areas.csv).")
@click.option("--outdir", default=None,
              help="Output directory (default: <basename>_output).")
def calculate_real_world_areas(
    image,
    ref_length,
    threshold_value,
    maxval,
    area_threshold,
    rotation_angle,
    output,
    outdir,
):
    """
    Calculate real-world contour areas using a reference scale.
    """

    # --------------------------------------------------
    # Handle PDF input
    # --------------------------------------------------
    is_pdf = image.lower().endswith(".pdf")
    temp_image_path = None

    if is_pdf:
        temp_image_path = convert_pdf_to_image(image)
        image = temp_image_path

    # --------------------------------------------------
    # Paths & output directories
    # --------------------------------------------------
    image = os.path.abspath(image)
    base_name = os.path.splitext(os.path.basename(image))[0]

    if outdir is None:
        outdir = f"{base_name}_output"

    processed_dir = os.path.join(outdir, "processed")
    contours_dir  = os.path.join(outdir, "contours")

    os.makedirs(processed_dir, exist_ok=True)
    os.makedirs(contours_dir, exist_ok=True)

    processed_image_path = os.path.join(
        processed_dir, f"{base_name}_processed.jpg"
    )
    contours_image_path = os.path.join(
        contours_dir, f"{base_name}_contours.jpg"
    )

    if output is None:
        output = os.path.join(outdir, f"{base_name}_areas.csv")

    # --------------------------------------------------
    # Load image
    # --------------------------------------------------
    img = cv2.imread(image)
    if img is None:
        raise RuntimeError(f"Could not read image: {image}")

    if rotation_angle != 0:
        h, w = img.shape[:2]
        center = (w // 2, h // 2)
        rot = cv2.getRotationMatrix2D(center, rotation_angle, 1.0)
        img = cv2.warpAffine(img, rot, (w, h))

    # --------------------------------------------------
    # Select reference points (interactive)
    # --------------------------------------------------
    points = select_two_points(img)

    if len(points) != 2:
        print("Please select exactly two reference points.")
        return

    # --------------------------------------------------
    # Compute scale
    # --------------------------------------------------
    pixel_distance = np.linalg.norm(
        np.array(points[0]) - np.array(points[1])
    )
    pixels_per_cm = pixel_distance / ref_length
    print(f"Pixels per cm: {pixels_per_cm:.4f}")

    # --------------------------------------------------
    # Threshold & contours
    # --------------------------------------------------
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(
        img_gray, threshold_value, maxval, cv2.THRESH_BINARY_INV
    )

    contours, _ = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )

    # Filled contour mask (white objects)
    contour_img = np.zeros(img_gray.shape, dtype=np.uint8)
    cv2.drawContours(contour_img, contours, -1, 255, -1)

    # --------------------------------------------------
    # Area calculation + annotation
    # --------------------------------------------------
    with open(output, "w") as f:
        f.write("Contour X,Contour Y,Area (cm²)\n")

        for cnt in contours:
            area_px = cv2.contourArea(cnt)
            if area_px < area_threshold:
                continue

            area_cm2 = area_px / (pixels_per_cm ** 2)
            x, y, w, h = cv2.boundingRect(cnt)

            cv2.putText(
                img,
                f"{area_cm2:.2f} cm2",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 255),
                2,
            )

            f.write(f"{x},{y},{area_cm2:.2f}\n")

    # --------------------------------------------------
    # Save outputs
    # --------------------------------------------------
    cv2.imwrite(processed_image_path, img)
    cv2.imwrite(contours_image_path, contour_img)

    print(f"Processed image: {processed_image_path}")
    print(f"Contour mask:    {contours_image_path}")
    print(f"CSV file:        {output}")

    # --------------------------------------------------
    # Final display (user-controlled exit)
    # --------------------------------------------------
    cv2.imshow("Processed image (press ENTER to close)", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # --------------------------------------------------
    # Cleanup temp PDF image
    # --------------------------------------------------
    if is_pdf and temp_image_path and os.path.exists(temp_image_path):
        os.remove(temp_image_path)


if __name__ == "__main__":
    calculate_real_world_areas()