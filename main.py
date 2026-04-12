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
QTabWidget::pane {{
    border: none;
    background: {C['bg']};
}}
QTabBar::tab {{
    background: {C['bg_panel']};
    color: {C['text_muted']};
    padding: 10px 28px;
    border: none;
    border-bottom: 2px solid transparent;
    font-size: 12px;
    margin-right: 2px;
    margin-top: 10px;
}}
QTabBar::tab:selected {{
    color: {C['blue']};
    border-bottom: 2px solid {C['blue']};
    background: {C['bg_panel']};
    font-weight: bold;
}}
QTabBar::tab:hover:!selected {{
    color: {C['text']};
    background: {C['bg_card']};
}}
QPushButton {{
    background: {C['blue']};
    color: #FFFFFF;
    border: none;
    border-radius: 7px;
    padding: 9px 20px;
    font-size: 12px;
    font-weight: 600;
}}
QPushButton:hover {{
    background: {C['blue_dark']};
}}
QPushButton:pressed {{
    background: #1D4F8A;
}}
QPushButton#btn_green {{
    background: {C['green']};
}}
QPushButton#btn_green:hover {{
    background: #2D8055;
}}
QPushButton#btn_red {{
    background: {C['red']};
}}
QPushButton#btn_red:hover {{
    background: #A83535;
}}
QPushButton#btn_neutral {{
    background: {C['bg_card2']};
    color: {C['text_muted']};
    border: 1px solid {C['border']};
}}
QPushButton#btn_neutral:hover {{
    background: {C['border']};
    color: {C['text']};
}}
QSpinBox {{
    background: {C['bg_card']};
    color: {C['text']};
    border: 1px solid {C['border']};
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 12px;
}}
QSpinBox:focus {{
    border: 1px solid {C['blue']};
}}
QSpinBox::up-button, QSpinBox::down-button {{
    width: 18px;
    background: {C['bg_card2']};
    border: none;
}}
QLabel {{
    background: transparent;
    color: {C['text']};
}}
QTextEdit {{
    background: {C['bg_card']};
    color: {C['text']};
    border: 1px solid {C['border']};
    border-radius: 8px;
    font-family: 'Cascadia Code', 'Courier New', monospace;
    font-size: 11px;
    padding: 10px;
    selection-background-color: {C['border_hi']};
}}
QStatusBar {{
    background: {C['header_bg']};
    color: {C['text_muted']};
    border-top: 1px solid {C['border']};
    font-size: 11px;
    padding: 4px 14px;
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