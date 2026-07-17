---
name: pesquisa-mercado
description: Esta skill deve ser usada para mapear nicho, público, concorrentes, dores, desejos, objeções, promessas e ângulos de venda antes de criar qualquer campanha. Acione quando o usuário disser "analisar meu nicho", "quem é meu concorrente", "mapear meu mercado" ou rodar /pesquisa-mercado.
---

# Pesquisa de mercado e ângulos de venda

Diferença em relação à skill `pesquisa-palavras-chave`: aquela mapeia o que as pessoas digitam no Google; esta mapeia o **mercado como um todo** — quem compra, quem vende, e por qual ângulo entrar. As duas se complementam; se `pesquisa-[produto].md` já existir, aproveitar as dores/objeções já levantadas em vez de repetir a busca.

## O que levantar

1. **Nicho e sub-nicho**: definir com precisão (ex.: não "emagrecimento", e sim "mulheres 35-50 pós-parto que já tentaram dieta e falharam").
2. **Público**: quem compra de fato (nem sempre é quem usa o produto — ex.: presente, produto infantil).
3. **Concorrentes diretos**: 3-5 negócios/produtos que resolvem o mesmo problema. Levantar via busca no Google e, se o usuário fornecer, análise de páginas/anúncios que ele já viu do concorrente (nunca inventar dado de concorrente que não foi verificado).
4. **Dores** (o que incomoda agora) e **desejos** (o que a pessoa quer sentir/ser depois) — sempre em linguagem do cliente, não da empresa.
5. **Objeções** que fazem a pessoa não comprar (preço, confiança, tempo, "já tentei antes e não funcionou", ceticismo com a categoria).
6. **Promessas que o mercado já usa**: o que os concorrentes prometem — serve para o produto do usuário se diferenciar, não copiar.
7. **Ângulos de venda possíveis**: pelo menos 3 formas diferentes de vender o mesmo produto (ex.: ângulo da dor, ângulo do resultado rápido, ângulo da transformação de identidade, ângulo do mecanismo único/"como funciona").

## Fontes

- Busca no Google (Chrome) para concorrentes, avaliações públicas, fóruns/comunidades do nicho.
- O que o próprio usuário já sabe do público (perguntar diretamente: "o que seus clientes mais reclamam antes de comprar?").
- Se houver `pesquisa-[produto].md`, reaproveitar as objeções e termos de busca já levantados.

## Saída

Salvar `mercado-[produto].md` com: nicho definido, perfil de público, tabela de concorrentes (nome, promessa principal, ponto fraco percebido), lista de dores/desejos/objeções, e 3+ ângulos de venda com 1 frase de exemplo cada. Este arquivo alimenta diretamente `/oferta`, `/hooks`, `/ugc` e `/publico`.
