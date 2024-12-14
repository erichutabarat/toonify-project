import cv2
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QApplication
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from cartoon_filter import cartoonize_frame


class CameraApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Real-Time Cartoon Filter")
        self.setGeometry(100, 100, 800, 600)

        # Widget untuk menampilkan video
        self.label = QLabel(self)
        self.label.setScaledContents(True)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Timer untuk menangkap frame kamera
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        # Membuka kamera
        self.cap = cv2.VideoCapture(0)  # Kamera default

        # Mulai timer
        self.timer.start(30)  # 30 ms interval (33 FPS)

    def update_frame(self):
        """
        Fungsi untuk menangkap frame dari kamera dan menampilkannya
        dengan filter kartun.
        """
        ret, frame = self.cap.read()
        if ret:
            # Terapkan efek kartun
            cartoon_frame = cartoonize_frame(frame)

            # Konversi frame ke QImage untuk ditampilkan di PyQt5
            h, w, ch = cartoon_frame.shape
            bytes_per_line = ch * w
            qt_image = QImage(
                cartoon_frame.data, w, h, bytes_per_line, QImage.Format_BGR888
            )
            self.label.setPixmap(QPixmap.fromImage(qt_image))

    def closeEvent(self, event):
        """
        Menutup kamera saat aplikasi ditutup.
        """
        self.cap.release()
        cv2.destroyAllWindows()
