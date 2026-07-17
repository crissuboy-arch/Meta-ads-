---
description: Audita a página de venda e dá uma nota de prontidão para conversão (não é previsão de vendas)
argument-hint: "[produto] [URL da página de venda]"
---

Audite a página de venda seguindo a skill `auditoria-pagina-venda` na íntegra.

## Passos

1. Peça (ou use `$ARGUMENTS`) a URL da página de venda do produto. Se `pesquisa-[produto].md` e/ou `criativos/[produto]/variacoes.md` já existirem, leia-os para checar coerência entre objeções do público, copy do anúncio e a página.
2. Abra a página via Claude in Chrome e avalie os 10 critérios da skill.
3. Salve `auditoria-[produto].md` com a nota, o detalhamento e a recomendação de verba inicial.

## Saída

Apresente ao usuário: a nota (0-10), os 2-3 pontos que mais pesam contra, e a recomendação de verba. **Reforce explicitamente que a nota mede prontidão da página segundo boas práticas — não é, e não pode ser, uma previsão de quantas vendas vai fazer.** Sugira o próximo passo: se a nota for baixa, corrigir a página antes de seguir; se estiver boa, `/campanha [produto]` (que vai puxar essa nota para sugerir o orçamento).
