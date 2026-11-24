"""Fase C: tool 'gestor-mentor-trafego' presente e correto em todos os
idiomas, e o system prompt compoe de verdade pelo pipeline real do app
(sem mock) - usa config.py/app_core.py tal como em producao.
"""
import os

os.environ.setdefault("NVIDIA_API_KEY", "dummy-test-key")

import config
import app_core

TOOL_ID = "gestor-mentor-trafego"
LANGS = ["en", "pt", "es", "fr", "tr", "de"]


def test_tool_and_prompt_exist_in_every_language():
    for lang in LANGS:
        cfg = config.get_lang_config(lang=lang)
        ids = [t["id"] for t in cfg["tools"]]
        assert TOOL_ID in ids, f"missing tool in {lang}"
        assert cfg["prompts"].get(TOOL_ID), f"missing prompt in {lang}"


def test_system_prompt_composes_with_module_brief():
    for lang in LANGS:
        out = app_core._compose_module_system(TOOL_ID, lang=lang)
        assert "MODULE BRIEF" in out
        assert len(out) > len(app_core._BASE_SYSTEM_EN)


def test_mentor_prompt_requires_grounded_data_and_explanation():
    """A regra central do pedido do usuario: nunca inventar metrica, e
    sempre explicar o porque (mentoria)."""
    cfg = config.get_lang_config(lang="pt")
    prompt = cfg["prompts"][TOOL_ID].lower()
    assert "nunca invente" in prompt or "never invent" in prompt
    assert "risco" in prompt
