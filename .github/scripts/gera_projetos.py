#!/usr/bin/env python3
"""
Gera o `PROJETOS.md`: o mural de todos os projetos da comunidade.

O mural é uma função das pastas de cartão que existem no repositório. Ele é
reescrito inteiro a cada execução, nunca acrescentado — assim rodar duas vezes
dá o mesmo resultado, ninguém precisa resolver conflito e um cartão atualizado
(um vídeo de demo que entrou depois, por exemplo) aparece no mural sozinho,
sem ninguém editar tabela na mão.

Uso:
    python gera_projetos.py [--conferir]

Sem argumento, escreve o arquivo. Com `--conferir`, só avisa se o arquivo no
disco está desatualizado, sem escrever (útil para rodar em PR).
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cartao import (  # noqa: E402
    le_metadados,
    procura_cartoes,
    utf8_no_console,
    valida_metadados,
)

SAIDA = "PROJETOS.md"

# Rótulo de cada desafio no mural, do mais recente para o mais antigo. Ao abrir
# um mês novo, acrescente a linha no topo. Pasta sem rótulo aqui ainda aparece
# no mural, usando o próprio nome — só fica menos bonita.
DESAFIOS = {
    "desafio-vendas": "Agosto/2026 — Agente de Vendas de Ponta a Ponta",
}

CABECALHO = """<!-- ATENÇÃO: arquivo gerado automaticamente por .github/scripts/gera_projetos.py
     a partir dos cartões em <desafio>/projetos/<usuario>/README.md.
     Não edite à mão: qualquer alteração é sobrescrita no próximo merge.
     Para entrar no mural, envie o seu cartão — veja o COMO-SUBMETER.md. -->

# Projetos da comunidade

Todo projeto aqui foi construído por um aluno da Jornada de Dados, no
repositório dele, do zero. Este mural é só o índice: clique no nome do projeto
para ler o cartão, ou vá direto no repositório de quem construiu.
"""

RODAPE = """
---

Quer o seu projeto aqui? O passo a passo está em
[COMO-SUBMETER.md](COMO-SUBMETER.md). Leva uns 20 minutos, e o mural se
atualiza sozinho assim que o seu pull request entra.
"""


def linha_de_links(dados):
    links = [f"[repo]({dados['repositorio']})"]
    if dados.get("linkedin"):
        links.append(f"[linkedin]({dados['linkedin']})")
    if dados.get("plataforma"):
        links.append(f"[comunidade]({dados['plataforma']})")
    if dados.get("video"):
        links.append(f"[vídeo]({dados['video']})")
    return " · ".join(links)


def escapa(texto):
    """Impede que um pipe no texto do aluno quebre a tabela markdown."""
    return texto.replace("|", "\\|")


def monta():
    utf8_no_console()

    por_desafio = {}
    ignorados = []

    for desafio, usuario, caminho in procura_cartoes("."):
        dados, erros_leitura = le_metadados(caminho)
        problemas = erros_leitura + (
            valida_metadados(dados, usuario_da_pasta=usuario) if dados else []
        )
        if problemas:
            # Cartão quebrado na main não derruba o mural inteiro: fica de fora
            # e o log diz por quê. Isso só acontece se algo entrou sem passar
            # pela validação do PR.
            ignorados.append((caminho, problemas[0]))
            continue
        por_desafio.setdefault(desafio, []).append((usuario, dados))

    ordem = [d for d in DESAFIOS if d in por_desafio]
    ordem += sorted(d for d in por_desafio if d not in DESAFIOS)

    total = sum(len(v) for v in por_desafio.values())
    partes = [CABECALHO]

    if total == 0:
        partes.append(
            "\nAinda não há projetos no mural. O primeiro pode ser o seu.\n"
        )
    else:
        plural = "projeto" if total == 1 else "projetos"
        partes.append(f"\n**{total} {plural}** na galeria até agora.\n")

    for desafio in ordem:
        rotulo = DESAFIOS.get(desafio, desafio)
        partes.append(f"\n## {rotulo}\n")
        partes.append("| Projeto | Autor | Domínio | Links |")
        partes.append("|---|---|---|---|")
        for usuario, dados in sorted(por_desafio[desafio], key=lambda x: x[0].lower()):
            cartao = f"{desafio}/projetos/{usuario}/README.md"
            partes.append(
                "| [{projeto}]({cartao}) "
                "| {autor} ([@{usuario}](https://github.com/{usuario})) "
                "| {dominio} | {links} |".format(
                    projeto=escapa(dados["projeto"]),
                    cartao=cartao,
                    autor=escapa(dados["autor"]),
                    usuario=usuario,
                    dominio=escapa(dados["dominio"]),
                    links=linha_de_links(dados),
                )
            )
        partes.append("")

    partes.append(RODAPE)
    return "\n".join(partes).rstrip() + "\n", ignorados


def main():
    conteudo, ignorados = monta()

    for caminho, motivo in ignorados:
        print(f"AVISO: `{caminho}` ficou de fora do mural — {motivo}", file=sys.stderr)

    atual = ""
    if os.path.isfile(SAIDA):
        atual = open(SAIDA, encoding="utf-8").read()

    if "--conferir" in sys.argv:
        if atual != conteudo:
            print(f"{SAIDA} está desatualizado. Rode: python .github/scripts/gera_projetos.py")
            return 1
        print(f"{SAIDA} está em dia.")
        return 0

    if atual == conteudo:
        print(f"{SAIDA} já estava em dia, nada a fazer.")
        return 0

    with open(SAIDA, "w", encoding="utf-8", newline="\n") as f:
        f.write(conteudo)
    print(f"{SAIDA} atualizado.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
