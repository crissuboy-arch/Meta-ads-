---
description: Monta a estrutura da campanha (objetivo, orçamento, segmentação, posicionamentos)
argument-hint: "[produto] — precisa de criativos aprovados em criativos/[produto]/"
---

Monte o brief da campanha usando os dados de `meta-ads-config.json`, `pesquisa-[produto].md` e `criativos/[produto]/variacoes.md`.

## Passos

1. Confirme que há pelo menos 1 criativo aprovado no checklist. Se não houver, oriente a rodar `/criativo [produto]` primeiro.
2. Se existir `auditoria-[produto].md`, leia a nota e a recomendação de verba dela — é o ponto de partida para o orçamento sugerido abaixo. Se não existir, sugira rodar `/auditoria [produto]` antes (não é bloqueante, mas evita gastar em tráfego pago pra uma página de venda fraca).
3. Defina, confirmando cada item com o usuário (nunca travar nos padrões sem perguntar):
   - **Objetivo da campanha** (tráfego, conversão, geração de cadastro, mensagens) — padrão do config, mas o produto pode pedir outro.
   - **Orçamento diário**: parta da verba padrão do config, ajustada pela nota da auditoria (nota ≥8 → verba cheia; 5-7,9 → metade; <5 → sugerir corrigir a página antes). Se o usuário informar que não tem a verba padrão disponível, recalcule a estrutura (menos públicos/menos anúncios em teste) para caber no valor real que ele tem, em vez de simplesmente reduzir tudo proporcionalmente a ponto de não gerar dado nenhum — informe o mínimo diário abaixo do qual não vale a pena testar (regra prática: pelo menos o valor de 3-5 cliques estimados do nicho por dia).
   - Duração do teste inicial (sugira no mínimo 3-4 dias antes de qualquer decisão de otimização — verba menor que isso não gera dado suficiente).
   - **Público**: localização e faixa etária do config + os interesses sugeridos em `pesquisa-[produto].md`. Monte 1-2 conjuntos de público para teste (ex.: "interesses amplos" vs "interesses específicos") em vez de um público só, quando a verba permitir.
   - **Posicionamentos**: recomende posicionamento automático (Advantage+) salvo se o usuário tiver motivo específico para restringir (ex.: só Stories, só Reels).
   - **Estrutura**: 1 campanha → 1-2 conjuntos de anúncios (públicos de teste) → os criativos aprovados dentro de cada conjunto.
3. Salve `campanha-[produto].md` com toda a estrutura definida, pronta para ser lida pelo `/publicar`.

## Saída

Apresente o brief completo ao usuário para revisão antes de publicar. Deixe explícito que o brief só vira campanha de fato quando o usuário confirmar (o `/publicar` não roda sozinho). Sugira o próximo passo: `/publicar [produto]`.
