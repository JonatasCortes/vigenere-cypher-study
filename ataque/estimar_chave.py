from collections import Counter

from ataque.utils import ALFABETO


def indice_de_coincidencia(texto):
    n = len(texto)

    if n < 2:
        return 0.0

    frequencias = Counter(texto)

    numerador = 0

    for freq in frequencias.values():
        numerador += freq * (freq - 1)

    denominador = n * (n - 1)

    return numerador / denominador


def estimar_chave(texto, maximo_k):
    letras = ''.join(caractere for caractere in texto if caractere in ALFABETO)
    resultados = []

    for k in range(1, maximo_k + 1):
        colunas = [letras[i::k] for i in range(k)]

        indice_colunas = [
            indice_de_coincidencia(coluna)
            for coluna in colunas
        ]

        indice_medio = sum(indice_colunas) / k

        resultados.append((k, indice_medio))

    return resultados
