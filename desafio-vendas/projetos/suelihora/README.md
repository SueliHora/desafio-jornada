---
projeto: "Rash Rolamentos: Agente de Vendas Técnicas B2B"
autor: Sueli Hora
usuario: suelihora
dominio: Distribuidora de rolamentos e vedações industriais
repositorio: https://github.com/SueliHora/rash-rolamentos
linkedin: https://www.linkedin.com/posts/sueli-da-hora_jornadadedados-inteligenciaartificial-engenhariadedados-ugcPost-7496332845825548288-Thb_
plataforma: https://suajornadadedados.curseduca.pro/m/community/posts/suelihora-rash-rolamentos
---

# Rash Rolamentos — Agente de Vendas Técnicas de Ponta a Ponta

A **Rash Rolamentos Industriais** é uma distribuidora B2B focada em atendimento consultivo de peças mecânicas. O cliente chega descrevendo a aplicação mecânica ou medidas aproximadas, e o **RashBot** conduz o atendimento técnico até a cotação estruturada, sem nunca alucinar estoque ou preços.

## Arquitetura Planejada

* **Consulta Determinística:** Tabela de estoque e medidas consultada via banco de dados estruturado (Postgres/SQLite).
* **Human-in-the-Loop:** Trava de segurança obrigatória antes da emissão da proposta formal — o pedido fica retido para aprovação do Diretor Comercial.
* **Governança & LGPD:** Mascaramento de dados de contato e monitoramento de custos de LLM por sessão.