# vigenere-cypher-study

Este repositório tem por objetivo a implementação da Cifra de Vigenère em python, assim como a de um algorítmo capaz de quebra-la. Este é o primeiro projeto da disciplina de Segurança Computacional - Turma 1 - 2026/2

## Instruções de Uso

### 1. Cifra de Vigenère

**Via Linha de Comando:**
```bash
# Encriptar
python3 vigenere_cipher.py enc CHAVE "Mensagem de teste"

# Desencriptar
python3 vigenere_cipher.py dec CHAVE "VLXOS FL TZWVL"
```

**Via Python:**
```python
from vigenere_cipher import encrypt, decrypt

criptograma = encrypt("CHAVE", "Mensagem de teste")
original = decrypt("CHAVE", criptograma)
```

### 2. Ataque / Criptoanálise (CLI)

```bash
# Execução básica (Português, max_chave=20)
python3 -m ataque.main <caminho_do_arquivo>

# Opções de linha de comando
python3 -m ataque.main <caminho_do_arquivo> [-i pt|en] [-m MAX_CHAVE] [--interativo]
```

**Parâmetros:**
- `-i`, `--idioma`: Idioma do texto (`pt` ou `en`, padrão: `pt`).
- `-m`, `--max-chave`: Tamanho máximo de chave a testar (padrão: `20`).
- `--interativo`: Exibe prévias e permite selecionar o melhor candidato a chave.

### 3. Avaliação automatizada

```bash
python3 -m evaluation.testar_ataque [caminho_do_texto] [--casos N] [-i pt|en]
```

Sem um caminho explícito, o avaliador utiliza `evaluation/quincas.txt`.
