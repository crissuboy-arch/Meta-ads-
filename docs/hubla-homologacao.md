# Hubla — homologação de lançamento

Endpoint: `POST /api/webhooks/hubla`, Webhooks 2.0, modo **Integração recomendada** (`standard`).
Autenticação oficial: `x-hubla-token`, comparação constante; não é uma assinatura HMAC.

Configuração exclusivamente no servidor:
- `HUBLA_WEBHOOK_TOKEN`: token da integração Hubla, nunca no frontend/repositório.
- `HUBLA_PRODUCT_ID`: ID real do produto em `event.products[].id` (não ID da oferta).
- `HUBLA_LIVE_ACCESS_ENABLED`: ausente/false durante homologação.
- `HUBLA_ACCESS_MODEL`: `one_time` somente após confirmar pagamento único. Não ativar para assinatura: expiração/cancelamento recorrente não foi implementado.

A oferta inicial aceita R$97 BRL (`totalCents=9700`), sem descontos/order bumps.
Pagamento confirmado concede acesso à conta identificada por `event.user.email`.
Não cria contas, não altera senha nem contas existentes: o comprador utiliza o login existente
ou o cadastro já disponível. Reembolso revoga somente aquela compra Hubla. Outra compra
ativa ou licença legada continua válida. Não enviar Pixel/CAPI artificial por homologação.

`x-hubla-sandbox=true` valida o formato sem escrever comprador, licença, venda ou CAPI.
Pagamentos reais com a liberação desativada recebem 503 para permitir reenvio, não um 200 silencioso.
Recibos e licença são atômicos no mesmo Supabase, via migração aditiva 008.
IDs de entrega deduplicados, conflito de conteúdo recusado, versão antiga ignorada,
reembolso terminal; uma fatura não pode trocar de titular/produto.
Tabelas/RPC acessíveis apenas ao service_role, sem acesso anon/authenticated.

Validação: 36 testes direcionados (Hubla e preservação checkout/tracking) passaram.
RPC executada com service_role em transação revertida: repetição, conflito,
reembolso, reordenação, tentativa de reativação, outra compra e troca de titular.
Depois do rollback: zero recibos/licenças de teste; app_buyers intacta.

Pendentes externos: confirmar modalidade comercial; configurar token/produto reais;
receber sandbox oficial; testar entrega pela sessão do titular; só então autorizar
um teste financeiro real e a abertura do checkout. Não foi realizada cobrança.
Manter checkout público desativado também no painel Hubla: o bloqueio do backend
não desativa por si só um checkout hospedado pela Hubla.

Rollback: retornar ao deployment de checkpoint; deixar tabelas aditivas intactas.
Não apagar recibos/licenças nem reverter dados. Webhook permanece desabilitado
sem variáveis explícitas; não tocar nos endpoints Hotmart/Cakto existentes.

Fontes oficiais:
- https://hubla.gitbook.io/docs/webhooks/proteja-seu-endpoint
- https://hubla.gitbook.io/docs/webhooks/sandbox
- https://hubla.gitbook.io/docs/webhooks/como-enviar-seus-dados
