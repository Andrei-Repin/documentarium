import cv2
import os
from typing import Optional
from image_processing.image_processing import process_image

def preprocess_image(image_path, output_path, settings):
    """
    Pre-processing of images before OCR.
    
    Args:
        image_path (str): Path to original image
        output_path (str): Path to save the processed image
        settings (dict): Processing settings
        
    Returns:
        numpy.ndarray: The processed image or None on error
    """
    image = cv2.imread(image_path)
    if image is None:
        print(f"Loading error: {image_path}")
        return None

    # Image processing
    processed = process_image(image, settings)

    # Convert to grayscale if needed
    if settings['FORCE_GRAYSCALE']:
        if len(processed.shape) == 3 and processed.shape[2] == 3:
            processed = cv2.cvtColor(processed, cv2.COLOR_BGR2GRAY)

    # Saving the processed image
    cv2.imwrite(output_path, processed, [cv2.IMWRITE_JPEG_QUALITY, 75])
    return processed
