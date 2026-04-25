"""
Etap 3 - Mechanizm wzmacniający: Substytucja deterministyczna (klasa A)
========================================================================
Po permutacji pikseli z Etapu 2 stosujemy substytucję wartości pikseli:

  f(p, k)   = (p + S[i]) mod 256      -- szyfrowanie
  f^-1(p,k) = (p - S[i]) mod 256      -- deszyfrowanie

gdzie S[i] to deterministyczny strumień bajtów generowany z klucza (seed).
Operacja jest XOR-opodobna ale addytywna modulo 256.

Kolejność operacji (scramble):
  1. Permutacja pikseli (Etap 2)
  2. Substytucja addytywna

Kolejność odwrotna (unscramble):
  1. Odwrotna substytucja
  2. Odwrotna permutacja
"""

import numpy as np
from stage2 import (
    _generate_permutation,
    _invert_permutation,
)


def _generate_substitution_stream(n_bytes: int, key: int) -> np.ndarray:
    """
    Generuje strumień substytucji S o długości n_bytes.
    Używamy drugiego ziarna = key XOR 0xDEADBEEF żeby S != permutacja.
    """
    sub_key = key ^ 0xDEADBEEF
    rng = np.random.default_rng(sub_key)
    return rng.integers(0, 256, size=n_bytes, dtype=np.uint8)


def scramble(image: np.ndarray, key: int) -> np.ndarray:
    """
    Krok 1: Permutacja pikseli (jak Etap 2).
    Krok 2: Substytucja addytywna f(p,k) = (p + S[i]) mod 256.
    """
    shape = image.shape
    # --- Permutacja ---
    flat = image.reshape(-1)          # spłaszczamy do bajtów
    n    = len(flat)
    channels = shape[2] if image.ndim == 3 else 1

    # permutujemy piksele (grupy kanałów)
    n_pixels = n // channels
    perm = _generate_permutation(n_pixels, key)

    img_pixels = image.reshape(n_pixels, channels)
    permuted   = img_pixels[perm].reshape(shape)

    # --- Substytucja ---
    flat_p = permuted.reshape(-1).astype(np.int16)
    stream = _generate_substitution_stream(len(flat_p), key)
    substituted = ((flat_p + stream.astype(np.int16)) % 256).astype(np.uint8)

    return substituted.reshape(shape)


def unscramble(image: np.ndarray, key: int) -> np.ndarray:
    """
    Krok 1: Odwrotna substytucja f^-1(p,k) = (p - S[i]) mod 256.
    Krok 2: Odwrotna permutacja.
    """
    shape = image.shape
    channels = shape[2] if image.ndim == 3 else 1
    n_pixels = image.size // channels

    # --- Odwrotna substytucja ---
    flat_s = image.reshape(-1).astype(np.int16)
    stream = _generate_substitution_stream(len(flat_s), key)
    desubstituted = ((flat_s - stream.astype(np.int16)) % 256).astype(np.uint8)

    # --- Odwrotna permutacja ---
    perm     = _generate_permutation(n_pixels, key)
    inv_perm = _invert_permutation(perm)

    pixels_back = desubstituted.reshape(n_pixels, channels)
    restored    = pixels_back[inv_perm].reshape(shape)

    return restored


def test_invertibility(image: np.ndarray, key: int) -> bool:
    s = scramble(image, key)
    u = unscramble(s, key)
    return np.array_equal(image, u)


def pixel_correlation(img: np.ndarray) -> float:
    """Korelacja pozioma sąsiednich pikseli (kanał R)."""
    ch = img[:, :, 0].astype(float) if img.ndim == 3 else img.astype(float)
    return float(np.corrcoef(ch[:, :-1].ravel(), ch[:, 1:].ravel())[0, 1])