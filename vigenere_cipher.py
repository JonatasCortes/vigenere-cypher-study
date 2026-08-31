from unicodedata import normalize, combining
from typing import Callable
from math import ceil
from operator import add, sub


def encrypt(key: str, plaintext: str) -> str:
    """
    Encrypts the given plaintext using the provided
    key and returns the resulting ciphertext.
    """
    return __vigenere_cipher(plaintext, key, add)


def decrypt(key: str, ciphertext: str) -> str:
    """
    Decrypts the given ciphertext using the provided
    key and returns the resulting plaintext.
    """
    return __vigenere_cipher(ciphertext, key, sub)


def __vigenere_cipher(text: str, key: str, operation: Callable[[int, int], int]) -> str:
    """
    Transforms the given text using the provided key and operation.
    Non-alphabetic characters from the text are preserved unchanged.
    """
    full_key: str = __expand_key(key, text)
    return __cipher_text_with_key(text, full_key, operation)


def __expand_key(key: str, text: str) -> str:
    """Repeats the given key until it matches the length of the text."""
    return ceil(len(text) / len(key)) * key


def __cipher_text_with_key(text: str, key: str, operation: Callable[[int, int], int]) -> str:
    """
    Transforms `text` using `key` by applying `operation` to corresponding character
    pairs. The operation receives the alphabetic index of each letter, ranging from
    0 to 25, and must return an integer value. Non-letter characters from `text` are
    preserved unchanged.
    """
    return "".join(__apply_operation_if_alpha(char1, char2, operation)
                   for char1, char2 in zip(text, key))


def __apply_operation_if_alpha(text_char: str, key_char: str, operation: Callable[[int, int], int]) -> str:
    """
    Applies the given operation to text_char and key_char when
    both are alphabetic. If either character is not alphabetic,
    text_char is returned unchanged.
    """
    if text_char.isalpha() and key_char.isalpha():
        return __letter_operation(text_char, key_char, operation)
    return text_char


def __letter_operation(letter1: str, letter2: str, operation: Callable[[int, int], int]) -> str:
    """
    Combines two normalized letters using the given operation. Converts
    characters to 0-25 indices, applies `operation` and uses modulo 26
    to constrain the output within the 0-25 range. This ensures the
    returned value never exceeds the alphabet bounds ('A'-'Z').
    """
    offset = ord("A")
    alphabet_range = 26
    result = operation(ord(__normalize_letter(letter1)) - offset,
                       ord(__normalize_letter(letter2)) - offset)
    return chr((result % alphabet_range) + offset)


def __normalize_letter(raw_letter: str) -> str:
    """Returns the uppercase, accent-free form of the given letter."""
    letter_components = normalize('NFD', raw_letter)
    without_accents = next(l for l in letter_components
                           if not combining(l))
    return without_accents.upper()
