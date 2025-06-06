import cv2
import numpy as np

def apply_brightness_gradient(image, gradient_type='radial', strength=0.5, gradient_direction=None):
    """
    Applies brightness gradient to an image to correct uneven illumination.
    
    Parameters:
        image (numpy.ndarray): Input image (BGR or grayscale)
        gradient_type (str): Gradient type:
            - 'radial': radial gradient (brighter center, darker edges)
            - 'horizontal': horizontal gradient (left_to_right or right_to_left)
            - 'vertical': vertical gradient (top_to_bottom or bottom_to_top)
            - 'edges': brightness increases towards edges
        strength (float): Effect strength (0 - no change, 1 - maximum effect)
        gradient_direction (str): Gradient direction (for horizontal/vertical):
            - horizontal: 'left_to_right' or 'right_to_left'
            - vertical: 'top_to_bottom' or 'bottom_to_top'
    
    Returns:
        numpy.ndarray: Image with applied brightness gradient
    """
    h, w = image.shape[:2]

    # Normalize the image
    img_float = image.astype(np.float32) / 255.0

    # Create mask
    if gradient_type == 'radial':
        y, x = np.ogrid[:h, :w]
        center_y, center_x = h / 2, w / 2
        aspect = w / h
        norm_x = (x - center_x) / aspect
        norm_y = (y - center_y)
        distance = np.sqrt(norm_x**2 + norm_y**2)
        max_distance = np.sqrt((center_x / aspect)**2 + center_y**2)
        mask = 1 + strength * ((distance / max_distance) - 1)

    elif gradient_type == 'horizontal':
        if gradient_direction == 'right_to_left':
            x = np.linspace(1, 1 - strength, w)
        else:  # Default - left_to_right
            x = np.linspace(1 - strength, 1, w)
        mask = np.tile(x, (h, 1))

    elif gradient_type == 'vertical':
        if gradient_direction == 'bottom_to_top':
            y = np.linspace(1, 1 - strength, h)
        else:  # Default - top_to_bottom
            y = np.linspace(1 - strength, 1, h)
        mask = np.tile(y[:, np.newaxis], (1, w))

    elif gradient_type == 'edges':
        y, x = np.ogrid[:h, :w]
        dist_y = np.minimum(y, h - y - 1)
        dist_x = np.minimum(x, w - x - 1)
        distance = np.minimum(dist_y, dist_x)
        mask = 1 + strength * (1 - distance / np.max(distance))

    else:
        # No changes
        mask = np.ones((h, w), dtype=np.float32)

    # Apply mask
    if img_float.ndim == 3 and img_float.shape[2] == 3:
        mask = np.repeat(mask[:, :, np.newaxis], 3, axis=2)

    adjusted = img_float * mask
    adjusted = np.clip(adjusted, 0, 1)
    return (adjusted * 255).astype(np.uint8)

def enhance_contrast(image, force_grayscale=False, clip_limit=(1, 99)):
    """
    Enhances image contrast with optional grayscale conversion.
    
    Parameters:
        image (numpy.ndarray): Input image
        force_grayscale (bool): Force grayscale conversion
        clip_limit (tuple): Histogram clipping percentiles (lower, upper)
    
    Returns:
        numpy.ndarray: Contrast-enhanced image
    """
    if force_grayscale:
        # Convert to grayscale if needed
        if len(image.shape) == 3 and image.shape[2] == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image  # Already grayscale
        
        # Stretch histogram while ignoring outliers
        min_val, max_val = np.percentile(gray, clip_limit)
        if max_val - min_val < 1:  # Prevent division by zero
            return gray 
               
        enhanced = np.clip((gray - min_val) * (255.0 / (max_val - min_val)), 0, 255).astype(np.uint8)
        return enhanced
    
    else:
        # Process each color channel separately
        channels = cv2.split(image)
        stretched_channels = []

        for channel in channels:
            min_val, max_val = np.percentile(channel, clip_limit)
            if max_val - min_val < 1:
                stretched_channels.append(channel)
                continue
                        
            stretched = np.clip((channel - min_val) * (255.0 / (max_val - min_val)), 0, 255).astype(np.uint8)
            stretched_channels.append(stretched)

        enhanced = cv2.merge(stretched_channels)
        return enhanced

def apply_brightness_contrast_gamma(image, settings):
    """
    Adjusts image brightness, contrast and gamma.
    
    Args:
        image (numpy.ndarray): Input image (BGR or grayscale)
        settings (dict): Adjustment settings with keys:
            'BRIGHTNESS' (int): -255 to +255 (default 0)
            'CONTRAST' (int): -127 to +127 (default 0)
            'GAMMA' (float): > 0.0 (default 1.0)
    
    Returns:
        numpy.ndarray: Processed image
    """
    img = image.copy()
    
    # Convert to float32 for precise calculations
    img = img.astype(np.float32)
    
    brightness = settings.get('BRIGHTNESS', 0)
    contrast = settings.get('CONTRAST', 0)
    gamma = settings.get('GAMMA', 1.0)

    # Brightness: simple addition/subtraction
    if brightness != 0:
        img += brightness

    # Contrast: multiply by coefficient
    if contrast != 0:
        f = 131 * (contrast + 127) / (127 * (131 - contrast))
        img = f * (img - 127) + 127

    # Gamma correction
    if gamma != 1.0:
        # Normalize to 0-1 range, apply gamma, then scale back
        img = np.clip(img, 0, 255) / 255.0
        img = np.power(img, 1.0 / gamma)
        img *= 255.0

    # Clip values and convert back to uint8
    img = np.clip(img, 0, 255).astype(np.uint8)
    
    return img
