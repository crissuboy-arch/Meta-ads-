---
description: Pesquisa no Google o que as pessoas buscam sobre o produto/nicho e organiza por intenção
argument-hint: "[produto ou nicho] [praça] — opcional, usa os padrões do config"
---

Pesquise intenção de busca real seguindo a skill `pesquisa-palavras-chave`.

## Preparação

1. Leia `meta-ads-config.json` na pasta conectada. Se não existir, oriente a rodar `/setup` primeiro.
2. Determine produto/nicho e praça: use `$ARGUMENTS` se informado; senão, pergunte ao usuário (nunca trave nos padrões do config, confirme antes de seguir).

## Execução

Siga a skill `pesquisa-palavras-chave` na íntegra para levantar:

- Termos de busca reais relacionados ao produto/nicho (autocomplete do Google, "as pessoas também perguntam", termos relacionados no rodapé de resultados)
- Classificação por intenção: **informacional** (dúvida, ainda não decidiu comprar), **comercial** (comparando opções) e **transacional** (pronto para comprar/agendar)
- Dores e objeções que aparecem nas perguntas reais (ex.: "vale a pena", "é seguro", "quanto custa", "funciona mesmo")
- 2-3 concorrentes ou termos de marca que aparecem nos resultados, só para referência de posicionamento

## Saída

Salve `pesquisa-[produto].md` na pasta conectada com:

1. Tabela de palavras-chave por intenção (informacional / comercial / transacional)
2. Lista de dores e objeções reais encontradas (viram matéria-prima da copy)
3. 5-8 interesses do Meta Ads sugeridos a partir dos termos (nomes de categorias que existem no seletor de público do Gerenciador — ex.: se a busca revela interesse em "pilates para iniciantes", sugerir o interesse "Pilates")
4. Resumo de 3 linhas: o que o público mais quer saber antes de comprar

Apresente o resumo ao usuário e sugira o próximo passo: `/criativo [produto]`.
