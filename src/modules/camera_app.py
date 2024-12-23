# root/src/module/camerapp.py
import cv2
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from cartoon_filter import cartoonize_frame  # Ensure cartoon_filter exists and is implemented


class CameraApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Toonify")
        self.setGeometry(100, 100, 800, 600)

        # Widget to display video
        self.label = QLabel(self)
        self.label.setScaledContents(True)

        # Button to toggle filtering
        self.filter_button = QPushButton("Start Filtering", self)
        self.filter_button.clicked.connect(self.toggle_filtering)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.filter_button)  # Add the button to the layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Timer to capture camera frames
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        # Open camera
        self.cap = cv2.VideoCapture(0)

        # Filtering state
        self.filtering = False  # Start with no filter applied

        # Start timer
        self.timer.start(30)  # 30 ms interval (33 FPS)

    def update_frame(self):
        """
        Capture frame from camera, reverse it, and apply a cartoon filter if filtering is enabled.
        """
        ret, frame = self.cap.read()
        if ret:
            # Reverse the frame (flip horizontally)
            frame = cv2.flip(frame, 1)  # Use 1 for horizontal flip, 0 for vertical flip

            if self.filtering:
                # Apply cartoon effect
                frame = cartoonize_frame(frame)

            # Convert frame to QImage for display in PyQt5
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_BGR888)
            self.label.setPixmap(QPixmap.fromImage(qt_image))


    def toggle_filtering(self):
        """
        Toggle the filtering state and update the button text.
        """
        self.filtering = not self.filtering
        if self.filtering:
            self.filter_button.setText("Stop Filtering")
        else:
            self.filter_button.setText("Start Filtering")

    def closeEvent(self, event):
        """
        Release the camera when the application is closed.
        """
        self.cap.release()
        cv2.destroyAllWindows()
