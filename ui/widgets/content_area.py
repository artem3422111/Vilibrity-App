from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from ui.styles.colors import Colors
from api.api_client import api_client
from .continue_watching_section import ContinueWatchingSection
from .banner_widget import BannerWidget

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
        
        # Секция "Продолжить просмотр"
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