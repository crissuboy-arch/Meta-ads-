"""MCP module tests — all external calls mocked. No Meta, no Supabase needed."""
import json
import os
import sys
import tempfile

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import meta_api
from meta_api import MetaAPIError
import approvals


@pytest.fixture(autouse=True)
def _env(tmp_path, monkeypatch):
    monkeypatch.setenv("META_ACCESS_TOKEN", "TEST_TOKEN")
    monkeypatch.setenv("META_AD_ACCOUNT_ID", "12345")
    # force local-file fallback for proposals (no Supabase in tests)
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_SERVICE_KEY", raising=False)
    monkeypatch.setattr(approvals, "_local_path",
                        lambda: tmp_path / "proposals.local.json")
    yield


class _Resp:
    def __init__(self, payload, status=200):
        self._p, self.status_code = payload, status
        self.content = json.dumps(payload).encode()

    def json(self):
        return self._p

    def raise_for_status(self):
        if self.status_code >= 400:
            raise meta_api.requests.HTTPError(str(self.status_code))


def _mock_request(monkeypatch, payload=None, status=200, capture=None):
    payload = {"data": []} if payload is None else payload

    def fake(method, url, params=None, json=None, headers=None, timeout=None):
        if capture is not None:
            capture.append({"method": method, "url": url,
                            "params": params, "json": json})
        return _Resp(payload, status)

    monkeypatch.setattr(meta_api.requests, "request", fake)


# ------------------------------------------------------------- read tools

def test_list_campaigns_hits_account_endpoint(monkeypatch):
    cap = []
    _mock_request(monkeypatch, {"data": [{"id": "1"}]}, capture=cap)
    out = meta_api.list_campaigns()
    assert out == [{"id": "1"}]
    assert cap[0]["url"].endswith("/act_12345/campaigns")
    assert cap[0]["params"]["access_token"] == "TEST_TOKEN"


def test_meta_error_raised(monkeypatch):
    _mock_request(monkeypatch, {"error": {"code": 190, "message": "bad token"}},
                  status=400)
    with pytest.raises(MetaAPIError, match="190"):
        meta_api.list_campaigns()


def test_missing_token_fails_fast(monkeypatch):
    monkeypatch.delenv("META_ACCESS_TOKEN")
    with pytest.raises(MetaAPIError, match="META_ACCESS_TOKEN"):
        meta_api.list_campaigns()


# ------------------------------------------------------- approval gate

def test_propose_does_not_execute(monkeypatch):
    cap = []
    _mock_request(monkeypatch, capture=cap)  # would record any POST
    prop = approvals.propose_action(
        "create_campaign",
        {"name": "Teste R$50", "objective": "OUTCOME_SALES",
         "daily_budget_cents": 1000})
    assert prop["status"] == "pending"
    assert cap == []  # nothing hit the network
    rows = approvals.list_proposals("pending")
    assert len(rows) == 1 and rows[0]["status"] == "pending"


def test_unknown_action_rejected_at_propose():
    with pytest.raises(MetaAPIError, match="not allowed"):
        approvals.propose_action("delete_everything", {})


def test_approve_executes_once(monkeypatch):
    cap = []
    _mock_request(monkeypatch, {"id": "999"}, capture=cap)
    prop = approvals.propose_action(
        "set_status", {"object_id": "111", "status": "PAUSED"})
    res = approvals.approve_proposal(prop["proposal_id"])
    assert res["status"] == "executed"
    assert cap[0]["json"] == {"status": "PAUSED"}  # the real API call
    # second approval must refuse (no double spend)
    with pytest.raises(MetaAPIError, match="already decided"):
        approvals.approve_proposal(prop["proposal_id"])


def test_approve_nonexistent_refuses():
    with pytest.raises(MetaAPIError, match="not found"):
        approvals.approve_proposal("prop_nope")


def test_reject_never_executes(monkeypatch):
    cap = []
    _mock_request(monkeypatch, capture=cap)
    prop = approvals.propose_action(
        "set_status", {"object_id": "111", "status": "ACTIVE"})
    out = approvals.reject_proposal(prop["proposal_id"], "humano disse nao")
    assert out["status"] == "rejected"
    assert cap == []


def test_campaign_always_created_paused(monkeypatch):
    cap = []
    _mock_request(monkeypatch, {"id": "777"}, capture=cap)
    prop = approvals.propose_action(
        "create_campaign",
        {"name": "X", "objective": "OUTCOME_SALES", "daily_budget_cents": 500})
    approvals.approve_proposal(prop["proposal_id"])
    assert cap[0]["json"]["status"] == "PAUSED"


def test_missing_params_rejected():
    with pytest.raises(MetaAPIError, match="missing params"):
        approvals.propose_action("create_campaign", {"name": "X"})


# ------------------------------------------------- ad creation pipeline

def test_upload_image_posts_file(monkeypatch, tmp_path):
    img = tmp_path / "ad.jpg"
    img.write_bytes(b"\xff\xd8\xff\x00fakejpg")
    cap = []

    def fake_post(url, params=None, files=None, timeout=None):
        cap.append({"url": url, "files": list(files.keys())})
        return _Resp({"images": {"ad.jpg": {"hash": "abc123"}}})

    monkeypatch.setattr(meta_api.requests, "post", fake_post)
    out = meta_api.do_upload_image(str(img))
    assert out["images"]["ad.jpg"]["hash"] == "abc123"
    assert cap[0]["url"].endswith("/act_12345/adimages")
    assert cap[0]["files"] == ["file"]


def test_upload_image_missing_file():
    with pytest.raises(MetaAPIError, match="not found"):
        meta_api.do_upload_image("/tmp/nope.jpg")


def test_create_adcreative_payload(monkeypatch):
    cap = []
    _mock_request(monkeypatch, {"id": "555"}, capture=cap)
    out = meta_api.do_create_adcreative(
        page_id="999", name="Creative 1", link="https://example.com/sales",
        image_hash="abc123", message="Stop boosting posts.",
        headline="From Product to Profitable Ad", description="$19/mo")
    assert out == {"id": "555"}
    spec = cap[0]["json"]["object_story_spec"]
    assert spec["page_id"] == "999"
    assert spec["link_data"]["image_hash"] == "abc123"
    assert spec["link_data"]["call_to_action"]["type"] == "LEARN_MORE"


def test_create_adcreative_bad_cta():
    with pytest.raises(MetaAPIError, match="invalid cta"):
        meta_api.do_create_adcreative("1", "n", "https://x.com", "h",
                                      "m", "h", "d", cta="BUY_NOW_X")


def test_create_ad_starts_paused(monkeypatch):
    cap = []
    _mock_request(monkeypatch, {"id": "777"}, capture=cap)
    meta_api.do_create_ad("adset_1", "Ad 1", "cr_1")
    assert cap[0]["json"]["status"] == "PAUSED"


def test_new_actions_in_allowlist():
    for a in ("upload_image", "create_adcreative", "create_ad"):
        assert a in meta_api.ACTIONS
    # still no way to run them without propose -> approve
    with pytest.raises(MetaAPIError, match="not found"):
        approvals.approve_proposal("prop_nope")


# --------------------------------------- optional params are not dropped

def test_optional_params_reach_executor(monkeypatch):
    cap = []
    _mock_request(monkeypatch, {"id": "1"}, capture=cap)
    approvals.propose_action("create_adset", {
        "campaign_id": "c1", "name": "AS",
        "optimization_goal": "LINK_CLICKS",
        "promoted_object": {"pixel_id": "p1",
                            "custom_event_type": "PURCHASE"}})
    prop_id = approvals.list_proposals("pending")[0]["id"]
    approvals.approve_proposal(prop_id)
    sent = cap[0]["json"]
    assert sent["optimization_goal"] == "LINK_CLICKS"
    assert sent["promoted_object"]["pixel_id"] == "p1"


def test_unknown_param_rejected():
    with pytest.raises(MetaAPIError, match="unknown params"):
        approvals.propose_action("create_adset",
                                 {"campaign_id": "c", "name": "n",
                                  "delete_everything": True})


def test_cbo_adset_omits_budget(monkeypatch):
    cap = []
    _mock_request(monkeypatch, {"id": "2"}, capture=cap)
    meta_api.do_create_adset("c1", "AS sem budget")
    assert "daily_budget" not in cap[0]["json"]
    meta_api.do_create_adset("c1", "AS com budget", daily_budget_cents=1000)
    assert cap[1]["json"]["daily_budget"] == "1000"
