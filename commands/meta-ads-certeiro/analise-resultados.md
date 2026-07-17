---
description: Interpreta métricas coladas manualmente (CPM, CPC, CTR, CPA, ROAS, frequência, impressões, alcance, conversões) e sugere próximo passo
argument-hint: "[produto] — cole as métricas (print, tabela ou texto)"
---

Interprete as métricas seguindo a skill `leitura-metricas` na íntegra. Esta skill nunca puxa dado automaticamente do Gerenciador de Anúncios — trabalha só com o que o usuário colar aqui.

## Passos

1. Reúna as métricas que o usuário colou. Se faltar alguma métrica relevante para o diagnóstico (ex.: CPA sem saber o quanto ele pode pagar por resultado), pergunte especificamente — não estimar.
2. Aplique a leitura combinada da skill (CTR x CPM x frequência x CPA x ROAS) para chegar no diagnóstico mais provável.
3. Indique 1-2 próximos passos concretos, apontando o comando do sistema que resolve cada um.

## Exemplo de uso

```
/analise-resultados clareamento dental a laser
CPM: R$ 45 | CTR: 0,8% | CPC: R$ 5,60 | CPA: R$ 90 | Frequência: 4,2 | Alcance: 12.000 | Impressões: 50.400 | Conversões: 8
```

## Saída

Apresente a leitura de cada métrica relevante, o diagnóstico combinado mais provável, e os próximos passos recomendados (`/hooks`, `/oferta`, `/auditoria-completa`, `/teste-ab`, conforme o caso). Se o volume de dado for baixo, avisar que ainda não dá pra concluir com segurança em vez de recomendar mudança precipitada.
