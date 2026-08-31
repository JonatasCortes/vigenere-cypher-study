from collections import Counter

from utils import ALFABETO, FREQ_EN, FREQ_PT


def decifrar_deslocamento(texto, deslocamento):
    return ''.join(
        ALFABETO[(ALFABETO.index(caractere) - deslocamento) % len(ALFABETO)]
        for caractere in texto
    )


def chi_quadrado(texto, frequencias=FREQ_PT):
    freqs_plain = Counter(texto)
    n = len(texto)

    if n == 0:
        return float('inf')

    x2 = 0
    for letra, frequencia_esperada in frequencias.items():
        o = freqs_plain.get(letra, 0)
        e = frequencia_esperada * n

        x2 += (o - e)**2 / e

    return x2


def descobrir_caractere_chave(texto, frequencias=FREQ_PT):
    melhor_deslocamento = 0
    melhor_x2 = float('inf')

    for deslocamento in range(len(ALFABETO)):
        candidato = decifrar_deslocamento(texto, deslocamento)
        x2 = chi_quadrado(candidato, frequencias)

        if x2 < melhor_x2:
            melhor_x2 = x2
            melhor_deslocamento = deslocamento

    return ALFABETO[melhor_deslocamento]


def descobrir_chave(texto, tamanho_chave, idioma="pt"):
    if tamanho_chave < 1:
        raise ValueError("o tamanho da chave deve ser positivo")

    frequencias_por_idioma = {
        "pt": FREQ_PT,
        "en": FREQ_EN,
    }

    try:
        frequencias = frequencias_por_idioma[idioma.lower()]
    except KeyError as erro:
        raise ValueError("idioma deve ser 'pt' ou 'en'") from erro

    letras = ''.join(caractere for caractere in texto if caractere in ALFABETO)
    chave = []

    for i in range(tamanho_chave):
        coluna = letras[i::tamanho_chave]

        caractere = descobrir_caractere_chave(
            coluna,
            frequencias,
        )
        chave.append(caractere)

    return ''.join(chave)


def reduzir_chave_repetida(chave):
    for tamanho in range(1, len(chave) + 1):
        if len(chave) % tamanho != 0:
            continue

        periodo = chave[:tamanho]
        repeticoes = len(chave) // tamanho

        if periodo * repeticoes == chave:
            return periodo

    return chave
