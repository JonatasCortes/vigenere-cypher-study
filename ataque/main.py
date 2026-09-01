import argparse

from ataque.estimar_chave import estimar_chave
from ataque.quebrar_cipher import descobrir_chave, reduzir_chave_repetida
from ataque.utils import normalizar_texto
from vigenere_cipher import decrypt


TAMANHO_PREVIA = 200
LIMITE_CANDIDATOS = 5


def mostrar_candidatos(candidatos):
    print("Melhores candidatos:")

    for indice, (tamanho, ic, chave) in enumerate(candidatos, start=1):
        indicador_reducao = " (reduzida)" if len(chave) < tamanho else ""

        print(
            f"{indice}. Tamanho testado: {tamanho:2d} | "
            f"IC médio: {ic:.5f} | "
            f"Chave: {chave}{indicador_reducao}"
        )


def selecionar_candidato(candidatos, criptograma):
    indice_selecionado = 0

    while True:
        candidato = candidatos[indice_selecionado]
        chave = candidato[2]
        texto_decifrado = decrypt(chave, criptograma)

        print()
        print(
            f"Prévia do candidato {indice_selecionado + 1} "
            f"(chave {chave}):"
        )
        print(texto_decifrado[:TAMANHO_PREVIA])

        if len(texto_decifrado) > TAMANHO_PREVIA:
            print(f"[prévia limitada a {TAMANHO_PREVIA} caracteres]")

        resposta = input(
            "Digite o número de outro candidato ou A para aceitar: "
        ).strip().lower()

        if resposta in ("", "a", "aceitar"):
            return candidato

        try:
            novo_indice = int(resposta) - 1
        except ValueError:
            novo_indice = -1

        if 0 <= novo_indice < len(candidatos):
            indice_selecionado = novo_indice
        else:
            print(
                f"Escolha um número de 1 a {len(candidatos)} "
                "ou A para aceitar."
            )


def analisar_criptograma(criptograma, idioma, maximo_chave):
    resultados = estimar_chave(criptograma, maximo_chave)
    resultados_ordenados = sorted(
        resultados,
        key=lambda x: x[1],
        reverse=True,
    )

    candidatos_chave = []

    # O IC ranqueia os tamanhos; a frequência reconstrói uma chave para cada um.
    for tamanho, ic in resultados_ordenados:
        chave = descobrir_chave(
            criptograma,
            tamanho,
            idioma,
        )
        chave = reduzir_chave_repetida(chave)

        candidatos_chave.append(
            (tamanho, ic, chave),
        )

    return sorted(
        candidatos_chave,
        key=lambda x: x[1],
        reverse=True,
    )


def main():
    parser = argparse.ArgumentParser(
        description="Estima a chave e decifra um criptograma de Vigenère."
    )
    parser.add_argument(
        "arquivo",
        help="caminho do criptograma",
    )
    parser.add_argument(
        "-i",
        "--idioma",
        choices=("pt", "en"),
        default="pt",
        help="idioma esperado do texto original (padrão: pt)",
    )
    parser.add_argument(
        "-m",
        "--max-chave",
        type=int,
        default=20,
        help="tamanho máximo de chave a testar (padrão: 20)",
    )
    parser.add_argument(
        "--interativo",
        action="store_true",
        help="permite visualizar e escolher entre os melhores candidatos",
    )
    args = parser.parse_args()

    if args.max_chave < 1:
        parser.error("o tamanho máximo da chave deve ser positivo")

    with open(args.arquivo, "r", encoding="utf-8", newline="") as arquivo:
        criptograma = normalizar_texto(arquivo.read())

    chaves_sorted = analisar_criptograma(
        criptograma,
        args.idioma,
        args.max_chave,
    )

    melhores_candidatos = chaves_sorted[:LIMITE_CANDIDATOS]
    mostrar_candidatos(melhores_candidatos)

    if args.interativo:
        chave_final = selecionar_candidato(
            melhores_candidatos,
            criptograma,
        )
    else:
        chave_final = melhores_candidatos[0]

    print()
    print("Chave estimada:", chave_final[2])
    print()
    print(decrypt(chave_final[2], criptograma))


if __name__ == "__main__":
    main()
