---
name: leitura-metricas
description: Esta skill deve ser usada para interpretar métricas de campanha Meta Ads coladas manualmente pelo usuário (CPM, CPC, CTR, CPA, ROAS, frequência, impressões, alcance, conversões) e sugerir próximo passo. Não busca dados automaticamente — trabalha só com o que o usuário colar. Acione quando o usuário disser "analisar meus resultados", "essas métricas estão boas", "o que fazer com esses números" ou rodar /analise-resultados.
---

# Leitura de métricas coladas manualmente

Esta skill nunca acessa o Gerenciador de Anúncios diretamente para puxar dado — trabalha só com o que o usuário colar no chat (print, tabela, texto). Se faltar uma métrica importante para a leitura, pedir especificamente, não estimar ou inventar o valor.

## O que cada métrica indica (isoladamente é limitado — ler em conjunto)

- **CPM** (custo por mil impressões): reflete competição pelo público e qualidade do criativo/relevância. CPM subindo ao longo dos dias com público igual costuma indicar fadiga de criativo.
- **CTR** (taxa de cliques): reflete a força do hook/criativo e a relevância do público. CTR baixo com CPM normal → problema é o criativo, não o público.
- **CPC** (custo por clique): combinação de CPM e CTR — não ler isolado, ver os dois primeiro.
- **Frequência**: quantas vezes a mesma pessoa viu o anúncio. Acima de ~3-4 num público pequeno costuma sinalizar fadiga — CTR cai e CPM sobe junto.
- **CPA** (custo por resultado/aquisição): a métrica que mais importa para decisão de negócio — comparar contra o quanto o usuário pode pagar por resultado (se ele informar isso) antes de dizer se está "bom" ou "ruim".
- **ROAS** (retorno sobre investimento em anúncio): só decidir escalar ou pausar com base nisso quando o usuário informar a margem/lucro do produto — ROAS "positivo" pode ainda dar prejuízo se a margem for baixa.
- **Alcance vs. Impressões**: impressões muito maiores que alcance com público pequeno reforça o diagnóstico de frequência/fadiga.
- **Taxa de conversão da página** (conversões ÷ cliques, se o usuário informar): separa problema de anúncio (tráfego não qualificado) de problema de página/oferta (tráfego bom, mas não converte).

## Diagnóstico combinado (padrões comuns)

- CTR bom + CPA alto → tráfego está clicando mas não convertendo: revisar página/oferta (`/auditoria` ou `/oferta`), não o criativo.
- CTR baixo + CPM normal → criativo/hook fraco: revisar com `hooks-criativos` e testar novo ângulo.
- CPM subindo + frequência alta → fadiga de criativo: trocar criativo ou ampliar público.
- Poucos dados (baixo volume de cliques/resultados) → não tirar conclusão ainda, is amostra pequena engana; informar isso ao usuário em vez de recomendar mudança precipitada.

## Saída

Apresentar: leitura de cada métrica relevante, o diagnóstico combinado mais provável, e 1-2 próximos passos concretos (qual comando do sistema usar — `/hooks`, `/oferta`, `/auditoria-completa`, `/teste-ab` — conforme o diagnóstico). Nunca prometer resultado futuro ("vai melhorar X%") — só indicar a causa mais provável e a ação recomendada.
