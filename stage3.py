import numpy as np
from stage2 import _generate_permutation, _invert_permutation


def _generate_substitution_stream(n_bytes: int, key: int) -> np.ndarray:
    sub_key = key ^ 0xDEADBEEF
    rng = np.random.default_rng(sub_key)
    return rng.integers(0, 256, size=n_bytes, dtype=np.uint8)


def scramble(image: np.ndarray, key: int) -> np.ndarray:
    shape = image.shape
    channels = shape[2] if image.ndim == 3 else 1
    n_pixels = image.size // channels
    perm = _generate_permutation(n_pixels, key)
    img_pixels = image.reshape(n_pixels, channels)
    permuted   = img_pixels[perm].reshape(shape)
    flat_p = permuted.reshape(-1).astype(np.int16)
    stream = _generate_substitution_stream(len(flat_p), key)
    substituted = ((flat_p + stream.astype(np.int16)) % 256).astype(np.uint8)
    return substituted.reshape(shape)


def unscramble(image: np.ndarray, key: int) -> np.ndarray:
    shape = image.shape
    channels = shape[2] if image.ndim == 3 else 1
    n_pixels = image.size // channels
    flat_s = image.reshape(-1).astype(np.int16)
    stream = _generate_substitution_stream(len(flat_s), key)
    desubstituted = ((flat_s - stream.astype(np.int16)) % 256).astype(np.uint8)
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
    ch = img[:, :, 0].astype(float) if img.ndim == 3 else img.astype(float)
    return float(np.corrcoef(ch[:, :-1].ravel(), ch[:, 1:].ravel())[0, 1])