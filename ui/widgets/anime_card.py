from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPixmap, QColor, QPainterPath, QFont
from ui.styles.colors import Colors

class AnimeCard(QWidget):
    def __init__(self, title="", genre="", episodes="", image_path="", parent=None):
        super().__init__(parent)
        self.title = title
        self.genre = genre
        self.episodes = episodes
        self.image_path = image_path
        self.setFixedSize(270, 450)
        self.setup_ui()
        
    def setup_ui(self):
        # Сначала создаем фоновые элементы, затем текстовые поверх них
        self.setup_card_content()
        
    def setup_card_content(self):
        # Верхняя часть с изображением (270x330)
        self.image_label = QLabel(self)
        self.image_label.setGeometry(0, 0, 270, 330)
        
        # Загружаем изображение если путь указан
        if self.image_path:
            pixmap = QPixmap(self.image_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(270, 330, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
                self.image_label.setPixmap(scaled_pixmap)
        else:
            self.image_label.setStyleSheet(f"""
                QLabel {{
                    background-color: {Colors.LIGHT_GRAY};
                    border-top-left-radius: 18px;
                    border-top-right-radius: 18px;
                    border-bottom-left-radius: 0px;
                    border-bottom-right-radius: 0px;
                }}
            """)
        
        # Нижняя часть с информацией (270x120) - создаем ПЕРВОЙ
        self.info_label = QLabel(self)
        self.info_label.setGeometry(0, 330, 270, 120)
        self.info_label.setStyleSheet(f"""
            QLabel {{
                background-color: {Colors.DARK_LIGHT_GRAY};
                border-top-left-radius: 0px;
                border-top-right-radius: 0px;
                border-bottom-left-radius: 18px;
                border-bottom-right-radius: 18px;
            }}
        """)
        
        # Название аниме (отступ слева 20px, сверху от изображения 30px)
        self.title_label = QLabel(self.title, self)
        self.title_label.setGeometry(20, 360, 230, 25)  # 330 + 30 = 360
        self.title_label.setStyleSheet(f"""
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                font-family: Inter;
                font-size: 12px;
                font-weight: bold;
                background: transparent;
            }}
        """)
        
        # Жанр аниме (отступ слева 20px, снизу 20px)
        self.genre_label = QLabel(self.genre, self)
        self.genre_label.setGeometry(20, 405, 150, 20)  # 450 - 20 - 25 = 405
        self.genre_label.setStyleSheet(f"""
            QLabel {{
                color: {Colors.TEXT_SECONDARY};
                font-family: Inter;
                font-size: 12px;
                background: transparent;
            }}
        """)
        
        # Количество эпизодов (отступ справа 20px, снизу 20px)
        self.episodes_label = QLabel(self.episodes, self)
        self.episodes_label.setGeometry(150, 405, 100, 20)
        self.episodes_label.setStyleSheet(f"""
            QLabel {{
                color: {Colors.TEXT_SECONDARY};
                font-family: Inter;
                font-size: 12px;
                background: transparent;
            }}
        """)
        self.episodes_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Рисуем обводку вокруг всей карточки
        border_path = QPainterPath()
        border_path.addRoundedRect(0, 0, self.width(), self.height(), 18, 18)
        painter.strokePath(border_path, QColor(Colors.DEEP_BLUE))