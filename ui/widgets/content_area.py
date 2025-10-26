from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPainter, QPixmap, QLinearGradient, QColor, QPainterPath, QFont
from ui.styles.colors import Colors
from ui.widgets.anime_card import AnimeCard

class CategorySwitchWidget(QWidget):
    category_changed = pyqtSignal(str)  # Сигнал смены категории
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(500, 40)
        self.active_category = "Все"
        self.buttons = {}
        self.setup_ui()
        
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)  # Внутренние отступы
        layout.setSpacing(5)  # Расстояние между кнопками
        
        # Данные кнопок категорий
        categories = ["Все", "В тренде", "Новинки", "Популярное"]
        
        for category in categories:
            button = QPushButton(category)
            button.setFixedSize(120, 30)
            
            # Устанавливаем шрифт
            font = QFont("Inter")
            font.setPointSize(12)
            font.setBold(True)
            button.setFont(font)
            
            # Начальная стилизация
            if category == "Все":
                # Активная кнопка по умолчанию
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
                # Неактивные кнопки
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
            
            # Подключаем обработчик
            button.clicked.connect(lambda checked, cat=category: self.on_category_clicked(cat))
            
            layout.addWidget(button)
            self.buttons[category] = button
        
    def on_category_clicked(self, category):
        # Деактивируем предыдущую активную категорию
        if self.active_category:
            self.set_category_active(self.active_category, False)
        
        # Активируем новую категорию
        self.set_category_active(category, True)
        self.active_category = category
        
        # Отправляем сигнал
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
        # Отрисовка фона плашки
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Рисуем закругленный прямоугольник
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
        layout.setSpacing(20)
        
        # Заголовок "Продолжить просмотр"
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
        
        # Горизонтальный контейнер для карточек
        cards_container = QWidget()
        cards_layout = QHBoxLayout(cards_container)
        cards_layout.setContentsMargins(0, 0, 0, 0)
        cards_layout.setSpacing(20)  # Расстояние между карточками
        
        # Первая карточка: Доктор Стоун
        card1 = AnimeCard(
            title="Доктор Стоун: Финальная битва",
            genre="Научное",
            episodes="65 эп.",
            image_path="assets/images/Rectangle.png"
        )
        cards_layout.addWidget(card1)
        
        # Вторая карточка: Наруто
        card2 = AnimeCard(
            title="Наруто",
            genre="Приключение", 
            episodes="220 эп.",
            image_path="assets/images/Rectangle13.png"
        )
        cards_layout.addWidget(card2)
        
        # Spacer для выравнивания слева
        cards_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        layout.addWidget(cards_container)

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
        content_layout.setContentsMargins(50, 40, 50, 0)  # Отступ слева 50px от левой панели
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        content_layout.setSpacing(40)
        
        # Баннер рекомендуемого аниме
        self.banner = BannerWidget()
        content_layout.addWidget(self.banner)
        
        self.continue_watching_section = ContinueWatchingSection()
        content_layout.addWidget(self.continue_watching_section)
        
        # Плашка переключения категорий (уменьшенный отступ 40px от секции продолжения просмотра)
        categories_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        content_layout.addItem(categories_spacer)
        
        self.category_switch = CategorySwitchWidget()
        content_layout.addWidget(self.category_switch)
        
        # Подключаем сигнал смены категории
        self.category_switch.category_changed.connect(self.on_category_changed)
        
        # Здесь будут другие элементы контента
        # TODO: Добавить секции с карточками аниме
        
    def on_category_changed(self, category):
        print(f"Выбрана категория: {category}")
        # Здесь будет логика фильтрации контента по категории