"""
Etap 2 - Czysta permutacja pikseli sterowana kluczem (Fisher-Yates + seed).
P: {0..N-1} -> {0..N-1}   gdzie N = H*W
Funkcja odwrotna P^-1 wyznaczana przez inwersję tablicy permutacji.
Wartości pikseli NIE są zmieniane.
"""

import numpy as np


def _generate_permutation(n: int, key: int) -> np.ndarray:
    """Generuje permutację N elementów algorytmem Fisher-Yates z seedem."""
    rng = np.random.default_rng(key)
    perm = rng.permutation(n)
    return perm


def _invert_permutation(perm: np.ndarray) -> np.ndarray:
    """Wyznacza permutację odwrotną: inv[perm[i]] = i"""
    inv = np.empty_like(perm)
    inv[perm] = np.arange(len(perm))
    return inv


def scramble(image: np.ndarray, key: int) -> np.ndarray:
    """
    Spłaszcza obraz do wektora pikseli, stosuje permutację P,
    a następnie składa z powrotem do oryginalnego kształtu.
    """
    shape = image.shape
    flat = image.reshape(-1, shape[2]) if image.ndim == 3 else image.ravel()
    n = flat.shape[0]

    perm = _generate_permutation(n, key)
    scrambled_flat = flat[perm]

    return scrambled_flat.reshape(shape)


def unscramble(image: np.ndarray, key: int) -> np.ndarray:
    """
    Stosuje permutację odwrotną P^-1.
    P^-1(P(i)) = i  dla każdego indeksu i.
    """
    shape = image.shape
    flat = image.reshape(-1, shape[2]) if image.ndim == 3 else image.ravel()
    n = flat.shape[0]

    perm = _generate_permutation(n, key)
    inv_perm = _invert_permutation(perm)
    restored_flat = flat[inv_perm]

    return restored_flat.reshape(shape)


def test_invertibility(image: np.ndarray, key: int) -> bool:
    """Sprawdza czy P^-1(P(img)) == img dla wszystkich pikseli."""
    scrambled   = scramble(image, key)
    unscrambled = unscramble(scrambled, key)
    return np.array_equal(image, unscrambled)


def wrong_key_diff(image: np.ndarray, correct_key: int, wrong_key: int) -> float:
    """
    Zwraca średnią różnicę bezwzględną między oryginalem
    a obrazem odtworzonym błędnym kluczem.
    Wysoka wartość → algorytm jest wrażliwy na klucz.
    """
    scrambled        = scramble(image, correct_key)
    wrong_unscramble = unscramble(scrambled, wrong_key)
    return float(np.mean(np.abs(image.astype(float) - wrong_unscramble.astype(float))))


def avalanche_effect(key: int, bit_flip_position: int = 0) -> tuple:
    """
    Porównuje permutacje dla klucza i klucza z 1 zmienionym bitem.
    Zwraca (key, flipped_key, procent_roznych_pozycji).
    """
    flipped_key = key ^ (1 << bit_flip_position)
    n = 1000  # rozmiar testowej permutacji
    p1 = _generate_permutation(n, key)
    p2 = _generate_permutation(n, flipped_key)
    diff_ratio = float(np.mean(p1 != p2))
    return key, flipped_key, diff_ratio