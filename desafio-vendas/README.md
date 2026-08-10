# Desafio Jornada de Dados — Construa um Agente de Vendas de Ponta a Ponta

## O que é este desafio

Este repositório é um convite para você construir um produto de verdade com IA. Não um chatbot de demonstração, mas um sistema de atendimento e vendas que sai do primeiro "oi" do cliente e chega até o fim: recomendação, pedido, pagamento, documento emitido.

Aqui você não vai encontrar código pronto, lista de tarefas nem resposta certa. Vai encontrar **um pedido de cliente**. Traduzir esse pedido em escopo, arquitetura e código é o trabalho. Todas as decisões são suas: domínio, stack, quantidade de agentes, ferramentas, recorte da primeira versão. É assim que funciona no mundo real: o cliente sabe o que quer, mas não sabe como se constrói. Quem decide como construir é você.

> **Regra nº 1 do desafio: o case é seu, e é inédito.**
> Não existe gabarito para copiar. Escolha o negócio: petshop, clínica, imobiliária, oficina, loja de instrumentos, consultoria... Qualquer ramo em que o cliente chega conversando sem saber o que pedir, e em que existe pelo menos uma etapa em que errar é inaceitável. E não pare no ramo: **batize o negócio, batize o cliente, batize o produto.**

---

# Parte 1 — O pedido do cliente

## A conversa

Imagine que eu sou o dono de um pequeno negócio e cheguei até você com esta conversa:

"Meu negócio vende coisas que exigem conversa. Meu cliente não chega sabendo o nome do produto. Ele chega com uma necessidade: quer um presente para alguém, quer resolver um problema, quer a recomendação de quem entende. O meu site tem filtros e categorias, e isso não funciona. O cliente não sabe traduzir o que ele quer em filtro, desiste e vai embora.

Eu quero um atendimento que converse de verdade. Que entenda o que o cliente precisa mesmo quando ele não sabe explicar direito, que recomende bem, e que conduza a venda até o final.

Mas eu tenho medos, e preciso que você me leve a sério neles. Tenho medo de o robô inventar coisas sobre os meus produtos. Tenho medo de alguém espertinho enganar o robô na conversa. Tenho medo de sair documento importante sem ninguém da minha equipe ter olhado antes. Tenho medo de a conta dessa inteligência artificial vir gigante no fim do mês. E tenho medo de dado dos meus clientes vazar em algum canto do sistema.

Ah, e se der problema, eu quero conseguir entender o que aconteceu. Não aceito um sistema que funciona 'por mágica'."

## O que eu quero no produto

Estes são os meus desejos, do jeito que eu sei falar. São amplos de propósito: o que cada um significa **no seu domínio**, e como cada um vira sistema, é você quem define.

- Quero um agente de IA capaz de compreender o meu catálogo e recomendar o melhor produto de acordo com o que o cliente busca, mesmo quando o cliente descreve por necessidade e não por nome
- Quero que estoque, preço e prazo que o agente informa estejam sempre de acordo com o meu banco de dados. Nada saindo da cabeça do robô
- Quero que a conversa leve a venda até o fim, e não pare no "posso te ajudar em mais alguma coisa?"
- Quero aprovar, eu ou alguém da minha equipe, aquilo que não tem volta depois de feito
- Quero conseguir olhar um atendimento depois e entender o que aconteceu ali dentro
- Quero saber quanto essa inteligência artificial me custa e ter controle sobre isso
- Quero que o dado do meu cliente esteja protegido em qualquer canto do sistema
- Quero que a minha equipe, e não só você, consiga colocar isso para rodar

**Duas restrições minhas:** nada de dinheiro de verdade (use os ambientes de teste dos meios de pagamento) e nada de documento com validade real (uma simulação fiel resolve).

> Cliente fala de resultado e de medo, nunca de framework. Se algum desses desejos parece vago demais para virar código, ótimo: **extrair requisito de cliente leigo é parte do desafio.** Pergunte nas Discussions e eu respondo como o cliente responderia.

---

# Parte 2 — O projeto de engenharia

O produto é metade do desafio. A outra metade é **como você constrói**, porque é isso que separa um script pessoal de um projeto que outra pessoa consegue entender, revisar e continuar.

O projeto nasce de documentação, não de código. Antes de implementar, queremos ver o seu pensamento registrado. Formato, ferramenta e nível de detalhe são seus: o que segue é o que cada peça precisa responder, não um modelo para preencher.

## 1. O seu case, com nome e sobrenome

Antes de qualquer documento, **invente o case inteiro.** Não é escolher um ramo genérico e escrever "o cliente" e "o produto" pelo resto do repositório: é criar um cenário que existe, com nomes próprios, e sustentar esses nomes em toda a documentação e no código.

Dê nome a tudo o que aparecer no seu projeto:

- **O negócio.** Fique livre para criar os nomes
- **O cliente que te contratou.** Quem é o dono, o que ele faz, por que ele está preocupado. É essa pessoa que vai aparecer nos seus ADRs quando você escrever "descartamos X porque a Dona Marta precisa aprovar antes"
- **O produto que você está construindo.** Um nome, um estilo de conversa, uma identidade. Você escolhe!
- **Quem é atendido.** É importante saber o público que usará seu produto. Deixe isso evidenciado.

Case genérico gera documento genérico e código genérico. Case com nome próprio força decisão concreta: quando o negócio é a Pet&Cia e ela vende ração por peso, você para de escrever requisito abstrato e começa a resolver problema de verdade. E é o que faz o seu repositório parecer um produto, e não um exercício.

> Você é livre inclusive no tom: o case pode ser sério, regional, engraçado. O que ele não pode ser é vago.

## 2. Escopo definido: PRD, SPECs e ADRs

| Documento | O que ele responde |
|---|---|
| **PRD** — documento de produto | Que problema estamos resolvendo, para quem, o que entra na primeira versão, **o que fica de fora** e como o sucesso será medido |
| **SPECs** — especificações | O que exatamente será implementado, com o comportamento esperado escrito sem ambiguidade, de forma que outra pessoa (ou um agente de código) consiga implementar sem adivinhar |
| **ADRs** — registro de decisões | As decisões de arquitetura que você tomou, cada uma com as alternativas consideradas e as consequências que você aceitou |

O ADR é o documento que mais vale no seu portfólio. Decisão sem alternativa descartada não é decisão, é acaso.

## 3. Arquitetura do projeto

Um desenho e um texto curto explicando como o sistema se sustenta: quantos agentes existem e por quê, o que cada um pode e não pode fazer, onde ficam os dados, onde entra o humano, o que acontece quando algo falha no meio do caminho.

Não existe arquitetura certa aqui. Existe arquitetura **explicada**.

## 4. Estrutura do repositório e o seu Agent Harness

Você vai construir este projeto com agentes de código, e queremos ver isso explícito. Escolha o seu harness — **Claude Code, Codex, Cursor, Kimi, Gemini CLI, Aider, o que for** — e deixe o repositório preparado para ele trabalhar bem:

- Qual harness você escolheu e por quê
- O arquivo de contexto do projeto (`CLAUDE.md`, `AGENTS.md`, ou o equivalente do seu): o que um agente precisa saber para não quebrar o seu projeto
- Como o repositório está organizado: onde vive a documentação, onde vive o código, onde vivem os testes
- O que você automatizou para o agente (comandos, skills, hooks, regras) e o que você deliberadamente **não** deixou na mão dele
- Como você revisa o que o agente escreve

Essa seção não é enfeite. Saber dirigir um agente de código, com contexto e limites bem definidos, é a habilidade que este desafio existe para treinar.

## 5. Processo visível

O histórico do repositório deve contar a história do projeto: branch principal protegida, mudanças entrando por pull request, commits que se entendem, validações automáticas que barram o que não deveria passar. Quais validações rodar é escolha sua — que elas existam e bloqueiem, não é.

---

## Antes de codar: as perguntas que valem mais que o código

Sente com um arquivo em branco e responda com honestidade. Estas respostas são o seu discovery, e viram o seu PRD:

- [ ] Qual é a jornada completa do cliente no meu domínio, da chegada ao pós-venda?
- [ ] Em cada etapa dessa jornada: linguagem natural gera **valor** ou gera **risco**?
- [ ] O que de pior pode acontecer se o modelo errar em cada etapa?
- [ ] O que, no meu fluxo, é **irreversível**, e quem deveria aprovar antes?
- [ ] Onde o meu cliente precisa de **garantia absoluta**, e não de resposta plausível?
- [ ] Como vou saber, **com números**, que o atendimento está bom?
- [ ] O que fica de fora da primeira versão? (Lembre: escopo é decisão de risco, não preguiça)

---

## Como participar

1. **Assista ao vídeo de abertura dos desafios** na plataforma da Jornada de Dados: o intuito desta série de projetos e as instruções gerais de como prosseguir
2. **Invente o seu case.** Negócio, cliente, produto e personas, tudo com nome próprio, do seu jeito
3. **Crie o seu repositório público.** Este repositório aqui é o enunciado; o trabalho acontece no seu
4. **Submeta o cartão do seu projeto à galeria** deste repositório, abrindo um pull request que adiciona a sua pasta com o cartão, seguindo o passo a passo do [COMO-SUBMETER.md](../COMO-SUBMETER.md) (esse PR já é a sua primeira prática do fluxo)
5. **Faça o discovery, documente, construa.** Nessa ordem
6. **Dúvidas sobre o pedido?** Pergunte na categoria [**Como construir**](https://github.com/suajornadadedados/desafio-jornada/discussions/new?category=como-construir) das Discussions. Eu respondo como o cliente responderia: sobre o negócio, as prioridades e os medos, nunca sobre qual tecnologia usar, porque o cliente não sabe o que é um banco de dados

## Datas e o que acontece com os projetos

| Data | O que acontece |
|---|---|
| 11/08/2026 | Desafio aberto, junto com o vídeo de abertura na plataforma |
| Ao longo do desafio | Perguntas respondidas nas Discussions; projetos na galeria podem ser comentados na live exclusiva para alunos |
| **05/09/2026** | Data de referência do desafio: submeta o seu cartão à galeria e avance o quanto conseguir |
| Semana seguinte | Projetos que mais se destacarem aparecem no vídeo de encerramento no canal e nas redes da Jornada, com os devidos créditos |
| Depois de 05/09 | O desafio continua aberto: galeria recebendo cartões e perguntas sendo respondidas nas Discussions. A data existe para dar ritmo; o método fica |

Projetos em diferentes estágios são bem-vindos. Um discovery bem feito, com PRD e ADRs sólidos, já é uma entrega valiosa mesmo com a implementação no começo. E lembre: o seu repositório fica público no seu perfil. Um projeto documentado, com decisões defendidas e processo visível, vale mais em um portfólio do que dez tutoriais seguidos.

---

Boa construção. E lembre da regra que costura tudo:

> **O modelo de linguagem decide o que dizer. O código decide o que pode ser feito.**
