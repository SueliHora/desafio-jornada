# Desafio Jornada de Dados — Construa um Agente de Vendas de Ponta a Ponta

## O que é este desafio

Este repositório é um convite para você construir um produto de verdade com IA. Não um chatbot de demonstração, mas um sistema completo de atendimento e vendas, do primeiro "oi" do cliente até o documento final emitido, passando por recomendação, pagamento e aprovação humana.

Aqui você não vai encontrar código pronto nem respostas. Vai encontrar um pedido de cliente, um conjunto de garantias que o produto precisa oferecer e requisitos de processo de engenharia. Todas as decisões são suas: arquitetura, stack, escopo e organização do seu harness. É assim que funciona no mundo real: o cliente sabe o que quer, mas não sabe como se constrói. Quem decide como construir é você.

> **Regra nº 1 do desafio: o seu projeto não pode ser a Vendinha.**
> A Vendinha é o exemplo trabalhado no workshop, e as decisões dela estão no vídeo. Escolha o **seu** domínio: petshop, clínica, imobiliária, oficina, loja de instrumentos, consultoria... Qualquer negócio em que o cliente chega conversando sem saber o que pedir, e em que existe pelo menos uma etapa em que errar é inaceitável.

---

## O pedido do cliente

Imagine que eu sou o dono de um pequeno negócio e cheguei até você com a seguinte conversa:

"Meu negócio vende coisas que exigem conversa. Meu cliente não chega sabendo o nome do produto. Ele chega com uma necessidade: quer um presente para alguém, quer resolver um problema, quer uma recomendação de quem entende. O meu site atual tem filtros e categorias, e isso não funciona. O cliente não sabe traduzir o que ele quer em filtros, desiste e vai embora.

Eu quero um atendimento que converse de verdade. Que entenda o que o cliente precisa mesmo quando ele não sabe explicar direito, que recomende bem, que conduza a venda até o final: pedido feito, pagamento realizado, documento emitido, cliente satisfeito.

Mas eu tenho medos, e preciso que você me leve a sério neles. Tenho medo de o robô inventar coisas sobre os meus produtos. Tenho medo de alguém espertinho enganar o robô na conversa. Tenho medo de sair documento importante sem ninguém da minha equipe ter olhado antes, porque documento emitido não tem volta. Tenho medo de a conta dessa inteligência artificial vir gigante no fim do mês. E tenho medo de dado pessoal dos meus clientes vazar em algum canto do sistema.

Ah, e se der problema, eu quero conseguir entender o que aconteceu. Não aceito um sistema que funciona 'por mágica'."

Cliente fala de resultado e de medo, nunca de framework. Transformar essa conversa em requisitos, arquitetura e código é o seu trabalho. A tabela abaixo ajuda a começar:

| Medo do cliente | Sua tarefa como engenheiro |
|---|---|
| "O robô pode inventar coisas sobre meus produtos" | Garantir que toda afirmação do agente tenha origem em dados verificáveis do sistema |
| "Alguém pode enganar o robô na conversa" | Garantir que manipulação por conversa não execute nada fora do permitido, por arquitetura e não por pedido no prompt |
| "Pode sair documento sem ninguém revisar" | Identificar o que é irreversível no seu domínio e desenhar onde e como um humano aprova, com registro |
| "A conta da IA pode vir gigante" | Definir teto de custo por atendimento, configurável |
| "Dado de cliente pode vazar" | Garantir que dados pessoais nunca apareçam legíveis em logs e rastros |
| "Não aceito sistema que funciona por mágica" | Garantir rastreabilidade completa de cada atendimento |

---

## As garantias que o produto precisa oferecer

Independente do domínio e das ferramentas escolhidas, o produto final precisa oferecer as garantias abaixo. **Como** garantir cada uma é decisão sua. O que não é negociável é que elas existam e que você consiga demonstrá-las.

| # | Garantia | O que precisa ser verdade no seu produto |
|---|---|---|
| G1 | Nenhum fato inventado | Toda afirmação sobre produtos ou serviços tem origem em dado verificável do sistema |
| G2 | Preço nunca vem do modelo | Valores, totais e cálculos financeiros nunca são gerados pelo modelo de linguagem |
| G3 | Nenhuma ação sem permissão | O agente só executa o que foi explicitamente permitido; segurança garantida pela construção, não pelo comportamento do modelo |
| G4 | Nada irreversível sem humano | Ações sem volta passam por aprovação humana registrada (quem e quando) |
| G5 | Dados pessoais protegidos | Nome, CPF, e-mail e afins nunca legíveis em logs ou rastros de execução |
| G6 | Custo sob controle | Teto de custo por atendimento, configurado e respeitado |
| G7 | Tudo rastreável | Qualquer atendimento pode ser reconstruído: o que o agente decidiu, consultou, executou e gastou |
| G8 | Qualidade que se prova | Critérios objetivos de qualidade definidos antes de implementar, versionados no repositório e verificados automaticamente; a qualidade não regride silenciosamente |
| G9 | Qualquer pessoa roda | O projeto sobe na máquina de outra pessoa em poucos minutos, seguindo o seu próprio repositório, sem dados reais |

**Restrições do cliente:**
- Nada de dinheiro de verdade. Use ambientes de teste dos meios de pagamento
- Nada de documento com validade real. Uma simulação fiel resolve

---

## Requisitos de processo

Este desafio não é só sobre o produto final. É sobre como você trabalha. Os itens abaixo são requisitos do projeto. Não daremos os detalhes de implementação: pesquisar, decidir e configurar faz parte do desafio.

### O que o seu repositório deve ter

- [ ] Branch principal protegida: nenhuma mudança entra sem pull request
- [ ] Validações automáticas que bloqueiam o que não estiver de acordo (quais validações rodar, como testes, análise de código e verificação de qualidade do agente, é escolha sua, mas elas precisam existir e barrar)
- [ ] Padrão de commits consistente, que permita entender o histórico do projeto
- [ ] Pull requests que contam uma história: o que foi feito, por quê, e com evidência de que funciona
- [ ] Processo visível: qualquer pessoa que abra o repositório entende como o projeto foi construído

### Documentação exigida antes do código

O projeto nasce de documentação, não de código. Antes de implementar, o repositório deve conter:

| Documento | O que deve responder |
|---|---|
| Mapeamento da jornada | Quais são as etapas da jornada do seu cliente, e em cada uma: a IA entra ou não entra? Por quê? |
| Levantamento de riscos | Quais riscos existem no seu domínio e como cada um será tratado |
| Documento de produto | O que será construído, o que fica de fora, e como o sucesso será medido |
| Registro de decisões | As decisões de arquitetura tomadas, com as alternativas consideradas e as consequências aceitas |
| Especificações | O que será implementado, com cenários de comportamento esperado escritos sem ambiguidade, de forma que qualquer pessoa, ou qualquer agente de código, entenda |

Como organizar esses documentos, quais formatos e ferramentas usar, e como estruturar o seu ambiente de trabalho com agentes de código: tudo é decisão sua. O que pedimos é que as decisões estejam registradas.

---

## Discovery: o que você precisa responder antes de codar

Sente com um arquivo em branco e responda com honestidade. Estas perguntas são o coração do método. As respostas da Vendinha estão no workshop; as do seu domínio, só você pode dar.

- [ ] Qual é a jornada completa do cliente no meu domínio, da chegada ao pós-venda?
- [ ] Em cada etapa dessa jornada: linguagem natural gera **valor** ou gera **risco**?
- [ ] O que de pior pode acontecer se o modelo errar em cada etapa?
- [ ] O que, no meu fluxo, é **irreversível**, e quem deveria aprovar antes?
- [ ] Onde o meu cliente precisa de **garantia absoluta**, e não de resposta plausível?
- [ ] Como vou saber, **com números**, que o atendimento está bom, antes de implementar?
- [ ] O que fica de fora da primeira versão? (Lembre: escopo é decisão de risco, não preguiça)

## O que você vai precisar pesquisar e decidir

| Decisão | Perguntas para se fazer |
|---|---|
| Domínio e escopo | Que negócio? Que jornada? O que entra na primeira versão? |
| Stack | Que linguagem, frameworks, banco de dados, modelo de linguagem? Por quê? |
| Arquitetura do agente | Um agente ou vários? Que ferramentas cada um pode usar? Como limitar permissões? |
| Ponto de aprovação humana | O que é irreversível? Como pausar o fluxo, guardar o estado e retomar após aprovação? |
| Observabilidade | Como rastrear cada atendimento? Como proteger dados pessoais nos rastros? |
| Qualidade e testes | Como medir a qualidade das conversas? Como impedir regressão a cada mudança? |
| Proteção do repositório | Que validações rodar? Como configurar para bloquear o que não passa? |
| Harness de desenvolvimento | Como organizar seu trabalho com agentes de código? O que documentar para eles trabalharem bem? |

Cada uma dessas decisões merece registro no seu repositório, com as alternativas que você considerou.

---

## Como participar

1. **Assista ao workshop completo da Vendinha** para ver o método aplicado de ponta a ponta
2. **Escolha o seu domínio** (diferente da Vendinha)
3. **Crie o seu repositório público.** Este repositório aqui é o enunciado; o trabalho acontece no seu
4. **Registre o seu projeto no mural** deste repositório, abrindo um pull request que adiciona uma linha à tabela do mural com seu nome, o domínio escolhido e o link do seu projeto (esse PR já é sua primeira prática do fluxo)
5. **Faça o discovery, documente, construa.** Nessa ordem
6. **Dúvidas sobre o pedido?** Abra uma issue com o modelo "Pergunta ao cliente". Eu respondo como o cliente responderia: sobre o negócio, as prioridades e os medos, nunca sobre qual tecnologia usar, porque o cliente não sabe o que é um banco de dados. Extrair requisitos de um cliente leigo é parte do desafio.

## Datas e o que acontece com os projetos

| Data | O que acontece |
|---|---|
| 11/08/2026 | Desafio aberto, junto com o lançamento do workshop |
| Ao longo do mês | Perguntas ao cliente respondidas; projetos registrados no mural podem ser comentados na live exclusiva para alunos |
| **28/08/2026** | Data de referência do desafio: registre seu projeto no mural e avance o quanto conseguir |
| Semana final de agosto | Projetos que mais se destacarem aparecem no vídeo de encerramento no canal e nas redes da Jornada, com os devidos créditos |
| Depois de 28/08 | O desafio continua aberto: mural recebendo projetos e perguntas sendo respondidas. A data existe para dar ritmo; o método fica |

Projetos em diferentes estágios são bem-vindos. Um discovery bem feito com uma especificação sólida já é uma entrega valiosa, mesmo que a implementação esteja no começo. E lembre: o seu repositório fica público no seu perfil. Um projeto completo, documentado e com processo visível vale mais em um portfólio do que dez tutoriais seguidos.

---

Boa construção. E lembre da regra que costura tudo:

> **O modelo de linguagem decide o que dizer. O código decide o que pode ser feito.**