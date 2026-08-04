# Como Submeter o Seu Projeto

Você construiu (ou está construindo) o seu projeto do desafio? Então esta página é para você. Ao submeter, o seu projeto entra na galeria oficial do mês, você se torna um contribuidor deste repositório da Jornada de Dados e o seu trabalho fica visível para toda a comunidade.

## Como funciona

O seu projeto completo vive no **seu** repositório, no seu perfil do GitHub. É lá que está o código, a documentação e todo o histórico do seu trabalho. Isso é proposital: o portfólio é seu e fica com você.

O que você submete aqui é o **cartão do seu projeto**: uma pasta com o seu nome de usuário contendo um README de apresentação, seguindo o modelo abaixo. Esse cartão entra na galeria do mês e aponta para o seu repositório completo.

| O que fica no SEU repositório | O que entra AQUI (galeria) |
|---|---|
| Código completo do projeto | Uma pasta com o seu nome de usuário |
| Toda a documentação (jornada, riscos, PRD, decisões, specs) | Um README de apresentação (o cartão) |
| Histórico de commits, PRs e evolução | Link para o seu repositório completo |
| CI, validações e proteções que você configurou | Um diagrama ou imagem do seu projeto (opcional, mas recomendado) |

## Passo a passo da submissão

Siga na ordem. O processo inteiro leva uns 20 minutos e é, ele mesmo, uma prática do fluxo de trabalho que o desafio ensina.

1. **Faça um fork deste repositório** para a sua conta, usando o botão Fork no topo da página

2. **Crie uma branch no seu fork** com o padrão `projeto/mes/seu-usuario`. Exemplo: `projeto/2026-08/caiomachado`

3. **Crie a sua pasta** dentro da pasta de projetos do mês correspondente. Exemplo: dentro de `desafio-vendas/projetos/`, crie a pasta `caiomachado`

4. **Crie o README do seu cartão** dentro da sua pasta, copiando o modelo da seção abaixo e preenchendo com as informações do seu projeto

5. **Adicione uma imagem** na sua pasta, se quiser: um diagrama da arquitetura ou um print do produto funcionando deixa o seu cartão muito mais atraente na galeria

6. **Faça o commit** seguindo um padrão consistente. Exemplo: `docs: adiciona projeto de caiomachado ao desafio 2026-08`

7. **Abra o pull request** do seu fork para este repositório, com um título claro e uma breve descrição do seu projeto no corpo

8. **Aguarde a revisão.** Vamos conferir se o cartão segue o modelo e se os links funcionam. Se algo precisar de ajuste, comentamos no próprio PR, como em qualquer revisão de código do mundo real

9. **Merge feito, você está na galeria.** Seu nome entra na lista de contribuidores do repositório da Jornada de Dados e seu projeto fica visível para toda a comunidade

## Checklist antes de abrir o PR

- [ ] Meu repositório de projeto é público e o link está correto no cartão
- [ ] Meu repositório tem README próprio com instruções de como rodar o projeto
- [ ] O cartão segue o modelo abaixo, com todas as seções preenchidas
- [ ] A pasta tem o meu nome de usuário do GitHub, em letras minúsculas
- [ ] A pasta está dentro do mês correto
- [ ] Não incluí código do projeto aqui, apenas o cartão e a imagem
- [ ] Não incluí nenhum dado real ou informação sensível

## Modelo do cartão

Copie o conteúdo abaixo para o README da sua pasta e preencha cada seção.

```markdown
# Nome do Projeto

**Autor:** seu nome (@seu-usuario)
**Domínio:** o negócio que você escolheu
**Repositório completo:** link para o seu repositório
**Status:** Discovery / Em construção / Funcionando / Em produção

## O projeto em três linhas

Descreva o que o seu agente faz, para quem, e qual problema resolve.

## Arquitetura

Uma imagem ou diagrama, e um parágrafo explicando como o sistema funciona:
quantos agentes, o que cada um pode fazer, onde o humano entra.

## Stack escolhida

Liste as principais tecnologias e uma frase sobre o porquê de cada escolha.

## As três decisões mais difíceis

Conte as três decisões de engenharia mais difíceis que você tomou,
o que considerou como alternativa e por que decidiu assim.

## Como atendi às garantias

| Garantia | Como resolvi |
|---|---|
| G1 Nenhum fato inventado | |
| G3 Nenhuma ação sem permissão | |
| G4 Nada irreversível sem humano | |
| G7 Tudo rastreável | |
| G8 Qualidade que se prova | |

Preencha as garantias que já atendeu; as demais podem entrar conforme o projeto evolui.

## O que eu aprendi

Um parágrafo honesto: o que foi mais difícil, o que faria diferente,
o que este projeto mudou na sua forma de trabalhar.
```

## Regras da galeria

- Um cartão por pessoa por mês. Você pode participar de todos os meses, e quem participa de vários entra no Hall dos Construtores no README principal
- Projetos em qualquer estágio são bem-vindos. Um discovery bem documentado já é uma submissão válida; atualize o cartão via novo PR conforme o projeto evolui
- O cartão deve ser do seu próprio projeto, em domínio diferente do exemplo trabalhado no workshop do mês
- Seja generoso na seção de aprendizados. É a parte que a comunidade mais lê

## Depois do merge

Projetos na galeria podem ser comentados na live exclusiva para alunos, e os que mais se destacarem aparecem no vídeo de encerramento do mês no canal da Jornada de Dados e nas nossas redes, sempre com os devidos créditos. Compartilhe o seu cartão no LinkedIn marcando a Jornada: a gente adora repostar projeto de aluno.

Dúvidas sobre a submissão? Abra uma issue neste repositório. Dúvidas sobre o desafio em si? Use o modelo de issue "Pergunta ao cliente" e leia o README do mês correspondente.