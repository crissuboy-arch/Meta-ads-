# Motor local (Modo Local) — o que está confirmado vs. o que precisa de teste pessoal

Este documento acompanha `local_engine/` e as mudanças em `src-tauri/` da
Fase III/IV. Segue a mesma regra do resto do projeto: nada aqui é
apresentado como "operacional" sem teste real — e aqui há duas categorias
de teste real diferentes, por isso a separação explícita abaixo.

## Confirmado por teste automatizado (`test_local_engine.py`, roda em CI/local)

- **Detecção de CLIs** (`engine.detect_clis`): 100% real, só `shutil.which`
  no PATH. Testado neste próprio ambiente de desenvolvimento rodando o
  servidor de verdade (não só os testes mockados) — `claude` (instalado
  via npm nesta máquina) foi detectado corretamente como presente, e
  `codex`/`opencode` (não instalados aqui) como ausentes.
- **Carregar os agentes** (`engine.load_agents`): lê direto de
  `configs/meta-ads*.json`, a mesma fonte de verdade da Fase II — sem
  duplicar texto. Confirmado rodando o servidor real: os 10 módulos (9
  especialistas + `gestor-mentor-trafego`) aparecem com prompt completo.
- **Repasse MCP** (`engine.mcp_relay`): chama o conector `/mcp/{key}` que
  já existe e já está em produção (mesmo da tela "Conectar Claude"),
  reaproveitando a trava de escrita corrigida na Fase I. Testado com
  transporte HTTP mockado: ferramentas de escrita são bloqueadas sem
  `approved=true` explícito; ferramentas de leitura passam direto.
- **BYOK** (`engine.byok_call`): mesmo formato de requisição HTTP já usado
  e testado em `app_core._prov_text` para Anthropic/OpenAI/OpenRouter/
  Gemini — só portado para não duplicar um segundo formato divergente.
  Testado com transporte mockado.
- **Servidor HTTP** (`local_engine/server.py`): roda só em `127.0.0.1`
  (loopback), nunca expõe a porta publicamente. Testado de verdade nesta
  conversa: processo real, subido, respondido via `curl` em `/health`,
  `/agents` e `/providers/detect`.

## Assumido, NÃO confirmado por execução real — precisa da sua validação pessoal

- **Comando não-interativo exato de `codex` e `opencode`**
  (`engine.CLI_EXEC`): `codex exec --skip-git-repo-check "<prompt>"` e
  `opencode run "<prompt>"` são o melhor entendimento a partir da
  documentação pública consultada nesta conversa, mas **nenhum dos dois
  CLIs está instalado neste ambiente de desenvolvimento** — não executei
  nenhum dos dois de verdade. Antes de depender disso: instale `codex`/
  `opencode` (mesmos instaladores oficiais já usados na VPS pessoal nesta
  conversa) e rode manualmente, por exemplo:
  ```
  codex exec --skip-git-repo-check "responda apenas: OK"
  opencode run "responda apenas: OK"
  ```
  Se o comando real for diferente, ajuste `CLI_EXEC` em
  `local_engine/engine.py` — é uma função isolada, a troca não afeta o
  resto do motor.
- **Abrir terminal autenticado por plataforma** (`engine.TERMINAL_CMD`):
  a construção do comando para Windows (`cmd /c start cmd /k <cli>`) foi
  testada manualmente nesta conversa (abre, de fato, um novo terminal
  Windows rodando o comando). As variantes macOS (`osascript`/Terminal) e
  Linux (`x-terminal-emulator`) seguem o padrão documentado dessas
  plataformas, mas não foram testadas aqui porque este ambiente de
  desenvolvimento é Windows — confirme numa máquina Mac/Linux real antes
  de anunciar como testado nesses sistemas.
- **Capacidade remota do Tauri** (`src-tauri/capabilities/default.json`):
  a janela do app carrega uma URL remota (`app.ofensivacriativa.com`), e o
  Tauri v2 só injeta `window.__TAURI__`/permite `invoke()` em conteúdo
  remoto se o domínio estiver explicitamente na lista `remote.urls` de uma
  capability — sem isso, nenhum dos comandos novos (detecção de CLI, motor
  local) funcionaria a partir da página hospedada. Escrito seguindo a
  documentação oficial do Tauri v2, mas **não pôde ser confirmado
  rodando o app de verdade** (exigiria a build compilada - ver item
  abaixo). Primeira coisa a verificar manualmente ao testar o instalador.
- **Processo órfão ao fechar o app**: `start_local_engine` guarda o
  processo filho no estado do Tauri, mas o `main.rs` atual não mata esse
  processo automaticamente ao fechar a janela (removido de propósito desta
  primeira versão para reduzir risco de erro de compilação que eu não
  conseguiria depurar sem `cargo` instalado aqui). Por enquanto, o
  frontend deve chamar `stop_local_engine` antes de navegar para fora do
  Modo Local; fechar o app sem isso pode deixar um processo Python
  pendente — aceitável para uso pessoal nesta fase, mas listar como
  pendência antes de distribuir comercialmente.
- **Compilação do lado Rust/Tauri** (`src-tauri/src/main.rs`): este
  ambiente de desenvolvimento não tem `cargo`/`rustc` instalado, então o
  código Rust novo não foi compilado localmente. A validação real vem do
  GitHub Actions (`redesign-build.yml`, que builda em `windows-latest` e
  `macos-latest` com Rust/Tauri de verdade) — adicionei a branch
  `finalizacao-funcional` ao gatilho desse workflow justamente para isso.
  **Não anuncie o motor local como "funcionando no instalador" até essa
  build do CI terminar com sucesso.**
- **Empacotamento para distribuição comercial**: esta primeira versão do
  motor local depende do Python do sistema do próprio comprador
  (`local_engine/` não tem dependências externas de propósito, só
  biblioteca padrão). Um comprador sem Python instalado não conseguirá
  rodar o motor local ainda — empacotar um runtime Python próprio dentro
  do instalador (PyInstaller/Nuitka ou similar) é trabalho futuro, fora
  desta rodada, e deve ser registrado como pendência no relatório final.

## Por que o Meta Ads não tem OAuth duplicado aqui

De propósito: o motor local **não** reimplementa login do Meta nem chama a
Graph API diretamente. Ele fala com o conector MCP que já existe no app
hospedado (`/mcp/{key}`), usando a mesma chave pessoal já gerada na tela
"Conectar Claude". Isso evita duplicar OAuth do Meta/Graph API em dois
lugares e mantém uma única trilha de auditoria/segurança (a mesma
corrigida na Fase I) para qualquer chamada de escrita, venha ela do Claude
Code, do motor local, ou da própria tela web.
