---
description: Publica a campanha no Gerenciador de Anúncios da Meta via navegador
argument-hint: "[produto] — precisa de campanha-[produto].md já confirmado"
---

Publique a campanha seguindo a skill `meta-ads-manager`. Esta ação gasta dinheiro real do usuário — confirmação explícita é obrigatória antes de qualquer clique em "Publicar".

## Passos

1. Leia `campanha-[produto].md` e o campo `modoPublicacao` de `meta-ads-config.json` (padrão: `confirmar` se o campo não existir).
2. Mostre o resumo final ao usuário: objetivo, orçamento diário total, duração, públicos, criativos que vão ao ar.
   - **Modo `confirmar`** (padrão): peça confirmação explícita ("pode publicar?") antes de prosseguir, e de novo antes do clique final de cada nível (campanha/conjunto/anúncio) — nunca publique automaticamente.
   - **Modo `automatico`**: peça confirmação **uma única vez**, aqui, mostrando o resumo completo de tudo que vai ser criado e o gasto diário total. Após esse "sim", publique campanha, conjuntos e anúncios sem parar a cada nível — mas ainda assim gere e guarde print de cada nível publicado para o usuário auditar depois.
3. Siga a skill `meta-ads-manager`: abra o Gerenciador de Anúncios via Claude in Chrome (o usuário já deve estar logado; se não estiver, peça para ele logar — nunca digitar credenciais da Meta em nome do usuário), crie a campanha, os conjuntos de anúncios e os anúncios exatamente conforme o brief.
4. No modo `confirmar`, antes do clique final de publicação de cada nível, mostre uma captura de tela do que será enviado para o usuário confirmar que bate com o brief.
5. Após publicar, verifique o status de cada anúncio (em revisão / aprovado / rejeitado). Se algum for rejeitado, leia o motivo dado pela Meta e ajuste o texto/criativo seguindo a política, depois reenvie — reenvio de anúncio rejeitado sempre passa por confirmação, mesmo em modo automático.

## Saída

Liste os IDs/nomes da campanha, conjuntos e anúncios publicados, o status de cada um e o link direto para o Gerenciador de Anúncios. Atualize `campanha-[produto].md` com a data de publicação e o status. Sugira: aguardar pelo menos o período de teste definido no brief antes de rodar `/analisar [produto]` — otimizar campanha com poucas horas de dados é contraproducente.
