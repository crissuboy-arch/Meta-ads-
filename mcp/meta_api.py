"""Thin client for the Meta Marketing API (read + gated writes).

Auth: a Meta user or system-user access token with ads_management / ads_read,
pasted by the OWNER into mcp/.env (never in chat, never committed).
"""
from __future__ import annotations

import os
import requests

API_VERSION = os.getenv("META_API_VERSION", "v21.0")
BASE = f"https://graph.facebook.com/{API_VERSION}"


class MetaAPIError(RuntimeError):
    pass


def _token() -> str:
    tok = os.getenv("META_ACCESS_TOKEN", "")
    if not tok:
        raise MetaAPIError("META_ACCESS_TOKEN is not set (see mcp/.env.example)")
    return tok


def _ad_account() -> str:
    acct = os.getenv("META_AD_ACCOUNT_ID", "")
    if not acct:
        raise MetaAPIError("META_AD_ACCOUNT_ID is not set (see mcp/.env.example)")
    return acct if acct.startswith("act_") else f"act_{acct}"


def _req(method: str, path: str, params: dict | None = None,
         payload: dict | None = None) -> dict:
    params = dict(params or {})
    params["access_token"] = _token()
    try:
        resp = requests.request(method, f"{BASE}{path}", params=params,
                                json=payload, timeout=30)
    except requests.RequestException as exc:
        raise MetaAPIError(f"network error talking to Meta: {exc}") from exc
    try:
        data = resp.json()
    except ValueError:
        raise MetaAPIError(f"Meta returned non-JSON (HTTP {resp.status_code})")
    if resp.status_code >= 400 or "error" in data:
        err = data.get("error", {})
        detail = err.get("error_data") or err.get("error_subcode") or ""
        raise MetaAPIError(
            f"Meta API error {err.get('code')}: {err.get('message')} {detail}"
            .strip())
    return data


# ---------------------------------------------------------------- read tools

def list_campaigns(limit: int = 25) -> list[dict]:
    data = _req("GET", f"/{_ad_account()}/campaigns",
                {"fields": "id,name,objective,status,effective_status,"
                           "daily_budget,lifetime_budget",
                 "limit": max(1, min(limit, 100))})
    return data.get("data", [])


def list_adsets(campaign_id: str = "", limit: int = 50) -> list[dict]:
    params = {"fields": "id,name,campaign_id,status,effective_status,"
                        "daily_budget,billing_event,optimization_goal",
              "limit": max(1, min(limit, 100))}
    path = f"/{campaign_id}/adsets" if campaign_id else f"/{_ad_account()}/adsets"
    return _req("GET", path, params).get("data", [])


def get_insights(level: str, object_id: str = "",
                 date_preset: str = "last_30d") -> list[dict]:
    """level: campaign | adset | ad | account."""
    if level == "account":
        path = f"/{_ad_account()}/insights"
    else:
        if not object_id:
            raise MetaAPIError("object_id is required for non-account insights")
        path = f"/{object_id}/insights"
    return _req("GET", path, {
        "fields": "campaign_name,adset_name,ad_name,spend,impressions,"
                  "clicks,ctr,cpm,cpc,actions,cost_per_action_type",
        "date_preset": date_preset, "limit": 100}).get("data", [])


# ------------------------------------------------------- gated write actions
# Every write below is ONLY reachable through propose -> approve in server.py.
# Nothing here is exposed as a direct MCP tool.

def _create(path: str, payload: dict) -> dict:
    return _req("POST", path, payload=payload)


def do_create_campaign(name: str, objective: str,
                       daily_budget_cents: int | None = None,
                       is_adset_budget_sharing_enabled: bool | None = None
                       ) -> dict:
    """Campaigns are ALWAYS created PAUSED. Activation needs a 2nd approval.
    v21+: campaigns WITHOUT campaign budget (ABO) MUST declare
    is_adset_budget_sharing_enabled (True/False)."""
    payload = {"name": name, "objective": objective,
               "status": "PAUSED",
               "special_ad_categories": []}
    if daily_budget_cents:
        payload["daily_budget"] = str(daily_budget_cents)
    if is_adset_budget_sharing_enabled is not None:
        payload["is_adset_budget_sharing_enabled"] = \
            is_adset_budget_sharing_enabled
    return _create(f"/{_ad_account()}/campaigns", payload)


def do_create_adset(campaign_id: str, name: str,
                    daily_budget_cents: int | None = None,
                    optimization_goal: str = "OFFSITE_CONVERSIONS",
                    billing_event: str = "IMPRESSIONS",
                    bid_strategy: str | None = None,
                    targeting: dict | None = None,
                    promoted_object: dict | None = None,
                    start_time: str | None = None) -> dict:
    payload = {"name": name, "campaign_id": campaign_id,
               "status": "PAUSED",
               "optimization_goal": optimization_goal,
               "billing_event": billing_event,
               "targeting": targeting or {"geo_locations": {"countries": ["US"]}}}
    if bid_strategy:
        # omit by default: Meta's default works, and passing it explicitly
        # can trigger "bid amount required" errors on some accounts
        payload["bid_strategy"] = bid_strategy
    if daily_budget_cents:
        # omit when the campaign already has a budget (CBO): Meta rejects
        # ad-set-level budgets under campaign budget optimization
        payload["daily_budget"] = str(daily_budget_cents)
    if promoted_object:
        # e.g. {"pixel_id": "123", "custom_event_type": "PURCHASE"}
        # required by Meta for SALES campaigns optimizing to conversions
        payload["promoted_object"] = promoted_object
    if start_time:
        payload["start_time"] = start_time
    return _create(f"/{_ad_account()}/adsets", payload)


def do_set_status(object_id: str, status: str) -> dict:
    """status: ACTIVE | PAUSED | ARCHIVED."""
    if status not in ("ACTIVE", "PAUSED", "ARCHIVED"):
        raise MetaAPIError(f"invalid status: {status}")
    return _req("POST", f"/{object_id}", payload={"status": status})


def do_upload_image(image_path: str) -> dict:
    """Upload an image to the ad account. Returns {'images': {filename: {'hash': ...}}}."""
    from pathlib import Path
    p = Path(image_path)
    if not p.is_file():
        raise MetaAPIError(f"image not found: {image_path}")
    token = _token()
    try:
        with p.open("rb") as fh:
            resp = requests.post(
                f"{BASE}/{_ad_account()}/adimages",
                params={"access_token": token},
                files={"file": (p.name, fh, "image/jpeg")},
                timeout=60)
    except requests.RequestException as exc:
        raise MetaAPIError(f"network error uploading image: {exc}") from exc
    try:
        data = resp.json()
    except ValueError:
        raise MetaAPIError(f"Meta returned non-JSON (HTTP {resp.status_code})")
    if resp.status_code >= 400 or "error" in data:
        err = data.get("error", {})
        raise MetaAPIError(
            f"Meta API error {err.get('code')}: {err.get('message')}")
    return data


def do_create_adcreative(page_id: str, name: str, link: str, image_hash: str,
                         message: str, headline: str, description: str,
                         cta: str = "LEARN_MORE") -> dict:
    """Create a link ad creative. Always linked to the given Page."""
    if cta not in ("LEARN_MORE", "SHOP_NOW", "SIGN_UP", "SUBSCRIBE"):
        raise MetaAPIError(f"invalid cta: {cta}")
    payload = {
        "name": name,
        "object_story_spec": {
            "page_id": page_id,
            "link_data": {
                "image_hash": image_hash,
                "link": link,
                "message": message,
                "name": headline,
                "description": description,
                "call_to_action": {"type": cta, "value": {"link": link}},
            },
        },
    }
    return _create(f"/{_ad_account()}/adcreatives", payload)


def do_create_adcreative_from_post(name: str, object_story_id: str) -> dict:
    """Create an ad creative from an EXISTING Page post.

    Works with dev-mode apps (no Page post is created via API), so it does
    not require the app to be Live. The post should already contain the
    destination link in its text.
    """
    payload = {"name": name, "object_story_id": object_story_id}
    return _create(f"/{_ad_account()}/adcreatives", payload)


def do_create_ad(adset_id: str, name: str, creative_id: str) -> dict:
    """Create the ad (always PAUSED; activation needs another approval)."""
    return _create(f"/{_ad_account()}/ads",
                   {"name": name, "adset_id": adset_id,
                    "creative": {"creative_id": creative_id},
                    "status": "PAUSED"})


# action name -> executor + required/optional params (the allowlist)
ACTIONS: dict[str, dict] = {
    "create_campaign": {"fn": do_create_campaign,
                        "params": ["name", "objective"],
                        "optional": ["daily_budget_cents",
                                     "is_adset_budget_sharing_enabled"],
                        "summary": "Create campaign '{name}' ({objective}), "
                                   "budget {budget_label} — starts PAUSED"},
    "create_adset": {"fn": do_create_adset,
                     "params": ["campaign_id", "name"],
                     "optional": ["daily_budget_cents", "optimization_goal",
                                  "billing_event", "bid_strategy",
                                  "targeting", "promoted_object",
                                  "start_time"],
                     "summary": "Create ad set '{name}' in {campaign_id}, "
                                "budget {budget_label} — starts PAUSED"},
    "set_status": {"fn": do_set_status,
                   "params": ["object_id", "status"],
                   "optional": [],
                   "summary": "Set {object_id} status to {status}"},
    "upload_image": {"fn": do_upload_image,
                     "params": ["image_path"],
                     "optional": [],
                     "summary": "Upload image '{image_path}' to the ad account"},
    "create_adcreative": {"fn": do_create_adcreative,
                          "params": ["page_id", "name", "link", "image_hash",
                                     "message", "headline", "description"],
                          "optional": ["cta"],
                          "summary": "Create ad creative '{name}' "
                                     "(headline: '{headline}') for {link}"},
    "create_adcreative_from_post": {
        "fn": do_create_adcreative_from_post,
        "params": ["name", "object_story_id"],
        "optional": [],
        "summary": "Create ad creative '{name}' from existing Page post "
                   "{object_story_id} (no Live app needed)"},
    "create_ad": {"fn": do_create_ad,
                  "params": ["adset_id", "name", "creative_id"],
                  "optional": [],
                  "summary": "Create ad '{name}' in {adset_id} — starts PAUSED"},
}


def describe_action(action: str, params: dict) -> str:
    spec = ACTIONS.get(action)
    if not spec:
        raise MetaAPIError(f"action not allowed: {action}")
    missing = [p for p in spec["params"] if p not in params]
    if missing:
        raise MetaAPIError(f"missing params for {action}: {missing}")
    unknown = [k for k in params
               if k not in spec["params"] + spec.get("optional", [])]
    if unknown:
        raise MetaAPIError(f"unknown params for {action}: {unknown}")
    fmt = dict(params)
    if "daily_budget_cents" in fmt:
        fmt["daily_budget_reais"] = f"{fmt['daily_budget_cents'] / 100:.2f}"
    cents = fmt.get("daily_budget_cents")
    if cents:
        fmt["budget_label"] = f"R$ {cents / 100:.2f}/day (CBO)"
    elif fmt.get("is_adset_budget_sharing_enabled") is False:
        fmt["budget_label"] = "per ad set (ABO)"
    else:
        fmt["budget_label"] = "from campaign (CBO)"
    try:
        return spec["summary"].format(**fmt)
    except KeyError:
        return f"{action} {params}"


def execute_action(action: str, params: dict) -> dict:
    spec = ACTIONS.get(action)
    if not spec:
        raise MetaAPIError(f"action not allowed: {action}")
    allowed = spec["params"] + spec.get("optional", [])
    kwargs = {k: params[k] for k in allowed if k in params}
    return spec["fn"](**kwargs)
