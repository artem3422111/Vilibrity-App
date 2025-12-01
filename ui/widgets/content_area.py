import json
import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, QGridLayout
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPainter, QPixmap, QLinearGradient, QColor, QPainterPath, QFont
from ui.styles.colors import Colors
from api.api_client import api_client
from .continue_watching_card import ContinueWatchingCard

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

class ContinueWatchingSection(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.continue_watching_data = []
        self.setup_ui()
        self.load_continue_watching_data()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Заголовок секции
        title_label = QLabel("Продолжить просмотр")
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                font-family: Inter;
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 30px;
            }}
        """)
        layout.addWidget(title_label)
        
        # Сетка для карточек с 5 в строке и отступом 43px
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setHorizontalSpacing(43)  # Отступ между карточками по горизонтали 43px
        self.grid_layout.setVerticalSpacing(30)    # Отступ между карточками по вертикали 30px
        
        layout.addLayout(self.grid_layout)
        
        # Добавляем растягивающийся спейсер после сетки
        layout.addStretch()
        
    def load_continue_watching_data(self):
        """Загружает данные о продолжении просмотра из JSON файла"""
        try:
            if os.path.exists('continue_watching.json'):
                with open('continue_watching.json', 'r', encoding='utf-8') as f:
                    self.continue_watching_data = json.load(f)
            
            self.update_cards_display()
        except Exception as e:
            print(f"Ошибка загрузки continue_watching.json: {e}")
            self.continue_watching_data = []
    
    def update_cards_display(self):
        """Обновляет отображение карточек в сетке"""
        # Очищаем старые карточки
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        # Если есть данные, показываем карточки в сетке 5 в строке
        if self.continue_watching_data:
            for i, anime_data in enumerate(self.continue_watching_data):
                row = i // 5  # Номер строки
                col = i % 5   # Номер колонки
                
                card = ContinueWatchingCard(anime_data)
                self.grid_layout.addWidget(card, row, col)

class ContentArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.load_initial_data()
        
    def setup_ui(self):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                background-color: {Colors.DARK_GRAY};
                border: none;
            }}
            QScrollArea > QWidget > QWidget {{
                background-color: {Colors.DARK_GRAY};
            }}
        """)
        
        scroll_content = QWidget()
        scroll_area.setWidget(scroll_content)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(scroll_area)
        
        content_layout = QVBoxLayout(scroll_content)
        content_layout.setContentsMargins(50, 40, 50, 40)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        content_layout.setSpacing(0)
        
        # Баннер с рекомендациями
        self.banner = BannerWidget()
        content_layout.addWidget(self.banner)
        
        # Отступ 70px после баннера
        continue_watching_spacer = QSpacerItem(20, 70, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        content_layout.addItem(continue_watching_spacer)
        
        # Секция "Продолжить просмотр" (будет скрыта если нет данных)
        self.continue_watching_section = ContinueWatchingSection()
        content_layout.addWidget(self.continue_watching_section)
        
        # Spacer для заполнения оставшегося пространства
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        content_layout.addItem(spacer)
        
    def load_initial_data(self):
        recommended_data = api_client.get_recommended()
        self.banner.update_recommended(recommended_data)
        
        # Скрываем секцию "Продолжить просмотр" если нет данных
        if not self.continue_watching_section.continue_watching_data:
            self.continue_watching_section.hide()
        else:
            self.continue_watching_section.show()