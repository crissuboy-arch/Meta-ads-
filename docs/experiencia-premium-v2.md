# Experiência premium v2 — prévia para aprovação

Base: `197c4d7a711b76dfa78dc625c378e5e82cc3d1e5` (main mais recente consultada).
Branch isolada: `redesign/experiencia-premium-v2`.
Checkpoint local: `checkpoint/ux-premium-20261127`.

Alterações limitadas à apresentação e ao encaminhamento da interface para
contratos HTTP/IPC já existentes. Nenhuma migração, pagamento, credencial,
campanha, autenticação do servidor ou configuração de infraestrutura alterada.

- Central de IA em lista de seis provedores, com ações individuais e estados
  separados de instalação, configuração, seleção e teste de resposta.
- Gemini, OpenRouter e APIs suportadas usam os quatro espaços existentes de
  texto/imagem e principal/reserva. A seleção “Minha API” utiliza o endpoint
  existente `/api/providers/generate`, mantendo a cadeia principal/reserva.
- Claude/Codex reutilizam `detect_providers`, `open_provider_terminal` e
  `local_chat`. Abrir o login não marca a conexão como testada. A ponte atual
  abre a aplicação oficial do fornecedor; não foi criado OAuth embutido.
- Na web, as conexões locais explicam o requisito do aplicativo instalado.
  OpenCode permanece experimental; seleção antiga é preservada como tal.
- Central dos nove especialistas em lista operacional, painel de contexto e
  seleção explícita de provedor. Sem coordenação autônoma declarada.
- Guia das nove etapas solicitadas, ajuda contextual, retomada e progresso
  local por utilizador. Etapa visitada não significa configuração validada.
  Pagamento não é declarado confirmado por existir uma sessão autenticada.
- Dashboard com hierarquia de indicadores, menos superfícies repetidas,
  navegação consistente, responsividade e respeito a movimento reduzido.

Validação direcionada: `scripts/check_frontend.py` e
`scripts/verify_experience_v2.py` (localhost isolado). Onze grupos de checagens
passaram, incluindo cinco resoluções, perfis legados, erros e desconexão.
IPC/API são simulados somente dentro do navegador de testes; isso não é uma
nova homologação comercial ou inferência ao vivo. Capturas usam estados
vazios locais, sem métricas fictícias ou contas de produção.

Ícones de identificação obtidos dos próprios fornecedores:
- OpenAI: https://openai.com/apple-icon.png
- Claude: https://claude.ai/favicon.ico
- OpenCode: https://opencode.ai/favicon-96x96-v3.png
- Gemini: imagem referenciada pelo HTML público https://gemini.google.com/app
- OpenRouter: https://openrouter.ai/favicon/glyph.png

Não há merge, push nem publicação desta prévia. Após aprovação visual,
conferir a main atual antes de integrar e validar no instalador correspondente.
