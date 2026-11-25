# Modelo definitivo do produto — Modo Local e Modo Servidor 24h

**Este documento é um plano de arquitetura, não uma implementação.** Registra
a decisão do produto e o caminho técnico para chegar lá, sem alterar o app
que já está consolidado (`handoff-tecnico.md`) e sem atrasar a entrega atual
para o redesign. Nenhum código deste repositório foi alterado para produzir
este documento.

## Decisão do produto (como definida pela própria dona do projeto)

Comercialização via plataforma tipo Hotmart, com instaladores Windows/macOS
e vídeos de configuração. Dois modos de uso:

- **Modo 1 — Local:** o comprador instala o app no próprio computador,
  conecta suas próprias contas de IA (ChatGPT/Codex, Claude Code, APIs
  próprias) pelos mecanismos oficiais de cada fornecedor, conecta sua conta
  Meta Ads, e usa os nove agentes dentro da plataforma. **Não pode exigir
  VPS.**
- **Modo 2 — Servidor 24h:** o comprador usa a própria VPS para manter os
  agentes disponíveis o tempo todo, com um assistente de instalação guiada
  (futuro) que configura o servidor, instala componentes, autentica contas e
  liga os agentes. Acesso também por WhatsApp/Telegram quando suportado.
  A integração com o OpenBot (mecanismo já testado nesta conversa, ver
  `../../openbot-poc/`) só entra aqui, e só **mediante aquisição da licença
  comercial do OpenBot** junto à nightly-labs — a licença atual
  (PolyForm Noncommercial) não cobre uso comercial.

Requisito transversal: **cada comprador usa suas próprias credenciais num
ambiente isolado**, nunca um backend ou assinatura compartilhada entre
compradores. A VPS usada nos testes desta conversa continua exclusiva da
dona do projeto — nunca serve de backend para compradores.

## Por que isso NÃO é a mesma coisa que a Central de IA atual

A Central de IA de hoje (`app_core.py`, Fase A) já suporta múltiplos
provedores (OpenAI/Gemini/OpenRouter/Anthropic), mas por **chave de API**
(BYOK), num backend **compartilhado** (Vercel + Supabase, um projeto só para
todos os compradores — ver `handoff-tecnico.md`, seção "Isolamento entre
compradores"). Login com assinatura pessoal (ChatGPT Plus, Claude Pro/Max) —
diferente de chave de API — é, pelos termos de uso de OpenAI/Anthropic,
pensado para uso **individual**, não para autenticar dentro de um backend
multi-cliente de terceiros. É por isso que o app hoje usa chave de API, e é
por isso que o Modo 1/Modo 2 têm que rodar **no ambiente do próprio
comprador** (computador dele, ou VPS dele), nunca na Vercel compartilhada.

Isso já foi confirmado tecnicamente nesta mesma VPS, nesta conversa: o
OpenBot instalado lá só funciona porque é uma instalação de uma pessoa só
(a dona do projeto) com as próprias contas — não é multi-tenant.

## Estado atual vs. o que falta, por peça

| Peça | Hoje | Modo 1 (Local) precisa | Modo 2 (Servidor) precisa |
|---|---|---|---|
| Instalador desktop (`src-tauri/`) | Casca fina — só abre a URL de produção na Vercel (`docs/app-instalavel.md`) | Passar a rodar um backend/agente **local** dentro do instalador (não só abrir o site) — maior mudança técnica pendente | Não se aplica (o agente roda na VPS do comprador) |
| Login ChatGPT/Codex, Claude Code | Não existe (só chave de API) | Rodar o CLI oficial (`claude`, `codex`) **no computador do comprador**, com login OAuth oficial de cada um — exatamente o que foi validado nesta VPS para a dona do projeto | Mesmo mecanismo, rodando na VPS do comprador |
| Meta Ads | Já funciona (OAuth próprio, por comprador, já isolado por `owner_email`) | Reaproveitar sem mudança | Reaproveitar sem mudança |
| Os nove agentes | Prontos como subagentes do Claude Code (`../../openbot-poc/agentes/*.md`), validados nesta VPS | Empacotar os mesmos arquivos dentro do instalador local | Mesmo pacote, copiado pelo instalador guiado da VPS |
| MCP (`mcp/server.py`) | Já roda local via stdio; validado nesta VPS com venv próprio e `claude mcp add` | Empacotar Python + dependências dentro do instalador (ou usar um binário standalone) | Já é o mesmo padrão testado na VPS desta conversa |
| Assistente de instalação guiada (Modo 2) | Não existe | — | A construir: wizard que faz na VPS do comprador o que foi feito manualmente aqui (Docker, venv, CLIs, agentes, MCP) |
| Integração OpenBot comercial | PoC pessoal, licença não-comercial | — | Bloqueada até a compra da licença comercial junto à nightly-labs |
| WhatsApp/Telegram | Não existe | Futuro, fora deste escopo agora | Futuro, fora deste escopo agora |

## O que explicitamente NÃO entra agora (fora de escopo desta rodada)

- Nenhuma tela de "login com ChatGPT/Claude" na Vercel compartilhada —
  violaria os termos de uso dos fornecedores e o próprio requisito de
  isolamento por comprador.
- Nenhuma reescrita do app existente (dashboard, Meta Ads, Supabase, Vercel,
  Athena, MCP, financeiro, rastreamento, pixels, webhooks) — tudo continua
  como está, testado (51 testes, `pytest -q`, 100% passando nesta revisão).
- Nenhuma integração comercial com o OpenBot sem a licença paga.
- Nenhum assistente de instalação guiada ainda — é o próximo grande bloco de
  trabalho, não cabe nesta rodada sem atrasar o redesign.

## Próximo passo real (depois do redesign do Codex)

1. Prototipar o Modo 1: um backend local mínimo (Python local, mesma base de
   `mcp/server.py` + os nove agentes) embutido no instalador Tauri/outra
   casca, substituindo a "casca fina" atual.
2. Validar com o fornecedor (OpenAI/Anthropic) se o fluxo de login oficial
   do CLI funciona de forma redistribuível dentro de um instalador de
   terceiros (hoje validado manualmente nesta VPS, mas isso foi uma
   instalação direta do CLI oficial, não um instalador empacotado para
   terceiros — vale confirmar que não há restrição adicional de
   redistribuição antes de embutir no instalador comercial).
3. Só depois disso, desenhar o assistente de instalação guiada do Modo 2.
