import unicodedata


ALFABETO = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def normalizar_texto(texto):
    """Normaliza letras convertiveis para A-Z e preserva os demais caracteres."""
    texto_composto = unicodedata.normalize("NFC", texto)
    resultado = []

    for caractere in texto_composto:
        if not caractere.isalpha():
            resultado.append(caractere)
            continue

        caractere_normalizado = ''.join(
            parte
            for parte in unicodedata.normalize("NFD", caractere.upper())
            if not unicodedata.combining(parte)
        )

        if caractere_normalizado and all(
            parte in ALFABETO for parte in caractere_normalizado
        ):
            resultado.extend(caractere_normalizado)
        else:
            resultado.append(caractere)

    return ''.join(resultado)


FREQ_PT = {
    'A': 0.1463,
    'B': 0.0104,
    'C': 0.0388,
    'D': 0.0499,
    'E': 0.1257,
    'F': 0.0102,
    'G': 0.0130,
    'H': 0.0128,
    'I': 0.0618,
    'J': 0.0040,
    'K': 0.0002,
    'L': 0.0278,
    'M': 0.0474,
    'N': 0.0505,
    'O': 0.1073,
    'P': 0.0252,
    'Q': 0.0120,
    'R': 0.0653,
    'S': 0.0781,
    'T': 0.0434,
    'U': 0.0463,
    'V': 0.0167,
    'W': 0.0001,
    'X': 0.0021,
    'Y': 0.0001,
    'Z': 0.0047,
}

FREQ_EN = {
    'A': 0.0817,
    'B': 0.0149,
    'C': 0.0278,
    'D': 0.0425,
    'E': 0.1270,
    'F': 0.0223,
    'G': 0.0202,
    'H': 0.0609,
    'I': 0.0697,
    'J': 0.0015,
    'K': 0.0077,
    'L': 0.0403,
    'M': 0.0241,
    'N': 0.0675,
    'O': 0.0751,
    'P': 0.0193,
    'Q': 0.0010,
    'R': 0.0599,
    'S': 0.0633,
    'T': 0.0906,
    'U': 0.0276,
    'V': 0.0098,
    'W': 0.0236,
    'X': 0.0015,
    'Y': 0.0197,
    'Z': 0.0007,
}


def normalizar_chave(chave):
    chave_normalizada = normalizar_texto(chave)

    if not chave_normalizada:
        raise ValueError("a chave não pode ser vazia")

    if any(caractere not in ALFABETO for caractere in chave_normalizada):
        raise ValueError("a chave deve conter apenas letras de A a Z")

    return chave_normalizada


def transformar_vigenere(texto, chave, direcao):
    chave_normalizada = normalizar_chave(chave)
    resultado = []
    indice_chave = 0

    for caractere in texto:
        if caractere not in ALFABETO:
            resultado.append(caractere)
            continue

        deslocamento = ALFABETO.index(
            chave_normalizada[indice_chave % len(chave_normalizada)]
        )
        indice_texto = ALFABETO.index(caractere)
        resultado.append(
            ALFABETO[
                (indice_texto + direcao * deslocamento) % len(ALFABETO)
            ]
        )
        indice_chave += 1

    return ''.join(resultado)


def encriptar_vigenere(chave, texto):
    return transformar_vigenere(normalizar_texto(texto), chave, 1)
