---
description: Cria plano de testes A/B de criativo, copy, público, oferta, CTA e formato
argument-hint: "[produto]"
---

Monte o plano de teste seguindo a skill `plano-teste-ab` na íntegra.

## Passos

1. Determine o produto e verifique o que já existe: `mercado-[produto].md`, `oferta-[produto].md`, `publico-[produto].md`, `criativos/[produto]/`. Quanto mais existir, mais concreto o plano — mas o comando funciona mesmo com pouco material, priorizando o que testar primeiro dentro do que já foi levantado.
2. Monte a sequência priorizada de testes (oferta → hook/criativo → formato → público → CTA), cada um isolando uma variável, com métrica de decisão, verba/duração mínima e critério de corte.
3. Salve `teste-ab-[produto].md`.

## Exemplo de uso

```
/teste-ab clareamento dental a laser
```

## Saída

Apresente a sequência de testes com o que cada um vai responder e os critérios de decisão. Sugira o próximo passo: `/campanha [produto]` para transformar a primeira rodada de teste em conjuntos de anúncios reais.
