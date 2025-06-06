import os

# --- Image Processing Settings ---
settings = {
    # --- Path Settings ---
    # All paths are relative to current working directory
    'BASE_DIR': os.getcwd(),

    # Image folders
    'INPUT_FOLDER': os.path.join(os.getcwd(), "input_images"),
    'PROCESSED_FOLDER': os.path.join(os.getcwd(), "processed_images"),

    # Output directory
    'OUTPUT_DIR': os.path.join(os.getcwd(), "output"),

    # Main recognition output file
    'OUTPUT_TEXT_FILE': os.path.join(os.getcwd(), "output", "recognized_text.txt"),

    # Post-processing files
    'CLEANED_TEXT_FILE': os.path.join(os.getcwd(), "output", "cleaned_text.txt"),
    'SPELLCHECKED_TEXT_FILE': os.path.join(os.getcwd(), "output", "spell_checked_text.txt"),
    'TSV_OUTPUT_FILE': os.path.join(os.getcwd(), "output", "recognized_text.tsv"),

    # Dictionaries
    'CUSTOM_DICTIONARIES_DIR': os.path.join(os.getcwd(), "resources", "dictionaries", "custom_ru"),
    'HUNSPELL_DICT_PATH': os.path.join(os.getcwd(), "resources", "dictionaries", "ru_RU"),

    # Logs
    'SPELLCHECK_LOG_PATH': os.path.join(os.getcwd(), "logs", "spell_log.txt"),
    
    # --- Operation Modes ---
    'ENABLE_OCR': True,                              # Enable OCR text recognition (False = image processing only)
    'SKIP_PREPROCESSING': True,                      # Skip preprocessing (True = OCR only without image enhancement)
    'ENABLE_POSTPROCESSING': True,                   # Enable postprocessing (cleanup, spellcheck, formatting)
    
    # --- Color Settings ---
    'FORCE_GRAYSCALE': True,                          # Convert images to grayscale before processing
    
    # --- Brightness/Contrast Settings ---
    'APPLY_BRIGHTNESS': True,                         # Enable brightness correction
    'BRIGHTNESS_GRADIENT_TYPE': 'vertical',           # Gradient type: 'radial', 'horizontal', 'vertical', 'edges'
    'BRIGHTNESS_GRADIENT_DIRECTION': 'top_to_bottom', # Gradient direction 
                                                      # ('left_to_right', 'right_to_left', 'top_to_bottom', 'bottom_to_top')
    'BRIGHTNESS_STRENGTH': 0.1,                       # Brightness effect strength (0-1)
    'ENHANCE_CONTRAST': True,                         # Enable contrast enhancement
    'CONTRAST_CLIP_LIMIT': (1, 99),                   # Histogram clip percentiles for contrast stretching
    'CORRECT_BRIGHTNESS_CONTRAST_GAMMA': True,        # Enable brightness, contrast, gamma correction
    'BRIGHTNESS': -73,                                # Brightness adjustment (-255 to +255),
                                                      # working value: -73 (optimized for specific use case)
    'CONTRAST': 30,                                   # Contrast adjustment (-127 to +127), 
                                                      # working value: 30 (optimized for specific use case)
    'GAMMA': 4.80,                                    # Gamma correction (1.0=no change), 
                                                      # working value: 4.80 (optimized for specific use case)
    
    # --- Cropping Settings ---
    'CROP': True,                                     # Enable automatic image cropping
    'CROP_PADDING': 0,                                # Additional padding (in pixels) for cropped edges

    'STABILITY_RANGE': 10,                            # Pixel range for edge detection stability zone
                                                      # the area after brightness transition where luminosity should stabilize

    'CENTER_BOX_MARGIN': {                            # Margins from image edges defining the central area 
                                                      # where edge detection begins (avoids false border detection)
        'left': 0.15,                                 # Left margin as percentage of image width
        'right': 0.15,                                # Right margin as percentage of image width
        'top': 0.15,                                  # Top margin as percentage of image height
        'bottom': 0.15                                # Bottom margin as percentage of image height
    },

    'BRIGHTNESS_DIFF_THRESHOLD': {                    # Brightness difference threshold for edge detection
        'left': 30,                                   # Left edge threshold (0-255)
        'right': 30,                                  # Right edge threshold (0-255)
        'top': 30,                                    # Top edge threshold (0-255)
        'bottom': 30                                  # Bottom edge threshold (0-255)
    },
    
    # --- Rotation Settings ---
    'ROTATE': True,                                   # Enable automatic image rotation
    'ROTATION_ANGLE': 90,                             # Rotation angle (degrees or 'auto')
    'ROTATION_METHOD': 'auto',                        # Rotation detection method ('auto','horizontal','vertical')
    'FINE_ROTATION': True,                            # Enable fine rotation adjustment after initial rotation
    
    # --- OCR Settings ---
    'DOCUMENT_TYPE': 'typewritten',                   # Document content type ('typewritten' or 'handwritten')    
    'OCR_LANGUAGE': 'rus',                            # Language code for OCR engine ('rus', 'deu', 'lav', or 'auto')
    'SPELLCHECK_LANGUAGE': 'ru'                       # Language code for spell checker (ISO format: 'ru', 'de', 'lv')

}

# --- Create Required Directories ---
os.makedirs(settings['INPUT_FOLDER'], exist_ok=True)
os.makedirs(settings['PROCESSED_FOLDER'], exist_ok=True)
os.makedirs(settings['OUTPUT_DIR'], exist_ok=True)

# Create directory for spellcheck log if it doesn't exist
spell_log_dir = os.path.dirname(settings['SPELLCHECK_LOG_PATH'])
os.makedirs(spell_log_dir, exist_ok=True)

# Module exports
__all__ = ['settings']