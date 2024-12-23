import cv2
import numpy as np
from cvzone.SelfiSegmentationModule import SelfiSegmentation

# Initialize the segmentation object
segmentor = SelfiSegmentation()

def cartoonize_frame(frame):
    """
    Removes the background from a video frame, replaces it with a white background, and applies a cartoon effect.
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
    gray = cv2.medianBlur(gray, 1)

    # Step 4: Detect edges using adaptiveThreshold
    edges1 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

    # Step 5: Apply bilateral filter to the original frame for a smooth, paint-like effect
    color = cv2.bilateralFilter(frame_no_bg, 9, 250, 250)

    # Step 6: Combine the color image with the edges to create the cartoon effect
    cartoon1 = cv2.bitwise_and(color, color, mask=edges1)

    return cartoon1
