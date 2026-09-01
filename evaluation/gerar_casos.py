import random

from ataque.utils import ALFABETO, normalizar_texto
from vigenere_cipher import encrypt


MARCADOR_INICIO = "CAPITULO PRIMEIRO"
MARCADOR_FIM = "*** END OF THE PROJECT GUTENBERG EBOOK"


def extrair_corpo_livro(texto):
    inicio = texto.find(MARCADOR_INICIO)
    fim = texto.find(MARCADOR_FIM)

    if inicio == -1:
        inicio = 0

    if fim == -1:
        fim = len(texto)

    return texto[inicio:fim]


def gerar_chave(tamanho, gerador):
    return ''.join(
        gerador.choice(ALFABETO)
        for _ in range(tamanho)
    )


def gerar_casos(
    texto,
    quantidade,
    minimo_texto,
    maximo_texto,
    minimo_chave,
    maximo_chave,
    semente,
):
    corpo = extrair_corpo_livro(texto)
    gerador = random.Random(semente)
    casos = []

    for _ in range(quantidade):
        tamanho_texto = gerador.randint(minimo_texto, maximo_texto)
        tamanho_texto = min(tamanho_texto, len(corpo))
        inicio = gerador.randint(0, len(corpo) - tamanho_texto)
        trecho = corpo[inicio:inicio + tamanho_texto]
        texto_claro = normalizar_texto(trecho)

        tamanho_chave = gerador.randint(minimo_chave, maximo_chave)
        chave = gerar_chave(tamanho_chave, gerador)
        criptograma = encrypt(chave, texto_claro)

        casos.append(
            {
                "inicio": inicio,
                "texto_claro": texto_claro,
                "criptograma": criptograma,
                "chave": chave,
            }
        )

    return casos
