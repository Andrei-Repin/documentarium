from typing import Tuple, Optional
import cv2
import numpy as np
from image_processing.rotation import apply_rotation
from image_processing.cropping import smart_crop
from image_processing.brightness_contrast import enhance_contrast, apply_brightness_gradient, apply_brightness_contrast_gamma

def process_image(image, settings) -> np.ndarray:
    """
    The main function of image processing
    
    Args:
        image (numpy.ndarray): Input image
        settings (dict): Processing settings
        
    Returns:
        numpy.ndarray: Processed image
    """
    # 1. Rotate image
    rotated, fine_angle = apply_rotation(image, settings)

    # 2. Background cropping
    if settings.get('CROP', True):
        rotated = smart_crop(rotated, settings)  

    # 4. Apply brightness (if needed)
    if settings.get('APPLY_BRIGHTNESS'):
        rotated = apply_brightness_gradient(rotated, **{
        'gradient_type': settings.get('BRIGHTNESS_GRADIENT_TYPE', 'radial'),
        'strength': settings.get('BRIGHTNESS_STRENGTH', 0.5),
        'gradient_direction': settings.get('BRIGHTNESS_GRADIENT_DIRECTION', None)
    })

    # 5. Apply contrast
    enhanced = enhance_contrast(rotated, force_grayscale=settings['FORCE_GRAYSCALE'])

    # 6. Correction of brightness, contrast, gamma (if needed)
    if settings.get('CORRECT_BRIGHTNESS_CONTRAST_GAMMA', True):
        enhanced = apply_brightness_contrast_gamma(enhanced, settings)

    return enhanced