#!/usr/bin/env bash
# Modo Servidor 24h - assistente de instalacao guiada (generico, SEM OpenBot).
#
# Roda na VPS do PROPRIO comprador (Ubuntu/Debian), nunca na VPS da dona do
# projeto. Faz, de forma automatizada e idempotente, o que foi validado
# manualmente nesta conversa numa VPS pessoal: instala as CLIs oficiais de
# IA, prepara o MCP e publica os 9 agentes como subagentes do Claude Code.
#
# Integracao com o OpenBot continua FORA deste script, de proposito - exige
# a licenca comercial da nightly-labs antes de poder ser oferecida a
# compradores (ver docs/modelo-produto-local-servidor.md).
#
# Uso:
#   sudo ./install.sh
#
# O que o script NUNCA faz: nao pede nem guarda email/senha de nenhum
# provedor (o login das CLIs e sempre feito depois, pessoalmente, pelo
# proprio comprador), nao preenche credenciais do Meta Ads/Supabase (deixa
# .env vazio de proposito).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
SERVICE_USER="${OFENSIVA_SERVICE_USER:-ofensiva}"
INSTALL_DIR="/home/${SERVICE_USER}/ofensiva-trafego-ia"

log() { echo "[ofensiva-modo-servidor] $*"; }

if [ "$(id -u)" -ne 0 ]; then
    echo "Execute como root (sudo ./install.sh)." >&2
    exit 1
fi

log "1/7 - Dependencias do sistema (idempotente)"
apt-get update -qq
apt-get install -y -qq python3 python3-venv curl git >/dev/null

log "2/7 - Usuario de servico dedicado"
if ! id -u "$SERVICE_USER" >/dev/null 2>&1; then
    useradd -m -s /bin/bash "$SERVICE_USER"
    log "Usuario '$SERVICE_USER' criado."
else
    log "Usuario '$SERVICE_USER' ja existe - nada a fazer."
fi

log "3/7 - CLIs oficiais de IA (claude, codex)"
su - "$SERVICE_USER" -c '
set -e
if ! command -v claude >/dev/null 2>&1; then
    curl -fsSL https://claude.ai/install.sh | bash
else
    echo "claude ja instalado."
fi
if ! command -v codex >/dev/null 2>&1; then
    curl -fsSL https://chatgpt.com/codex/install.sh | sh
else
    echo "codex ja instalado."
fi
'

log "4/7 - Copiando o MCP e o motor local para $INSTALL_DIR"
mkdir -p "$INSTALL_DIR"
cp -r "$REPO_DIR/mcp" "$INSTALL_DIR/mcp"
cp -r "$REPO_DIR/local_engine" "$INSTALL_DIR/local_engine"
cp -r "$REPO_DIR/configs" "$INSTALL_DIR/configs"
if [ ! -f "$INSTALL_DIR/mcp/.env" ]; then
    cp "$INSTALL_DIR/mcp/.env.example" "$INSTALL_DIR/mcp/.env"
    log "mcp/.env criado vazio de proposito - preencha pessoalmente (ver docs/motor-local.md)."
fi
chown -R "$SERVICE_USER:$SERVICE_USER" "$INSTALL_DIR"

log "5/7 - Ambiente Python do MCP"
su - "$SERVICE_USER" -c "
set -e
if [ ! -d '$INSTALL_DIR/mcp-venv' ]; then
    python3 -m venv '$INSTALL_DIR/mcp-venv'
fi
'$INSTALL_DIR/mcp-venv/bin/pip' install -q --upgrade pip
'$INSTALL_DIR/mcp-venv/bin/pip' install -q -r '$INSTALL_DIR/mcp/requirements.txt'
"

log "6/7 - Publicando os 9 agentes como subagentes do Claude Code"
su - "$SERVICE_USER" -c "
mkdir -p ~/.claude/agents
python3 '$SCRIPT_DIR/export_agents.py' '$INSTALL_DIR/configs/meta-ads-pt.json' ~/.claude/agents
"

log "7/7 - Registrando o servidor MCP no Claude Code"
su - "$SERVICE_USER" -c "
claude mcp add --scope user ofensiva-trafego-ia -- '$INSTALL_DIR/mcp-venv/bin/python' '$INSTALL_DIR/mcp/server.py' || true
"

cat <<EOF

Instalacao automatizada concluida. Proximos passos (voce mesmo, pessoalmente):

1) Autentique as CLIs com as SUAS proprias contas:
   su - $SERVICE_USER -c claude
   su - $SERVICE_USER -c codex

2) Preencha $INSTALL_DIR/mcp/.env com as SUAS credenciais (Meta/Supabase):
   nano $INSTALL_DIR/mcp/.env

3) Confirme a conexao:
   su - $SERVICE_USER -c 'claude mcp list'

A integracao com o OpenBot NAO faz parte deste script - exige a licenca
comercial da nightly-labs antes de poder ser oferecida comercialmente (ver
docs/modelo-produto-local-servidor.md).
EOF
