---
name: definicao-publico
description: Esta skill deve ser usada para montar avatar de cliente, interesses, comportamentos e a segmentação em público frio, morno e quente para campanhas Meta Ads. Acione quando o usuário disser "montar meu avatar", "definir público", "quem é meu cliente ideal" ou rodar /publico.
---

# Definição de público e avatar

## Avatar

Montar um perfil concreto (não "mulheres 25-45 interessadas em beleza" — genérico demais pra guiar copy ou segmentação). Incluir: idade aproximada, contexto de vida relevante ao produto, o que ela busca resolver agora, o que já tentou antes, onde ela passa tempo online. Se `mercado-[produto].md` existir, usar as dores/desejos já levantados em vez de reinventar.

## Interesses e comportamentos (para o seletor de público do Gerenciador de Anúncios)

Sugerir 8-12 interesses reais plausíveis no seletor da Meta — marcas, publicações, atividades, páginas do nicho — e sinalizar quando não houver certeza do nome exato ("verificar no seletor ao montar a campanha", nunca inventar nome de interesse). Separar em 2-3 grupos temáticos (ex.: interesses de concorrentes, interesses de estilo de vida relacionado, interesses de comportamento de compra) para facilitar testes A/B de público depois.

## Temperatura de público

- **Frio**: nunca teve contato com a marca. Segmentação por interesses/comportamentos/dados demográficos. Criativo deve educar e gerar primeiro interesse — hooks de dor/identificação funcionam bem aqui.
- **Morno**: já teve algum contato (seguiu perfil, visitou site, engajou com conteúdo) mas não comprou. Ideal para retargeting via públicos personalizados (visitantes do site, engajamento no Instagram/Facebook) — criativo pode assumir que a pessoa já conhece o produto e focar em quebra de objeção/prova social.
- **Quente**: já demonstrou intenção forte (carrinho abandonado, iniciou checkout, lista de contatos/clientes antigos). Criativo pode ser mais direto: oferta, urgência real (nunca fabricada), prova social específica.

## Saída

Salvar `publico-[produto].md` com: avatar descrito, lista de interesses por grupo temático, e a segmentação frio/morno/quente com a recomendação de que tipo de público personalizado usar em cada temperatura (o `meta-ads-manager` usa isso ao montar os conjuntos de anúncios no `/campanha` e `/publicar`).
