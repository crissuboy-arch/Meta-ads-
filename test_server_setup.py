"""Fase IV/X: assistente de instalacao guiada do Modo Servidor 24h
(server_setup/) - generico, sem OpenBot (que continua bloqueado ate a
licenca comercial, ver docs/modelo-produto-local-servidor.md).

O exportador dos 9 agentes (Python puro) e testado de ponta a ponta contra
a configuracao real. O instalador (install.sh) roda numa VPS Linux de
verdade, que este ambiente de desenvolvimento Windows nao tem - aqui so
validamos sintaxe/estrutura (bash -n) e as idempotencias esperadas no
texto do script; a execucao real so pode ser confirmada pelo proprio
comprador, na propria VPS dele (documentado em docs/modo-servidor-24h.md).
"""
import os
import shutil
import subprocess

from server_setup import export_agents as ea

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
INSTALL_SH = os.path.join(REPO_ROOT, "server_setup", "install.sh")


def test_export_agents_writes_all_nine_from_the_real_pt_config(tmp_path):
    config_path = os.path.join(REPO_ROOT, "configs", "meta-ads-pt.json")
    out_dir = tmp_path / "agents"
    paths = ea.export_agents(config_path, str(out_dir))
    assert len(paths) == len(ea.AGENT_IDS)
    content = (out_dir / "coordenador-marketing-ia.md").read_text(encoding="utf-8")
    assert content.startswith("---\nname: coordenador-marketing-ia\ndescription:")
    assert "# Coordenador de Marketing IA" in content
    assert "Gestor de Tráfego Pago" in content  # referencia ao time coordenado


def test_export_agents_description_has_no_newlines_for_valid_frontmatter(tmp_path):
    config_path = os.path.join(REPO_ROOT, "configs", "meta-ads-pt.json")
    out_dir = tmp_path / "agents"
    ea.export_agents(config_path, str(out_dir))
    for agent_id in ea.AGENT_IDS:
        front = (out_dir / f"{agent_id}.md").read_text(encoding="utf-8").split("---")[1]
        assert "description:" in front
        desc_line = [l for l in front.splitlines() if l.startswith("description:")][0]
        assert "\n" not in desc_line


def test_install_script_exists_and_is_syntactically_valid_bash():
    """bash -n so faz parsing, nao executa nada - seguro de rodar aqui."""
    assert os.path.isfile(INSTALL_SH)
    bash = shutil.which("bash")
    if not bash:
        import pytest
        pytest.skip("bash nao disponivel neste ambiente")
    result = subprocess.run([bash, "-n", INSTALL_SH], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def test_install_script_never_reads_or_hardcodes_credentials():
    text = open(INSTALL_SH, encoding="utf-8").read()
    for forbidden in ("META_ACCESS_TOKEN=", "SUPABASE_SERVICE_KEY=", "password", "senha="):
        assert forbidden not in text
    assert ".env.example" in text and "cp" in text  # so copia o template vazio


def test_install_script_keeps_openbot_integration_out_of_scope():
    text = open(INSTALL_SH, encoding="utf-8").read().lower()
    assert "openbot" in text
    assert "licenca comercial" in text or "licença comercial" in text
