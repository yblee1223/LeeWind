import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLineEdit, QSlider, QLabel
from PyQt6.QtGui import QPainter, QColor, QPixmap, QBrush, QIcon
from PyQt6.QtCore import Qt, QRectF, QPropertyAnimation, QEasingCurve, pyqtSignal

color = QColor(0, 0, 0, 255)

class Button(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        # self.setFixedSize(100, 50)
        self.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 100);
                color: white;
                font-size: 18px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 150);
            }            
            QPushButton:pressed {
                background: rgba(255, 255, 255, 200);
            }  
        """)
        self.clicked.connect(self.onClicked)
    
    def onClicked(self):
        print(f"Button clicked: {self.text()}")

class SearchBar(QWidget):
    searchRequested = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.lineEdit = QLineEdit()
        self.lineEdit.setPlaceholderText("Search...")
        self.lineEdit.returnPressed.connect(self.onSearch)
        
        self.button = QPushButton()
        self.button.setIcon(QIcon("asset/img/search_icon.png"))  # 검색 아이콘 설정
        self.button.clicked.connect(self.onSearch)
        
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.button)
        
        self.setStyleSheet("""
            QLineEdit {
                margin-left: 400px;
                border: 2px solid #c0c0c0;
                border-radius: 10px;
                padding: 16px;
                background-color: rgba(255, 255, 255, 200);
                selection-background-color: #c0c0c0;
                font-size: 15px;

            }
            QLineEdit:focus {
                border-color: #a0a0a0;
            }
            QPushButton {
                margin-right: 400px;
                background: #e0e0e0;
                border: 2px solid #c0c0c0;
                border-radius: 10px;
                padding: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #d0d0d0;
            }
            QPushButton:pressed {
                background: rgba(255, 255, 255, 255);
            }  
        """)
        
    def onSearch(self):
        text = self.lineEdit.text()
        if text:
            self.searchRequested.emit(text)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LeeWind")
        self.showFullScreen()

        self.background = QPixmap("data/img/Screenshot 2024-07-25 at 11.32.41 PM.png")  # 이미지 파일 경로를 지정하세요

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)

        layout.addStretch()

        # Search input
        self.search_input = QLineEdit()
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 50);
                border: 2px solid white;
                border-radius: 5px;
                color: white;
                padding: 5px;
                font-size: 18px;
            }
        """)
        
        self.search_bar = SearchBar()
        self.search_bar.searchRequested.connect(self.onSearch)
        
        layout.addWidget(self.search_bar)
        layout.addStretch()

        # Slider
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: white;
                height: 4px;
            }
            QSlider::handle:horizontal {
                background: white;
                width: 16px;
                height: 16px;
                margin: -6px 0;
                border-radius: 8px;
            }
        """)
        layout.addWidget(self.slider)

        # label
        label_layout = QHBoxLayout()
        date_label = QLabel("2024-07-25")
        program_label = QLabel("VS Code")
        padding = QLabel("")

        # 왼쪽 정렬
        program_label.setStyleSheet("""
            color: white;
            font-size: 30px;
            font-weight: bold;
        """)
        program_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        # 오른쪽 정렬
        date_label.setStyleSheet("""
            color: white;
            font-size: 20px;
            font-weight: bold;
        """)
        date_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        label_layout.addWidget(program_label)
        label_layout.addWidget(padding)
        label_layout.addWidget(date_label)
        layout.addLayout(label_layout)

        # layout.addWidget(date_label)

        # Buttons
        button_layout = QHBoxLayout()
        button2 = Button("OCR")
        button1 = Button("Summary")
        button_layout.addWidget(button2)
        button_layout.addWidget(button1)
        layout.addLayout(button_layout)
    
    def onSearch(self, text):
        print(f"Searching for: {text}")
    
    def 


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())