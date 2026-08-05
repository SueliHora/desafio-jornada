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

# Cada campo de link só precisa começar com o endereço certo e ter alguma coisa
# depois dele. Não conferimos se o link abre, nem o formato do identificador: o
# que interessa é que o aluno colou um post, e não o perfil ou a home.
LINKS = {
    "repositorio": (
        "https://github.com/",
        "o seu repositório público no GitHub",
    ),
    "linkedin": (
        "https://www.linkedin.com/posts/",
        "o link do post sobre o projeto, não o do seu perfil",
    ),
    "plataforma": (
        "https://suajornadadedados.curseduca.pro/m/community/posts/",
        "o link do seu post na comunidade da plataforma",
    ),
    "video": (
        "https://",
        "o link da sua demo em vídeo",
    ),
}

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


def _valida_link(campo, valor):
    """Confere só que o link existe e começa com o endereço esperado."""
    prefixo, oque = LINKS[campo]

    if not valor.startswith(prefixo):
        return [
            f"O campo `{campo}` precisa ser {oque}, começando com `{prefixo}`.\n"
            f"     Você colocou: `{valor}`"
        ]

    if len(valor.rstrip("/")) <= len(prefixo.rstrip("/")):
        return [
            f"O campo `{campo}` tem só o começo do endereço (`{prefixo}`), "
            "sem o link do post em si."
        ]

    return []


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

    for campo in LINKS:
        if dados.get(campo):
            erros += _valida_link(campo, dados[campo])

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
