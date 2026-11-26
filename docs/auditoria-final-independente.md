# Auditoria independente e correções de finalização

26/11/2026. Base auditada: `finalizacao-funcional`, `95d8c4f`.
Branch de correção: `fix/finalizacao-funcional-validada`.
Checkpoint: `checkpoint/auditoria-95d8c4f`.

## Preservação e escopo

O histórico contém `f73713f`, a entrega premium `dcf380f` e os oito commits
da finalização do Claude. Não houve reconstrução do produto, migração,
alteração de credenciais, campanha real, merge ou publicação de produção.
Os blocos CSS premium foram comparados e permaneceram iguais.

Os aliases `app.ofensivacriativa.com` e `meta-ads-unmc.vercel.app` foram
verificados no mesmo projeto Vercel `meta-ads-unmc`, apontando para o deploy
`dpl_HNbFuue3uqeS7HVEfx5ybom1SMyh`, commit de produção `dcf380f`.
As consultas de auditoria ao Supabase existente foram somente leitura.
Inventário observado: 3 utilizadores, 1 conexão Meta, 6 contas, 24 linhas de
insights, 4 configurações de tracking, 1 venda, 1 chave MCP e 0 compradores
na tabela de concessão de acesso. Quatro tokens CAPI guardados não provam
validade: somente uma configuração tinha resultado positivo armazenado.

## Falhas reproduzidas e correções

- O pacote desktop guardava Python em `_up_/local_engine`, mas o Rust
  procurava `local_engine`; faltavam as configurações e o próprio runtime.
  Agora o CI empacota Python e configurações com PyInstaller, em diretório
  mapeado explicitamente para `runtime/local-engine`. Versão desktop 1.0.1.
- O chat ignorava o motor local. A seleção explícita da CLI agora envia
  a conversa pela ponte Tauri autenticada. Uma falha local não provoca
  envio silencioso ao fornecedor hospedado. O modo hospedado continua
  disponível e é possível voltar a ele.
- O adaptador Claude não resolvia corretamente o executável Windows.
  Usa o caminho real; o shim npm oficial é resolvido para seu binário
  nativo. Claude/Codex recebem o prompt por stdin, evitando o limite da
  linha de comando Windows. Não se leem arquivos de autenticação.
- O servidor local aceitava chamadas sem autenticação e origens externas.
  Agora exige token efêmero mantido na ponte nativa, rejeita Origin,
  limita o corpo JSON e não expõe o token ao JavaScript hospedado.
- `approved: "false"` era convertido em autorização. O relay local e o
  MCP remoto deixam a execução de campanhas ao assistente web autenticado,
  com confirmação humana e feature flag. O MCP stdio mantém propostas,
  mas a execução exige confirmação num terminal interativo independente.
- As funções de propostas do MCP stdio chamavam a si próprias. Foram
  corrigidas para chamar o módulo de persistência, preservando os contratos.
- Os nove especialistas passam a receber contexto de leitura do mesmo
  MCP/Meta do utilizador autenticado. Há cache curto separado por dono.
  O motor local recebe contexto da sessão existente, sem recadastrar contas.
  Continuam sendo especialistas de chat; não há coordenação autônoma.
- O identificador opcional do Pixel usava `cakto-ID-paid`, diferente do
  CAPI `cakto-ID-purchase_approved`. O gerador foi alinhado. O checkout
  ainda precisa disponibilizar o ID real da transação; isso não é universal.
- O instalador Linux foi corrigido para não aninhar diretórios numa
  reinstalação, não copiar `.env`/propostas/virtualenv do desenvolvedor,
  preservar a configuração existente, usar o comando oficial npm do Codex,
  registrar MCP sem esconder erros e preparar um serviço systemd privado.
  Scripts shell têm finais de linha LF. O token do serviço fica em arquivo
  privado, não no journal. Não há porta pública ou acesso à VPS da dona.

## Evidência de validação

- Base Claude: 101 testes aprovados independentemente.
- Após as correções Python: 107 testes aprovados; um aviso de depreciação
  Starlette/AnyIO, sem falha funcional.
- Frontend: seis unidades JavaScript válidas, IDs únicos e ícones válidos.
- Navegador isolado: 29 verificações de regressão aprovadas. O teste
  adicional de ponte nativa simulada validou os nove botões e sua seleção
  de módulo/provedor/contexto. Isso não equivale a nove chamadas pagas reais.
- Claude e Codex responderam por execução real antes do ajuste final stdin;
  Claude também respondeu após stdin. Um teste Codex com limite de 35 s
  expirou: não se deve converter esse resultado em conexão aprovada.
- Build CI do commit `4ed6d97`: Windows e macOS aprovados no run
  https://github.com/crissuboy-arch/Meta-ads-/actions/runs/45688581175 .
  O CI da versão candidata inclui teste Rust que inicia o runtime real,
  consulta agentes com token, rejeita acesso sem token e encerra o filho.
  Usar os resultados do run correspondente ao SHA final, não um build antigo.
- Linux descartável: instalação e reinstalação concluíram; nove arquivos
  de agentes foram exportados, `.env` de teste preservado e nenhuma cópia
  `mcp/mcp` foi criada. Instalação das CLIs foi omitida explicitamente.
  O ambiente não iniciou systemd: isso não comprova disponibilidade 24h.

## Bloqueadores reais e limites para lançamento comercial

1. Validar o instalador do SHA final e a ponte nativa; um build anterior
   verde não certifica arquivos alterados depois. O instalador abre a URL
   hospedada: antes da publicação, ela ainda apresenta o frontend de main.
2. Homologar pagamentos e concessão/revogação de plano. Não havia comprador
   Cakto ativo demonstrado no banco; um rótulo profissional não comprova
   compra. Os segredos de webhook devem ser conferidos pelo operador.
   A verificação Hotmart/Cakto permanece condicional à configuração e ao
   formato; outros formatos genéricos não têm assinatura equivalente.
3. Homologar conta/Pixel/token e event_id com evento de teste autorizado.
   Reenvio sequencial tem testes; concorrência entre instâncias Vercel não
   ganhou garantia transacional nesta auditoria, que não altera o banco.
4. Antes de anunciar macOS comercial: testar instalação, Gatekeeper,
   abertura, autenticação e retomada num Mac real; obter Developer ID e
   notarização. O artefato observado é Apple Silicon, não prova Intel.
5. Windows sem assinatura foi confirmado. Assinatura/reputação e política
   de distribuição precisam ser resolvidas antes de prometer instalação
   comercial sem advertências. Não se contornam proteções do sistema.
6. Validar reinício, boot, autenticação das CLIs e serviço systemd numa
   máquina Linux descartável com systemd antes de anunciar o modo 24h.

Não se comprovou nesta máquina uma consulta real dos nove agentes através
da chave MCP pessoal: o cliente Claude local não tinha essa conexão
configurada. A chave existente não foi regenerada. Não se deve pedir novo
cadastro de Meta/Supabase, nem confundir inventário com token válido.

## Opcionais e autorização comercial

OpenCode estava ausente: não anunciar inferência aprovada sem instalação
e autenticação próprias. Coordenação autônoma, Hubla e OpenBot não foram
implementados. Hubla pode ser integrada futuramente com eventos de teste,
token de webhook e adaptação de estados/idempotência/planos.

Codex usa Apache-2.0; OpenCode usa MIT, respeitando avisos e termos dos
modelos. A política atual do Claude Code permite produtos de terceiros
sob termos comerciais e condições: binário intacto, métodos oficiais de
login disponíveis, autenticação própria de cada utilizador e sem revenda
do consumo de Claude. Isso não autoriza compartilhar assinaturas.
OpenBot/nightly-labs requer licença comercial para o uso comercial do seu
código; a referência visual não transforma o produto numa redistribuição.
Não foi demonstrado contrato/licença paga de OpenBot nesta auditoria.

Fontes oficiais verificadas:
- https://code.claude.com/docs/en/legal-and-compliance
- https://learn.chatgpt.com/docs/app-server
- https://github.com/openai/codex/blob/main/LICENSE
- https://github.com/anomalyco/opencode/blob/dev/LICENSE
- https://github.com/nightly-labs/openbot/blob/main/LICENSE
- https://hubla.gitbook.io/docs/webhooks/introducao
- https://developer.apple.com/developer-id/
- https://learn.microsoft.com/windows/apps/package-and-deploy/code-signing-options

## Publicação e rollback, somente após autorização

1. Conferir SHA final, CI e artefatos; fazer checkpoint do main/deploy atual.
2. Concluir as homologações externas pendentes e registrar aprovação visual.
3. Revisar/mesclar a branch aprovada, sem migração ou mudança de credenciais.
4. Publicar/promover no MESMO projeto `meta-ads-unmc`; manter ambos os aliases.
5. Conferir login, dados por dono, planos, Meta, tracking, agentes e desktop.
   Não disparar campanha, compra ou evento real como simples health check.
6. Em regressão crítica, promover de volta o deploy de checkpoint no mesmo
   projeto. Reverter código por commit se necessário, sem apagar dados.
   Instalar novamente o pacote desktop anterior se o defeito for nativo,
   preservando o perfil/autenticação do utilizador.

O relatório local entregue com os artefatos registra os resultados finais
do CI e os caminhos dos instaladores efetivamente baixados.
