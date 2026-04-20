"""
Etap 1 - Naiwny scrambling (etap porażki)
Prosta permutacja wierszy i kolumn sterowana seedem.
Słabość: lokalne struktury obrazu pozostają widoczne.
"""

import numpy as np


def scramble(image: np.ndarray, key: int) -> np.ndarray:
    """
    Permutacja wierszy i kolumn obrazu sterowana kluczem (seedem).
    Nie zmienia wartości pikseli - tylko ich kolejność w skali makro.
    """
    rng = np.random.default_rng(key)
    img = image.copy()

    h, w = img.shape[:2]

    # Permutacja wierszy
    row_perm = rng.permutation(h)
    img = img[row_perm, :]

    # Permutacja kolumn
    col_perm = rng.permutation(w)
    img = img[:, col_perm]

    return img


def unscramble(image: np.ndarray, key: int) -> np.ndarray:
    """
    Odwrotna permutacja wierszy i kolumn.
    Algorytm odwrotny: wyznaczamy inwersję permutacji i stosujemy ją.
    """
    rng = np.random.default_rng(key)
    img = image.copy()

    h, w = img.shape[:2]

    # Odtwarzamy te same permutacje co przy scramblingu
    row_perm = rng.permutation(h)
    col_perm = rng.permutation(w)

    # Inwersja permutacji wierszy
    row_inv = np.empty_like(row_perm)
    row_inv[row_perm] = np.arange(h)

    # Inwersja permutacji kolumn
    col_inv = np.empty_like(col_perm)
    col_inv[col_perm] = np.arange(w)

    # Zastosowanie inwersji
    img = img[row_inv, :]
    img = img[:, col_inv]

    return img


def analyze_weakness(original: np.ndarray, scrambled: np.ndarray) -> dict:
    """
    Analiza słabości metody:
    - korelacja sąsiednich pikseli przed i po scramblingu
    - widoczność struktury (odchylenie standardowe)
    """
    def pixel_correlation(img):
        """Korelacja pozioma sąsiednich pikseli (kanał 0 lub cały obraz)."""
        flat = img[:, :, 0].astype(float) if img.ndim == 3 else img.astype(float)
        left  = flat[:, :-1].ravel()
        right = flat[:, 1:].ravel()
        return float(np.corrcoef(left, right)[0, 1])

    return {
        "corr_original":  pixel_correlation(original),
        "corr_scrambled": pixel_correlation(scrambled),
        "std_original":   float(np.std(original)),
        "std_scrambled":  float(np.std(scrambled)),
        "weakness": (
            "Permutacja wierszy/kolumn zachowuje strukturę lokalną. "
            "Gradienty i jednolite obszary pozostają widoczne, "
            "bo sąsiadujące piksele wewnątrz wiersza/kolumny nie są rozdzielane."
        )
    }
