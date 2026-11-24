"""Ofensiva TrÃ¡fego IA — MCP server (Meta Marketing API, approval-gated).

Run:  mcp/.venv/bin/python mcp/server.py   (stdio; connect via `claude mcp add`)
Read tools run free. Write actions ONLY exist as propose -> human yes -> approve.
There is NO direct write tool on purpose: the allowlist in meta_api.py can only
be reached through approvals.approve_proposal.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp.server.fastmcp import FastMCP  # noqa: E402

import meta_api  # noqa: E402
from approvals import (  # noqa: E402
    approve_proposal,
    list_proposals,
    propose_action,
    reject_proposal,
)

mcp = FastMCP("meta-ads-pro")


# ------------------------------------------------------------------ reads

@mcp.tool()
def list_campaigns(limit: int = 25) -> list[dict]:
    """List campaigns in the ad account (read-only)."""
    return meta_api.list_campaigns(limit)


@mcp.tool()
def list_adsets(campaign_id: str = "", limit: int = 50) -> list[dict]:
    """List ad sets, optionally filtered by campaign (read-only)."""
    return meta_api.list_adsets(campaign_id, limit)


@mcp.tool()
def get_insights(level: str, object_id: str = "",
                 date_preset: str = "last_30d") -> list[dict]:
    """Read performance insights. level: account|campaign|adset|ad (read-only)."""
    return meta_api.get_insights(level, object_id, date_preset)


# ------------------------------------------------- approval-gated writes

@mcp.tool()
def propose_action(action: str, params: dict) -> dict:
    """Stage a write action for human approval. Executes NOTHING.

    Allowed actions: create_campaign, create_adset, set_status,
      upload_image, create_adcreative, create_ad.
    create_campaign params: name, objective (e.g. OUTCOME_SALES),
      daily_budget_cents (e.g. 1000 = R$10/day). Campaigns start PAUSED.
    create_adset params: campaign_id, name, daily_budget_cents.
    set_status params: object_id, status (ACTIVE|PAUSED|ARCHIVED).
    upload_image params: image_path (local file).
    create_adcreative params: page_id, name, link, image_hash, message,
      headline, description.
    create_ad params: adset_id, name, creative_id. Ads start PAUSED.
    """
    return propose_action(action, params)


@mcp.tool()
def approve_proposal(proposal_id: str) -> dict:
    """Execute a pending proposal. Call ONLY after the human explicitly
    approved it in chat. One-shot: a decided proposal never runs twice."""
    return approve_proposal(proposal_id)


@mcp.tool()
def reject_proposal(proposal_id: str, reason: str = "") -> dict:
    """Discard a pending proposal without executing it."""
    return reject_proposal(proposal_id, reason)


@mcp.tool()
def list_proposals(status: str = "", limit: int = 20) -> list[dict]:
    """Audit log of proposals: pending|approved|executed|rejected|failed."""
    return list_proposals(status, limit)


if __name__ == "__main__":
    mcp.run()
