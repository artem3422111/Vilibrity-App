from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QFont, QPixmap, QIcon
from ui.styles.colors import Colors
import config

class LeftPanel(QWidget):
    button_clicked = pyqtSignal(str)  # Сигнал с ID нажатой кнопки
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(config.LEFT_PANEL_WIDTH, config.LEFT_PANEL_HEIGHT)
        self.active_button = None
        self.buttons = {}
        self.setup_ui()
        
        # Устанавливаем кнопку "Главная" активной по умолчанию
        self.set_default_active_button()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 20, 25, 20)  # Отступы: слева/справа 25px, сверху 20px
        layout.setSpacing(10)  # Расстояние между кнопками 10px
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Словарь с данными кнопок навигации
        buttons_data = {
            "Main": {
                "icon": "assets/icons/Городские ворота.png",
                "text": "Главная"
            },
            "Popular": {
                "icon": "assets/icons/Линейный график.png",
                "text": "Популярное"
            },
            "Recent": {
                "icon": "assets/icons/Время.png",
                "text": "Недавние"
            },
            "Favourites": {
                "icon": "assets/icons/Звезды.png",
                "text": "Избранное"
            },
            "Collection": {
                "icon": "assets/icons/Полка для документов.png",
                "text": "Коллекция"
            }
        }
        
        # Создаем кнопки навигации
        for button_id, button_data in buttons_data.items():
            button = self.create_nav_button(
                button_data["icon"],
                button_data["text"],
                button_id
            )
            layout.addWidget(button)
            self.buttons[button_id] = button
        
        # Отступ 25px перед разделом "Жанры"
        genres_spacer = QSpacerItem(20, 25, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        layout.addItem(genres_spacer)
        
        # Заголовок "Жанры"
        genres_label = QLabel("Жанры")
        genres_label.setStyleSheet(f"""
            QLabel {{
                color: {Colors.TEXT_GRAY};
                font-family: Inter;
                font-size: 16px;
                font-weight: bold;
            }}
        """)
        layout.addWidget(genres_label)
        
        # Отступ 20px после заголовка
        after_label_spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        layout.addItem(after_label_spacer)
        
        # Словарь с данными кнопок жанров
        genres_data = {
            "Action": {
                "text": "Экшен"
            },
            "Adventures": {
                "text": "Приключения"
            },
            "Comedy": {
                "text": "Комедия"
            },
            "Drama": {
                "text": "Драма"
            },
            "Fantasy": {
                "text": "Фэнтези"
            },
            "Romance": {
                "text": "Романтика"
            },
            "Science_fiction": {
                "text": "Научная фантастика"
            },
            "Thriller": {
                "text": "Триллер"
            }
        }
        
        # Создаем кнопки жанров
        for genre_id, genre_data in genres_data.items():
            button = self.create_genre_button(
                genre_data["text"],
                genre_id
            )
            layout.addWidget(button)
            self.buttons[genre_id] = button
        
        # Spacer для заполнения оставшегося пространства
        spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(spacer)
        
    def create_nav_button(self, icon_path, text, button_id):
        button = QPushButton(text)
        button.setFixedSize(250, 38)
        button.setObjectName(button_id)
        
        # Устанавливаем шрифт Inter, Bold, 16
        font = QFont("Inter")
        font.setBold(True)
        font.setPointSize(12)
        button.setFont(font)
        
        # Базовая стилизация (неактивное состояние)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                border-radius: 10px;
                color: {Colors.TEXT_PRIMARY};
                text-align: left;
                padding-left: 10px; /* Отступ слева 10px */
            }}
            QPushButton:hover {{
                background-color: {Colors.BUTTON_HOVER_BLUE};
            }}
        """)
        
        # Устанавливаем иконку без отступа от текста
        pixmap = QPixmap(icon_path)
        if not pixmap.isNull():
            icon = QIcon(pixmap)
            button.setIcon(icon)
            button.setIconSize(pixmap.rect().size())
        
        # Подключаем обработчик клика
        button.clicked.connect(lambda checked, bid=button_id: self.on_button_clicked(bid))
        
        return button
    
    def create_genre_button(self, text, button_id):
        button = QPushButton(text)
        button.setFixedSize(250, 38)
        button.setObjectName(button_id)
        
        # Устанавливаем шрифт Inter, Bold, 16
        font = QFont("Inter")
        font.setBold(True)
        font.setPointSize(12)
        button.setFont(font)
        
        # Стилизация для кнопок жанров (без иконок)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                border-radius: 10px;
                color: {Colors.TEXT_PRIMARY};
                text-align: left;
                padding-left: 10px; /* Отступ слева 10px */
            }}
            QPushButton:hover {{
                background-color: {Colors.BUTTON_HOVER_BLUE};
            }}
        """)
        
        # Подключаем обработчик клика
        button.clicked.connect(lambda checked, bid=button_id: self.on_button_clicked(bid))
        
        return button
    
    def set_default_active_button(self):
        # Устанавливаем кнопку "Главная" активной по умолчанию
        self.on_button_clicked("Main")
    
    def on_button_clicked(self, button_id):
        # Деактивируем предыдущую активную кнопку
        if self.active_button:
            self.set_button_active(self.active_button, False)
        
        # Активируем новую кнопку
        self.set_button_active(button_id, True)
        self.active_button = button_id
        
        # Отправляем сигнал
        self.button_clicked.emit(button_id)
    
    def set_button_active(self, button_id, active):
        button = self.buttons.get(button_id)
        if button:
            if active:
                button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {Colors.BUTTON_COLOR_BLUE};
                        border: none;
                        border-radius: 10px;
                        color: {Colors.TEXT_PRIMARY};
                        text-align: left;
                        padding-left: 10px;
                    }}
                    QPushButton:hover {{
                        background-color: {Colors.BUTTON_HOVER_BLUE};
                    }}
                """)
            else:
                button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: transparent;
                        border: none;
                        border-radius: 10px;
                        color: {Colors.TEXT_PRIMARY};
                        text-align: left;
                        padding-left: 10px;
                    }}
                    QPushButton:hover {{
                        background-color: {Colors.BUTTON_HOVER_BLUE};
                    }}
                """)
    
    def paintEvent(self, event):
        # Отрисовка фона панели с правой обводкой
        painter = QPainter(self)
        
        # Заливаем фон
        painter.fillRect(self.rect(), QColor(Colors.DARK_GRAY))
        
        # Рисуем правую обводку 2px
        border_rect = self.rect()
        border_rect.setLeft(border_rect.right() - 2)
        painter.fillRect(border_rect, QColor(Colors.DEEP_BLUE))