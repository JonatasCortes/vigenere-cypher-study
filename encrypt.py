from math import ceil


def encrypt(key: str, plaintext: str) -> str:
    full_key: str = ceil(len(plaintext) / len(key)) * key
    ciphertext = ""
    for key_character, text_character in zip(full_key, plaintext):
        ciphertext += chr(ord(text_character) + ord(key_character))
    return ciphertext
