from typing import Callable
from math import ceil
from operator import add, sub


def encrypt(key: str, plaintext: str) -> str:
    """
    Encrypts the given plaintext using the provided
    key and returns the resulting ciphertext.
    """
    return __transform_text(plaintext, key, add)


def decrypt(key: str, ciphertext: str) -> str:
    """
    Decrypts the given ciphertext using the provided
    key and returns the resulting plaintext.
    """
    return __transform_text(ciphertext, key, sub)


def __transform_text(text: str, key: str, operation: Callable[[int, int], int]) -> str:
    """
    Transforms the given text using the provided key
    and operation, returning the resulting text.
    """
    full_key: str = __build_full_key(key, text)
    return __text_operation(text, full_key, operation)


def __build_full_key(key: str, text: str) -> str:
    """
    Builds the full key by repeating it until its length
    is greater than or equal to the length of the text.
    """
    return ceil(len(text) / len(key)) * key


def __text_operation(text1: str, text2: str, operation: Callable[[int, int], int]) -> str:
    """
    Applies the given operation to the Unicode code points of each corresponding
    character pair from text1 and text2, and returns the resulting string.
    """
    return "".join([__char_operation(char1, char2, operation)
                    for char1, char2 in zip(text1, text2)])


def __char_operation(char1: str, char2: str, operation: Callable[[int, int], int]):
    """
    Applies the given operation to the Unicode code points
    of char1 and char2 and returns the resulting character.
    """
    return chr(operation(ord(char1), ord(char2)))
