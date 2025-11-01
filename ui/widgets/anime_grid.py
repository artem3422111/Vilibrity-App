# anime_grid.py
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QFont
from ui.styles.colors import Colors

class AnimeCard(QWidget):
    clicked = pyqtSignal(dict)
    
    def __init__(self, anime_data: dict, parent=None):
        super().__init__(parent)
        self.anime_data = anime_data
        self.setFixedSize(200, 300)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)
        
        poster = QLabel()
        poster.setFixedSize(190, 250)
        poster.setStyleSheet(f"""
            QLabel {{
                background-color: {Colors.DARK_LIGHT_GRAY};
                border-radius: 10px;
            }}
        """)
        poster.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel(self.anime_data.get("title", "Название"))
        title.setStyleSheet(f"""
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                font-family: Inter;
                font-size: 14px;
                font-weight: bold;
            }}
        """)
        title.setWordWrap(True)
        title.setMaximumHeight(40)
        
        layout.addWidget(poster)
        layout.addWidget(title)
        
    def mousePressEvent(self, event):
        self.clicked.emit(self.anime_data)

class AnimeGridWidget(QWidget):
    load_more = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_page = 1
        self.current_category = "Все"
        self.has_more = True
        self.setup_ui()
        
    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(50, 0, 0, 0)
        
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(20)
        
        self.layout.addLayout(self.grid_layout)
        
        self.load_more_button = QPushButton("Загрузить еще")
        self.load_more_button.setFixedSize(200, 40)
        self.load_more_button.setStyleSheet(f"""
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
        self.load_more_button.clicked.connect(self.load_more.emit)
        self.layout.addWidget(self.load_more_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
    def clear_grid(self):
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
                
    def add_anime_cards(self, anime_list: list):
        row, col = 0, 0
        max_cols = 6
        
        for anime_data in anime_list:
            card = AnimeCard(anime_data)
            self.grid_layout.addWidget(card, row, col)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1