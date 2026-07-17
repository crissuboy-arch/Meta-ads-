---
description: Publica campanha de pesquisa no Google Ads via navegador (paralelo ao /publicar do Meta)
argument-hint: "[produto] — precisa de pesquisa-[produto].md e campanha-[produto].md"
---

Publique a campanha de pesquisa no Google Ads seguindo a skill `google-ads-manager`. Mesma regra do `/publicar`: dinheiro real, confirmação explícita obrigatória antes de qualquer publicação (salvo se `meta-ads-config.json` tiver `"modoPublicacao": "automatico"` — ver seção abaixo).

## Passos

1. Leia `meta-ads-config.json`, `pesquisa-[produto].md` e `campanha-[produto].md`. Se a pesquisa de palavras-chave não existir, oriente a rodar `/pesquisar [produto]` primeiro — a campanha de pesquisa no Google depende diretamente das palavras-chave reais levantadas.
2. Monte o brief específico do Google Ads (grupos de anúncios por intenção, palavras-chave e correspondências, negativas, títulos/descrições no formato do Google) e mostre ao usuário.
3. **Confirmação**:
   - Se `modoPublicacao` for `"confirmar"` (padrão) ou não estiver definido: peça confirmação explícita antes de publicar cada nível (campanha, grupo, anúncio), igual ao `/publicar`.
   - Se `modoPublicacao` for `"automatico"`: peça confirmação **uma única vez**, no início, mostrando o resumo completo (orçamento total, todos os grupos e anúncios) — depois disso publique sem parar a cada nível, mas ainda assim mostre os prints ao final para auditoria.
4. Siga a skill `google-ads-manager` para criar campanha, grupos, palavras-chave e anúncios.
5. Verifique o status de cada anúncio após publicar.

## Saída

Liste campanha, grupos e anúncios publicados, status de cada um e o link direto para o Google Ads. Atualize `campanha-[produto].md` com a publicação no Google. Sugira aguardar dados antes de otimizar, mesma lógica do `/analisar`.
