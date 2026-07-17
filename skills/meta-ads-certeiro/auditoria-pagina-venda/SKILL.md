---
name: auditoria-pagina-venda
description: Esta skill deve ser usada para auditar uma página de venda/produto ANTES de criar a campanha — dá uma nota objetiva de prontidão para conversão baseada em checklist de CRO, nunca uma previsão de vendas. Acione quando o usuário disser "avaliar minha página", "analisar meu produto", "vai vender bem" ou rodar /auditoria.
---

# Auditoria de prontidão para conversão

## Sobre o número que esta skill entrega

Esta skill dá uma **nota de prontidão da página (1-10)**, não uma probabilidade de compra. Ninguém — nem essa skill, nem nenhuma ferramenta de IA — sabe a chance real de alguém comprar antes de rodar tráfego de verdade; isso depende do público, da oferta, do preço e do momento, e só o mercado responde. Sempre que a nota for apresentada ao usuário, deixar essa distinção explícita: é uma nota de **quão bem a página segue boas práticas comprovadas de conversão e reduz atrito**, usada só pra decidir se vale ir com verba maior ou testar pequeno primeiro.

## Como auditar

1. Abrir a página de venda (via Claude in Chrome se for necessário renderizar, ou ler o HTML/URL fornecido).
2. Avaliar cada critério abaixo como **atende / parcial / não atende**.
3. Calcular a nota: cada critério "atende" = 1 ponto, "parcial" = 0,5, "não atende" = 0, num total de 10 critérios → nota final de 0 a 10.

## Critérios (10, peso igual)

1. **Clareza da promessa em até 5 segundos**: dá pra entender o que é, pra quem é e o benefício principal sem rolar a página.
2. **Headline é benefício, não rótulo** (mesma régua da skill `copywriting-anuncios`).
3. **Prova social real e visível**: depoimento, avaliação, número de clientes, case — verificável, não genérico.
4. **Resposta às objeções óbvias do nicho**: preço, funciona mesmo, é seguro, prazo — usar as objeções reais coletadas em `pesquisa-[produto].md` se existir.
5. **CTA único e repetido**: mesma ação em vários pontos da página, sem CTAs concorrentes confundindo a decisão.
6. **Oferta clara**: o que a pessoa recebe exatamente, preço visível (ou processo claro pra saber o preço), forma de pagamento.
7. **Garantia ou redutor de risco**: política de reembolso, teste, suporte — qualquer coisa que reduza o medo de errar na compra.
8. **Mobile-first**: textos legíveis e botão de compra alcançável sem esforço no celular (a maior parte do tráfego pago vem de mobile).
9. **Velocidade de carregamento**: página não deve travar/demorar (isso mata o clique que você pagou pra trazer).
10. **Coerência com o anúncio**: a página entrega exatamente o que a copy do anúncio promete (mesma linguagem, mesma oferta) — checar contra `criativos/[produto]/variacoes.md` se já existir.

## Saída

Salvar `auditoria-[produto].md` na pasta conectada com:

- Nota final (0-10) e o detalhamento critério a critério
- Os 2-3 pontos que mais pesam contra a nota, com sugestão objetiva de correção
- Uma recomendação de verba inicial baseada na nota (não é garantia, é prudência):
  - **Nota ≥ 8**: página está pronta, pode ir com a verba diária padrão do config.
  - **Nota 5-7,9**: dá pra testar, mas sugerir começar com metade da verba padrão até confirmar que a página converte quem chega.
  - **Nota < 5**: recomendar corrigir os pontos críticos antes de gastar em tráfego — mandar clique pago pra uma página fraca é o jeito mais caro de descobrir isso.

Deixar claro ao usuário: essa recomendação de verba é um ponto de partida prudente, a decisão final é dele, e o `/campanha` vai usar essa nota para sugerir o orçamento inicial.
