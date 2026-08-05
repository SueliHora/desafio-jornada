#!/usr/bin/env python3
"""
Leitura do cartão de submissão da galeria.

O corpo do cartão é markdown livre: o aluno escreve, organiza e ilustra como
quiser. A única parte com contrato são os metadados no topo, no bloco
delimitado por `---`.

Este módulo é a fonte única de verdade desse contrato. A validação do pull
request e o gerador do mural leem daqui, para nunca discordarem sobre o que
um cartão válido tem dentro.
"""

import os
import re
import sys
import unicodedata
from urllib.parse import urlsplit

OBRIGATORIOS = [
    "projeto",
    "autor",
    "usuario",
    "dominio",
    "repositorio",
    "status",
    "linkedin",
    "plataforma",
]
OPCIONAIS = ["video"]
CONHECIDOS = OBRIGATORIOS + OPCIONAIS

STATUS = ["Discovery", "Em construção", "Funcionando", "Em produção"]

HOSTS_GITHUB = {"github.com", "www.github.com"}
HOSTS_LINKEDIN = {"linkedin.com", "www.linkedin.com"}
# O "copy link" do LinkedIn gera /posts/ para post normal e /feed/update/ para
# alguns tipos de publicação. Os dois são válidos; o slug depois disso varia
# demais (aparece tanto -activity- quanto -share-) para valer a pena validar.
PREFIXOS_LINKEDIN = ("/posts/", "/feed/update/")
HOST_PLATAFORMA = "suajornadadedados.curseduca.pro"
PREFIXO_PLATAFORMA = "/m/community/posts/"

USUARIO_RE = re.compile(r"^[a-z0-9](?:[a-z0-9]|-(?=[a-z0-9])){0,38}$")

# <desafio>/projetos/<usuario>/<resto>
CARTAO_RE = re.compile(
    r"^(?P<desafio>[a-z0-9][a-z0-9._-]*)/projetos/(?P<usuario>[^/]+)/(?P<resto>.+)$"
)


def utf8_no_console():
    """O relatório usa emoji e acento; sem isto quebra em console Windows."""
    for fluxo in (sys.stdout, sys.stderr):
        if hasattr(fluxo, "reconfigure"):
            fluxo.reconfigure(encoding="utf-8", errors="replace")


def sem_acento(texto):
    nfkd = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in nfkd if not unicodedata.combining(c)).lower()


def status_canonico(valor):
    """Aceita o status sem ligar para acento ou caixa, devolve a forma oficial.

    O mural é gerado a partir daqui, então "em construcao" e "Em Construção"
    precisam virar a mesma string, senão a coluna fica com três grafias.
    """
    alvo = sem_acento(valor.strip())
    for oficial in STATUS:
        if sem_acento(oficial) == alvo:
            return oficial
    return None


def le_metadados(caminho):
    """Lê o bloco de metadados do topo de um cartão.

    Devolve (dados, erros). Aceita o subconjunto plano de YAML: uma
    `chave: valor` por linha. Isso cobre o cartão inteiro e evita depender de
    biblioteca externa no runner.
    """
    erros = []
    try:
        texto = open(caminho, encoding="utf-8").read()
    except OSError as e:
        return {}, [f"Não consegui ler `{caminho}`: {e}."]

    linhas = texto.splitlines()
    if not linhas or linhas[0].strip() != "---":
        return {}, [
            "O cartão precisa começar com o bloco de metadados. A primeiríssima "
            "linha do arquivo tem que ser `---`, sem linha em branco antes. "
            "Veja o modelo no COMO-SUBMETER.md."
        ]

    fim = None
    for i in range(1, len(linhas)):
        if linhas[i].strip() == "---":
            fim = i
            break
    if fim is None:
        return {}, [
            "O bloco de metadados abre com `---` mas nunca fecha. "
            "Feche com outra linha `---` antes de começar o texto do cartão."
        ]

    dados = {}
    for numero, linha in enumerate(linhas[1:fim], start=2):
        if not linha.strip() or linha.lstrip().startswith("#"):
            continue
        if ":" not in linha:
            erros.append(
                f"Linha {numero} dos metadados (`{linha.strip()}`) não está no "
                "formato `chave: valor`."
            )
            continue
        chave, valor = linha.split(":", 1)
        chave = sem_acento(chave.strip())
        valor = valor.strip()
        # Valor com dois-pontos precisa vir entre aspas para o GitHub renderizar
        # o bloco; aqui as aspas são só embalagem e saem antes de usar.
        if len(valor) >= 2 and valor[0] == valor[-1] and valor[0] in "\"'":
            valor = valor[1:-1]
        if chave in dados:
            erros.append(f"O campo `{chave}` aparece mais de uma vez nos metadados.")
        dados[chave] = valor.strip()

    return dados, erros


def _valida_link(campo, valor, hosts, prefixos=None, exemplo=""):
    """Confere um link: https, host esperado, caminho esperado, sem rastreio."""
    erros = []
    partes = urlsplit(valor)

    if partes.scheme != "https":
        erros.append(f"O link do campo `{campo}` precisa começar com `https://`.")
        return erros

    if partes.netloc.lower() not in hosts:
        erros.append(
            f"O campo `{campo}` aponta para `{partes.netloc or 'lugar nenhum'}`, e "
            f"deveria apontar para {' ou '.join(sorted(hosts))}." + exemplo
        )
        return erros

    if prefixos and not partes.path.startswith(tuple(prefixos)):
        erros.append(
            f"O campo `{campo}` não parece o link de uma publicação: o caminho "
            f"`{partes.path or '/'}` deveria começar com "
            f"{' ou '.join(f'`{p}`' for p in prefixos)}." + exemplo
        )
        return erros

    # O botão de compartilhar cola parâmetros de rastreamento que identificam
    # quem copiou o link. Isso não entra num repositório público e permanente.
    if partes.query or partes.fragment:
        limpo = f"{partes.scheme}://{partes.netloc}{partes.path.rstrip('/')}"
        erros.append(
            f"O link do campo `{campo}` veio com parâmetros de rastreamento no "
            f"fim (`?{partes.query}`). Eles identificam quem copiou o link e não "
            f"entram no repositório. Use assim:\n     `{limpo}`"
        )

    return erros


def valida_metadados(dados, usuario_da_pasta=None):
    """Confere o contrato do cartão. Devolve a lista de erros."""
    erros = []

    for campo in OBRIGATORIOS:
        if campo not in dados:
            erros.append(f"Falta o campo obrigatório `{campo}` nos metadados do cartão.")
        elif not dados[campo]:
            erros.append(f"O campo `{campo}` está vazio.")

    for campo in dados:
        if campo not in CONHECIDOS:
            erros.append(
                f"O campo `{campo}` não faz parte do cartão. "
                f"Conhecidos: {', '.join(f'`{c}`' for c in CONHECIDOS)}."
            )

    usuario = dados.get("usuario", "")
    if usuario:
        if not USUARIO_RE.match(usuario):
            erros.append(
                f"`usuario: {usuario}` não parece um nome de usuário do GitHub "
                "válido. Use exatamente o seu usuário, tudo em minúsculas."
            )
        elif usuario_da_pasta and usuario != usuario_da_pasta.lower():
            erros.append(
                f"O campo `usuario: {usuario}` não bate com o nome da pasta "
                f"`{usuario_da_pasta}`. Os dois precisam ser o seu usuário do GitHub."
            )

    status = dados.get("status", "")
    if status and status_canonico(status) is None:
        erros.append(
            f"`status: {status}` não é um dos valores aceitos. "
            f"Use um destes: {', '.join(STATUS)}."
        )

    if dados.get("repositorio"):
        erros += _valida_link(
            "repositorio",
            dados["repositorio"],
            HOSTS_GITHUB,
            exemplo="\n     Exemplo: `https://github.com/seu-usuario/seu-projeto`",
        )

    if dados.get("linkedin"):
        erros += _valida_link(
            "linkedin",
            dados["linkedin"],
            HOSTS_LINKEDIN,
            PREFIXOS_LINKEDIN,
            exemplo=(
                "\n     Precisa ser o link do post, não o do seu perfil."
                "\n     Exemplo: `https://www.linkedin.com/posts/seu-usuario_meu-projeto-...`"
            ),
        )

    if dados.get("plataforma"):
        erros += _valida_link(
            "plataforma",
            dados["plataforma"],
            {HOST_PLATAFORMA},
            [PREFIXO_PLATAFORMA],
            exemplo=(
                "\n     É o link do seu post na comunidade da plataforma."
                f"\n     Exemplo: `https://{HOST_PLATAFORMA}{PREFIXO_PLATAFORMA}<id-do-post>`"
            ),
        )

    if dados.get("video"):
        erros += _valida_link("video", dados["video"], {
            "youtube.com", "www.youtube.com", "youtu.be",
            "loom.com", "www.loom.com",
        }, exemplo="\n     Aceita YouTube ou Loom.")

    return erros


def procura_cartoes(raiz="."):
    """Encontra todos os cartões do repositório: <desafio>/projetos/<usuario>/README.md."""
    achados = []
    for desafio in sorted(os.listdir(raiz)):
        pasta_projetos = os.path.join(raiz, desafio, "projetos")
        if not os.path.isdir(pasta_projetos):
            continue
        for usuario in sorted(os.listdir(pasta_projetos)):
            pasta = os.path.join(pasta_projetos, usuario)
            cartao = os.path.join(pasta, "README.md")
            if os.path.isdir(pasta) and os.path.isfile(cartao):
                achados.append((desafio, usuario, cartao.replace(os.sep, "/")))
    return achados
