import os
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QFont, QPixmap, QColor, QIcon
from ui.styles.colors import Colors
import config

class TopPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(config.TOP_PANEL_HEIGHT)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Левый блок с логотипом и названием
        self.setup_left_section(layout)
        
        # Центральный блок с поиском
        self.setup_center_section(layout)
        
        # Правый блок с иконками
        self.setup_right_section(layout)
        
    def setup_left_section(self, layout):
        # Отступ слева 80px
        left_spacer = QSpacerItem(80, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        layout.addItem(left_spacer)
        
        # Квадрат логотипа 40x40 с закруглением 12
        self.logo_container = QLabel()
        self.logo_container.setFixedSize(40, 40)
        self.logo_container.setStyleSheet(f"""
            QLabel {{
                background-color: {Colors.ACCENT_BLUE};
                border-radius: 12px;
                color: white;
                font-size: 20px;
                font-weight: bold;
            }}
        """)
        self.logo_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_container.setText("V")
        
        layout.addWidget(self.logo_container)
        
        # Отступ между логотипом и названием 5px
        logo_text_spacer = QSpacerItem(5, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        layout.addItem(logo_text_spacer)
        
        # Название приложения
        self.app_name = QLabel("Vilibrity")
        font = QFont("M PLUS 1p")
        font.setBold(True)
        font.setPointSize(16)
        self.app_name.setFont(font)
        self.app_name.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        
        layout.addWidget(self.app_name)
        
    def setup_center_section(self, layout):
        # Spacer для центрирования поисковой строки
        center_left_spacer = QSpacerItem(430, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        layout.addItem(center_left_spacer)
        
        # Контейнер для поисковой строки
        search_container = QWidget()
        search_container.setFixedSize(600, 40)
        search_container.setStyleSheet(f"""
            QWidget {{
                background-color: {Colors.DARK_LIGHT_GRAY};
                border-radius: 14px;
            }}
        """)
        
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(10, 0, 10, 0)
        search_layout.setSpacing(15)
        
        # Иконка поиска
        search_icon = QLabel()
        search_icon.setFixedSize(24, 24)
        # Загружаем реальную иконку поиска
        search_pixmap = QPixmap("assets/icons/Поиск.png")
        if not search_pixmap.isNull():
            search_icon.setPixmap(search_pixmap.scaled(24, 24, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            # Заглушка если файл не найден
            search_icon.setStyleSheet(f"""
                QLabel {{
                    background-color: {Colors.TEXT_SECONDARY};
                    border-radius: 12px;
                }}
            """)
        search_layout.addWidget(search_icon)
        
        # Поле ввода поиска
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск аниме...")
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: transparent;
                border: none;
                color: {Colors.TEXT_PRIMARY};
                font-size: 16px;
            }}
            QLineEdit::placeholder {{
                color: {Colors.TEXT_SECONDARY};
            }}
        """)
        search_layout.addWidget(self.search_input)
        
        layout.addWidget(search_container)
        
        # Spacer для центрирования поисковой строки
        center_right_spacer = QSpacerItem(20, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        layout.addItem(center_right_spacer)
        
    def setup_right_section(self, layout):
        # Spacer для выравнивания правого блока
        right_spacer = QSpacerItem(20, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        layout.addItem(right_spacer)
        
        # Иконка колокольчика
        self.bell_icon = self.create_icon_button("assets/icons/Напоминать.png")
        layout.addWidget(self.bell_icon)
        
        # Отступ между иконками 25px
        icon_spacer1 = QSpacerItem(25, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        layout.addItem(icon_spacer1)
        
        # Иконка профиля
        self.profile_icon = self.create_icon_button("assets/icons/Пользователь.png")
        layout.addWidget(self.profile_icon)
        
        # Отступ между иконками 25px
        icon_spacer2 = QSpacerItem(25, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        layout.addItem(icon_spacer2)
        
        # Иконка настроек
        self.settings_icon = self.create_icon_button("assets/icons/Настроить.png")
        layout.addWidget(self.settings_icon)
        
        # Отступ от правого края 80px
        right_margin_spacer = QSpacerItem(80, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        layout.addItem(right_margin_spacer)
        
    def create_icon_button(self, icon_path):
        button = QPushButton()
        button.setFixedSize(35, 35)
        
        # Загружаем реальную иконку
        pixmap = QPixmap(icon_path)
        if not pixmap.isNull():
            # Создаем QIcon из QPixmap
            icon = QIcon(pixmap)
            button.setIcon(icon)
            button.setIconSize(pixmap.rect().size())
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    border: none;
                    border-radius: 12px;
                }}
                QPushButton:hover {{
                    background-color: {Colors.BUTTON_COLOR_BLUE};
                }}
            """)
        else:
            # Заглушка если файл не найден
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {Colors.TEXT_SECONDARY};
                    border: none;
                    border-radius: 12px;
                }}
                QPushButton:hover {{
                    background-color: {Colors.ACCENT_BLUE};
                }}
            """)
        
        return button
        
    def paintEvent(self, event):
        # Отрисовка фона панели с нижней обводкой
        painter = QPainter(self)
        
        # Заливаем фон
        painter.fillRect(self.rect(), QColor(Colors.DARK_GRAY))
        
        # Рисуем нижнюю обводку 2px
        border_rect = self.rect()
        border_rect.setTop(border_rect.bottom() - 2)
        painter.fillRect(border_rect, QColor(Colors.DEEP_BLUE))