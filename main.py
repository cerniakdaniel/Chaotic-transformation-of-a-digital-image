import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtCore import Qt


C = {
    "bg":          "#0B0F1A",
    "bg_panel":    "#111827",
    "bg_card":     "#1A2234",
    "bg_card2":    "#1E2A40",
    "border":      "#2A3A55",
    "border_hi":   "#3D5280",
    "text":        "#E8EDF5",
    "text_muted":  "#6B7FA3",
    "text_dim":    "#3D5280",
    "blue":        "#4A90D9",
    "blue_dark":   "#2D6BAD",
    "green":       "#3DAA6E",
    "red":         "#D94A4A",
    "orange":      "#D98C4A",
    "header_bg":   "#0D1220",
}

STYLESHEET = f"""
QMainWindow, QWidget {{
    background-color: {C['bg']};
    color: {C['text']};
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    font-size: 12px;
}}
QScrollArea {{
    border: none;
    background: transparent;
}}
QScrollBar:vertical {{
    background: {C['bg_panel']};
    width: 8px;
    border-radius: 4px;
}}
QScrollBar::handle:vertical {{
    background: {C['border_hi']};
    border-radius: 4px;
    min-height: 30px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Projekt M-II — Chaotyczne przekształcanie obrazu")
        self.setMinimumSize(1100, 820)
        self.setStyleSheet(STYLESHEET)
        central = QWidget()
        self.setCentralWidget(central)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    w = MainWindow()
    w.show()
    sys.exit(app.exec())