# Integração funcional da jornada — 27/11/2026

Branch: `redesign/experiencia-premium-v2`. Visual aprovado preservado em `a0b4b54`, tag `checkpoint/central-ia-aprovada-20261127`.

## Entregue nesta etapa

- Meta: OAuth e token oficiais existentes preservados; contas selecionadas disparam importação automática, com atualização do painel e mensagens de falha. Não altera campanhas.
- Produto/financeiro: oferta, preço, custos e campanhas vinculadas salvos por utilizador; preenchimento automático e resultado estimado com receita atribuída real do Meta. Não considera receita atribuída como recebimento bancário; campos ausentes e resultados paginados incompletos não viram números inventados.
- Rastreamento: assistente usa os campos, scripts, botões de copiar, salvamento e testes existentes; busca Pixels autorizados, orienta token/domínio e exige código TEST no envio de evento de teste. Vinculação explícita ao produto; nenhum token é incluído nos agentes.
- Especialistas: o mesmo contexto de produto, conta, campanhas e custos segue para chat hospedado, APIs salvas e motor nativo existente. O servidor revalida propriedade do produto. Inclui os nove especialistas e preserva o mentor legado.
- Campanhas: nove etapas, rascunho persistente, revisão e aprovação humana; reutiliza os handlers Meta existentes para campanha/conjunto/anúncio PAUSADOS. Mantém a trava de escrita do servidor. IDs parciais são preservados; resultados incertos bloqueiam repetição automática. Assistente avançado e importações antigas continuam acessíveis.

## Verificação direcionada

28 testes Python distintos aprovados entre as execuções direcionadas de financeiro, contexto, wizard e novos módulos. Onze grupos de integração no navegador aprovados, incluindo importação automática, aprovação, falha parcial e envio de contexto aos nove especialistas.

Meta Graph e inferência foram substituídos por fixtures nos testes externos; **não constituem homologação da conta real**. Autenticação, cadastro de produto e persistência local foram exercitados nos endpoints reais da aplicação, em armazenamento isolado. Sintaxe JavaScript/Python e preservação dos 244 IDs verificados.

## Limites objetivos para a homologação

- A prévia `http://127.0.0.1:8831` não utiliza credenciais de produção. Conta Meta, permissões e respostas reais de IA exigem validação posterior no ambiente autorizado com a sessão existente; nenhuma conexão foi simulada na aplicação entregue.
- Criação real permanece indisponível quando `WRITE_ACTIONS_ENABLED` estiver desativado. Não foi alterado neste trabalho. A jornada integrada cobre Vendas e Tráfego; categorias especiais e demais objetivos exigem revisão específica/assistente avançado.
- Imagem do anúncio precisa de URL pública HTTPS, conforme a integração já disponível. A criação pode depender de exigências específicas da conta Meta; erros são mostrados e não são apresentados como sucesso.
- Receita recebida, estornos e conciliação de pagamentos não foram alterados. Deduplicação Pixel/CAPI continua exigindo o mesmo identificador de evento no site e no servidor; o assistente não comprova instalação no site de terceiros.
- Sem migração: os novos perfis usam o JSON de `ad_drafts`, com slug reservado e filtro de proprietário; não substituem os rascunhos existentes. A biblioteca não permite editar/apagar IDs reservados.

Sem alterações em pagamentos, credenciais, Supabase/configuração, infraestrutura, instaladores ou produção. Publicação e novo instalador continuam aguardando aprovação.
