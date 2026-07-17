---
name: pesquisa-palavras-chave
description: Esta skill deve ser usada para descobrir o que as pessoas realmente buscam no Google sobre um produto/nicho antes de escrever qualquer anúncio — autocomplete, perguntas relacionadas, intenção de busca. Acione quando o usuário disser "pesquisar palavras-chave", "o que as pessoas buscam", "pesquisa de mercado" ou rodar /pesquisar.
---

# Pesquisa de intenção de busca

Objetivo: a copy do anúncio não pode nascer de achismo. Ela nasce do que o público já está digitando no Google sobre o problema/produto.

## Fontes (nesta ordem)

1. **Autocomplete do Google**: digitar o termo base no Google (via Claude in Chrome ou busca) e coletar as sugestões de continuação (ex.: "clareamento dental" → "clareamento dental dói", "clareamento dental preço", "clareamento dental caseiro funciona").
2. **"As pessoas também perguntam"**: coletar as perguntas que aparecem na SERP para o termo base e para 2-3 variações.
3. **Buscas relacionadas** no rodapé dos resultados.
4. **Termos comparativos**: buscar "[produto] vale a pena", "[produto] x [alternativa]", "[produto] funciona" — são os termos de maior intenção comercial.

## Classificação por intenção

- **Informacional** ("o que é", "como funciona", "para que serve"): público ainda educando-se — bom para criativo de conteúdo/autoridade, não para CTA de compra direta.
- **Comercial** ("melhor", "vale a pena", "comparação", "opções"): público comparando — bom para criativo com prova social e diferencial.
- **Transacional** ("preço", "onde comprar", "agendar", "perto de mim"): público pronto — bom para CTA direto de conversão.

## Extração de dores e objeções

Toda pergunta com tom de dúvida ou resistência ("dói", "é seguro", "funciona mesmo", "vale o preço", "tem contraindicação") é uma objeção real do público — vira gancho ou resposta direta na copy do anúncio (a skill `copywriting-anuncios` usa isso).

## Tradução para interesses do Meta Ads

Ao final, sugerir 5-8 interesses reais do seletor de público do Gerenciador de Anúncios que conversem com os termos encontrados. Usar apenas nomes de categoria que plausivelmente existem no seletor (marcas, atividades, publicações do nicho) — se não tiver certeza do nome exato, sugerir o termo e marcar "verificar no seletor ao montar a campanha" em vez de inventar um nome de interesse.

## Boas práticas

- Nunca inventar volume de busca exato (não há acesso a dados reais de volume sem Google Keyword Planner/Trends autenticado) — reportar frequência relativa qualitativa ("aparece em quase toda variação", "aparece só em 1 busca") em vez de números fabricados.
- Priorizar qualidade sobre quantidade: 15-20 termos bem classificados valem mais que 100 termos genéricos.
- Registrar a fonte de cada dor/objeção (de qual busca ela veio) para rastreabilidade.
