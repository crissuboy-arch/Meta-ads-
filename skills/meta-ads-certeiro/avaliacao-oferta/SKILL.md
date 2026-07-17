---
name: avaliacao-oferta
description: Esta skill deve ser usada para avaliar a força de uma oferta (promessa, headline, bônus, preço, garantia, mecanismo único, diferenciais, CTA) e dar uma nota de 0 a 100. Não prevê vendas, mede solidez estrutural da oferta. Acione quando o usuário disser "avaliar minha oferta", "nota da minha oferta", "minha oferta está boa" ou rodar /oferta.
---

# Avaliação de força de oferta (0-100)

## Sobre a nota

Mede o quanto a oferta segue estrutura comprovada de ofertas que convertem — não é previsão de quantas vendas ela vai gerar (isso só o mercado responde). Sempre comunicar essa distinção ao apresentar o resultado, mesma lógica da skill `auditoria-pagina-venda`.

## Os 8 critérios (12,5 pontos cada = 100)

1. **Promessa central**: é específica, mensurável ou vívida o suficiente? ("perca peso" = fraco; "durma a noite toda sem acordar 3x" = forte).
2. **Headline**: comunica a promessa em uma frase, sem precisar de explicação.
3. **Mecanismo único**: existe um "porquê funciona" diferente do óbvio/genérico do nicho? (produtos sem mecanismo único competem só por preço).
4. **Diferenciais reais**: 2-3 motivos concretos pra escolher esse produto e não o concorrente (não "qualidade" vago — algo verificável).
5. **Bônus**: existem, são relevantes à promessa principal (não itens aleatórios só pra parecer mais valor) e têm valor percebido claro.
6. **Preço e ancoragem**: existe comparação que justifica o valor (custo do problema, preço de alternativa, valor total somado)?
7. **Garantia/redutor de risco**: existe, é clara, e reduz de fato o medo de comprar errado?
8. **CTA da oferta**: a ação pedida é óbvia e o que a pessoa recebe ao agir é imediato e claro.

Cada critério: 12,5 (atende bem) / 6 (parcial) / 0 (ausente ou fraco).

## Saída

Salvar `oferta-[produto].md` com: nota final, detalhamento critério a critério, os 2-3 pontos que mais derrubam a nota com sugestão objetiva de correção (nunca reescrever a oferta inteira sem pedir — sugerir o ajuste pontual). Se `mercado-[produto].md` existir, checar se a promessa e o ângulo escolhido conversam com as dores/desejos já levantados.

Faixas de leitura (comunicar como orientação, não veredito):
- **80-100**: oferta estruturalmente forte, pode ir para copy e campanha.
- **50-79**: oferta funcional mas com pontos a reforçar antes de escalar verba.
- **abaixo de 50**: vale revisar a oferta antes de investir em tráfego — o problema normalmente não é o anúncio, é a oferta por trás dele.
