---
description: Configura o sistema — conta de anúncios, público padrão e preferências (roda uma vez)
---

Configure o ambiente do Meta Ads Certeiro. Siga esta ordem:

## 1. Pasta de trabalho

Verifique se há uma pasta do usuário conectada. Se não houver, peça para conectar uma pasta (ex.: "Campanhas") — tudo (config, pesquisas, criativos e briefs) será salvo nela para persistir entre sessões.

## 2. Verificar config existente

Procure `meta-ads-config.json` na pasta conectada. Se existir, mostre um resumo e pergunte o que o usuário quer atualizar. Se não existir, colete os dados abaixo.

## 3. Dados do negócio (perguntar via AskUserQuestion / formulário)

Colete:

- **Negócio/produto principal** e uma frase de posicionamento (o que vende, para quem).
- **Praça padrão**: cidade/região/país para segmentação.
- **Público padrão**: faixa etária, gênero (se relevante) — sempre editável por campanha.
- **Verba diária padrão** de teste (sugira um valor mínimo razoável para o objetivo escolhido, sem prometer resultado).
- **Objetivo padrão**: tráfego, conversão, geração de cadastro (leads) ou mensagens no WhatsApp/Direct.
- **Link de destino padrão** (site, WhatsApp ou formulário).
- **Pixel/API de Conversões**: pergunte se já está instalado no site (se não estiver e o objetivo for conversão, avise que o resultado fica pior sem ele e sugira instalar antes de publicar campanhas de conversão).
- **Modo de publicação**: pergunte se o usuário quer confirmar cada nível antes de publicar (`confirmar`, padrão e recomendado) ou publicar direto após um resumo único no início (`automatico`). Deixe explícito que é dinheiro real saindo sem revisão nível a nível no modo automático, e que dá pra trocar a qualquer momento rodando `/setup` de novo.

## 4. Conta de anúncios da Meta

Pergunte se o usuário já tem conta de anúncios ativa no Gerenciador (business.facebook.com) com método de pagamento configurado.

- **Se não tiver**: explique que é preciso criar a conta e cadastrar forma de pagamento antes de publicar, e que o usuário deve voltar e rodar `/setup` de novo depois. Salve o config parcial e encerre.
- **Se já tiver**: peça o **nome da conta de anúncios** e o **Business Manager** (se houver mais de um) para facilitar a navegação no `/publicar`. Nunca peça token de acesso, senha ou API key — a publicação é sempre feita com a sessão logada do próprio usuário no navegador.

## 5. Salvar

Salve tudo em `meta-ads-config.json` na pasta conectada, neste formato:

```json
{
  "negocio": { "nome": "", "posicionamento": "", "linkPadrao": "" },
  "publico": { "praca": "", "idadeMin": 18, "idadeMax": 65, "genero": "todos" },
  "campanha": { "objetivoPadrao": "trafego", "verbaDiariaPadrao": 30, "pixelInstalado": false },
  "modoPublicacao": "confirmar",
  "contaAnuncios": { "nomeConta": "", "businessManager": "" }
}
```

## 6. Encerrar

Confirme o que foi salvo e explique o ciclo: `/pesquisar` → `/criativo` → `/campanha` → `/publicar` → `/analisar`.
