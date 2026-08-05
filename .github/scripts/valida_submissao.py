#!/usr/bin/env python3
"""
Valida um pull request de submissão de cartão para a galeria.

Confere duas coisas, e só elas: que o PR mexe apenas na pasta do próprio
cartão, e que os metadados no topo do cartão estão completos e corretos.

O corpo do cartão é livre. Como o aluno organiza, ilustra e escreve o texto
é escolha dele, e é assunto da revisão humana, não do CI.

Uso:
    python valida_submissao.py <arquivo-com-a-lista-de-arquivos-alterados>

O arquivo de entrada tem um caminho por linha, relativo à raiz do repositório
(a saída de `git diff --name-only`). Sai com código 1 se houver erro.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cartao import (  # noqa: E402
    CARTAO_RE,
    le_metadados,
    utf8_no_console,
    valida_metadados,
)

MAX_BYTES = 2 * 1024 * 1024
EXT_PERMITIDAS = {".md", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}

utf8_no_console()

erros = []
avisos = []


def erro(msg):
    erros.append(msg)


def aviso(msg):
    avisos.append(msg)


def valida_pasta(pasta, usuario):
    """Confere os arquivos da pasta do cartão e os metadados do README."""
    cartao = os.path.join(pasta, "README.md")
    if not os.path.isfile(cartao):
        erro(
            f"A pasta `{pasta}` não tem `README.md`. O cartão é obrigatório — "
            "veja o modelo no COMO-SUBMETER.md."
        )
        return

    tem_imagem = False
    for raiz, _, nomes in os.walk(pasta):
        for nome in nomes:
            caminho = os.path.join(raiz, nome).replace(os.sep, "/")
            ext = os.path.splitext(nome)[1].lower()

            if ext not in EXT_PERMITIDAS:
                erro(
                    f"`{caminho}` tem extensão `{ext or 'sem extensão'}`, que não "
                    f"entra na galeria. Permitido: {', '.join(sorted(EXT_PERMITIDAS))}."
                )
                continue

            if ext != ".md":
                tem_imagem = True

            tamanho = os.path.getsize(caminho)
            if tamanho > MAX_BYTES:
                erro(
                    f"`{caminho}` tem {tamanho / 1024 / 1024:.1f} MB, acima do limite "
                    f"de {MAX_BYTES / 1024 / 1024:.0f} MB. Comprima a imagem antes de subir."
                )

    dados, erros_leitura = le_metadados(cartao)
    for e in erros_leitura:
        erro(e)
    if dados:
        for e in valida_metadados(dados, usuario_da_pasta=usuario):
            erro(e)

    if not tem_imagem:
        aviso(
            f"`{pasta}` não tem imagem. Um diagrama da arquitetura ou um print do "
            "produto deixa o seu cartão bem mais atraente na galeria."
        )


def main():
    if len(sys.argv) < 2:
        print("uso: valida_submissao.py <arquivo-com-lista-de-arquivos>", file=sys.stderr)
        return 2

    with open(sys.argv[1], encoding="utf-8") as f:
        arquivos = [linha.strip() for linha in f if linha.strip()]

    if not arquivos:
        print("Nenhum arquivo alterado.")
        return 0

    cartoes = {}   # (desafio, usuario) -> pasta
    fora = []      # arquivos que não fazem parte de um cartão

    for caminho in arquivos:
        m = CARTAO_RE.match(caminho)
        if m:
            chave = (m.group("desafio"), m.group("usuario"))
            cartoes[chave] = f"{m.group('desafio')}/projetos/{m.group('usuario')}"
        else:
            fora.append(caminho)

    # Sem cartão nenhum: é PR de correção no material, não de submissão.
    if not cartoes:
        print("PR não altera nenhum cartão da galeria.")
        print("Validação de submissão não se aplica — a revisão é humana.")
        return 0

    print(f"Cartões detectados: {', '.join(sorted(cartoes.values()))}\n")

    if len(cartoes) > 1:
        erro(
            "Este PR mexe em mais de um cartão: "
            + ", ".join(f"`{v}`" for v in sorted(cartoes.values()))
            + ". Abra um PR por cartão, para a revisão e o histórico ficarem limpos."
        )

    if fora:
        erro(
            "Este PR mistura o cartão com arquivos que não pertencem à galeria:\n"
            + "\n".join(f"  - `{a}`" for a in sorted(fora)[:20])
            + "\n\nSubmissão de cartão só altera arquivos dentro da sua pasta. "
            "Código do projeto fica no seu repositório, e o `PROJETOS.md` é "
            "gerado automaticamente depois do merge."
        )

    for chave, pasta in cartoes.items():
        if not os.path.isdir(pasta):
            continue  # pasta removida no PR
        valida_pasta(pasta, usuario=chave[1])

    # ---- relatório ----
    linhas = []
    if erros:
        linhas.append(f"## ❌ {len(erros)} problema(s) para resolver\n")
        linhas += [f"{i}. {e}" for i, e in enumerate(erros, 1)]
    else:
        linhas.append("## ✅ Cartão validado\n")
        linhas.append(
            "Metadados completos e nada fora do lugar. A revisão humana segue "
            "daqui, olhando o conteúdo do projeto."
        )
    if avisos:
        linhas.append(f"\n## ⚠️ {len(avisos)} sugestão(ões)\n")
        linhas += [f"- {a}" for a in avisos]

    relatorio = "\n".join(linhas)
    print(relatorio)

    resumo = os.environ.get("GITHUB_STEP_SUMMARY")
    if resumo:
        with open(resumo, "a", encoding="utf-8") as f:
            f.write(relatorio + "\n")

    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
