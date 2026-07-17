---
description: Escreve variações de anúncio a partir da pesquisa e roda o checklist de qualidade
argument-hint: "[produto] — precisa de pesquisa-[produto].md já existente"
---

Escreva os criativos seguindo a skill `copywriting-anuncios`, depois avalie cada um com a skill `score-criativo`. Ambas obrigatórias, nesta ordem.

## Passos

1. Leia `meta-ads-config.json` e `pesquisa-[produto].md`. Se a pesquisa não existir, oriente a rodar `/pesquisar [produto]` primeiro — não invente palavras-chave.
2. Escreva **3 variações** de anúncio seguindo a skill `copywriting-anuncios`, cada uma testando um ângulo diferente (ex.: dor principal / benefício direto / prova social), sempre ancoradas nas dores e termos reais da pesquisa.
3. Para cada variação, gere: texto principal, título, descrição, CTA (botão), e uma sugestão objetiva de visual/vídeo (não gerar a imagem — descrever o que ela deve mostrar).
4. Rode o checklist da skill `score-criativo` em cada variação. Variação que não passa em algum item obrigatório do checklist é marcada como "ajustar" com o motivo específico — não é descartada, é corrigida e reavaliada antes de seguir.
5. Salve tudo em `criativos/[produto]/variacoes.md`: as 3 variações, o resultado do checklist de cada uma, e qual(is) está(ão) aprovada(s) para ir à campanha.

## Saída

Apresente as 3 variações e o resultado do checklist ao usuário. Deixe claro: o checklist reduz risco de reprovação e reforça boas práticas — não é previsão de performance, isso só o mercado responde depois de rodar. Sugira o próximo passo: `/campanha [produto]`.
