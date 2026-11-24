# Pix da Cakto → API de Conversões da Meta

O que o app faz agora com o webhook da Cakto (`/api/webhooks/sales/<chave>`):

| Evento da Cakto | O que vai para a Meta |
|---|---|
| `purchase_approved` (Pix, cartão, boleto pagos) | `Purchase`, com valor e moeda |
| `pix_gerado`, `boleto_gerado`, `picpay_gerado` | `InitiateCheckout` (boleto: `AddPaymentInfo`) |
| `pix_expirado`, `purchase_refused`, `refund`, `chargeback`, `checkout_abandonment`, `initiate_checkout` | nada (recebe e ignora, responde 200) |

Também envia e-mail, telefone e nome (criptografados), `fbp`/`fbc` e UTMs, quando a Cakto manda.
Se a Cakto reenviar o mesmo evento, o app não duplica (mesmo `event_id` = `cakto-<id>-<evento>`).

## Para ligar (por conta/pixel)
1. No app, tela **Rastreamento**: informe o pixel, cole o **token da API de Conversões** e salve.
   Use o código de teste e clique em "testar" para ver o evento no Gerenciador de Eventos.
2. Na Cakto, crie um webhook com o endereço `https://SEU-DOMINIO/api/webhooks/sales/<chave>`
   e marque: `purchase_approved`, `pix_gerado`, `pix_expirado`.
3. (Recomendado) Copie o "secret" do webhook da Cakto para a variável `CAKTO_WEBHOOK_SECRET`
   (Vercel). Sem ela, o app aceita qualquer envio para esse endereço.
4. Faça uma compra de teste pequena e veja na tela Rastreamento se a venda aparece como "enviada".

## Limites (honestos)
- **Deduplicação com o pixel do navegador**: só funciona se o pixel do site mandar o mesmo `event_id`.
  Hoje o servidor usa `cakto-<id>-<evento>`. Enquanto isso não for alinhado, `InitiateCheckout`
  pode contar em dobro (site + servidor). Se isso acontecer, desligue `pix_gerado` na Cakto.
- Um webhook por chave: cada pixel/conta precisa da sua própria chave e do seu webhook.
- Não testado com webhook real da Cakto, só com exemplos do formato documentado.
