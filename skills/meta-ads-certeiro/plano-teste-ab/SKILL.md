---
name: plano-teste-ab
description: Esta skill deve ser usada para criar um plano de testes A/B de criativo, copy, público, oferta, CTA e formato antes ou durante uma campanha Meta Ads. Acione quando o usuário disser "plano de teste", "o que testar primeiro", "teste A/B" ou rodar /teste-ab.
---

# Plano de teste A/B

## Princípio central

Testar **uma variável por vez** dentro de cada teste (não trocar copy E público E criativo ao mesmo tempo — se o resultado mudar, não dá pra saber o que causou). Cada rodada de teste isola 1 variável.

## Ordem recomendada de prioridade

Testar primeiro o que tem maior impacto potencial e é mais barato de descobrir:

1. **Oferta/ângulo de venda**: se a oferta não ressoa, nenhum ajuste de criativo salva a campanha — testar 2-3 ângulos diferentes (de `mercado-[produto].md`) primeiro, com o mesmo criativo básico.
2. **Hook/criativo**: dado que a oferta já validou algum ângulo, testar 2-4 hooks diferentes para esse ângulo (usar `hooks-criativos`).
3. **Formato**: o mesmo hook/ângulo em Feed vs. Reels vs. Carrossel — formatos diferentes de audiência consomem diferente.
4. **Público**: uma vez que criativo e formato estão validados, testar públicos frio vs. interesses diferentes.
5. **CTA**: ajuste fino, normalmente por último — costuma ter menor impacto que os anteriores.

## Montagem do teste

Para cada teste, definir:
- **Variável isolada** e as 2-3 variações dela.
- **O que mantém fixo** (todo o resto da campanha).
- **Métrica de decisão**: qual métrica decide o vencedor (CTR para hook/criativo, CPA/ROAS para oferta e público — nunca decidir só por CTR quando o objetivo é venda).
- **Verba e duração mínima**: recomendar rodar até ter volume suficiente de dado por variação (regra prática: pelo menos ~50 cliques ou ~3-4 dias, o que vier depois, antes de declarar vencedor — decisão com amostra pequena costuma estar errada).
- **Critério de corte**: a partir de quando pausar a variação perdedora (ex.: CPA 50% acima da melhor variação com volume mínimo atingido).

## Saída

Salvar `teste-ab-[produto].md` com a sequência de testes priorizada, o que cada um vai responder, e os critérios de decisão. Este plano alimenta a estrutura de conjuntos de anúncios do `/campanha` (cada variação testada vira um conjunto/anúncio separado) e a leitura de resultado do `/analise-resultados`.
