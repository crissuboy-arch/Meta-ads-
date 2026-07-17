---
description: Puxa as métricas reais da campanha publicada e sugere otimizações
argument-hint: "[produto] — só depois do período mínimo de teste definido em campanha-[produto].md"
---

Analise performance real — nunca antes do período mínimo definido no brief.

## Passos

1. Leia `campanha-[produto].md` para saber a data de publicação e o período mínimo de teste.
2. Se o período mínimo ainda não passou, avise o usuário e informe quando será possível analisar com dados confiáveis — não gere conclusões com amostra pequena.
3. Via Claude in Chrome, abra o Gerenciador de Anúncios e colete, por conjunto de anúncios e por criativo: alcance, CTR, CPM, custo por resultado, e o motivo de resultado (cliques no link, conversões, mensagens — conforme o objetivo escolhido).
4. Compare os públicos de teste entre si e os criativos entre si. Aponte objetivamente: qual público/criativo está performando melhor e por quê (CTR mais alto costuma indicar copy/criativo mais forte; CPA mais baixo indica público mais qualificado).
5. Sugira próximo passo com base no dado real, não em achismo:
   - Custo por resultado dentro do esperado e volume de dados suficiente → sugerir escalar orçamento gradualmente (ex.: +20% a cada 2-3 dias, nunca duplicar de uma vez).
   - Criativo com CTR muito abaixo dos outros → sugerir pausar e testar novo ângulo com `/criativo`.
   - Público sem diferença relevante → sugerir consolidar em um conjunto só para simplificar otimização.
   - Anúncio rejeitado ou com entrega limitada por política → explicar o motivo dado pela Meta antes de sugerir qualquer ajuste.

## Saída

Apresente uma tabela objetiva com as métricas coletadas e a recomendação de próximo passo. Deixe claro que a decisão final (pausar, escalar, trocar) é do usuário — o sistema informa o dado, não decide sozinho.
