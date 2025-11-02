import cv2
import numpy as np


# --- 1. Load Images ---
def find_popup(image):
    template = cv2.imread("actions.png")

    template_h, template_w = template.shape[:2]
    image_h, image_w = image.shape[:2]

    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    top_left = max_loc

    seed_point = (top_left[0], top_left[1] + template_h - 1)

    mask = np.zeros((image_h + 2, image_w + 2), np.uint8)

    lo_diff = (10, 10, 10)
    up_diff = (10, 10, 10)

    flags = 4 | cv2.FLOODFILL_MASK_ONLY | (1 << 8)

    cv2.floodFill(image, mask, seed_point, 0, lo_diff, up_diff, flags)

    filled_mask = mask[1:-1, 1:-1]
    rows, cols = np.where(filled_mask == 1)

    if rows.size > 0 and cols.size > 0:
        # Find the bounding box of the filled area
        y_min = np.min(rows)
        y_max = np.max(rows)
        x_min = np.min(cols)
        x_max = np.max(cols)

        final_cropped_image = image[y_min : y_max + 1, x_min : x_max + 1]
        return final_cropped_image
    else:
        return None


image = cv2.imread("image.png")
find_popup(image)
