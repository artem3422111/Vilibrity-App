import sys
from PyQt6.QtWidgets import QApplication
from ui.screens.main_screen import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())