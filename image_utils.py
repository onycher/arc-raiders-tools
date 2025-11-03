import logging
from typing import Any

import cv2
import mss
import numpy as np


from constants import TEMPLATE_IMAGE_PATH


def find_popup(
    image: np.ndarray[Any, np.dtype[Any]],
) -> np.ndarray[Any, np.dtype[Any]] | None:  # type: ignore
    """
    Find and extract the popup from the image using template matching and flood fill.

    Args:
        image: The input image.

    Returns:
        The cropped popup image or None if not found.
    """
    template = cv2.imread(str(TEMPLATE_IMAGE_PATH))
    if template is None:
        logging.error("Template image not found.")
        return None

    template_h, template_w = template.shape[:2]
    image_h, image_w = image.shape[:2]

    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    # Confidence threshold
    confidence_threshold = 0.4
    if max_val < confidence_threshold:
        logging.warning(f"Template match confidence too low: {max_val:.2f}")
        return None

    top_left = max_loc

    seed_point = (top_left[0], top_left[1] + template_h - 1)

    mask = np.zeros((image_h + 2, image_w + 2), np.uint8)

    lo_diff = (10, 10, 10)
    up_diff = (10, 10, 10)

    flags = 4 | cv2.FLOODFILL_MASK_ONLY | (1 << 8)

    _ = cv2.floodFill(image, mask, seed_point, 0, lo_diff, up_diff, flags)

    filled_mask = mask[1:-1, 1:-1]
    rows, cols = np.where(filled_mask == 1)

    if rows.size > 0 and cols.size > 0:
        y_min = np.min(rows)
        y_max = np.max(rows)
        x_min = np.min(cols)
        x_max = np.max(cols)

        # Ensure minimum size
        if (x_max - x_min) < 100 or (y_max - y_min) < 50:
            logging.warning("Detected popup too small.")
            return None

        cropped = image[y_min:y_max, x_min:x_max]
        logging.info(
            f"Popup found at ({x_min}, {y_min}) with size {x_max - x_min}x{y_max - y_min}"
        )
        return cropped
    else:
        logging.warning("Flood fill found no area.")
        return None


def capture_screen() -> np.ndarray[Any, np.dtype[Any]]:  # type: ignore
    """
    Capture the screen and return as a BGR image.

    Returns:
        The screenshot as a numpy array.
    """
    with mss.mss() as sct:
        sct_img = sct.grab(sct.monitors[1])
    img_np = np.array(sct_img)
    return cv2.cvtColor(img_np, cv2.COLOR_BGRA2BGR)
