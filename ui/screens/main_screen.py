from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt
from ui.widgets.title_bar import CustomTitleBar
from ui.widgets.top_panel import TopPanel
from ui.widgets.left_panel import LeftPanel
from ui.widgets.content_area import ContentArea
from ui.styles.colors import Colors
import config

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.setup_ui()
        
    def setup_window(self):
        # Полноэкранный режим 1920x1080
        self.setFixedSize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        # Убираем стандартную рамку
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        
    def setup_ui(self):
        # Главный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Кастомный title bar
        self.title_bar = CustomTitleBar(self)
        main_layout.addWidget(self.title_bar)
        
        # Верхняя панель
        self.top_panel = TopPanel()
        main_layout.addWidget(self.top_panel)
        
        # Контентная область (левая панель + основной контент)
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Левая панель навигации
        self.left_panel = LeftPanel()
        content_layout.addWidget(self.left_panel)
        
        # Основная область контента
        self.content_area = ContentArea()
        content_layout.addWidget(self.content_area)
        
        main_layout.addWidget(content_widget)
        
        # Подключаем сигналы левой панели
        self.left_panel.button_clicked.connect(self.on_nav_button_clicked)
    
    def on_nav_button_clicked(self, button_id):
        print(f"Нажата кнопка: {button_id}")
        # Здесь будет логика смены контента в зависимости от выбранной кнопки