---
description: Diagnóstico completo — página, oferta, copy, criativos, público, CTA — com nota geral e prioridades de melhoria
argument-hint: "[produto] [URL da página, opcional] [métricas coladas, opcional]"
---

Rode o diagnóstico completo seguindo a skill `diagnostico-completo` na íntegra.

## Passos

1. Determine o produto. Verifique quais arquivos já existem na pasta conectada (`mercado-`, `auditoria-`, `oferta-`, `publico-`, `criativos/.../variacoes.md`).
2. Para o que faltar, rode agora a skill correspondente (avisando o usuário do que está sendo gerado), conforme a skill `diagnostico-completo` orienta.
3. Se o usuário colar métricas reais da campanha, aplique também a skill `leitura-metricas` e inclua no diagnóstico.
4. Calcule a nota geral ponderada e a lista de prioridades ordenadas.
5. Salve `diagnostico-[produto].md`.

## Exemplo de uso

```
/auditoria-completa clareamento dental a laser
https://minhapagina.com/clareamento
[opcional: cola aqui métricas da campanha atual]
```

## Saída

Apresente a nota geral, a nota de cada bloco (página/oferta, público, copy, métricas se houver), e a lista de prioridades ordenadas — cada uma apontando o comando do sistema que resolve. Deixe claro que a nota mede solidez do conjunto, não prevê resultado de venda.
