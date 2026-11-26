# Modo Servidor 24h — assistente de instalação guiada (genérico, sem OpenBot)

Acompanha `server_setup/` (Fase IV/X da finalização funcional). Mesma regra
do resto do projeto: separa o que foi confirmado por execução real do que
ainda depende do próprio comprador testar na própria VPS.

## O que existe

- `server_setup/export_agents.py` — gera os 9 arquivos de subagente do
  Claude Code (`~/.claude/agents/*.md`) a partir da mesma fonte de verdade
  da Fase II (`configs/meta-ads-pt.json`), sem duplicar texto de prompt.
  **Testado de ponta a ponta** (`test_server_setup.py`) contra a
  configuração real do repositório.
- `server_setup/install.sh` — roteiriza, de forma idempotente, exatamente
  o que foi feito manualmente nesta conversa na VPS pessoal: dependências
  do sistema, usuário de serviço dedicado, CLIs oficiais (`claude`,
  `codex`), venv do MCP, cópia do `mcp/`+`local_engine/`, publicação dos 9
  agentes, e registro do servidor MCP no Claude Code. **Nunca** lê, pede
  ou preenche credenciais — `.env` fica vazio de propósito, e o login das
  CLIs é sempre feito depois, pessoalmente, pelo próprio comprador.

## O que está confirmado por teste automatizado

- `export_agents.py`: roda de verdade contra `configs/meta-ads-pt.json`
  nesta conversa — os 9 arquivos saem com frontmatter válido
  (`name`/`description` sem quebra de linha) e corpo completo.
- `install.sh`: sintaxe validada com `bash -n` (parsing real, sem
  executar nada) — confirma que o script não tem erro de sintaxe bash.
  Também confirmado por leitura de texto: nunca contém credencial
  hardcoded, só copia o `.env.example` vazio, e mantém a integração com o
  OpenBot fora do script.

## O que NÃO está confirmado — precisa de uma VPS Linux real

Este ambiente de desenvolvimento é Windows, sem acesso a uma VPS Ubuntu/
Debian descartável para rodar `install.sh` de ponta a ponta. **O script
nunca foi executado contra um servidor real.** Antes de oferecer a
compradores, rode pessoalmente numa VPS de teste e confirme:

1. `apt-get install` dos pacotes do sistema completa sem erro na
   distribuição real do comprador (testado aqui só com Ubuntu/Debian em
   mente — outras distros podem precisar de ajuste, ex.: `dnf`/`yum`).
2. Os instaladores oficiais (`claude.ai/install.sh`,
   `chatgpt.com/codex/install.sh`) continuam funcionando sem interação —
   já confirmados manualmente nesta conversa, numa execução anterior, na
   VPS pessoal, mas podem mudar do lado do fornecedor sem aviso.
3. `claude mcp add --scope user ...` registra o servidor corretamente
   quando rodado como o usuário de serviço (`su - ofensiva -c ...`), não
   como root — mesmo padrão já validado manualmente na VPS pessoal, mas
   não dentro deste script específico.
4. Permissões de arquivo (`chown -R`) resultam num ambiente que o usuário
   de serviço consegue de fato ler/escrever (venv, `.env`, agentes).

## Por que não tem Docker nem OpenBot aqui

A instalação manual anterior usava Docker porque o OpenBot (ferramenta de
terceiros) é distribuído como imagem Docker. Este assistente genérico não
depende do OpenBot — instala as CLIs oficiais e o MCP diretamente na VPS,
em um usuário de sistema dedicado, sem Docker. A integração com o OpenBot
em si (mencionada no pedido original) continua **fora de escopo** até a
compra da licença comercial junto à nightly-labs, conforme já registrado
em `modelo-produto-local-servidor.md`.

## Próximo passo real

Testar `install.sh` numa VPS de teste descartável, corrigir o que a
execução real revelar, e só então documentar como "testado" no relatório
final do produto — não antes.
