---
description: Recebe o usuário pela primeira vez, entende o produto e indica por onde começar no sistema
argument-hint: "(sem argumentos — o comando pergunta tudo que precisa)"
---

Dê as boas-vindas ao **Meta Ads Certeiro** e faça um diagnóstico rápido de onde o usuário está, para indicar o caminho certo dentro do sistema. Este comando não pesquisa, não avalia e não publica nada sozinho — só entende o contexto e aponta a sequência de comandos ideal.

## Perguntas (via AskUserQuestion / formulário, uma de cada vez ou agrupadas em blocos curtos)

1. **O que você vende?** (produto/serviço, em 1 frase)
2. **Qual é o seu nicho?** (se não souber definir com precisão, tudo bem — os próximos comandos ajudam a refinar)
3. **Em qual país/região vai anunciar?**
4. **Qual é o seu público?** (mesmo que só uma ideia inicial)
5. **Quanto pretende investir?** (verba diária ou total disponível para teste)
6. **Já tem página de vendas?** (sim/não — se sim, pedir o link)
7. **Já tem criativos prontos?** (sim/não — se sim, pedir para descrever ou colar)
8. **Qual o objetivo da campanha?** (vendas diretas, geração de cadastro/leads, mensagens no WhatsApp/Direct, tráfego/reconhecimento)

## Lógica de recomendação

Com base nas respostas, monte a sequência de comandos priorizada:

- **Sem pesquisa de mercado feita** → sempre começar por `/pesquisa-mercado [produto]`.
- **Sem oferta definida ou com dúvida sobre preço/garantia/bônus** → `/oferta [produto]` logo depois.
- **Já tem página de vendas** → incluir `/auditoria [produto] [URL]` antes de investir em tráfego.
- **Não tem página de vendas ainda** → avisar que sem página (ou destino claro tipo WhatsApp/formulário) não dá para publicar campanha de conversão, e sugerir resolver isso antes de `/campanha`.
- **Sem criativos prontos** → incluir `/hooks [produto]` e, se o objetivo combinar com vídeo/depoimento, `/ugc [produto]`, seguido de `/criativo [produto]`.
- **Já tem criativos** → pode pular direto para `/campanha [produto]` depois da oferta/público, mas vale rodar `/auditoria-completa` para checar se os criativos existentes passam no checklist.
- **Público ainda vago** → incluir `/publico [produto]` antes de `/campanha`.
- **Verba baixa ou primeira campanha do produto** → sugerir `/teste-ab [produto]` antes de `/campanha`, para não gastar testando tudo de uma vez.
- **Sempre por último no fluxo de criação** → `/campanha [produto]` → `/publicar [produto]` (e/ou `/google-ads [produto]`).
- **Se já existe campanha rodando** (o usuário mencionar isso em vez de estar começando do zero) → pular direto para `/analise-resultados [produto]` ou `/auditoria-completa [produto]`, conforme o que ele tiver: métricas para colar ou necessidade de diagnóstico geral.

## Saída

Primeiro, um resumo de 3-4 linhas do que foi entendido sobre o negócio. Depois, a sequência recomendada de comandos, numerada e nesta forma:

```
→ Comece por /pesquisa-mercado [produto]
→ Depois utilize /oferta [produto]
→ Em seguida execute /hooks [produto]
→ Depois /criativo [produto]
→ Finalize com /auditoria-completa [produto]
```

(ajustar a sequência exata conforme as respostas — o exemplo acima é ilustrativo, não fixo). Se `meta-ads-config.json` ainda não existir, recomendar `/setup` como o passo zero antes de tudo. Encerrar perguntando se o usuário quer já começar pelo primeiro comando sugerido.
