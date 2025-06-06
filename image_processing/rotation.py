import cv2
import numpy as np
import re
import pytesseract
from typing import Optional, Tuple

def detect_rotation(image) -> int:
    """
    Determines the rotation angle of an image using Tesseract OSD
    
    Args:
        image (numpy.ndarray): Input image
        
    Returns:
        int: Rotation angle in degrees (0, 90, 180, 270)
    """
    # Convert to Grayscale
    if len(image.shape) == 3 and image.shape[2] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    try:
        # Using Tesseract to Determine Orientation
        osd = pytesseract.image_to_osd(image)
        angle = int(re.search(r'Rotate: (\d+)', osd).group(1))
        return angle
    except (pytesseract.TesseractError, AttributeError) as e:
        print(f"[!] Unable to determine rotation angle: {e}")
        return 0  # Return 0 on error

def rotate_image(image, angle: int):
    """
    Rotates an image by a given angle while preserving all its contents.
    
    Args:
        image (numpy.ndarray): Input image
        angle (int): Rotation angle in degrees
        
    Returns:
        numpy.ndarray: Rotated image
    """
    (h, w) = image.shape[:2]
    center = (w / 2, h / 2)
    M = cv2.getRotationMatrix2D(center, -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    new_w = int((h * sin) + (w * cos))
    new_h = int((h * cos) + (w * sin))
    M[0, 2] += (new_w / 2) - center[0]
    M[1, 2] += (new_h / 2) - center[1]
    return cv2.warpAffine(image, M, (new_w, new_h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

def get_text_angle_by_horizontal_lines(image) -> float:

    # Determining the angle by horizontal lines of text (line spacing)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=150)

    if lines is None:
        return 0.0

    angles = []
    for rho, theta in lines[:, 0]:
        angle = (theta * 180) / np.pi
        if 80 < angle < 100:  # Selection of almost horizontal lines
            angles.append(angle - 90)  # Convert to text angle

    return np.mean(angles) if angles else 0.0

def get_text_angle_by_vertical_edges(image) -> float:

    # Determining the angle by vertical character boundaries
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=150)

    if lines is None:
        return 0.0

    angles = []
    for rho, theta in lines[:, 0]:
        angle_deg = np.degrees(theta)
        if angle_deg < 10 or angle_deg > 170:  # Selection of almost vertical lines
            angle = angle_deg if angle_deg < 90 else angle_deg - 180
            angles.append(angle)

    return np.mean(angles) if angles else 0.0

def get_text_angle_auto(image) -> float:

    # Automatic method selection based on image analysis
    angle_horizontal = get_text_angle_by_horizontal_lines(image)
    angle_vertical = get_text_angle_by_vertical_edges(image)
    
    # We evaluate the "confidence" of each method
    confidence_horizontal = count_relevant_lines(image, mode='horizontal')
    confidence_vertical = count_relevant_lines(image, mode='vertical')
    
    # Selection logic (thresholds can be adjusted)
    if confidence_horizontal >= confidence_vertical and abs(angle_horizontal) > 0.1:
        return angle_horizontal
    elif confidence_vertical > 0 and abs(angle_vertical) > 0.1:
        return angle_vertical
    return 0.0

def count_relevant_lines(image, mode='horizontal') -> int:

    # Calculation of relevant lines for assessing the confidence of the method
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=150)
    
    if lines is None:
        return 0
    
    count = 0
    for rho, theta in lines[:, 0]:
        angle_deg = np.degrees(theta)
        if mode == 'horizontal' and 80 < angle_deg < 100:
            count += 1
        elif mode == 'vertical' and (angle_deg < 10 or angle_deg > 170):
            count += 1
    
    return count

def get_text_angle_by_hough(image, method='auto') -> float:
    """
    Determines the angle of the text with the choice of analysis method
    
    Args:
        image: input image (numpy.ndarray)
        method: 
            'horizontal' - by line spacing
            'vertical' - by character boundaries
            'auto' - automatic selection
            
    Returns:
        float: tilt angle in degrees
    """
    if method == 'horizontal':
        return get_text_angle_by_horizontal_lines(image)
    elif method == 'vertical':
        return get_text_angle_by_vertical_edges(image)
    else:
        return get_text_angle_auto(image)

def fine_rotate_projection(image: np.ndarray, angle_range=(-2, 2), step=0.1, verbose=False) -> np.ndarray:
    """
    Rotates the image by a small angle (±2°) to precisely align text lines.
    The method is based on the analysis of horizontal projections of the image.

    Args:
        image (np.ndarray): Input image (color or grayscale)
        angle_range (tuple): Range of angles to iterate over, for example (-2, 2)
        step (float): Angle enumeration step in degrees
        verbose (bool): If True - prints the best angle found

    Returns:
        np.ndarray: Rotated image
    """

    # Convert to grayscale
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    # Let's define a list of angles to iterate over, for example: -2.0, -1.9, ..., 1.9
    angles = np.arange(angle_range[0], angle_range[1] + step, step)

    scores = []  # list of "horizontal" ratings for each angle

    for angle in angles:
        # Rotate image to current angle
        M = cv2.getRotationMatrix2D(center=(gray.shape[1] // 2, gray.shape[0] // 2),
                                    angle=angle, scale=1.0)
        rotated = cv2.warpAffine(gray, M, (gray.shape[1], gray.shape[0]),
                                 flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

        # Horizontal projection: sum of pixels across rows
        projection = np.sum(rotated, axis=1)

        # Assessing the sharpness of horizontal lines: projection dispersion
        score = np.var(projection)
        scores.append(score)

    # Selecting the angle with the greatest dispersion (the most "horizontal" lines)
    best_angle = angles[np.argmax(scores)]

    if verbose:
        print(f"[Fine rotate] Optimal rotation angle: {best_angle:.2f}°")

    # Final rotation of the original image (color or grayscale)
    M = cv2.getRotationMatrix2D(center=(image.shape[1] // 2, image.shape[0] // 2),
                                angle=best_angle, scale=1.0)
    rotated_final = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]),
                                   flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return rotated_final

def apply_rotation(image, settings) -> Tuple[np.ndarray, Optional[float]]:
    """
    Applies image rotation according to the settings
    
    Args:
        image (numpy.ndarray): Input image
        settings (dict): Processing settings
        
    Returns:
        Tuple: (rotated image, refined rotation angle)
    """
    if not settings['ROTATE']:
        return image, None
    
    # Determining the basic rotation angle
    if isinstance(settings['ROTATION_ANGLE'], int):  # Specific angle
        angle = settings['ROTATION_ANGLE']
    elif settings['ROTATION_ANGLE'] == 'auto':
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        angle = detect_rotation(gray)
    else:
        angle = 0  # Default is no rotation
    
    # Apply the basic rotation
    rotated = rotate_image(image, angle)
    
    # Adjust the angle of the text if required
    fine_angle = None

    doc_type = settings.get('DOCUMENT_TYPE', 'unknown')

    if settings.get('FINE_ROTATION', True):
        if doc_type in ['typewritten']:
            fine_angle = get_text_angle_by_hough(
                rotated, 
                method=settings.get('ROTATION_METHOD', 'auto')
            )
            if abs(fine_angle) > 0.5:
                rotated = rotate_image(rotated, -fine_angle)
        elif doc_type == 'handwritten':
            rotated = fine_rotate_projection(rotated)
            fine_angle = None  # No angle - separate logic applied
    
    return rotated, fine_angle