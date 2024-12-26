import cv2
import numpy as np
from cvzone.SelfiSegmentationModule import SelfiSegmentation

# Initialize the segmentation object
segmentor = SelfiSegmentation()

def cartoonize_frame(frame):
    """
    Removes the background from a video frame, replaces it with a white background,
    and applies a cartoon effect with edge detection applied before the oil painting effect.
    Args:
        frame (np.ndarray): Original video frame.
    Returns:
        np.ndarray: Cartoon-stylized video frame with background removed, brightened, oil-painted, and detailed edges.
    """
    # Step 1: Remove the background using SelfiSegmentation and replace it with white
    white = (255, 255, 255)  # White background
    frame_no_bg = segmentor.removeBG(frame, white)

    # Step 2: Increase brightness of the background-removed frame
    brightness_factor = 80  # Adjust brightness level
    bright_frame = cv2.convertScaleAbs(frame_no_bg, alpha=1, beta=brightness_factor)

    # Step 3: Detect edges from the brightened frame
    gray_frame = cv2.cvtColor(bright_frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    gray_frame = cv2.medianBlur(gray_frame, 7)  # Reduce noise
    edges = cv2.adaptiveThreshold(gray_frame, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

    # Step 4: Apply oil painting effect to the background-removed frame
    oil_painted = cv2.xphoto.oilPainting(bright_frame, 5, 1)

    # Step 5: Combine the oil-painted image with the edges
    cartoon = cv2.bitwise_and(oil_painted, oil_painted, mask=edges)

    return cartoon
