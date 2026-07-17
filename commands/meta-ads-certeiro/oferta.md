---
description: Avalia a força da oferta (promessa, headline, bônus, preço, garantia, mecanismo único, diferenciais, CTA) e dá nota de 0 a 100
argument-hint: "[produto] — descreva a oferta ou cole o texto/link dela"
---

Avalie a oferta seguindo a skill `avaliacao-oferta` na íntegra.

## Passos

1. Reúna os dados da oferta: peça ao usuário para descrever ou colar (texto da página, print, ou link) promessa, headline, bônus, preço, garantia, mecanismo único, diferenciais e CTA. Não avaliar com dado incompleto — perguntar especificamente o que falta.
2. Se `mercado-[produto].md` existir, cheque se a promessa/ângulo escolhido conversa com as dores/desejos já mapeados.
3. Aplique os 8 critérios da skill e calcule a nota.
4. Salve `oferta-[produto].md`.

## Exemplo de uso

```
/oferta curso de inglês online para iniciantes
[cola a headline, o preço, a garantia e os bônus da página]
```

## Saída

Apresente a nota final, o detalhamento por critério, e os 2-3 pontos que mais pesam contra — com sugestão pontual de correção (não reescreva a oferta inteira sem pedir). Deixe claro: a nota mede solidez estrutural da oferta, não prevê vendas. Sugira o próximo passo conforme a faixa: nota alta → `/hooks` ou `/ugc`; nota baixa → corrigir os pontos fracos antes de seguir.
