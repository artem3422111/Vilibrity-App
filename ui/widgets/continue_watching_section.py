import json
import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt
from ui.styles.colors import Colors
from .continue_watching_card import ContinueWatchingCard

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
        
        # Контейнер для строк с карточками
        self.cards_container = QWidget()
        self.cards_layout = QVBoxLayout(self.cards_container)
        self.cards_layout.setContentsMargins(0, 0, 0, 0)
        self.cards_layout.setSpacing(30)  # Отступ между строками карточек
        
        layout.addWidget(self.cards_container)
        
        # Растягивающий элемент для прижатия карточек к верху
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
        """Обновляет отображение карточек в строки по 5 штук"""
        # Очищаем старые строки
        for i in reversed(range(self.cards_layout.count())):
            widget = self.cards_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        # Если нет данных, выходим
        if not self.continue_watching_data:
            return
        
        # Разбиваем данные на строки по 5 карточек
        cards_per_row = 5
        for i in range(0, len(self.continue_watching_data), cards_per_row):
            row_data = self.continue_watching_data[i:i + cards_per_row]
            
            # Создаем строку для карточек
            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(43)  # Отступ между карточками 43px
            row_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Прижимаем к левому краю
            
            # Добавляем карточки в строку
            for anime_data in row_data:
                card = ContinueWatchingCard(anime_data)
                row_layout.addWidget(card)
            
            # Если в строке меньше 5 карточек, добавляем растягивающий элемент
            # чтобы оставшиеся карточки не растягивались
            if len(row_data) < cards_per_row:
                row_layout.addStretch()
            
            self.cards_layout.addWidget(row_widget)