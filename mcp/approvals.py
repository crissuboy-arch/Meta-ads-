"""Approval gate for Meta write actions.

Nothing that spends money (or changes account state) runs directly.
Flow: propose_action -> (human says yes in chat) -> approve_proposal -> executes.
Proposals live in Supabase table mcp_proposals (service_role, server-side only).
Falls back to a local JSON file when Supabase envs are absent (dev only).
"""
from __future__ import annotations

import json
import os
import time
import uuid
from pathlib import Path

import requests

from meta_api import describe_action, execute_action, MetaAPIError

TABLE = "mcp_proposals"


def _sb() -> tuple[str | None, str | None]:
    url = os.getenv("SUPABASE_URL", "").rstrip("/")
    key = os.getenv("SUPABASE_SERVICE_KEY", "")
    return (url, key) if url and key else (None, None)


def _sb_req(method: str, params: dict | None = None,
            payload: dict | list | None = None):
    url, key = _sb()
    headers = {"apikey": key, "Authorization": f"Bearer {key}",
               "Content-Type": "application/json",
               "Prefer": "return=representation,resolution=merge-duplicates"}
    resp = requests.request(method, f"{url}/rest/v1/{TABLE}", params=params,
                            json=payload, headers=headers, timeout=15)
    resp.raise_for_status()
    if resp.status_code == 204 or not resp.content:
        return None
    return resp.json()


def _local_path() -> Path:
    p = Path(__file__).parent / "proposals.local.json"
    if not p.exists():
        p.write_text("[]", encoding="utf-8")
    return p


def _local_all() -> list[dict]:
    try:
        return json.loads(_local_path().read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return []


def _local_save(rows: list[dict]) -> None:
    _local_path().write_text(json.dumps(rows, ensure_ascii=False, indent=1),
                             encoding="utf-8")


def _store_get(proposal_id: str) -> dict | None:
    url, _ = _sb()
    if url:
        rows = _sb_req("GET", {"id": f"eq.{proposal_id}", "select": "*",
                               "limit": "1"})
        return rows[0] if rows else None
    return next((r for r in _local_all() if r["id"] == proposal_id), None)


def _store_put(row: dict) -> None:
    url, _ = _sb()
    if url:
        _sb_req("POST", payload=row)
        return
    rows = [r for r in _local_all() if r["id"] != row["id"]]
    rows.append(row)
    _local_save(rows)


def _store_patch(proposal_id: str, patch: dict) -> None:
    url, _ = _sb()
    if url:
        _sb_req("PATCH", {"id": f"eq.{proposal_id}"}, payload=patch)
        return
    rows = _local_all()
    for r in rows:
        if r["id"] == proposal_id:
            r.update(patch)
    _local_save(rows)


def propose_action(action: str, params: dict, requested_by: str = "claude") -> dict:
    """Stage a write action. Returns the proposal — NOTHING is executed."""
    summary = describe_action(action, params)  # validates allowlist + params
    row = {"id": f"prop_{uuid.uuid4().hex[:12]}",
           "action": action, "params": params, "summary": summary,
           "status": "pending", "requested_by": requested_by,
           "result": None,
           "created_at": int(time.time()), "decided_at": None}
    _store_put(row)
    return {"proposal_id": row["id"], "status": "pending",
            "summary": summary,
            "next_step": "Show this summary to the human. Only call "
                         "approve_proposal AFTER the human explicitly says yes."}


def approve_proposal(proposal_id: str) -> dict:
    """Human said yes -> mark approved and EXECUTE now. One shot."""
    row = _store_get(proposal_id)
    if not row:
        raise MetaAPIError(f"proposal not found: {proposal_id}")
    if row["status"] != "pending":
        raise MetaAPIError(f"proposal {proposal_id} is {row['status']} — "
                           "already decided, will not run twice")
    _store_patch(proposal_id, {"status": "approved",
                               "decided_at": int(time.time())})
    try:
        result = execute_action(row["action"], row["params"])
    except MetaAPIError as exc:
        _store_patch(proposal_id, {"status": "failed",
                                   "result": {"error": str(exc)}})
        raise
    _store_patch(proposal_id, {"status": "executed", "result": result})
    return {"proposal_id": proposal_id, "status": "executed",
            "summary": row["summary"], "result": result}


def reject_proposal(proposal_id: str, reason: str = "") -> dict:
    row = _store_get(proposal_id)
    if not row:
        raise MetaAPIError(f"proposal not found: {proposal_id}")
    if row["status"] != "pending":
        raise MetaAPIError(f"proposal {proposal_id} is {row['status']}")
    _store_patch(proposal_id, {"status": "rejected",
                               "decided_at": int(time.time()),
                               "result": {"reason": reason}})
    return {"proposal_id": proposal_id, "status": "rejected"}


def list_proposals(status: str = "", limit: int = 20) -> list[dict]:
    url, _ = _sb()
    if url:
        params = {"select": "id,action,summary,status,created_at,decided_at",
                  "order": "created_at.desc", "limit": str(limit)}
        if status:
            params["status"] = f"eq.{status}"
        return _sb_req("GET", params) or []
    rows = sorted(_local_all(), key=lambda r: r["created_at"], reverse=True)
    if status:
        rows = [r for r in rows if r["status"] == status]
    return [{k: r.get(k) for k in
             ("id", "action", "summary", "status", "created_at", "decided_at")}
            for r in rows[:limit]]
