import sys
import os
import numpy as np
from PIL import Image
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QSpinBox, QFileDialog, QTabWidget,
    QTextEdit, QFrame, QSizePolicy, QStatusBar, QScrollArea
)
from PyQt6.QtGui import QPixmap, QImage, QDragEnterEvent, QDropEvent
from PyQt6.QtCore import Qt, pyqtSignal

import stage1
import stage2
import stage3
import metrics


C = {
    "bg": "#0B0F1A",
    "bg_panel": "#111827",
    "bg_card": "#1A2234",
    "bg_card2": "#1E2A40",
    "border": "#2A3A55",
    "border_hi": "#3D5280",
    "text": "#E8EDF5",
    "text_muted": "#6B7FA3",
    "text_dim": "#3D5280",
    "blue": "#4A90D9",
    "blue_dark": "#2D6BAD",
    "green": "#3DAA6E",
    "red": "#D94A4A",
    "orange": "#D98C4A",
    "header_bg": "#0D1220",
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


def numpy_to_qpixmap(arr: np.ndarray) -> QPixmap:
    arr = np.ascontiguousarray(arr)
    h, w, c = arr.shape
    qimg = QImage(arr.data, w, h, w * c, QImage.Format.Format_RGB888)
    return QPixmap.fromImage(qimg)


def load_image(path: str) -> np.ndarray:
    return np.array(Image.open(path).convert("RGB"), dtype=np.uint8)


def save_image(arr: np.ndarray, path: str):
    Image.fromarray(arr).save(path)


class ImagePanel(QFrame):
    def __init__(self, title: str, accent: str = None, fixed_height: int = 260, parent=None):
        super().__init__(parent)

        self._accent = accent or C["blue"]
        self._info_text = ""
        self._arr = None

        self.setStyleSheet(f"""
            QFrame {{
                background: {C['bg_card']};
                border: 1px solid {C['border']};
                border-radius: 12px;
            }}
        """)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 12)
        root.setSpacing(0)

        top_bar = QFrame()
        top_bar.setFixedHeight(4)
        top_bar.setStyleSheet(
            f"background: {self._accent}; border-radius: 12px 12px 0 0; border: none;"
        )
        root.addWidget(top_bar)

        inner = QVBoxLayout()
        inner.setContentsMargins(12, 10, 12, 0)
        inner.setSpacing(8)

        self.title_lbl = QLabel(title)
        self.title_lbl.setStyleSheet(
            f"color: {C['text_muted']}; font-size: 10px; "
            f"font-weight: bold; letter-spacing: 1.5px;"
        )
        inner.addWidget(self.title_lbl)

        self.img_lbl = QLabel()
        self.img_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.img_lbl.setFixedHeight(fixed_height)
        self.img_lbl.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )
        self.img_lbl.setStyleSheet(
            f"border: 1px solid {C['border']}; border-radius: 8px; "
            f"background: {C['bg_panel']}; color: {C['text_dim']}; font-size: 12px;"
        )
        self.img_lbl.setText("Brak obrazu")
        inner.addWidget(self.img_lbl)

        self.info_lbl = QLabel("")
        self.info_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_lbl.setStyleSheet(
            f"color: {C['text_muted']}; font-size: 10px; padding: 0px;"
        )
        inner.addWidget(self.info_lbl)

        root.addLayout(inner)

    def set_image(self, arr, info: str = ""):
        self._arr = arr
        self._info_text = info

        if arr is None:
            self.img_lbl.setText("Brak obrazu")
            self.img_lbl.setPixmap(QPixmap())
            self.info_lbl.setText("")
            return

        pix = numpy_to_qpixmap(arr)
        target_w = self.img_lbl.width() - 8
        target_h = self.img_lbl.height() - 8

        if target_w > 10 and target_h > 10:
            scaled = pix.scaled(
                target_w,
                target_h,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.img_lbl.setPixmap(scaled)

        self.info_lbl.setText(info)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self._arr is not None:
            self.set_image(self._arr, self._info_text)

    def get_array(self):
        return self._arr


class DropZone(QLabel):
    file_dropped = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedHeight(52)
        self.setText("📂   Przeciągnij obraz tutaj  lub  kliknij aby wybrać")
        self.setToolTip("PNG, JPG, BMP, TIFF")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._normal()

    def _normal(self):
        self.setStyleSheet(
            f"border: 2px dashed {C['border_hi']}; border-radius: 8px; "
            f"background: {C['bg_card']}; color: {C['text_muted']}; "
            f"font-size: 12px; padding: 6px;"
        )

    def _hover(self):
        self.setStyleSheet(
            f"border: 2px dashed {C['blue']}; border-radius: 8px; "
            f"background: {C['bg_card2']}; color: {C['blue']}; "
            f"font-size: 12px; padding: 6px;"
        )

    def mousePressEvent(self, e):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Wybierz obraz",
            "",
            "Obrazy (*.png *.jpg *.jpeg *.bmp *.tiff)"
        )

        if path:
            self.file_dropped.emit(path)

    def dragEnterEvent(self, e: QDragEnterEvent):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()
            self._hover()

    def dragLeaveEvent(self, e):
        self._normal()

    def dropEvent(self, e: QDropEvent):
        self._normal()

        urls = e.mimeData().urls()
        if urls:
            p = urls[0].toLocalFile()
            if p.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff")):
                self.file_dropped.emit(p)


def make_divider() -> QFrame:
    f = QFrame()
    f.setFrameShape(QFrame.Shape.HLine)
    f.setFixedHeight(1)
    f.setStyleSheet(f"background: {C['border']}; border: none;")
    return f


STAGE_DESC = [
    "Permutacja wierszy i kolumn sterowana kluczem. Prosta i odwracalna — ale lokalna struktura obrazu pozostaje widoczna.",
    "Permutacja Fisher-Yates sterowana seedem. Każdy piksel ląduje w losowym miejscu. Histogram pozostaje niezmieniony.",
    "Permutacja + substytucja addytywna:  f(p,k) = (p + S[i]) mod 256.  Zmienia pozycje i wartości pikseli.",
]

STAGE_ACCENTS = [C["orange"], C["blue"], C["red"]]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Projekt M-II — Chaotyczne przekształcanie obrazu")
        self.setMinimumSize(1100, 820)
        self.setStyleSheet(STYLESHEET)

        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        header = QFrame()
        header.setFixedHeight(100)
        header.setStyleSheet(
            f"background: {C['header_bg']}; "
            f"border-bottom: 1px solid {C['border']};"
        )

        hl = QHBoxLayout(header)
        hl.setContentsMargins(24, 0, 24, 0)
        hl.setSpacing(16)

        logo_pix = QPixmap("uwb.png")
        logo = QLabel()

        if not logo_pix.isNull():
            logo.setPixmap(
                logo_pix.scaled(
                    144,
                    144,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            )
        else:
            logo.setText("LOGO")
            logo.setFixedSize(44, 44)
            logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
            logo.setStyleSheet(
                f"border: 2px dashed {C['border_hi']}; border-radius: 8px; "
                f"background: {C['bg_card']}; color: {C['text_dim']}; "
                f"font-size: 9px; font-weight: bold;"
            )

        hl.addWidget(logo)

        t_col = QVBoxLayout()
        t_col.setSpacing(3)

        t1 = QLabel("PROJEKT M-II")
        t1.setStyleSheet(
            f"color: {C['text']}; font-size: 20px; "
            f"font-weight: bold; letter-spacing: 5px;"
        )

        t2 = QLabel("Chaotyczne przekształcanie obrazu cyfrowego")
        t2.setStyleSheet(f"color: {C['text_muted']}; font-size: 15px;")

        t_col.addWidget(t1)
        t_col.addWidget(t2)

        hl.addLayout(t_col)
        hl.addStretch()

        pill = QLabel("    Daniel Czerniak\n  Informatyka II rok  ")
        pill.setStyleSheet(
            f"color: {C['blue']}; font-size: 10px; font-weight: bold; "
            f"letter-spacing: 1px; border: 1px solid {C['border_hi']}; "
            f"border-radius: 10px; padding: 3px 8px; background: {C['bg_card']};"
        )
        hl.addWidget(pill)

        root.addWidget(header)

        tabs = QTabWidget()
        self.tabs = tabs

        for i in range(1, 4):
            tab = StageTab(i)
            tab.status_message.connect(self._status)
            tabs.addTab(tab, f"ETAP {i}")

        root.addWidget(tabs)

        sb = QStatusBar()
        sb.showMessage("Gotowy. Wczytaj obraz przeciągając go lub klikając strefę wczytywania.")
        self.setStatusBar(sb)
        self._sb = sb

    def _status(self, msg: str):
        self._sb.showMessage(msg)


class StageTab(QWidget):
    status_message = pyqtSignal(str)

    def __init__(self, stage_num: int, parent=None):
        super().__init__(parent)

        self.stage_num = stage_num
        self.original_arr = None
        self.scrambled_arr = None
        self.unscrambled_arr = None
        self.wrong_arr = None

        self._build_ui()

    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        outer.addWidget(scroll)

        container = QWidget()
        scroll.setWidget(container)

        root = QVBoxLayout(container)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(16)

        accent = STAGE_ACCENTS[self.stage_num - 1]

        desc_row = QHBoxLayout()

        indicator = QFrame()
        indicator.setFixedWidth(4)
        indicator.setStyleSheet(
            f"background: {accent}; border-radius: 2px; border: none;"
        )

        desc_row.addWidget(indicator)

        desc_lbl = QLabel(STAGE_DESC[self.stage_num - 1])
        desc_lbl.setWordWrap(True)
        desc_lbl.setStyleSheet(
            f"color: {C['text_muted']}; font-size: 11px; "
            f"padding: 4px 12px; background: transparent;"
        )

        desc_row.addWidget(desc_lbl)

        root.addLayout(desc_row)
        root.addWidget(make_divider())

        ctrl = QHBoxLayout()
        ctrl.setSpacing(14)

        dz_col = QVBoxLayout()

        dz_lbl = QLabel("WCZYTAJ OBRAZ")
        dz_lbl.setStyleSheet(
            f"color: {C['text_dim']}; font-size: 10px; "
            f"font-weight: bold; letter-spacing: 1px;"
        )

        dz_col.addWidget(dz_lbl)

        self.drop_zone = DropZone()
        self.drop_zone.file_dropped.connect(self._on_file)

        dz_col.addWidget(self.drop_zone)

        ctrl.addLayout(dz_col, stretch=3)

        key_col = QVBoxLayout()
        key_col.setSpacing(6)

        kl = QLabel("KLUCZ POPRAWNY")
        kl.setStyleSheet(
            f"color: {C['text_dim']}; font-size: 10px; "
            f"font-weight: bold; letter-spacing: 1px;"
        )

        key_col.addWidget(kl)

        self.key_input = QSpinBox()
        self.key_input.setRange(0, 2**30)
        self.key_input.setValue(42)

        key_col.addWidget(self.key_input)

        ctrl.addLayout(key_col, stretch=1)

        wkey_col = QVBoxLayout()
        wkey_col.setSpacing(6)

        wkl = QLabel("KLUCZ BŁĘDNY")
        wkl.setStyleSheet(
            f"color: {C['red']}; font-size: 10px; "
            f"font-weight: bold; letter-spacing: 1px;"
        )

        wkey_col.addWidget(wkl)

        self.wrong_key = QSpinBox()
        self.wrong_key.setRange(0, 2**30)
        self.wrong_key.setValue(43)

        wkey_col.addWidget(self.wrong_key)

        ctrl.addLayout(wkey_col, stretch=1)

        root.addLayout(ctrl)
        root.addWidget(make_divider())

        self.panel_orig = ImagePanel("ORYGINAŁ", C["blue"], fixed_height=320)
        root.addWidget(self.panel_orig)

        small_row = QHBoxLayout()
        small_row.setSpacing(12)

        self.panel_scrambled = ImagePanel("PO SCRAMBLE", accent, fixed_height=200)
        self.panel_restored = ImagePanel("UNSCRAMBLE — POPRAWNY KLUCZ", C["green"], fixed_height=200)
        self.panel_wrong_img = ImagePanel("UNSCRAMBLE — BŁĘDNY KLUCZ", C["red"], fixed_height=200)

        for p in (self.panel_scrambled, self.panel_restored, self.panel_wrong_img):
            small_row.addWidget(p)

        root.addLayout(small_row)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        self.btn_scramble = QPushButton("🔀  Scramble")
        self.btn_unscramble = QPushButton("🔓  Unscramble — poprawny klucz")
        self.btn_wrong_un = QPushButton("❌  Unscramble — błędny klucz")
        self.btn_save = QPushButton("💾  Zapisz wyniki")

        self.btn_unscramble.setObjectName("btn_green")
        self.btn_wrong_un.setObjectName("btn_red")
        self.btn_save.setObjectName("btn_neutral")

        self.btn_scramble.clicked.connect(self.do_scramble)
        self.btn_unscramble.clicked.connect(self.do_unscramble)
        self.btn_wrong_un.clicked.connect(self.do_wrong_unscramble)
        self.btn_save.clicked.connect(self.save_results)

        for b in (
            self.btn_scramble,
            self.btn_unscramble,
            self.btn_wrong_un,
            self.btn_save
        ):
            b.setFixedHeight(40)
            btn_row.addWidget(b)

        root.addLayout(btn_row)
        root.addWidget(make_divider())

        metrics_lbl = QLabel("METRYKI")
        metrics_lbl.setStyleSheet(
            f"color: {C['text_dim']}; font-size: 10px; "
            f"font-weight: bold; letter-spacing: 1px;"
        )
        root.addWidget(metrics_lbl)

        self.metrics_box = QTextEdit()
        self.metrics_box.setReadOnly(True)
        self.metrics_box.setFixedHeight(160)
        self.metrics_box.setPlaceholderText(
            "Metryki pojawią się tutaj po wykonaniu operacji…"
        )

        root.addWidget(self.metrics_box)
        root.addStretch()

    def _on_file(self, path: str):
        self.original_arr = load_image(path)
        self.scrambled_arr = None
        self.unscrambled_arr = None
        self.wrong_arr = None

        h, w = self.original_arr.shape[:2]
        name = os.path.basename(path)

        self.panel_orig.set_image(
            self.original_arr,
            f"{name}  ·  {w} × {h} px"
        )
        self.panel_scrambled.set_image(None)
        self.panel_restored.set_image(None)
        self.panel_wrong_img.set_image(None)

        self.metrics_box.clear()
        self.status_message.emit(f"Wczytano: {name}  [{w}×{h}]")

    def _sc(self, arr, key):
        return [
            stage1.scramble,
            stage2.scramble,
            stage3.scramble
        ][self.stage_num - 1](arr, key)

    def _un(self, arr, key):
        return [
            stage1.unscramble,
            stage2.unscramble,
            stage3.unscramble
        ][self.stage_num - 1](arr, key)

    def do_scramble(self):
        if self.original_arr is None:
            self.status_message.emit("⚠  Najpierw wczytaj obraz!")
            return

        key = self.key_input.value()
        self.scrambled_arr = self._sc(self.original_arr, key)

        corr = metrics.pixel_correlation(self.scrambled_arr)
        self.panel_scrambled.set_image(
            self.scrambled_arr,
            f"Korelacja H: {corr:.5f}"
        )

        self.status_message.emit(
            f"Etap {self.stage_num} · Scramble wykonany  (klucz = {key})"
        )

        self._refresh_metrics()

    def do_unscramble(self):
        if self.scrambled_arr is None:
            self.status_message.emit("⚠  Najpierw wykonaj Scramble!")
            return

        key = self.key_input.value()
        self.unscrambled_arr = self._un(self.scrambled_arr, key)

        mad = metrics.mean_absolute_diff(self.original_arr, self.unscrambled_arr)
        ok = mad == 0.0

        info = "✅  IDENTYCZNY Z ORYGINAŁEM" if ok else f"⚠  Różnica MAD = {mad:.3f}"

        self.panel_restored.set_image(self.unscrambled_arr, info)

        self.status_message.emit(
            f"Unscramble (poprawny klucz): {'IDENTYCZNY' if ok else f'MAD={mad:.3f}'}"
        )

        self._refresh_metrics()

    def do_wrong_unscramble(self):
        if self.scrambled_arr is None:
            self.status_message.emit("⚠  Najpierw wykonaj Scramble!")
            return

        wk = self.wrong_key.value()
        self.wrong_arr = self._un(self.scrambled_arr, wk)

        mad = metrics.mean_absolute_diff(self.original_arr, self.wrong_arr)

        self.panel_wrong_img.set_image(
            self.wrong_arr,
            f"❌  MAD = {mad:.1f}  (klucz = {wk})"
        )

        self.status_message.emit(
            f"Unscramble (błędny klucz = {wk}): MAD = {mad:.1f}"
        )

        self._refresh_metrics(wrong_arr=self.wrong_arr)

    def _refresh_metrics(self, wrong_arr=None):
        if self.original_arr is None or self.scrambled_arr is None:
            return

        orig = self.original_arr
        scr = self.scrambled_arr
        uns = self.unscrambled_arr

        lines = [
            f"═══  ETAP {self.stage_num} — METRYKI  ═══",
            "",
            "  KORELACJA SĄSIEDNICH PIKSELI (kanał R):",
            f"    Oryginał   [poziomo] :  {metrics.pixel_correlation(orig, 'horizontal'):>9.5f}",
            f"    Scrambled  [poziomo] :  {metrics.pixel_correlation(scr,  'horizontal'):>9.5f}",
            f"    Oryginał   [pionowo] :  {metrics.pixel_correlation(orig, 'vertical'):>9.5f}",
            f"    Scrambled  [pionowo] :  {metrics.pixel_correlation(scr,  'vertical'):>9.5f}",
            "",
            "  ENTROPIA SHANNONA (bity/piksel):",
            f"    Oryginał  :  {metrics.entropy(orig):>7.4f}",
            f"    Scrambled :  {metrics.entropy(scr):>7.4f}",
        ]

        if uns is not None:
            mad = metrics.mean_absolute_diff(orig, uns)

            lines += [
                "",
                "  ODWRACALNOŚĆ:",
                f"    MAD (poprawny klucz) :  {mad:.6f}"
                + ("  ←  idealne odtworzenie ✓" if mad == 0 else "  ←  BŁĄD ✗"),
            ]

        if wrong_arr is not None:
            mad_w = metrics.mean_absolute_diff(orig, wrong_arr)

            lines.append(
                f"    MAD (błędny klucz)   :  {mad_w:.4f}"
                + ("  ←  wysoka wrażliwość ✓" if mad_w > 50 else "  ←  niska wrażliwość !")
            )

        self.metrics_box.setText("\n".join(lines))

    def save_results(self):
        if self.scrambled_arr is None:
            self.status_message.emit("⚠  Brak wyników do zapisania.")
            return

        folder = QFileDialog.getExistingDirectory(self, "Wybierz folder zapisu")

        if not folder:
            return

        save_image(
            self.original_arr,
            os.path.join(folder, f"etap{self.stage_num}_oryginal.png")
        )

        save_image(
            self.scrambled_arr,
            os.path.join(folder, f"etap{self.stage_num}_scrambled.png")
        )

        if self.unscrambled_arr is not None:
            save_image(
                self.unscrambled_arr,
                os.path.join(folder, f"etap{self.stage_num}_unscrambled.png")
            )

        if self.wrong_arr is not None:
            save_image(
                self.wrong_arr,
                os.path.join(folder, f"etap{self.stage_num}_wrong_key.png")
            )

        self.status_message.emit(f"✅  Zapisano wyniki → {folder}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    w = MainWindow()
    w.show()

    sys.exit(app.exec())