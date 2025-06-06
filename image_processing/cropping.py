import cv2
import numpy as np
import numbers


def smart_crop(image, settings):
    """
    Cropping an image, starting from a rectangle defined by margins from the edges, 
    with expansion to a stable brightness difference
    
    Args:
        image (numpy.ndarray): Input image (color or grayscale)
        settings (dict): Processing settings
        
    Returns:
        numpy.ndarray: Cropped image
    """
    # Grayscale Conversion
    if len(image.shape) == 3 and image.shape[2] == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    # Settings
    padding = settings.get('CROP_PADDING', 20)
    stability_range = settings.get('STABILITY_RANGE', 10)

    height, width = gray.shape

    # Margins from the edges that define the starting rectangle
    margin_settings = settings.get('CENTER_BOX_MARGIN', {})
    margin_left = int(margin_settings.get('left', 0.15) * width)
    margin_right = int(margin_settings.get('right', 0.15) * width)
    margin_top = int(margin_settings.get('top', 0.10) * height)
    margin_bottom = int(margin_settings.get('bottom', 0.10) * height)

    # Initial borders
    left = margin_left
    right = width - margin_right
    top = margin_top
    bottom = height - margin_bottom

    # Brightness threshold
    base_threshold = settings.get('BRIGHTNESS_DIFF_THRESHOLD', 25)
    if isinstance(base_threshold, dict):
        thresholds = {
            'left': base_threshold.get('left', 25),
            'right': base_threshold.get('right', 25),
            'top': base_threshold.get('top', 25),
            'bottom': base_threshold.get('bottom', 25)
        }
    elif isinstance(base_threshold, numbers.Number):
        thresholds = dict.fromkeys(['left', 'right', 'top', 'bottom'], base_threshold)
    else:
        raise ValueError("BRIGHTNESS_DIFF_THRESHOLD должен быть числом или словарём.")

    def expand_line(start, direction, axis='horizontal', threshold=25):
        """
        Moves from the starting position in the given direction along the axis (horizontal/vertical) 
        until it encounters a stable sharp brightness drop. The drop is considered true 
        if it is followed by a new stable zone of length STABILITY_RANGE.
        """
        max_range = width if axis == 'horizontal' else height

        for i in range(start, 0 if direction < 0 else max_range, direction):
            # Indexes for the "before" zone and the "after" zone
            prev_idx = i - direction * stability_range
            next_idxs = [i + j * direction for j in range(1, stability_range + 1)]

            if prev_idx < 0 or prev_idx >= max_range:
                continue
            if any(idx < 0 or idx >= max_range for idx in next_idxs):
                continue

            # Base brightness before the drop
            base = (
                np.mean(gray[:, prev_idx]) if axis == 'horizontal'
                else np.mean(gray[prev_idx, :])
            )

            # Brightness of the current strip
            current = (
                np.mean(gray[:, i]) if axis == 'horizontal'
                else np.mean(gray[i, :])
            )

            # Check for sudden changes
            diff = abs(current - base)
            if diff > threshold:
                # Check: is the brightness stable after the change?
                new_zone = [
                    np.mean(gray[:, idx]) if axis == 'horizontal'
                    else np.mean(gray[idx, :])
                    for idx in next_idxs
                ]
                new_mean = np.mean(new_zone)
                deviations = [abs(val - new_mean) for val in new_zone]

                if all(dev < threshold for dev in deviations):
                    return i

        return start

    # Expand on all sides
    left = expand_line(left, -1, axis='horizontal', threshold=thresholds['left'])
    right = expand_line(right, +1, axis='horizontal', threshold=thresholds['right'])
    top = expand_line(top, -1, axis='vertical', threshold=thresholds['top'])
    bottom = expand_line(bottom, +1, axis='vertical', threshold=thresholds['bottom'])

    # Apply padding
    left = max(0, left - padding)
    right = min(width, right + padding)
    top = max(0, top - padding)
    bottom = min(height, bottom + padding)

    return image[top:bottom, left:right]