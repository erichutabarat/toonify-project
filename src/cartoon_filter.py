import cv2
import numpy as np

def cartoonize_frame(frame):
    """
    Mengonversi frame menjadi gaya kartun.
    Args:
        frame (np.ndarray): Gambar asli (frame dari kamera).
    Returns:
        np.ndarray: Gambar yang sudah diberi efek kartun.
    """
    # 1. Ubah ke grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 2. Lakukan GaussianBlur untuk mengurangi noise
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)

    # 3. Deteksi tepi menggunakan adaptiveThreshold
    edges = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9
    )

    # 4. Ubah kembali ke warna untuk dikombinasikan dengan hasil lainnya
    color = cv2.bilateralFilter(frame, d=9, sigmaColor=75, sigmaSpace=75)

    # 5. Kombinasikan tepi dengan gambar warna
    cartoon = cv2.bitwise_and(color, color, mask=edges)

    return cartoon
