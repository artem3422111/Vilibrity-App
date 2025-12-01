from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QFont
from ui.styles.colors import Colors
import config

class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(40)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 25, 0)
        layout.setSpacing(0)
        
        left_spacer = QSpacerItem(900, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        
        self.title_label = QLabel("Vilibrity App")
        font = QFont("M PLUS 1")
        font.setBold(True)
        font.setPointSize(12)
        self.title_label.setFont(font)
        
        self.title_label.setStyleSheet(f"""
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                background-color: transparent;
                padding: 0px;
            }}
        """)
        
        middle_spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        
        self.minimize_btn = QPushButton("−")
        self.minimize_btn.setFixedSize(25, 25)
        self.minimize_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                color: {Colors.TEXT_PRIMARY};
                font-size: 16px;
                font-weight: bold;
                border-radius: 10px;
            }}
            QPushButton:hover {{
                background-color: {Colors.BUTTON_COLOR_BLUE};
            }}
            QPushButton:pressed {{
                background-color: {Colors.BUTTON_HOVER_BLUE};
            }}
        """)
        
        button_spacer = QSpacerItem(20, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        
        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(25, 25)
        self.close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                color: {Colors.TEXT_PRIMARY};
                font-size: 16px;
                font-weight: bold;
                border-radius: 10px;
            }}
            QPushButton:hover {{
                background-color: {Colors.CLOSE_BUTTON_HOVER};
                color: white;
            }}
            QPushButton:pressed {{
                background-color: {Colors.CLOSE_BUTTON_PRESSED};
            }}
        """)
        
        layout.addItem(left_spacer)
        layout.addWidget(self.title_label)
        layout.addItem(middle_spacer)
        layout.addWidget(self.minimize_btn)
        layout.addItem(button_spacer)
        layout.addWidget(self.close_btn)
        
        layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        self.minimize_btn.clicked.connect(self.parent.showMinimized)
        self.close_btn.clicked.connect(self.parent.close)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        
        # Заливаем фон
        painter.fillRect(self.rect(), QColor(Colors.DARK_GRAY))
        
        # Рисуем нижнюю обводку 2px
        border_rect = self.rect()
        border_rect.setTop(border_rect.bottom() - 2)
        painter.fillRect(border_rect, QColor(Colors.DEEP_BLUE))