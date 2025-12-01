from PyQt6.QtWidgets import QWidget, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPixmap, QLinearGradient, QColor, QPainterPath
from ui.styles.colors import Colors

class BannerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(1520, 430)
        self.setup_ui()
        
    def setup_ui(self):
        self.setup_banner_content()
        
    def setup_banner_content(self):
        self.recommend_label = QLabel("Рекомендуем", self)
        self.recommend_label.setGeometry(25, 190, 125, 25)
        self.recommend_label.setStyleSheet(f"""
            QLabel {{
                background-color: {Colors.ACCENT_BLUE};
                border-radius: 7px;
                color: white;
                font-family: Inter;
                font-size: 14px;
                font-weight: bold;
                padding: 5px 10px;
            }}
        """)
        self.recommend_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.title_label = QLabel("", self)
        self.title_label.setGeometry(25, 240, 800, 40)
        self.title_label.setStyleSheet(f"""
            QLabel {{
                color: white;
                font-family: Inter;
                font-size: 28px;
                font-weight: bold;
                background: transparent;
            }}
        """)
        
        self.desc_label = QLabel("", self)
        self.desc_label.setGeometry(25, 290, 800, 60)
        self.desc_label.setStyleSheet(f"""
            QLabel {{
                color: white;
                font-family: Inter;
                font-size: 16px;
                background: transparent;
            }}
        """)
        self.desc_label.setWordWrap(True)
        
        self.watch_button = QPushButton("Смотреть сейчас", self)
        self.watch_button.setGeometry(25, 365, 150, 35)
        self.watch_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.BUTTON_COLOR_BLUE};
                border: none;
                border-radius: 7px;
                color: white;
                font-family: Inter;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {Colors.BUTTON_HOVER_BLUE};
            }}
        """)
        
        self.details_button = QPushButton("Подробнее...", self)
        self.details_button.setGeometry(185, 365, 150, 35)
        self.details_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.BUTTON_COLOR_GRAY};
                border: none;
                border-radius: 7px;
                color: white;
                font-family: Inter;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {Colors.BUTTON_HOVER_GRAY};
            }}
        """)
    
    def update_recommended(self, anime_data):
        if isinstance(anime_data, dict):
            self.title_label.setText(anime_data.get("title", ""))
            self.desc_label.setText(anime_data.get("description", ""))
        else:
            self.title_label.setText("Доктор Стоун: Финальная битва")
            self.desc_label.setText("Эпический финал легендарного аниме. Сенку и его друзья вступают в последнюю битву за судьбу человечества.")
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 18, 18)
        painter.setClipPath(path)
        
        pixmap = QPixmap("assets/images/Rectangle.png")
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(self.width(), self.height(), 
                                        Qt.AspectRatioMode.IgnoreAspectRatio, 
                                        Qt.TransformationMode.SmoothTransformation)
            painter.drawPixmap(0, 0, scaled_pixmap)
        
        gradient = QLinearGradient(0, self.height() - 150, 0, self.height())
        gradient.setColorAt(0, Qt.GlobalColor.transparent)
        gradient.setColorAt(1, QColor(Colors.DARK_GRAY))
        
        painter.setBrush(gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(0, self.height() - 150, self.width(), 150)
        
        top_gradient = QLinearGradient(0, 0, 0, 200)
        top_gradient.setColorAt(0, QColor(0, 0, 0, 150))
        top_gradient.setColorAt(1, Qt.GlobalColor.transparent)
        
        painter.setBrush(top_gradient)
        painter.drawRect(0, 0, self.width(), 200)