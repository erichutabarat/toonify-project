# Updated camerapp.py
import cv2
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
from utils.cartoon_filter import cartoonize_frame


class CameraApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Toonify")
        self.resize(640, 480)  # Smaller default size

        # Video display widget
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("background-color: black;")  # Add background for better visibility
        self.label.setScaledContents(True)

        # Filter button
        self.filter_button = QPushButton("Start Filtering", self)
        self.filter_button.setMinimumHeight(40)
        self.filter_button.clicked.connect(self.toggle_filtering)

        # Layouts
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.filter_button)
        button_layout.addStretch()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.label)
        main_layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Timer to capture frames
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        # Open camera
        self.cap = cv2.VideoCapture(0)
        self.filtering = False  # Start without filtering
        self.timer.start(30)  # Refresh rate

    def update_frame(self):
        """
        Capture frame from camera, reverse it, and apply a cartoon filter if filtering is enabled.
        """
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)  # Flip horizontally
            if self.filtering:
                frame = cartoonize_frame(frame)

            # Convert the frame to QImage
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_BGR888)
            self.label.setPixmap(QPixmap.fromImage(qt_image))

    def toggle_filtering(self):
        """
        Toggle filtering and update button text.
        """
        self.filtering = not self.filtering
        self.filter_button.setText("Stop Filtering" if self.filtering else "Start Filtering")

    def closeEvent(self, event):
        """
        Release camera resources on close.
        """
        self.cap.release()
        cv2.destroyAllWindows()
