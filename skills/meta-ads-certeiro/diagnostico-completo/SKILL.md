---
name: diagnostico-completo
description: Esta skill deve ser usada para rodar um diagnóstico completo de uma campanha ou produto — página, oferta, copy, criativos, público e CTA — consolidando as demais skills numa nota geral e lista de prioridades. Acione quando o usuário disser "auditoria completa", "diagnóstico geral", "o que está travando minha campanha" ou rodar /auditoria-completa.
---

# Diagnóstico completo

Esta skill não substitui as skills específicas — ela **orquestra** o que já existir e preenche o que faltar, depois consolida tudo num relatório único com prioridades.

## Passos

1. Verificar quais arquivos já existem na pasta conectada para o produto: `mercado-[produto].md`, `auditoria-[produto].md`, `oferta-[produto].md`, `publico-[produto].md`, `criativos/[produto]/variacoes.md`.
2. Para o que **não existir**, rodar a skill correspondente agora (não pular etapa por preguiça, mas avisar o usuário do que está sendo gerado):
   - Falta página avaliada → rodar `auditoria-pagina-venda`.
   - Falta oferta avaliada → rodar `avaliacao-oferta`.
   - Falta público definido → rodar `definicao-publico`.
   - Falta copy/criativo → não gerar do zero aqui; avisar que copy ainda não existe e sugerir `/criativo` separadamente (diagnóstico avalia o que existe, não cria copy nova por conta própria).
3. Se o usuário colar métricas reais da campanha já rodando, aplicar também a skill `leitura-metricas` e incluir no diagnóstico.

## Nota geral

Calcular uma nota geral (0-100) como média ponderada das notas parciais disponíveis:
- Página/oferta: 40% (nota da auditoria + nota da oferta, média das duas)
- Público: 20% (qualitativo: bem definido = 20, parcial = 10, ausente = 0)
- Copy/criativo: 20% (usar resultado do checklist `score-criativo` se existir; se não existir copy ainda, não pontuar essa fatia e recalcular o peso proporcionalmente entre as demais)
- Métricas reais da campanha (se houver): 20% — CPA/ROAS dentro do esperado informado pelo usuário

Deixar claro: nota geral mede a **solidez do conjunto**, não prevê resultado de venda.

## Saída

Salvar `diagnostico-[produto].md` com: nota geral, nota de cada bloco, e uma lista de **prioridades ordenadas** (o que corrigir primeiro tem maior impacto e é mais barato de resolver — normalmente oferta/página antes de criativo, criativo antes de público, público antes de CTA). Para cada prioridade, indicar o comando do sistema que resolve (`/oferta`, `/auditoria`, `/criativo`, `/hooks`, `/publico`, `/teste-ab`).
