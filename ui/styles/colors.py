from dataclasses import dataclass

@dataclass
class Colors:
    DARK_GRAY: str = "#111111"
    DEEP_BLUE: str = "#2B2B2B"
    DARK_LIGHT_GRAY: str = "#191919"
    LIGHT_GRAY: str = "#474747"
    ACCENT_BLUE: str = "#20b3e0"
    
    # Дополнительные цвета
    TEXT_PRIMARY: str = "#e2e8f0"
    TEXT_SECONDARY: str = "#94a3b8"
    TEXT_GRAY: str = "#807F7F"
    BACKGROUND: str = "#0a0a12"
    SURFACE: str = "#151525"
    
    # Статусные цвета
    SUCCESS: str = "#10b981"
    WARNING: str = "#f59e0b"
    ERROR: str = "#ef4444"
    
    # Кнопки
    BUTTON_COLOR_BLUE: str = "#20b3e0"
    BUTTON_HOVER_BLUE: str = "#1A8AAC"
    BUTTON_COLOR_GRAY: str = "#2A2A2A"
    BUTTON_HOVER_GRAY: str = "#3F3F3F"  # Цвет для наведения серой кнопки
    CLOSE_BUTTON_HOVER: str = "#f23c3c"
    CLOSE_BUTTON_PRESSED: str = "#dc2626"