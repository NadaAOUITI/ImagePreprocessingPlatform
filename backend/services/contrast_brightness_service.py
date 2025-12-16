import cv2
import numpy as np


def apply_contrast_brightness(image, alpha=1.0, beta=0):
    """
    Apply contrast and brightness adjustment.

    :param image: Input image (numpy array)
    :param alpha: Contrast control (1.0 = original)
    :param beta: Brightness control (0 = original)
    :return: Processed image
    """
    if image is None:
        raise ValueError("Image invalide")

    # Convert to uint8 if needed
    if image.dtype != np.uint8:
        image = (image * 255).astype(np.uint8)

    adjusted = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return adjusted
