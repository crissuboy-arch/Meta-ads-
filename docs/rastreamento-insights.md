# Rastreamento e atribuição — melhoria de 28/11/2026

Referência de organização: [UTMify](https://utmify.com.br/), especialmente a identificação de [UTMs ausentes e incompletas](https://utmify.help.center/article/1024-voce-esta-tendo-vendas-nao-trackeadas). A identidade visual e as integrações da Ofensiva são preservadas; não há conexão nem dependência da UTMify.

O painel utiliza os registros reais do endpoint autenticado existente `/api/sales`, por produto de rastreamento selecionado. Permite filtrar período, moeda, estado, identificação e busca; agrupar por origem, campanha, criativo, público, plataforma ou meio de pagamento; investigar UTMs ausentes; consultar eventos e event_id; exportar os registros filtrados e gerar links UTM sem alterar anúncios. O exportador neutraliza fórmulas de planilha e omite detalhes técnicos brutos de erros CAPI.

Receitas são separadas por moeda. Pendências e reembolsos não são somados à receita paga informada. Valores ausentes e moedas desconhecidas não geram totais inventados. IDs de evento exatamente repetidos são agrupados para exibição, sem alterar a idempotência ou os registros no servidor.

Limites: a consulta existente fornece até 200 registros. O painel avisa quando esse limite é atingido e seus totais representam somente os registros carregados, não todo o histórico. A data mostrada é a do recebimento. Aceitação pela API Meta não comprova atribuição nem deduplicação navegador/servidor. O repasse de UTMs no checkout exige validação no site; o gerador não instala código nem modifica campanhas. Nenhum acesso bancário, nova integração de pagamento ou rastreamento de cliques foi criado.

Validação direcionada: `python scripts/check_frontend.py` inclui os 12 testes do núcleo de cálculo, filtros, URLs, CSV e consistência do código embutido. `python scripts/verify_tracking_insights.py` verifica a navegação local com serviços controlados, exportação, diagnóstico, falhas, limite da consulta e responsividade. As imagens de teste estão marcadas como dados fictícios; a aplicação não contém esses registros demonstrativos.

Sem mudanças no backend, autenticação, credenciais, pagamentos, Supabase, Vercel ou campanhas reais. Checkpoint local: `checkpoint/rastreamento-20261128`. Melhorias disponíveis somente na prévia até aprovação de publicação.
