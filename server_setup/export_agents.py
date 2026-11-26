"""Modo Servidor 24h: gera os arquivos de subagente do Claude Code
(~/.claude/agents/*.md) a partir da MESMA fonte de verdade dos 9 agentes
(configs/meta-ads-pt.json, portada na Fase II) - para o assistente de
instalacao guiada da VPS do comprador (install.sh) nao duplicar o texto
dos prompts numa segunda copia que poderia divergir.

Mesmo formato ja usado e validado manualmente nesta conversa na VPS
pessoal (frontmatter name/description + corpo em markdown).
"""
import json
import os
import sys

AGENT_IDS = [
    "coordenador-marketing-ia",
    "gestor-trafego-pago",
    "analista-financeiro",
    "auditor-campanhas",
    "especialista-pixel-rastreamento",
    "especialista-copy-criativos",
    "pesquisador-mercado",
    "especialista-funis-ofertas",
    "mentor-trafego-pago",
]


def build_agent_markdown(agent_id, label, desc, prompt):
    description = desc.replace("\n", " ").strip()
    return f"---\nname: {agent_id}\ndescription: {description}\n---\n\n# {label}\n\n{prompt}\n"


def export_agents(config_path, out_dir):
    with open(config_path, encoding="utf-8") as f:
        cfg = json.load(f)
    tools_by_id = {t["id"]: t for t in cfg.get("tools", [])}
    prompts = cfg.get("prompts", {})
    os.makedirs(out_dir, exist_ok=True)
    written = []
    for agent_id in AGENT_IDS:
        tool = tools_by_id.get(agent_id)
        prompt = prompts.get(agent_id)
        if not tool or not prompt:
            continue
        md = build_agent_markdown(agent_id, tool.get("label", agent_id), tool.get("desc", ""), prompt)
        path = os.path.join(out_dir, agent_id + ".md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(md)
        written.append(path)
    return written


def _default_config_path():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(os.path.dirname(here), "configs", "meta-ads-pt.json")


if __name__ == "__main__":
    config_path = sys.argv[1] if len(sys.argv) > 1 else _default_config_path()
    out_dir = sys.argv[2] if len(sys.argv) > 2 else "./claude-agents"
    for path in export_agents(config_path, out_dir):
        print(path)
