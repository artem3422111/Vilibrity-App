from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPixmap, QColor, QPainterPath
from ui.styles.colors import Colors

class ContinueWatchingCard(QWidget):
    def __init__(self, anime_data, parent=None):
        super().__init__(parent)
        self.anime_data = anime_data
        self.setFixedSize(270, 458)
        self.setup_ui()
        
    def setup_ui(self):
        # Верхняя часть с изображением (270x330)
        self.image_label = QLabel(self)
        self.image_label.setGeometry(0, 0, 270, 330)
        
        if self.anime_data.get("image_path"):
            pixmap = QPixmap(self.anime_data["image_path"])
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
        
        # Нижняя часть с фоном (270x128)
        self.info_label = QLabel(self)
        self.info_label.setGeometry(0, 330, 270, 128)
        self.info_label.setStyleSheet(f"""
            QLabel {{
                background-color: {Colors.DARK_LIGHT_GRAY};
                border: 0px solid {Colors.DEEP_BLUE};
                border-top-width: 0px;
                border-right-width: 2px;
                border-bottom-width: 2px;
                border-left-width: 2px;
                border-top-left-radius: 0px;
                border-top-right-radius: 0px;
                border-bottom-left-radius: 18px;
                border-bottom-right-radius: 18px;
            }}
        """)
        
        # Название аниме (отступ слева 20px, сверху от изображения 31px)
        self.title_label = QLabel(self.anime_data.get("title", ""), self)
        self.title_label.setGeometry(20, 361, 230, 35)  # 330 + 31 = 361
        self.title_label.setStyleSheet(f"""
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                font-family: 'M PLUS 1';
                font-size: 14px;
                font-weight: 800;
                background: transparent;
            }}
        """)
        
        # Жанр аниме (отступ слева 20px, снизу 20px)
        self.genre_label = QLabel(self.anime_data.get("genre", ""), self)
        self.genre_label.setGeometry(20, 408, 150, 20)  # 458 - 20 - 30 = 408 (30 для высоты текста)
        self.genre_label.setStyleSheet(f"""
            QLabel {{
                color: {Colors.TEXT_SECONDARY};
                font-family: 'M PLUS 1';
                font-size: 12px;
                font-weight: 500;
                background: transparent;
            }}
        """)
        
        # Количество эпизодов (отступ справа 20px, снизу 20px)
        self.episodes_label = QLabel(self.anime_data.get("episodes", ""), self)
        self.episodes_label.setGeometry(150, 408, 100, 20)
        self.episodes_label.setStyleSheet(f"""
            QLabel {{
                color: {Colors.TEXT_SECONDARY};
                font-family: 'M PLUS 1';
                font-size: 12px;
                font-weight: 500;
                background: transparent;
            }}
        """)
        self.episodes_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        
        # Рейтинг
        self.rating_widget = QWidget(self)
        self.rating_widget.setGeometry(201, 10, 59, 21)
        self.rating_widget.setStyleSheet(f"""
            QWidget {{
                background-color: #9932CC;
                border-radius: 5px;
            }}
        """)
        
        # Контейнер для содержимого рейтинга
        rating_content = QWidget(self.rating_widget)
        rating_content.setGeometry(5, 0, 49, 21)
        
        # Звезда рейтинга
        star_label = QLabel("★", rating_content)
        star_label.setGeometry(3, 3, 15, 15)
        star_label.setStyleSheet(f"""
            QLabel {{
                color: white;
                font-size: 12px;
                font-weight: bold;
                background: transparent;
            }}
        """)
        
        # Текст рейтинга
        rating_text = QLabel(str(self.anime_data.get("rating", "9.2")), rating_content)
        rating_text.setGeometry(20, 2, 30, 17)
        rating_text.setStyleSheet(f"""
            QLabel {{
                color: white;
                font-family: 'M PLUS 1';
                font-size: 12px;
                font-weight: 700;
                background: transparent;
            }}
        """)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Рисуем обводку вокруг всей карточки
        border_path = QPainterPath()
        border_path.addRoundedRect(0, 0, self.width(), self.height(), 18, 18)
        painter.strokePath(border_path, QColor(Colors.DEEP_BLUE))