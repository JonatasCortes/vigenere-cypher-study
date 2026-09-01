from unicodedata import normalize, combining
from typing import Callable
from operator import add, sub


ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


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
    normalized_text: str = __normalize_text(text)
    normalized_key: str = __normalize_key(key)
    return __cipher_text_with_key(normalized_text, normalized_key, operation)


def __normalize_key(key: str) -> str:
    """Returns a non-empty key containing only normalized A-Z letters."""
    normalized_key: str = __normalize_text(key)

    if not normalized_key:
        raise ValueError("a chave não pode ser vazia")

    if any(char not in ALPHABET for char in normalized_key):
        raise ValueError("a chave deve conter apenas letras de A a Z")

    return normalized_key


def __cipher_text_with_key(text: str, key: str, operation: Callable[[int, int], int]) -> str:
    """
    Transforms `text` using `key` by applying `operation` to corresponding character
    pairs. The operation receives the alphabetic index of each letter, ranging from
    0 to 25, and must return an integer value. Non-letter characters from `text` are
    preserved unchanged.
    """
    result: list[str] = []
    key_index: int = 0

    for text_char in text:
        if text_char not in ALPHABET:
            result.append(text_char)
            continue

        key_char: str = key[key_index % len(key)]
        result.append(__letter_operation(text_char, key_char, operation))
        key_index += 1

    return "".join(result)


def __letter_operation(letter1: str, letter2: str, operation: Callable[[int, int], int]) -> str:
    """
    Combines two normalized letters using the given operation. Converts
    characters to 0-25 indices, applies `operation` and uses modulo 26
    to constrain the output within the 0-25 range. This ensures the
    returned value never exceeds the alphabet bounds ('A'-'Z').
    """
    offset = ord("A")
    alphabet_range = 26
    result = operation(ord(letter1) - offset,
                       ord(letter2) - offset)
    return chr((result % alphabet_range) + offset)


def __normalize_text(text: str) -> str:
    """Normalizes convertible letters to A-Z and preserves other characters."""
    composed_text: str = normalize("NFC", text)
    result: list[str] = []

    for char in composed_text:
        if not char.isalpha():
            result.append(char)
            continue

        normalized_char: str = "".join(
            component
            for component in normalize("NFD", char.upper())
            if not combining(component)
        )

        if normalized_char and all(
            component in ALPHABET for component in normalized_char
        ):
            result.extend(normalized_char)
        else:
            result.append(char)

    return "".join(result)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Cifra de Vigenère")
    parser.add_argument("modo", choices=["enc", "dec"], help="Modo: 'enc' para encriptar ou 'dec' para decriptar")
    parser.add_argument("chave", help="Chave de cifragem")
    parser.add_argument("texto", help="Texto a ser processado")
    args = parser.parse_args()

    if args.modo == "enc":
        print(encrypt(args.chave, args.texto))
    else:
        print(decrypt(args.chave, args.texto))
