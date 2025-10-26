from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPixmap, QLinearGradient, QColor, QPainterPath, QFont
from ui.styles.colors import Colors

class BannerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(1520, 430)
        self.setup_ui()
        
    def setup_ui(self):
        # Не используем layout для абсолютного позиционирования элементов
        self.setup_banner_content()
        
    def setup_banner_content(self):
        # Прямоугольник с закруглением 7 и текстом "Рекомендуем"
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
        
        # Название аниме
        self.title_label = QLabel("Доктор Стоун: Финальная битва", self)
        self.title_label.setGeometry(25, 240, 800, 40)  # Отступ 20px от прямоугольника
        self.title_label.setStyleSheet(f"""
            QLabel {{
                color: white;
                font-family: Inter;
                font-size: 28px;
                font-weight: bold;
                background: transparent;
            }}
        """)
        
        # Описание аниме
        self.desc_label = QLabel("Эпический финал легендарного аниме. Сенку и его друзья вступают в последнюю битву за судьбу человечества.", self)
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
        
        # Кнопка "Смотреть сейчас"
        self.watch_button = QPushButton("Смотреть сейчас", self)
        self.watch_button.setGeometry(25, 365, 150, 35)  # Отступ 15px от текста, слева 25px
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
        
        # Кнопка "Подробнее..."
        self.details_button = QPushButton("Подробнее...", self)
        self.details_button.setGeometry(185, 365, 150, 35)  # Отступ 10px от первой кнопки
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
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Создаем закругленный прямоугольник для баннера
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 18, 18)
        painter.setClipPath(path)
        
        # Рисуем изображение
        pixmap = QPixmap("assets/images/Rectangle.png")
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(self.width(), self.height(), 
                                        Qt.AspectRatioMode.IgnoreAspectRatio, 
                                        Qt.TransformationMode.SmoothTransformation)
            painter.drawPixmap(0, 0, scaled_pixmap)
        
        # Рисуем градиентное затухание внизу
        gradient = QLinearGradient(0, self.height() - 150, 0, self.height())
        gradient.setColorAt(0, Qt.GlobalColor.transparent)
        gradient.setColorAt(1, QColor(Colors.DARK_GRAY))
        
        painter.setBrush(gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(0, self.height() - 150, self.width(), 150)
        
        # Рисуем затемнение сверху для лучшей читаемости текста
        top_gradient = QLinearGradient(0, 0, 0, 200)
        top_gradient.setColorAt(0, QColor(0, 0, 0, 150))
        top_gradient.setColorAt(1, Qt.GlobalColor.transparent)
        
        painter.setBrush(top_gradient)
        painter.drawRect(0, 0, self.width(), 200)

class ContentArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        # Создаем скроллируемую область
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                background-color: {Colors.DARK_GRAY};
                border: none;
            }}
            QScrollArea > QWidget > QWidget {{
                background-color: {Colors.DARK_GRAY};
            }}
        """)
        
        # Создаем виджет для скроллируемого контента
        scroll_content = QWidget()
        scroll_area.setWidget(scroll_content)
        
        # Layout для скроллируемого контента
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(scroll_area)
        
        # Layout для содержимого скролла
        content_layout = QVBoxLayout(scroll_content)
        content_layout.setContentsMargins(50, 40, 50, 0)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        content_layout.setSpacing(40)
        
        # Баннер рекомендуемого аниме
        self.banner = BannerWidget()
        content_layout.addWidget(self.banner)
        
        # Здесь будут другие элементы контента
        # TODO: Добавить другие секции (популярное, новинки и т.д.)