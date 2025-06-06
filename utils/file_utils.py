import os
import cv2
from typing import Optional
from ocr.tesseract_ocr import get_ocr_text
from utils.image_utils import preprocess_image

def recognize_ready_images(settings):
    """
    OCR text from already processed images in the specified folder.
    
    Args:
        output_folder (str): Path to processed images
        settings (dict): Processing settings
    """
    output_folder = settings['PROCESSED_FOLDER']
    
    # Getting a list of image files
    image_files = [f for f in os.listdir(output_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tif', '.tiff'))]

    if not image_files:
        print("No images to recognize. Place finished files in output folder.")
        return

    if settings.get('SKIP_PREPROCESSING'):
        print("Already processed images from the output folder are recognized.")

    with open(settings['OUTPUT_TEXT_FILE'], "w", encoding="utf-8") as out_f:
        for filename in image_files:
            image_path = os.path.join(output_folder, filename)
            image = cv2.imread(image_path)
            if image is None:
                print(f"Loading error: {filename}")
                continue

            # Text recognition based on document type
            recognized_text = get_ocr_text(image, settings)
            
            # Writing results to a file
            out_f.write(recognized_text + "\n")


def process_images_from_folder(input_folder, processed_folder, output_text_file, settings):
    """
    Processes all images in the specified folder.
    
    Args:
        input_folder (str): Folder with source images
        processed_folder (str): Folder for processed images
        output_text_file (str): File to save results
        settings (dict): Processing settings
    """
    with open(output_text_file, "w", encoding="utf-8") as out_f:
        for filename in sorted(os.listdir(input_folder)):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                input_path = os.path.join(input_folder, filename)
                output_path = os.path.join(processed_folder, filename)

                # Image processing
                processed = preprocess_image(input_path, output_path, settings)

                if processed is not None:
                    if settings.get('ENABLE_OCR', True):  # OCR is enabled by default
                        lang = 'rus+deu+lav'  # Basic languages
                        text = get_ocr_text(processed, lang=lang)
                        out_f.write(text + "\n")
                    else:
                        out_f.write(f"\n===== {filename} =====\n")
                        out_f.write("[OCR is disabled]\n")