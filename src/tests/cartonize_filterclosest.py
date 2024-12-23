import cv2
import numpy as np
from cvzone.SelfiSegmentationModule import SelfiSegmentation

# Initialize the segmentation object
segmentor = SelfiSegmentation()

def cartoonize_frame(frame):
    """
    Removes the background from a video frame, applies a cartoon effect without stylization, and replaces the background with white.
    Args:
        frame (np.ndarray): Original video frame.
    Returns:
        np.ndarray: Cartoon-stylized video frame with background removed and replaced with white.
    """
    # Step 1: Remove the background using SelfiSegmentation and replace it with white
    white = (255, 255, 255)  # White background
    frame_no_bg = segmentor.removeBG(frame, white)

    # Step 2: Convert the frame to grayscale
    gray = cv2.cvtColor(frame_no_bg, cv2.COLOR_BGR2GRAY)

    # Step 3: Apply median blur to reduce noise
    gray_blurred = cv2.medianBlur(gray, 7)

    # Step 4: Detect edges using adaptiveThreshold
    edges = cv2.adaptiveThreshold(
        gray_blurred,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        9,
        9,
    )

    # Step 5: Smooth the original frame using bilateral filtering
    color = cv2.bilateralFilter(frame_no_bg, d=9, sigmaColor=150, sigmaSpace=150)

    # Step 6: Convert edges to a 3-channel image to blend with the color image
    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    # Step 7: Combine the smoothed color image with the edges using bitwise operations
    final_cartoon = cv2.bitwise_and(color, edges_colored)

    return final_cartoon
