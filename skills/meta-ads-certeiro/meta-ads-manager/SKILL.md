---
name: meta-ads-manager
description: Esta skill deve ser usada ao publicar uma campanha no Gerenciador de Anúncios da Meta (Facebook/Instagram) via navegador — criação de campanha, conjunto de anúncios, anúncios e verificação de status. Acione quando o usuário disser "publicar campanha", "subir anúncio", "colocar no ar no Meta" ou rodar /publicar.
---

# Publicação no Gerenciador de Anúncios (via navegador)

Toda publicação é feita com a sessão logada do próprio usuário no Claude in Chrome, em business.facebook.com/adsmanager. O sistema nunca pede, armazena ou digita senha/token da Meta em nome do usuário.

## Regra de ouro — dinheiro real envolvido

Antes de clicar em publicar qualquer nível (campanha, conjunto ou anúncio), mostrar ao usuário exatamente o que vai ser criado e pedir confirmação explícita. Nunca publicar automaticamente em sequência sem checkpoint — um erro de verba ou público publicado sem revisão custa dinheiro real do usuário.

## Fluxo

1. **Login**: navegar até `business.facebook.com/adsmanager`. Se pedir login, pedir para o usuário logar manualmente — nunca preencher credenciais.
2. **Criar campanha**: "Criar" → escolher o objetivo definido em `campanha-[produto].md` → nomear a campanha de forma identificável (ex.: `[produto] — teste [data]`).
3. **Orçamento**: definir no nível de campanha (CBO) ou conjunto conforme o brief — usar exatamente o valor diário do brief, nunca arredondar para cima sem avisar.
4. **Conjunto(s) de anúncios**: para cada público de teste do brief — localização, idade, gênero, interesses (verificar se cada interesse sugerido existe no seletor; se não existir com esse nome exato, buscar o mais próximo e avisar o usuário da troca) e posicionamento (Advantage+ salvo indicação contrária no brief).
5. **Anúncios**: para cada criativo aprovado — subir texto principal, título, descrição, CTA e a imagem/vídeo (se o usuário já tiver o arquivo pronto na pasta conectada; caso contrário, avisar que falta o arquivo visual antes de publicar).
6. **Revisão antes de publicar**: mostrar print de cada nível (campanha/conjunto/anúncio) ao usuário para confirmação final.
7. **Publicar** e aguardar o status mudar de "Em revisão" para "Ativo" ou "Rejeitado" (a revisão da Meta pode levar minutos a horas — não travar a conversa esperando, informar o usuário que pode checar depois com `/analisar` ou voltando a pedir status).

## Se um anúncio for rejeitado

Ler o motivo exato dado pela Meta na interface (aparece no próprio anúncio). Ajustar apenas o ponto citado (copy, imagem ou link de destino) seguindo a skill `copywriting-anuncios` e `score-criativo`, e reenviar para revisão — nunca reenviar sem entender o motivo.

## Verificação pós-publicação

Confirmar: nome da campanha, orçamento configurado bate com o brief, públicos batem com o brief, e status de cada anúncio. Reportar tudo isso ao usuário — nunca assumir que publicou certo sem checar a tela final.
