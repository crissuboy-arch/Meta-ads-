---
description: Monta avatar, interesses, comportamentos e segmentação em público frio, morno e quente
argument-hint: "[produto]"
---

Monte a definição de público seguindo a skill `definicao-publico` na íntegra.

## Passos

1. Determine o produto. Leia `mercado-[produto].md` se existir; se não, pergunte ao usuário quem é o cliente ideal antes de seguir.
2. Monte o avatar, a lista de interesses por grupo temático, e a segmentação frio/morno/quente com recomendação de público personalizado para cada temperatura.
3. Salve `publico-[produto].md`.

## Exemplo de uso

```
/publico clareamento dental a laser
```

## Saída

Apresente o avatar, os grupos de interesses (marcando quando um nome de interesse precisa ser verificado no seletor da Meta) e a segmentação por temperatura. Sugira o próximo passo: `/campanha [produto]`, que vai usar essa definição para montar os conjuntos de anúncios.
