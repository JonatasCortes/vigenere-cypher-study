import argparse

from gerar_casos import gerar_casos
from main import analisar_criptograma
from quebrar_cipher import reduzir_chave_repetida
from utils import ALFABETO, decriptar_vigenere


def contar_letras(texto):
    return sum(caractere in ALFABETO for caractere in texto)


def encontrar_candidato_correto(caso, candidatos):
    chave_esperada = reduzir_chave_repetida(caso["chave"])

    for posicao, candidato in enumerate(candidatos, start=1):
        chave_encontrada = candidato[2]
        texto_encontrado = decriptar_vigenere(
            chave_encontrada,
            caso["criptograma"],
        )

        if (
            chave_encontrada == chave_esperada
            and texto_encontrado == caso["texto_claro"]
        ):
            return posicao

    return None


def main():
    parser = argparse.ArgumentParser(
        description="Gera casos aleatórios e avalia o ataque de Vigenère."
    )
    parser.add_argument(
        "arquivo",
        nargs="?",
        default="quincas.txt",
        help="texto usado para gerar os casos (padrão: quincas.txt)",
    )
    parser.add_argument(
        "--casos",
        type=int,
        default=20,
        help="quantidade de casos gerados (padrão: 20)",
    )
    parser.add_argument(
        "--semente",
        type=int,
        default=42,
        help="semente do gerador aleatório (padrão: 42)",
    )
    parser.add_argument(
        "-i",
        "--idioma",
        choices=("pt", "en"),
        default="pt",
        help="idioma esperado dos trechos (padrão: pt)",
    )
    parser.add_argument(
        "--min-texto",
        type=int,
        default=500,
        help="tamanho mínimo do trecho em caracteres (padrão: 500)",
    )
    parser.add_argument(
        "--max-texto",
        type=int,
        default=2000,
        help="tamanho máximo do trecho em caracteres (padrão: 2000)",
    )
    parser.add_argument(
        "--min-chave",
        type=int,
        default=1,
        help="tamanho mínimo da chave (padrão: 1)",
    )
    parser.add_argument(
        "--max-chave",
        type=int,
        default=15,
        help="tamanho máximo da chave gerada (padrão: 15)",
    )
    parser.add_argument(
        "--max-ataque",
        type=int,
        default=20,
        help="maior tamanho testado pelo ataque (padrão: 20)",
    )
    parser.add_argument(
        "--candidatos",
        type=int,
        default=5,
        help="quantidade de candidatos considerada (padrão: 5)",
    )
    parser.add_argument(
        "--exigir-todos",
        action="store_true",
        help="retorna erro se algum caso não estiver entre os candidatos",
    )
    args = parser.parse_args()

    if args.casos < 1:
        parser.error("a quantidade de casos deve ser positiva")

    if args.min_texto < 1 or args.max_texto < args.min_texto:
        parser.error("o intervalo de tamanho do texto é inválido")

    if args.min_chave < 1 or args.max_chave < args.min_chave:
        parser.error("o intervalo de tamanho da chave é inválido")

    if args.max_ataque < 1:
        parser.error("o tamanho máximo do ataque deve ser positivo")

    if args.candidatos < 1:
        parser.error("a quantidade de candidatos deve ser positiva")

    with open(args.arquivo, "r", encoding="utf-8", newline="") as arquivo:
        texto = arquivo.read()

    casos = gerar_casos(
        texto,
        args.casos,
        args.min_texto,
        args.max_texto,
        args.min_chave,
        args.max_chave,
        args.semente,
    )

    sucessos_automaticos = 0
    sucessos_candidatos = 0

    print(
        f"Semente: {args.semente} | Casos: {args.casos} | "
        f"Idioma: {args.idioma} | "
        f"Texto: {args.min_texto}-{args.max_texto} | "
        f"Chave: {args.min_chave}-{args.max_chave}"
    )
    print()

    for numero, caso in enumerate(casos, start=1):
        candidatos = analisar_criptograma(
            caso["criptograma"],
            args.idioma,
            args.max_ataque,
        )[:args.candidatos]
        posicao = encontrar_candidato_correto(caso, candidatos)

        if posicao == 1:
            sucessos_automaticos += 1

        if posicao is not None:
            sucessos_candidatos += 1

        resultado = f"top {posicao}" if posicao is not None else "falha"
        chave_estimada = candidatos[0][2]

        print(
            f"{numero:02d}. início={caso['inicio']:6d} | "
            f"letras={contar_letras(caso['texto_claro']):4d} | "
            f"chave={caso['chave']:<15} | "
            f"estimada={chave_estimada:<15} | {resultado}"
        )

    taxa_automatica = 100 * sucessos_automaticos / args.casos
    taxa_candidatos = 100 * sucessos_candidatos / args.casos

    print()
    print(
        f"Sucesso automático: {sucessos_automaticos}/{args.casos} "
        f"({taxa_automatica:.1f}%)"
    )
    print(
        f"Sucesso entre os {args.candidatos} candidatos: "
        f"{sucessos_candidatos}/{args.casos} "
        f"({taxa_candidatos:.1f}%)"
    )

    if args.exigir_todos and sucessos_candidatos != args.casos:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
