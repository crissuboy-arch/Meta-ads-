---
name: hooks-criativos
description: Esta skill deve ser usada para gerar hooks (ganchos de abertura) para Feed, Stories, Reels, UGC, Carrossel e vídeos curtos. Acione quando o usuário disser "criar hooks", "gancho de abertura", "primeira frase do vídeo" ou rodar /hooks.
---

# Hooks por formato

Hook é o que decide se a pessoa continua assistindo/lendo nos primeiros 1-3 segundos (vídeo) ou na primeira linha visível (feed/carrossel). Sempre ancorar em dores/desejos/objeções reais — de `mercado-[produto].md` ou `pesquisa-[produto].md` se existirem; nunca inventar dor genérica de nicho.

## Padrões de hook (usar como matéria-prima, misturar com a dor real do produto)

- **Pergunta direta**: "Você também já tentou [solução comum] e não funcionou?"
- **Afirmação de choque/contraste**: "Ninguém te conta isso sobre [tema]."
- **Identificação imediata**: "Se você [situação específica do avatar], isso é pra você."
- **Erro comum**: "O erro que 9 em cada 10 [avatar] cometem em [tema]."
- **Resultado como abertura**: mostrar o resultado/prova antes de explicar como chegou lá.
- **Confissão pessoal (para UGC)**: "Eu não queria admitir isso, mas..."

## Por formato

- **Feed (imagem estática)**: hook é a primeira linha do texto + a headline visual na imagem — as duas devem contar a mesma história, não competir.
- **Stories**: hook precisa funcionar em 1-2 segundos, geralmente com texto grande na tela + fala/áudio reforçando o mesmo gancho.
- **Reels/vídeo curto**: hook nos primeiros 3 segundos tem que ser dito E aparecer escrito na tela (legenda) — quem assiste sem som também precisa entender.
- **UGC**: hook precisa soar como fala natural de pessoa real, não como anúncio — evitar linguagem de propaganda logo de cara (a skill `roteiro-ugc` aprofunda isso).
- **Carrossel**: hook é o primeiro slide — precisa gerar curiosidade suficiente para a pessoa arrastar pro próximo, sem entregar tudo já no slide 1.

## Saída

Para cada formato pedido, entregar 3-5 hooks diferentes, cada um testando um padrão diferente da lista acima (nunca 5 variações do mesmo padrão). Marcar de qual dor/desejo/objeção real cada hook partiu, para rastreabilidade e para facilitar o teste A/B depois (`/teste-ab`).
