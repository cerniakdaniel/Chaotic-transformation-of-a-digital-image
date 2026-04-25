"""
Metryki analizy eksperymentalnej wymagane przez projekt.
"""

import numpy as np


def pixel_correlation(img: np.ndarray, direction: str = "horizontal") -> float:
    """
    Korelacja sąsiednich pikseli.
    direction: 'horizontal' | 'vertical'
    Bliska 1.0 → duża struktura, bliska 0.0 → brak struktury.
    """
    ch = img[:, :, 0].astype(float) if img.ndim == 3 else img.astype(float)
    if direction == "horizontal":
        a, b = ch[:, :-1].ravel(), ch[:, 1:].ravel()
    else:
        a, b = ch[:-1, :].ravel(), ch[1:, :].ravel()
    return float(np.corrcoef(a, b)[0, 1])


def mean_absolute_diff(img1: np.ndarray, img2: np.ndarray) -> float:
    """Średnia bezwzględna różnica między dwoma obrazami (MAD)."""
    return float(np.mean(np.abs(img1.astype(float) - img2.astype(float))))


def pixel_difference_map(img1: np.ndarray, img2: np.ndarray) -> np.ndarray:
    """Mapa różnic między dwoma obrazami (do wizualizacji)."""
    diff = np.abs(img1.astype(int) - img2.astype(int)).astype(np.uint8)
    return diff


def entropy(img: np.ndarray) -> float:
    """Entropia Shannona obrazu (kanał R lub skala szarości)."""
    ch = img[:, :, 0] if img.ndim == 3 else img
    hist, _ = np.histogram(ch.ravel(), bins=256, range=(0, 255))
    hist = hist / hist.sum()
    hist = hist[hist > 0]
    return float(-np.sum(hist * np.log2(hist)))


def report(label: str, original: np.ndarray, scrambled: np.ndarray,
           unscrambled: np.ndarray, wrong_unscrambled: np.ndarray) -> dict:
    """Pełny raport metryk dla jednego etapu."""
    return {
        "label": label,
        "corr_original_H":    pixel_correlation(original, "horizontal"),
        "corr_scrambled_H":   pixel_correlation(scrambled, "horizontal"),
        "corr_original_V":    pixel_correlation(original, "vertical"),
        "corr_scrambled_V":   pixel_correlation(scrambled, "vertical"),
        "entropy_original":   entropy(original),
        "entropy_scrambled":  entropy(scrambled),
        "mad_correct_key":    mean_absolute_diff(original, unscrambled),
        "mad_wrong_key":      mean_absolute_diff(original, wrong_unscrambled),
        "perfect_recovery":   mean_absolute_diff(original, unscrambled) == 0.0,
    }