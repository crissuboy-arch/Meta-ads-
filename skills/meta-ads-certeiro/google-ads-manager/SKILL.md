---
name: google-ads-manager
description: Esta skill deve ser usada ao publicar uma campanha de pesquisa no Google Ads via navegador — criação de campanha, grupo de anúncios, palavras-chave, anúncios responsivos de pesquisa e verificação de status. Acione quando o usuário disser "publicar no Google Ads", "anunciar no Google", "campanha de pesquisa" ou rodar /google-ads.
---

# Publicação no Google Ads (via navegador)

Toda publicação é feita com a sessão logada do próprio usuário no Claude in Chrome, em ads.google.com. O sistema nunca pede, armazena ou digita senha/token do Google em nome do usuário. Mesma regra de ouro do `meta-ads-manager`: dinheiro real, confirmação explícita antes de cada publicação.

## Diferenças-chave em relação ao Meta

- Google Ads (Rede de Pesquisa) é anúncio de **intenção**, não de interrupção: o público já está buscando ativamente — por isso as palavras-chave de `pesquisa-[produto].md` (principalmente as de intenção **transacional** e **comercial**) são o coração da campanha aqui, muito mais que os interesses usados no Meta.
- Não existe "criativo visual" no anúncio de pesquisa padrão — o anúncio é só texto (Anúncio de Pesquisa Responsivo/RSA): títulos e descrições que o Google testa e recombina automaticamente.
- Existe um conceito de **Índice de Qualidade** (relevância da palavra-chave + anúncio + página de destino) — por isso rodar `/auditoria` na página de destino antes ajuda a evitar CPC mais caro por baixa relevância.

## Fluxo

1. **Login**: navegar até `ads.google.com`. Se pedir login, pedir para o usuário logar manualmente.
2. **Criar campanha**: escolher objetivo compatível com o config (padrão: Vendas ou Leads, tipo de campanha "Pesquisa") → nomear de forma identificável (ex.: `[produto] — Pesquisa [data]`).
3. **Orçamento e lances**: usar o valor diário definido em `campanha-[produto].md` (a mesma lógica de sugestão por nota da auditoria vale aqui) → estratégia de lances simples para começar (Maximizar cliques ou CPC manual com teto), evitar estratégias automáticas de conversão antes de ter volume de dados/conversões rastreadas.
4. **Grupo de anúncios e palavras-chave**: 1 grupo por tema de intenção (ex.: "transacional" separado de "comercial"), usando as palavras-chave de `pesquisa-[produto].md`. Configurar correspondência de frase ou exata para controlar melhor o gasto no início — evitar ampla sem controle de termo de pesquisa negativo.
5. **Palavras-chave negativas**: adicionar termos claramente fora do público (ex.: "grátis", "curso", "vaga de emprego" se não for o caso) para não gastar com clique irrelevante.
6. **Anúncio responsivo de pesquisa**: subir de 3 a 15 títulos e de 2 a 4 descrições por grupo, usando a copy da skill `copywriting-anuncios` adaptada ao formato curto de texto do Google (sem emoji, título até 30 caracteres, descrição até 90).
7. **Extensões de anúncio**: preencher com dados reais do config — link de site, chamada (WhatsApp/telefone), texto de destaque, snippet estruturado. Extensões aumentam a área ocupada pelo anúncio sem custo extra e melhoram a relevância.
8. **Revisão antes de publicar**: mostrar print de cada nível (campanha/grupo/anúncio) ao usuário para confirmação final, igual ao fluxo do Meta.
9. **Publicar** e aguardar o status ("Em revisão", "Ativada", "Desaprovado").

## Se um anúncio for desaprovado

Ler o motivo exato no próprio Google Ads. Ajustar seguindo a política (claims de saúde/financeiro têm regra própria e mais rígida que a Meta em alguns pontos) e reenviar.

## Verificação pós-publicação

Confirmar: orçamento, palavras-chave e correspondências batem com o brief, extensões preenchidas, e status de cada anúncio. Reportar tudo ao usuário.
