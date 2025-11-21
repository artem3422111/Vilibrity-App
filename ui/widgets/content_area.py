# content_area.py (исправленная версия)
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPainter, QPixmap, QLinearGradient, QColor, QPainterPath, QFont
from ui.styles.colors import Colors
from api.api_client import api_client
from .anime_grid import AnimeGridWidget

class CategorySwitchWidget(QWidget):
    category_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(500, 40)
        self.active_category = "Все"
        self.buttons = {}
        self.setup_ui()
        
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        categories = ["Все", "В тренде", "Новинки", "Популярное"]
        
        for category in categories:
            button = QPushButton(category)
            button.setFixedSize(120, 30)
            
            font = QFont("Inter")
            font.setPointSize(12)
            font.setBold(True)
            button.setFont(font)
            
            if category == "Все":
                button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {Colors.BUTTON_COLOR_GRAY};
                        border: none;
                        border-radius: 7px;
                        color: {Colors.TEXT_PRIMARY};
                    }}
                    QPushButton:hover {{
                        background-color: {Colors.BUTTON_HOVER_GRAY};
                    }}
                """)
            else:
                button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: transparent;
                        border: none;
                        border-radius: 7px;
                        color: {Colors.TEXT_PRIMARY};
                    }}
                    QPushButton:hover {{
                        background-color: {Colors.BUTTON_HOVER_GRAY};
                    }}
                """)
            
            button.clicked.connect(lambda checked, cat=category: self.on_category_clicked(cat))
            
            layout.addWidget(button)
            self.buttons[category] = button
        
    def on_category_clicked(self, category):
        if self.active_category:
            self.set_category_active(self.active_category, False)
        
        self.set_category_active(category, True)
        self.active_category = category
        
        self.category_changed.emit(category)
    
    def set_category_active(self, category, active):
        button = self.buttons.get(category)
        if button:
            if active:
                button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {Colors.BUTTON_COLOR_GRAY};
                        border: none;
                        border-radius: 7px;
                        color: {Colors.TEXT_PRIMARY};
                    }}
                    QPushButton:hover {{
                        background-color: {Colors.BUTTON_HOVER_GRAY};
                    }}
                """)
            else:
                button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: transparent;
                        border: none;
                        border-radius: 7px;
                        color: {Colors.TEXT_PRIMARY};
                    }}
                    QPushButton:hover {{
                        background-color: {Colors.BUTTON_HOVER_GRAY};
                    }}
                """)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 10, 10)
        painter.fillPath(path, QColor(Colors.LIGHT_GRAY))

class ContinueWatchingSection(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        title_label = QLabel("Продолжить просмотр")
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                font-family: Inter;
                font-size: 24px;
                font-weight: bold;
            }}
        """)
        layout.addWidget(title_label)
        
        placeholder = QLabel("Здесь будут карточки аниме, которые вы не досмотрели")
        placeholder.setStyleSheet(f"""
            QLabel {{
                color: {Colors.TEXT_SECONDARY};
                font-family: Inter;
                font-size: 16px;
                padding: 20px;
                background-color: {Colors.DARK_LIGHT_GRAY};
                border-radius: 10px;
            }}
        """)
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setMinimumHeight(200)
        layout.addWidget(placeholder)

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

class ContentArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_category = "Все"
        self.setup_ui()
        self.load_initial_data()
        
    def setup_ui(self):
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
        
        scroll_content = QWidget()
        scroll_area.setWidget(scroll_content)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(scroll_area)
        
        content_layout = QVBoxLayout(scroll_content)
        content_layout.setContentsMargins(50, 40, 50, 0)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        content_layout.setSpacing(40)
        
        self.banner = BannerWidget()
        content_layout.addWidget(self.banner)
        
        continue_watching_spacer = QSpacerItem(20, 80, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        content_layout.addItem(continue_watching_spacer)
        
        self.continue_watching_section = ContinueWatchingSection()
        content_layout.addWidget(self.continue_watching_section)
        
        categories_spacer = QSpacerItem(20, 80, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        content_layout.addItem(categories_spacer)
        
        self.category_switch = CategorySwitchWidget()
        content_layout.addWidget(self.category_switch)
        
        self.anime_grid = AnimeGridWidget()
        content_layout.addWidget(self.anime_grid)
        
        self.category_switch.category_changed.connect(self.on_category_changed)
        self.anime_grid.load_more.connect(self.load_more_anime)
        
    def load_initial_data(self):
        recommended_data = api_client.get_recommended()
        self.banner.update_recommended(recommended_data)
        
        self.load_anime_by_category(self.current_category)
    
    def on_category_changed(self, category):
        self.current_category = category
        self.anime_grid.current_page = 1
        self.anime_grid.current_category = category
        self.anime_grid.clear_grid()
        self.load_anime_by_category(category)
    
    def load_anime_by_category(self, category):
        if category == "Все":
            data = api_client.get_anime_list("all", self.anime_grid.current_page)
        elif category == "В тренде":
            data = api_client.get_trending(self.anime_grid.current_page)
        elif category == "Новинки":
            data = api_client.get_new(self.anime_grid.current_page)
        elif category == "Популярное":
            data = api_client.get_popular(self.anime_grid.current_page)
        
        if "data" in data and isinstance(data["data"], list):
            self.anime_grid.add_anime_cards(data["data"])
    
    def load_more_anime(self):
        self.anime_grid.current_page += 1
        self.load_anime_by_category(self.current_category)