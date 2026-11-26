"""Fase II (finalizacao funcional): os nove agentes especialistas passam a
ser modulos reais de chat, pelo mesmo mecanismo que ja funciona para
'gestor-mentor-trafego' (prompts/tools em configs/meta-ads*.json + o
pipeline real de app_core._compose_module_system - sem motor novo).

Fonte dos papeis: openbot-poc/agentes/*.md (fora deste repo, uso pessoal/
PoC). Aqui eles sao portados para dentro do app principal como
modulos de chat de verdade, nao apenas texto decorativo na UI.
"""
import os

os.environ.setdefault("NVIDIA_API_KEY", "dummy-test-key")

import config
import app_core

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
# en/pt tem corpo de prompt proprio no idioma; es/fr/tr/de reaproveitam o
# texto em ingles por enquanto (documentado em docs/, nao e uma lacuna
# escondida) - so label/desc sao traduzidos nesses quatro.
LANGS = ["en", "pt", "es", "fr", "tr", "de"]


def test_all_nine_agents_exist_as_tools_and_prompts_in_every_language():
    for lang in LANGS:
        cfg = config.get_lang_config(lang=lang)
        ids = [t["id"] for t in cfg["tools"]]
        for agent_id in AGENT_IDS:
            assert agent_id in ids, f"missing tool {agent_id} in {lang}"
            assert cfg["prompts"].get(agent_id), f"missing prompt {agent_id} in {lang}"


def test_each_agent_system_prompt_composes_via_the_real_chat_pipeline():
    """O mesmo _compose_module_system usado por /api/chat - nao mock."""
    for lang in LANGS:
        for agent_id in AGENT_IDS:
            out = app_core._compose_module_system(agent_id, lang=lang)
            assert "MODULE BRIEF" in out
            assert len(out) > len(app_core._BASE_SYSTEM_EN)


def test_coordenador_references_the_other_eight_specialists():
    cfg = config.get_lang_config(lang="pt")
    prompt = cfg["prompts"]["coordenador-marketing-ia"]
    for keyword in ["Gestor de Tráfego", "Analista Financeiro", "Auditor de Campanhas",
                    "Pixel", "Copy", "Mercado", "Funis", "Mentor"]:
        assert keyword in prompt, f"coordenador nao menciona: {keyword}"


def test_gestor_trafego_requires_confirmation_before_write_actions():
    """Regra de seguranca: o agente de trafego nao pode sugerir ativar
    campanha sem confirmacao explicita - espelha a trava real do MCP
    (WRITE_ACTIONS_ENABLED + user_confirmed) corrigida na Fase I."""
    for lang in ["pt", "en"]:
        cfg = config.get_lang_config(lang=lang)
        prompt = cfg["prompts"]["gestor-trafego-pago"].lower()
        assert "confirma" in prompt or "confirm" in prompt
        assert "write_actions_enabled" in prompt


def test_auditor_never_executes_only_diagnoses():
    for lang in ["pt", "en"]:
        cfg = config.get_lang_config(lang=lang)
        prompt = cfg["prompts"]["auditor-campanhas"].lower()
        assert "nunca pause" in prompt or "never pause" in prompt


def test_mentor_prompt_still_requires_grounded_data_and_explanation():
    cfg = config.get_lang_config(lang="pt")
    prompt = cfg["prompts"]["mentor-trafego-pago"].lower()
    assert "nunca invente" in prompt or "never invent" in prompt
    assert "risco" in prompt
