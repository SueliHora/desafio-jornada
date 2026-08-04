#!/usr/bin/env python3
"""
Valida um pull request de submissão de cartão para a galeria.

Confere o que o COMO-SUBMETER.md pede, para que a revisão humana possa
gastar o tempo dela no conteúdo do projeto, e não em conferir estrutura.

Uso:
    python valida_submissao.py <arquivo-com-a-lista-de-arquivos-alterados>

O arquivo de entrada tem um caminho por linha, relativo à raiz do repositório
(a saída de `git diff --name-only`). Sai com código 1 se houver erro.
"""

import os
import re
import sys
import unicodedata

MAX_BYTES = 2 * 1024 * 1024
EXT_PERMITIDAS = {".md", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}

# <desafio>/projetos/<usuario>/<resto>
CARTAO_RE = re.compile(r"^(?P<desafio>[a-z0-9][a-z0-9._-]*)/projetos/(?P<usuario>[^/]+)/(?P<resto>.+)$")
# <desafio>/projetos/README.md  — o índice da galeria
INDICE_RE = re.compile(r"^[a-z0-9][a-z0-9._-]*/projetos/README\.md$")
USUARIO_RE = re.compile(r"^[a-z0-9](?:[a-z0-9]|-(?=[a-z0-9])){0,38}$")

SECOES = [
    ("o projeto em", "## O projeto em três linhas"),
    ("arquitetura", "## Arquitetura"),
    ("stack", "## Stack escolhida"),
    ("decisoes mais dificeis", "## As três decisões mais difíceis"),
    ("garantias", "## Como atendi às garantias"),
    ("aprendi", "## O que eu aprendi"),
]

CAMPOS = ["Autor", "Domínio", "Repositório completo", "Status"]

# Trechos do modelo que, se sobreviverem, indicam cartão não preenchido.
PLACEHOLDERS = [
    "seu nome (@seu-usuario)",
    "o negócio que você escolheu",
    "link para o seu repositório",
    "discovery / em construção / funcionando / em produção",
    "descreva o que o seu agente faz",
    "uma imagem ou diagrama, e um parágrafo",
    "liste as principais tecnologias",
    "conte as três decisões de engenharia",
    "um parágrafo honesto",
    "nome do projeto",
]

# O relatório usa emoji e acento; sem isto o script quebra em console
# Windows (cp1252). O runner do Actions é UTF-8, mas rodar local precisa valer.
for _fluxo in (sys.stdout, sys.stderr):
    if hasattr(_fluxo, "reconfigure"):
        _fluxo.reconfigure(encoding="utf-8", errors="replace")

erros = []
avisos = []


def sem_acento(texto):
    nfkd = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in nfkd if not unicodedata.combining(c)).lower()


def erro(msg):
    erros.append(msg)


def aviso(msg):
    avisos.append(msg)


def valida_cartao(pasta):
    """Valida o README do cartão dentro de <pasta>."""
    caminho = os.path.join(pasta, "README.md")
    if not os.path.isfile(caminho):
        erro(f"A pasta `{pasta}` não tem `README.md`. O cartão é obrigatório — veja o modelo no COMO-SUBMETER.md.")
        return

    texto = open(caminho, encoding="utf-8").read()
    normalizado = sem_acento(texto)

    for chave, titulo in SECOES:
        if chave not in normalizado:
            erro(f"O cartão está sem a seção `{titulo}`.")

    for campo in CAMPOS:
        padrao = re.compile(r"\*\*%s:?\*\*\s*(.+)" % re.escape(campo), re.IGNORECASE)
        m = padrao.search(texto)
        if not m:
            erro(f"O cartão está sem o campo `**{campo}:**` no cabeçalho.")
        elif not m.group(1).strip():
            erro(f"O campo `**{campo}:**` está vazio.")

    m = re.search(r"\*\*Repositório completo:?\*\*\s*(.+)", texto, re.IGNORECASE)
    if m and "http" not in m.group(1):
        erro("O campo `**Repositório completo:**` precisa ser um link (começando com http).")

    for ph in PLACEHOLDERS:
        if ph in normalizado:
            erro(f"O cartão ainda tem texto do modelo sem preencher: \"{ph}\".")

    if len(texto.strip()) < 400:
        aviso("O cartão está bem curto. A seção de aprendizados é a que a comunidade mais lê — vale caprichar.")


def main():
    if len(sys.argv) < 2:
        print("uso: valida_submissao.py <arquivo-com-lista-de-arquivos>", file=sys.stderr)
        return 2

    with open(sys.argv[1], encoding="utf-8") as f:
        arquivos = [l.strip() for l in f if l.strip()]

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
        elif INDICE_RE.match(caminho):
            continue  # atualizar o índice da galeria é permitido
        else:
            fora.append(caminho)

    # Sem cartão nenhum: é PR de correção no material, não de submissão.
    if not cartoes:
        print("PR não altera nenhum cartão da galeria.")
        print("Validação de submissão não se aplica — a revisão é humana.")
        return 0

    print(f"Cartões detectados: {', '.join(sorted(v for v in cartoes.values()))}\n")

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
            "Código do projeto fica no seu repositório."
        )

    for (desafio, usuario), pasta in cartoes.items():
        if not USUARIO_RE.match(usuario):
            erro(
                f"A pasta `{usuario}` não parece um usuário do GitHub válido em letras minúsculas. "
                "Use exatamente o seu usuário, tudo minúsculo."
            )

        if not os.path.isdir(pasta):
            continue  # pasta removida no PR

        tem_imagem = False
        for raiz, _, nomes in os.walk(pasta):
            for nome in nomes:
                caminho = os.path.join(raiz, nome).replace(os.sep, "/")
                ext = os.path.splitext(nome)[1].lower()

                if ext not in EXT_PERMITIDAS:
                    erro(
                        f"`{caminho}` tem extensão `{ext or 'sem extensão'}`, que não entra na galeria. "
                        f"Permitido: {', '.join(sorted(EXT_PERMITIDAS))}."
                    )
                    continue

                if ext != ".md":
                    tem_imagem = True

                tamanho = os.path.getsize(caminho)
                if tamanho > MAX_BYTES:
                    erro(
                        f"`{caminho}` tem {tamanho / 1024 / 1024:.1f} MB, acima do limite de "
                        f"{MAX_BYTES / 1024 / 1024:.0f} MB. Comprima a imagem antes de subir."
                    )

        valida_cartao(pasta)

        if not tem_imagem:
            aviso(
                f"`{pasta}` não tem imagem. Um diagrama da arquitetura ou um print do produto "
                "deixa o seu cartão bem mais atraente na galeria."
            )

    # ---- relatório ----
    linhas = []
    if erros:
        linhas.append(f"## ❌ {len(erros)} problema(s) para resolver\n")
        linhas += [f"{i}. {e}" for i, e in enumerate(erros, 1)]
    else:
        linhas.append("## ✅ Estrutura do cartão validada\n")
        linhas.append("Nada fora do lugar. A revisão humana segue daqui, olhando o conteúdo do projeto.")
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
