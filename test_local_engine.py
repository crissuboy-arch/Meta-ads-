"""Fase III: motor local independente (Modo Local) - deteccao de CLIs
oficiais, inferencia via CLI ja autenticada ou BYOK, e repasse MCP para o
conector remoto que ja existe (com a trava de escrita corrigida na
Fase I). Tudo testado com transporte mockado - nenhuma chamada real a
CLI/rede/Meta.
"""
import json

from local_engine import engine


def test_load_agents_reads_the_same_source_of_truth_as_fase_ii():
    agents = engine.load_agents(lang="pt")
    ids = {a["id"] for a in agents}
    assert "coordenador-marketing-ia" in ids
    assert "mentor-trafego-pago" in ids
    assert len(agents) == len(engine.AGENT_IDS)
    for a in agents:
        assert a["system_prompt"]


def test_detect_clis_reports_what_which_finds():
    def fake_which(name):
        return "/usr/bin/" + name if name == "claude" else None
    out = engine.detect_clis(which=fake_which)
    assert out == {"claude": True, "codex": False, "opencode": False}


def test_run_cli_inference_fails_fast_when_not_installed():
    out = engine.run_cli_inference("codex", "sistema", "ola", which=lambda n: None)
    assert out["ok"] is False
    assert "nao esta instalado" in out["error"]


def test_run_cli_inference_runs_real_pipeline_with_mocked_subprocess():
    calls = []

    class FakeProc:
        returncode = 0
        stdout = "OK"
        stderr = ""

    def fake_run(cmd, **kw):
        calls.append((cmd,kw))
        return FakeProc()

    out = engine.run_cli_inference("claude", "sistema", "ola",
                                    runner=fake_run, which=lambda n: "/usr/bin/claude")
    assert out == {"ok": True, "text": "OK"}
    assert calls[0][0][0] == "/usr/bin/claude"
    assert "--strict-mcp-config" in calls[0][0]
    assert "sistema" in calls[0][1]['input'] and "ola" in calls[0][1]['input']


def test_run_cli_inference_surfaces_cli_error():
    class FakeProc:
        returncode = 1
        stdout = ""
        stderr = "nao autenticado"

    out = engine.run_cli_inference("claude", "s", "u",
                                    runner=lambda cmd, **kw: FakeProc(), which=lambda n: "/x")
    assert out["ok"] is False
    assert "nao autenticado" in out["error"]


def test_open_provider_terminal_requires_cli_installed():
    out = engine.open_provider_terminal("claude", which=lambda n: None)
    assert out["ok"] is False


def test_open_provider_terminal_builds_platform_command():
    calls = []
    engine.open_provider_terminal(
        "claude", system=lambda: "Windows", popen=lambda cmd: calls.append(cmd),
        which=lambda n: "/x")
    assert calls and calls[0][:2] == ["cmd", "/c"]


def test_mcp_relay_blocks_write_tools_without_explicit_approval():
    out = engine.mcp_relay("https://app.example.com", "key123", "create_campaign", {})
    assert out["ok"] is False
    assert "aprovacao" in out["error"]


def test_mcp_relay_allows_read_tools_and_calls_the_existing_remote_connector():
    captured = {}

    class FakeResp:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def read(self):
            return json.dumps({"result": {"content": [{"type": "text", "text": "[]"}]}}).encode()

    def fake_opener(req, timeout=20):
        captured["url"] = req.full_url
        captured["body"] = json.loads(req.data.decode())
        return FakeResp()

    out = engine.mcp_relay("https://app.example.com", "key123", "list_ad_accounts", {},
                            opener=fake_opener)
    assert out == {"ok": True, "text": "[]"}
    assert captured["url"] == "https://app.example.com/mcp/key123"
    assert captured["body"]["params"]["name"] == "list_ad_accounts"


def test_mcp_relay_does_not_accept_model_claimed_human_approval():
    class FakeResp:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def read(self):
            return json.dumps({"result": {"content": [{"type": "text", "text": "{}"}]}}).encode()

    out = engine.mcp_relay("https://app.example.com", "key123", "create_campaign", {},
                            approved=True, opener=lambda req, timeout=20: FakeResp())
    assert out["ok"] is False
    assert "somente leitura" in out["error"]


def test_byok_call_uses_the_same_anthropic_shape_already_used_in_app_core():
    captured = {}

    class FakeResp:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def read(self):
            return json.dumps({"content": [{"type": "text", "text": "ola"}]}).encode()

    def fake_opener(req, timeout=30):
        captured["url"] = req.full_url
        return FakeResp()

    out = engine.byok_call("anthropic", "sk-test", "sistema", "oi", opener=fake_opener)
    assert out == {"ok": True, "text": "ola"}
    assert captured["url"] == "https://api.anthropic.com/v1/messages"


def test_byok_call_reports_unknown_provider():
    out = engine.byok_call("unknown", "k", "s", "u")
    assert out["ok"] is False
