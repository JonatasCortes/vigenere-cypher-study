from math import ceil


def decrypt(key: str, ciphertext: str) -> str:
    full_key: str = ceil(len(ciphertext) / len(key)) * key
    plaintext = ""
    for key_character, text_character in zip(full_key, ciphertext):
        plaintext += chr(ord(text_character) - ord(key_character))
    return plaintext
