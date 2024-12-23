import cv2
import numpy as np

def cartoonize_frame(frame):
    """
    Converts a video frame to a cartoon-styled frame.
    Args:
        frame (np.ndarray): Original video frame.
    Returns:
        np.ndarray: Cartoon-stylized video frame.
    """
    # 1. Convert the frame to grayscale
    gray_scale_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 2. Apply median blur to smooth the grayscale image
    smooth_gray_scale = cv2.medianBlur(gray_scale_image, 5)

    # 3. Detect edges using adaptiveThreshold
    edges = cv2.adaptiveThreshold(
        smooth_gray_scale,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        9,
        9,
    )

    # 4. Apply bilateral filter to the original frame for a smooth, paint-like effect
    color_image = cv2.bilateralFilter(frame, 9, 300, 300)

    # 5. Mask the edges with the color image
    cartoon_image = cv2.bitwise_and(color_image, color_image, mask=edges)

    return cartoon_image
