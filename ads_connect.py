"""Conectar contas de anúncios (Meta Ads) direto no app — sem Windsor.ai.

Fluxo: o usuário clica em "Conectar com Facebook" -> OAuth do Meta -> o app troca o
código por um token de longa duração (~60 dias), lista as contas de anúncio, guarda
tudo no Supabase (token criptografado) e sincroniza os insights por campanha/dia.

Usa só a Marketing API oficial (gratuita). Para contas em que VOCÊ tem papel no app
Meta (admin/desenvolvedor/testador) funciona em modo Desenvolvimento, sem App Review.

Variáveis de ambiente (Vercel):
  META_APP_ID, META_APP_SECRET   -> do app em developers.facebook.com
  META_REDIRECT_URI              -> opcional (padrão: <origem>/api/ads/meta/callback)
  META_SCOPES                    -> opcional (padrão: ads_read,ads_management,pages_show_list,pages_read_engagement,business_management)
  META_GRAPH_VERSION             -> opcional (padrão: v23.0)
  CRON_SECRET                    -> opcional, protege /api/ads/cron (Vercel Cron envia sozinho)
"""
import base64
import hashlib
import hmac
import json
import os
import re
import secrets
import sys
import time
import urllib.parse
import uuid
from datetime import date, timedelta

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse

STATE_TTL = 600  # segundos


def register(app, d):
    """d = dict com: sb_req, sb_target, auth_secret, scrub, requests, b64u, b64u_dec."""
    sb_req, sb_target = d["sb_req"], d["sb_target"]
    auth_secret, scrub, requests = d["auth_secret"], d["scrub"], d["requests"]
    b64u, b64u_dec = d["b64u"], d["b64u_dec"]
    trk_load, capi_send = d.get("trk_load"), d.get("capi_send")

    def graph_base():
        return "https://graph.facebook.com/" + os.getenv("META_GRAPH_VERSION", "v23.0")

    def configured():
        return bool(os.getenv("META_APP_ID") and os.getenv("META_APP_SECRET"))

    def need_supabase():
        url, _ = sb_target()
        if not url:
            raise HTTPException(503, "supabase_required")

    def redirect_uri(request: Request):
        env = os.getenv("META_REDIRECT_URI")
        if env:
            return env
        proto = request.headers.get("x-forwarded-proto", request.url.scheme)
        host = request.headers.get("x-forwarded-host") or request.headers.get("host") or request.url.netloc
        return f"{proto}://{host}/api/ads/meta/callback"

    # ---- criptografia do token (stdlib: keystream HMAC-SHA256 + MAC) ----
    def _keys():
        base = hashlib.sha256(b"ads-token|" + auth_secret()).digest()
        return (hmac.new(base, b"enc", hashlib.sha256).digest(),
                hmac.new(base, b"mac", hashlib.sha256).digest())

    def enc(text: str) -> str:
        ek, mk = _keys()
        nonce = secrets.token_bytes(16)
        raw = text.encode()
        stream = b""
        i = 0
        while len(stream) < len(raw):
            stream += hmac.new(ek, nonce + i.to_bytes(4, "big"), hashlib.sha256).digest()
            i += 1
        ct = bytes(a ^ b for a, b in zip(raw, stream))
        tag = hmac.new(mk, nonce + ct, hashlib.sha256).digest()
        return b64u(nonce + ct + tag)

    def dec(blob: str):
        try:
            data = b64u_dec(blob)
            nonce, ct, tag = data[:16], data[16:-32], data[-32:]
            ek, mk = _keys()
            if not hmac.compare_digest(tag, hmac.new(mk, nonce + ct, hashlib.sha256).digest()):
                return None
            stream = b""
            i = 0
            while len(stream) < len(ct):
                stream += hmac.new(ek, nonce + i.to_bytes(4, "big"), hashlib.sha256).digest()
                i += 1
            return bytes(a ^ b for a, b in zip(ct, stream)).decode()
        except Exception:
            return None

    # ---- state do OAuth (assinado, com validade) ----
    def make_state(email):
        payload = {"e": email, "n": secrets.token_hex(8), "x": int(time.time()) + STATE_TTL}
        part = b64u(json.dumps(payload, separators=(",", ":")).encode())
        sig = b64u(hmac.new(auth_secret(), b"ads-state|" + part.encode(), hashlib.sha256).digest())
        return part + "." + sig

    def read_state(state):
        try:
            part, sig = state.rsplit(".", 1)
            good = b64u(hmac.new(auth_secret(), b"ads-state|" + part.encode(), hashlib.sha256).digest())
            if not hmac.compare_digest(sig, good):
                return None
            p = json.loads(b64u_dec(part))
            return p["e"] if int(p["x"]) >= time.time() else None
        except Exception:
            return None

    def gget(path, token, params=None, timeout=25):
        q = dict(params or {})
        q["access_token"] = token
        r = requests.get(graph_base() + path, params=q, timeout=timeout)
        if r.status_code >= 400:
            try:
                msg = r.json().get("error", {}).get("message", "")
            except Exception:
                msg = r.text[:200]
            raise RuntimeError(scrub(f"meta_api {r.status_code}: {msg}"))
        return r.json()

    def get_token(email):
        rows = sb_req("GET", "ads_connections",
                      params={"email": f"eq.{email}", "platform": "eq.meta", "select": "*"})
        if not rows:
            return None, None
        return dec(rows[0].get("token_enc") or ""), rows[0]

    # ---------------------------------------------------------------- rotas
    @app.get("/api/ads/status")
    async def ads_status(request: Request):
        email = request.state.user_email
        out = {"configured": configured(), "connected": False, "accounts": []}
        need_supabase()
        rows = sb_req("GET", "ads_connections",
                      params={"email": f"eq.{email}", "platform": "eq.meta", "select": "name,expires_at"})
        if rows:
            out["connected"] = True
            out["name"] = rows[0].get("name") or ""
            out["expires_at"] = rows[0].get("expires_at")
            ap = {"email": f"eq.{email}", "platform": "eq.meta",
                  "select": "account_id,name,currency,status,selected,last_sync,business",
                  "order": "name.asc"}
            try:
                out["accounts"] = sb_req("GET", "ads_accounts", params=ap) or []
            except Exception:
                ap["select"] = "account_id,name,currency,status,selected,last_sync"
                out["accounts"] = sb_req("GET", "ads_accounts", params=ap) or []
        return out

    @app.post("/api/ads/meta/start")
    async def ads_meta_start(request: Request):
        if not configured():
            raise HTTPException(503, "meta_not_configured")
        email = request.state.user_email
        q = {
            "client_id": os.environ["META_APP_ID"],
            "redirect_uri": redirect_uri(request),
            "state": make_state(email),
            "scope": os.getenv("META_SCOPES", "ads_read,ads_management,pages_show_list,pages_read_engagement,business_management"),
            "response_type": "code",
        }
        url = "https://www.facebook.com/" + os.getenv("META_GRAPH_VERSION", "v23.0") + \
              "/dialog/oauth?" + urllib.parse.urlencode(q)
        return {"url": url}

    @app.get("/api/ads/meta/callback")
    async def ads_meta_callback(request: Request):
        qp = request.query_params
        if qp.get("error"):
            return RedirectResponse("/?ads=denied", status_code=302)
        email = read_state(qp.get("state") or "")
        code = qp.get("code")
        if not email or not code or not configured():
            return RedirectResponse("/?ads=error", status_code=302)
        try:
            need_supabase()
            app_id, secret = os.environ["META_APP_ID"], os.environ["META_APP_SECRET"]
            short = requests.get(graph_base() + "/oauth/access_token", params={
                "client_id": app_id, "client_secret": secret,
                "redirect_uri": redirect_uri(request), "code": code}, timeout=25)
            short.raise_for_status()
            llt = requests.get(graph_base() + "/oauth/access_token", params={
                "grant_type": "fb_exchange_token", "client_id": app_id,
                "client_secret": secret, "fb_exchange_token": short.json()["access_token"]},
                timeout=25)
            llt.raise_for_status()
            tok = llt.json()
            token = tok["access_token"]
            expires_at = int(time.time()) + int(tok.get("expires_in") or 5184000)
            me = gget("/me", token, {"fields": "id,name"})
            sb_req("POST", "ads_connections", params={"on_conflict": "email,platform"}, payload={
                "email": email, "platform": "meta", "fb_user_id": me.get("id", ""),
                "name": me.get("name", ""), "token_enc": enc(token), "expires_at": expires_at})
            fetch_accounts(email, token)
            return RedirectResponse("/?ads=connected", status_code=302)
        except Exception as exc:
            print(f"[ads] callback error: {scrub(str(exc))[:300]}", file=sys.stderr)
            return RedirectResponse("/?ads=error", status_code=302)

    def paged(path, token, params):
        out = []
        data = gget(path, token, params)
        while True:
            out.extend(data.get("data", []))
            nxt = (data.get("paging") or {}).get("next")
            if not nxt or len(out) > 2000:
                break
            data = requests.get(nxt, timeout=25).json()
        return out

    def fetch_accounts(email, token):
        existing = {r["account_id"]: r.get("selected") for r in (sb_req(
            "GET", "ads_accounts",
            params={"email": f"eq.{email}", "platform": "eq.meta", "select": "account_id,selected"}) or [])}
        fields = {"fields": "account_id,name,currency,account_status", "limit": 200}
        found = {}  # account_id -> dict

        def add(a, biz=None):
            aid = str(a.get("account_id") or str(a.get("id", "")).replace("act_", ""))
            if not aid.isdigit():
                return
            nm = a.get("name") or aid
            cur = found.get(aid)
            if cur and not biz:
                return
            found[aid] = {"name": nm, "business": biz or (cur or {}).get("business", ""),
                          "currency": a.get("currency") or "", "status": str(a.get("account_status", ""))}

        for a in paged("/me/adaccounts", token, fields):
            add(a)
        try:  # Usuário do Sistema: contas atribuídas
            for a in paged("/me/assigned_ad_accounts", token, fields):
                add(a)
        except RuntimeError:
            pass
        try:  # contas que estão DENTRO dos Business Managers (próprias e de clientes)
            for b in paged("/me/businesses", token, {"fields": "id,name", "limit": 50}):
                for edge in ("owned_ad_accounts", "client_ad_accounts"):
                    try:
                        for a in paged(f"/{b['id']}/{edge}", token, fields):
                            add(a, b.get("name"))
                    except RuntimeError:
                        continue
        except RuntimeError:
            pass
        rows = [{"email": email, "platform": "meta", "account_id": aid, "name": v["name"],
                 "currency": v["currency"], "status": v["status"], "business": v["business"],
                 "selected": existing.get(aid, True)} for aid, v in found.items()]
        if rows:
            try:
                sb_req("POST", "ads_accounts", params={"on_conflict": "email,platform,account_id"}, payload=rows)
            except Exception:  # coluna 'business' ainda não existe: salva sem ela
                for r in rows:
                    r.pop("business", None)
                sb_req("POST", "ads_accounts", params={"on_conflict": "email,platform,account_id"}, payload=rows)
        return rows

    @app.post("/api/ads/accounts/refresh")
    async def ads_accounts_refresh(request: Request):
        need_supabase()
        email = request.state.user_email
        token, _ = get_token(email)
        if not token:
            raise HTTPException(404, "not_connected")
        try:
            return {"count": len(fetch_accounts(email, token))}
        except RuntimeError as exc:
            raise HTTPException(502, str(exc)[:200])

    @app.post("/api/ads/accounts/select")
    async def ads_accounts_select(request: Request):
        need_supabase()
        email = request.state.user_email
        body = await request.json()
        aid = str(body.get("account_id") or "")
        if not aid.isdigit():
            raise HTTPException(400, "invalid_account")
        sb_req("PATCH", "ads_accounts",
               params={"email": f"eq.{email}", "platform": "eq.meta", "account_id": f"eq.{aid}"},
               payload={"selected": bool(body.get("selected"))})
        return {"ok": True}

    @app.post("/api/ads/accounts/select-all")
    async def ads_accounts_select_all(request: Request):
        need_supabase()
        email = request.state.user_email
        body = await request.json()
        sb_req("PATCH", "ads_accounts",
               params={"email": f"eq.{email}", "platform": "eq.meta"},
               payload={"selected": bool(body.get("selected"))})
        return {"ok": True}

    def num(v):
        try:
            return float(v)
        except Exception:
            return 0.0

    def derive_metrics(d):
        """CPA, CPC, CPM e frequencia a partir de spend/impressions/reach/clicks/purchases."""
        spend, impressions = d.get("spend") or 0, d.get("impressions") or 0
        reach, clicks, purchases = d.get("reach") or 0, d.get("clicks") or 0, d.get("purchases") or 0
        return {
            "cpa": (spend / purchases) if purchases else None,
            "cpc": (spend / clicks) if clicks else None,
            "cpm": (spend / impressions * 1000) if impressions else None,
            "frequency": (impressions / reach) if reach else None,
        }

    def sync_account(email, token, aid, days):
        since = (date.today() - timedelta(days=days)).isoformat()
        until = date.today().isoformat()
        params = {
            "level": "campaign", "time_increment": 1, "limit": 500,
            "fields": "campaign_id,campaign_name,spend,impressions,reach,clicks,ctr,actions,action_values",
            "time_range": json.dumps({"since": since, "until": until}),
        }
        data = gget(f"/act_{aid}/insights", token, params, timeout=40)
        out = []
        while True:
            for r in data.get("data", []):
                purchases = sum(num(a.get("value")) for a in (r.get("actions") or [])
                                if a.get("action_type") in ("purchase", "omni_purchase"))
                value = sum(num(a.get("value")) for a in (r.get("action_values") or [])
                            if a.get("action_type") in ("purchase", "omni_purchase"))
                out.append({"email": email, "platform": "meta", "account_id": aid,
                            "day": r.get("date_start"), "campaign_id": r.get("campaign_id") or "",
                            "campaign_name": r.get("campaign_name") or "",
                            "spend": num(r.get("spend")), "impressions": int(num(r.get("impressions"))),
                            "reach": int(num(r.get("reach"))),
                            "clicks": int(num(r.get("clicks"))), "ctr": num(r.get("ctr")),
                            "purchases": purchases, "purchase_value": value})
            nxt = (data.get("paging") or {}).get("next")
            if not nxt:
                break
            data = requests.get(nxt, timeout=40).json()
        for i in range(0, len(out), 500):
            sb_req("POST", "ads_insights",
                   params={"on_conflict": "email,platform,account_id,day,campaign_id"},
                   payload=out[i:i + 500])
        sb_req("PATCH", "ads_accounts",
               params={"email": f"eq.{email}", "platform": "eq.meta", "account_id": f"eq.{aid}"},
               payload={"last_sync": int(time.time())})
        return len(out)

    def sync_user(email, days):
        token, _ = get_token(email)
        if not token:
            return {"error": "not_connected"}
        accts = sb_req("GET", "ads_accounts",
                       params={"email": f"eq.{email}", "platform": "eq.meta",
                               "selected": "eq.true", "select": "account_id"}) or []
        total, errors = 0, []
        for a in accts:
            try:
                total += sync_account(email, token, a["account_id"], days)
            except Exception as exc:
                errors.append(scrub(str(exc))[:160])
        return {"rows": total, "accounts": len(accts), "errors": errors}

    @app.post("/api/ads/sync")
    async def ads_sync(request: Request):
        need_supabase()
        try:
            body = await request.json()
        except Exception:
            body = {}
        days = max(0, min(int(body.get("days", 30)), 90))
        return sync_user(request.state.user_email, days)

    @app.get("/api/ads/insights")
    async def ads_insights(request: Request):
        need_supabase()
        email = request.state.user_email
        days = max(0, min(int(request.query_params.get("days", "30")), 90))
        since = (date.today() - timedelta(days=days)).isoformat()
        params = {"email": f"eq.{email}", "platform": "eq.meta", "day": f"gte.{since}",
                  "select": "account_id,day,campaign_id,campaign_name,spend,impressions,reach,clicks,purchases,purchase_value",
                  "order": "day.desc", "limit": "5000"}
        aid = request.query_params.get("account_id")
        if aid and aid.isdigit():
            params["account_id"] = f"eq.{aid}"
        rows = sb_req("GET", "ads_insights", params=params) or []
        camp = {}
        for r in rows:
            c = camp.setdefault(r["campaign_id"], {"campaign_id": r["campaign_id"],
                                "campaign_name": r["campaign_name"], "spend": 0, "impressions": 0,
                                "reach": 0, "clicks": 0, "purchases": 0, "purchase_value": 0})
            for k in ("spend", "impressions", "reach", "clicks", "purchases", "purchase_value"):
                c[k] += r.get(k) or 0
        per = {}
        for r in rows:
            a = per.setdefault(r["account_id"], {"account_id": r["account_id"], "spend": 0, "clicks": 0, "impressions": 0})
            a["spend"] += r.get("spend") or 0
            a["clicks"] += r.get("clicks") or 0
            a["impressions"] += r.get("impressions") or 0
        camps = sorted(camp.values(), key=lambda c: -c["spend"])
        for c in camps:
            c.update(derive_metrics(c))
        tot = {k: sum(c[k] for c in camps) for k in ("spend", "impressions", "reach", "clicks", "purchases", "purchase_value")}
        tot["ctr"] = (tot["clicks"] / tot["impressions"] * 100) if tot["impressions"] else 0
        tot["roas"] = (tot["purchase_value"] / tot["spend"]) if tot["spend"] else 0
        tot.update(derive_metrics(tot))
        return {"days": days, "totals": tot, "campaigns": camps, "accounts": list(per.values())}

    @app.post("/api/ads/meta/token")
    async def ads_meta_token(request: Request):
        """Conecta com um token colado (ex.: Usuário do Sistema do Business Manager).
        Serve quando a conta de anúncios está em outro login/e-mail do Facebook."""
        need_supabase()
        email = request.state.user_email
        body = await request.json()
        token = str(body.get("token") or "").strip()
        if len(token) < 30 or len(token) > 1000 or " " in token:
            raise HTTPException(400, "invalid_token")
        info = {}
        if configured():
            try:
                r = requests.get(graph_base() + "/debug_token", params={
                    "input_token": token,
                    "access_token": os.environ["META_APP_ID"] + "|" + os.environ["META_APP_SECRET"]}, timeout=25)
                info = (r.json() or {}).get("data") or {}
            except Exception:
                info = {}
        if info and info.get("is_valid") is False:
            raise HTTPException(400, "token_invalid_or_expired")
        scopes = info.get("scopes") or []
        if scopes and "ads_read" not in scopes and "ads_management" not in scopes:
            raise HTTPException(400, "token_missing_ads_permission")
        try:
            me = gget("/me", token, {"fields": "id,name"})
        except RuntimeError as exc:
            raise HTTPException(400, str(exc)[:200])
        exp = info.get("expires_at") or 0
        sb_req("POST", "ads_connections", params={"on_conflict": "email,platform"}, payload={
            "email": email, "platform": "meta", "fb_user_id": me.get("id", ""),
            "name": me.get("name", ""), "token_enc": enc(token),
            "expires_at": int(exp) if exp else None})
        rows = fetch_accounts(email, token)
        return {"ok": True, "accounts": len(rows), "name": me.get("name", ""),
                "permanent": not exp, "scopes": scopes,
                "can_create": ("ads_management" in scopes) if scopes else None}

    @app.post("/api/ads/disconnect")
    async def ads_disconnect(request: Request):
        need_supabase()
        email = request.state.user_email
        for t in ("ads_insights", "ads_accounts", "ads_connections"):
            sb_req("DELETE", t, params={"email": f"eq.{email}", "platform": "eq.meta"})
        return {"ok": True}

    def _capi_by_pixel():
        """pixel_id -> {domain, has_token, last_test_ok} from stored tracking configs."""
        out = {}
        try:
            rows = sb_req("GET", "trk_configs",
                          params={"select": "pixel_id,domain,last_test_ok,token"}) or []
            for r in rows:
                px = str(r.get("pixel_id") or "").strip()
                if px:
                    out[px] = {"domain": r.get("domain") or "",
                               "has_token": bool(r.get("token")),
                               "last_test_ok": r.get("last_test_ok")}
        except Exception:
            pass
        if not out and trk_load:
            try:
                for _k, rec in (trk_load() or {}).items():
                    cfg = (rec or {}).get("config") or {}
                    px = str(cfg.get("pixel_id") or "").strip()
                    if px:
                        out[px] = {"domain": cfg.get("domain") or "",
                                   "has_token": bool(cfg.get("token")),
                                   "last_test_ok": (rec or {}).get("last_test_ok")}
            except Exception:
                pass
        return out

    @app.get("/api/ads/tracking-status")
    def ads_tracking_status(request: Request):
        need_supabase()
        email = request.state.user_email
        token, _row = get_token(email)
        if not token:
            raise HTTPException(404, "not_connected")
        capi = _capi_by_pixel()
        out = []
        for a in selected_accounts(email):
            aid = a["account_id"]
            acc = {"account_id": aid, "name": a.get("name") or aid,
                   "business": a.get("business") or "", "pixels": []}
            try:
                d = gget(f"/act_{aid}/adspixels", token,
                         {"fields": "id,name,last_fired_time", "limit": 50})
                for px in d.get("data") or []:
                    pid = str(px.get("id"))
                    c = capi.get(pid, {})
                    acc["pixels"].append({
                        "id": pid, "name": px.get("name") or pid,
                        "last_fired": px.get("last_fired_time") or None,
                        "capi_configured": bool(c.get("has_token")),
                        "capi_last_test_ok": c.get("last_test_ok"),
                        "domain": c.get("domain") or ""})
            except RuntimeError as exc:
                acc["error"] = str(exc)[:200]
            out.append(acc)
        return {"accounts": out}

    @app.post("/api/ads/tracking-test")
    async def ads_tracking_test(request: Request):
        need_supabase()
        email = request.state.user_email
        token, _row = get_token(email)
        if not token:
            raise HTTPException(404, "not_connected")
        body = await request.json()
        pixel = re.sub(r"\D", "", str(body.get("pixel_id") or ""))[:32]
        if not pixel:
            raise HTTPException(400, "invalid_pixel")
        capi = _capi_by_pixel().get(pixel)
        if not capi or not capi.get("has_token"):
            raise HTTPException(400, "capi_not_configured")
        if not capi_send:
            raise HTTPException(500, "no_sender")
        # rebuild minimal cfg from store (token never leaves the server)
        cfg = {"pixel_id": pixel, "token": None, "test_code": None}
        try:
            rows = sb_req("GET", "trk_configs",
                          params={"pixel_id": f"eq.{pixel}", "select": "token,test_code"}) or []
            if rows:
                cfg["token"] = rows[0].get("token")
                cfg["test_code"] = rows[0].get("test_code")
        except Exception:
            pass
        if not cfg["token"] and trk_load:
            try:
                for _k, rec in (trk_load() or {}).items():
                    c2 = (rec or {}).get("config") or {}
                    if str(c2.get("pixel_id") or "").strip() == pixel and c2.get("token"):
                        cfg["token"] = c2["token"]
                        cfg["test_code"] = c2.get("test_code")
                        break
            except Exception:
                pass
        if not cfg["token"]:
            raise HTTPException(400, "capi_not_configured")
        eid = "test-" + uuid.uuid4().hex[:24]
        ok, detail = capi_send(cfg, "PageView", eid, test_code=cfg.get("test_code"))
        return {"ok": ok, "detail": detail, "event_id": eid}

    @app.get("/api/ads/cron")
    async def ads_cron(request: Request):
        """Sincronização diária (Vercel Cron). Exige CRON_SECRET."""
        secret = os.getenv("CRON_SECRET", "")
        got = (request.headers.get("authorization") or "").removeprefix("Bearer ").strip()
        if not secret or not hmac.compare_digest(got.encode(), secret.encode()):
            raise HTTPException(401, "unauthorized")
        need_supabase()
        users = sb_req("GET", "ads_connections", params={"platform": "eq.meta", "select": "email"}) or []
        done = [{"email": u["email"], **sync_user(u["email"], 7)} for u in users]
        return JSONResponse({"ok": True, "users": len(done)})

    # ================================================================
    # Painel ao vivo: todas as contas/BMs -> campanhas -> conjuntos -> anúncios
    # ================================================================
    from concurrent.futures import ThreadPoolExecutor

    STATUS_NAMES = {"1": "ACTIVE", "2": "DISABLED", "3": "UNSETTLED", "7": "PENDING_RISK_REVIEW",
                    "8": "PENDING_SETTLEMENT", "9": "IN_GRACE_PERIOD", "100": "PENDING_CLOSURE",
                    "101": "CLOSED"}
    PRESETS = {"today", "yesterday", "last_3d", "last_7d", "last_14d", "last_30d", "this_month", "last_month"}
    INS_FIELDS = "spend,impressions,reach,frequency,clicks,ctr,cpc,cpm,actions,action_values"

    def act_sum(lst, types):
        return sum(num(a.get("value")) for a in (lst or []) if a.get("action_type") in types)

    def live_metrics(r):
        spend = num(r.get("spend"))
        acts, vals = r.get("actions"), r.get("action_values")
        purchases = act_sum(acts, ("purchase", "omni_purchase"))
        revenue = act_sum(vals, ("purchase", "omni_purchase"))
        leads = act_sum(acts, ("lead", "onsite_conversion.lead_grouped"))
        msgs = act_sum(acts, ("onsite_conversion.messaging_conversation_started_7d",))
        link = act_sum(acts, ("link_click",))
        if purchases:
            res, kind = purchases, "purchase"
        elif leads:
            res, kind = leads, "lead"
        elif msgs:
            res, kind = msgs, "message"
        else:
            res, kind = link, "link_click"
        return {"spend": spend, "impressions": int(num(r.get("impressions"))),
                "reach": int(num(r.get("reach"))), "frequency": num(r.get("frequency")),
                "clicks": int(num(r.get("clicks"))), "ctr": num(r.get("ctr")),
                "cpc": num(r.get("cpc")), "cpm": num(r.get("cpm")),
                "purchases": purchases, "revenue": revenue, "results": res, "result_type": kind,
                "cost_per_result": (spend / res) if res else 0,
                "roas": (revenue / spend) if spend else 0}

    def selected_accounts(email, only_id=None):
        params = {"email": f"eq.{email}", "platform": "eq.meta", "selected": "eq.true",
                  "select": "account_id,name,currency,business", "order": "name.asc"}
        if only_id:
            params.pop("selected")
            params["account_id"] = f"eq.{only_id}"
        try:
            return sb_req("GET", "ads_accounts", params=params) or []
        except Exception:  # coluna 'business' ainda não criada no Supabase
            params["select"] = "account_id,name,currency"
            return sb_req("GET", "ads_accounts", params=params) or []

    def account_overview(token, a, preset):
        aid = a["account_id"]
        out = {"account_id": aid, "name": a.get("name") or aid, "business": a.get("business") or "",
               "currency": a.get("currency") or ""}
        try:
            info = gget(f"/act_{aid}", token, {"fields": "account_status,disable_reason,currency"})
            out["account_status"] = STATUS_NAMES.get(str(info.get("account_status")), str(info.get("account_status")))
            out["currency"] = info.get("currency") or out["currency"]
            ins = gget(f"/act_{aid}/insights", token, {"level": "account", "date_preset": preset, "fields": INS_FIELDS})
            rows = ins.get("data") or []
            out.update(live_metrics(rows[0] if rows else {}))
            camps = gget(f"/act_{aid}/campaigns", token, {
                "fields": "id", "limit": 500,
                "filtering": json.dumps([{"field": "effective_status", "operator": "IN", "value": ["ACTIVE"]}])})
            out["active_campaigns"] = len(camps.get("data") or [])
        except RuntimeError as exc:
            out["error"] = str(exc)[:200]
        return out

    def overview_all(email, token, preset):
        accts = selected_accounts(email)
        with ThreadPoolExecutor(max_workers=6) as ex:
            return list(ex.map(lambda a: account_overview(token, a, preset), accts))

    def live_level(token, aid, level, parent, preset, only_active):
        edge = {"campaign": "campaigns", "adset": "adsets", "ad": "ads"}[level]
        fields = {"campaign": "id,name,status,effective_status,daily_budget,lifetime_budget,objective",
                  "adset": "id,name,campaign_id,status,effective_status,daily_budget,optimization_goal",
                  "ad": "id,name,adset_id,status,effective_status"}[level]
        flt = []
        if only_active:
            flt.append({"field": "effective_status", "operator": "IN", "value": ["ACTIVE"]})
        pflt = None
        if parent and parent.isdigit():
            pfield = {"adset": "campaign.id", "ad": "adset.id"}.get(level)
            if pfield:
                pflt = {"field": pfield, "operator": "IN", "value": [parent]}
        params = {"fields": fields, "limit": 200}
        f2 = flt + ([pflt] if pflt else [])
        if f2:
            params["filtering"] = json.dumps(f2)
        objs = gget(f"/act_{aid}/{edge}", token, params).get("data") or []
        ip = {"level": level, "date_preset": preset, "limit": 500, "fields": f"{level}_id," + INS_FIELDS}
        if pflt:
            ip["filtering"] = json.dumps([pflt])
        irows = gget(f"/act_{aid}/insights", token, ip).get("data") or []
        by_id = {r.get(f"{level}_id"): live_metrics(r) for r in irows}
        out = []
        for o in objs:
            m = by_id.get(o["id"]) or live_metrics({})
            row = {"id": o["id"], "name": o.get("name"), "status": o.get("effective_status") or o.get("status"),
                   "daily_budget": int(o["daily_budget"]) if str(o.get("daily_budget") or "").isdigit() else None,
                   "objective": o.get("objective") or o.get("optimization_goal")}
            row.update(m)
            out.append(row)
        out.sort(key=lambda r: -r["spend"])
        return out

    @app.get("/api/ads/live")
    def ads_live(request: Request):
        need_supabase()
        email = request.state.user_email
        token, _row = get_token(email)
        if not token:
            raise HTTPException(404, "not_connected")
        qp = request.query_params
        preset = qp.get("preset", "today")
        if preset not in PRESETS:
            raise HTTPException(400, "invalid_preset")
        view = qp.get("view", "overview")
        if view == "overview":
            return {"preset": preset, "accounts": overview_all(email, token, preset)}
        if view not in ("campaign", "adset", "ad"):
            raise HTTPException(400, "invalid_view")
        aid = str(qp.get("account_id") or "")
        if not aid.isdigit() or not selected_accounts(email, aid):
            raise HTTPException(400, "invalid_account")
        try:
            rows = live_level(token, aid, view, qp.get("parent") or "", preset, qp.get("only_active", "1") == "1")
        except RuntimeError as exc:
            raise HTTPException(502, str(exc)[:200])
        cur = (selected_accounts(email, aid)[0].get("currency")) or ""
        return {"preset": preset, "view": view, "currency": cur, "rows": rows}

    # ================================================================
    # Ferramentas MCP: ler e criar campanhas (SEMPRE pausadas) com o token
    # guardado do usuário. O Claude nunca vê o token.
    # ================================================================
    ZERO_DEC = {"JPY", "KRW", "VND", "CLP", "PYG", "UGX", "ISK", "XAF", "XOF", "KMF", "RWF", "DJF", "GNF", "VUV", "XPF"}
    OBJECTIVES = ["OUTCOME_SALES", "OUTCOME_LEADS", "OUTCOME_TRAFFIC", "OUTCOME_ENGAGEMENT",
                  "OUTCOME_AWARENESS", "OUTCOME_APP_PROMOTION"]

    class ToolError(Exception):
        pass

    def gcall(method, path, token, data=None, params=None, timeout=40):
        form = {}
        for k, v in (data or {}).items():
            if v is None:
                continue
            form[k] = json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v
        q = dict(params or {})
        q["access_token"] = token
        if method == "GET":
            r = requests.get(graph_base() + path, params=q, timeout=timeout)
        else:
            r = requests.post(graph_base() + path, params={"access_token": token}, data=form, timeout=timeout)
        try:
            body = r.json()
        except Exception:
            body = {}
        if r.status_code >= 400 or (isinstance(body, dict) and body.get("error")):
            err = (body.get("error") if isinstance(body, dict) else None) or {}
            msg = err.get("error_user_msg") or err.get("message") or r.text[:200]
            title = err.get("error_user_title") or ""
            if err.get("code") == 190:
                msg = "Token do Meta expirou ou foi revogado. Peça ao usuário para abrir o app > Conectar contas de anúncio > Reconectar."
            raise ToolError(scrub(f"Meta API: {title + ': ' if title else ''}{msg}"))
        return body

    def gcall_retry(method, path, token, data, fixes):
        """Tenta; se o Meta pedir um campo novo conhecido, repete uma vez com ele."""
        try:
            return gcall(method, path, token, data)
        except ToolError as exc:
            text = str(exc)
            for needle, patch in fixes:
                if needle in text:
                    return gcall(method, path, token, patch(dict(data)))
            raise

    def account_row(email, aid):
        aid = str(aid or "").replace("act_", "").strip()
        if not aid.isdigit():
            raise ToolError("ad_account_id inválido. Use list_ad_accounts para ver os IDs.")
        rows = sb_req("GET", "ads_accounts", params={"email": f"eq.{email}", "platform": "eq.meta",
                                                     "account_id": f"eq.{aid}", "select": "account_id,name,currency"})
        if not rows:
            raise ToolError("Essa conta de anúncio não está conectada. Use list_ad_accounts.")
        return rows[0]

    def to_minor(currency, amount):
        try:
            v = float(amount)
        except Exception:
            raise ToolError("Valor de orçamento inválido.")
        if v <= 0:
            raise ToolError("O orçamento precisa ser maior que zero.")
        return int(round(v * (1 if (currency or "").upper() in ZERO_DEC else 100)))

    def need(args, *names):
        miss = [n for n in names if args.get(n) in (None, "", [], {})]
        if miss:
            raise ToolError("Faltam campos obrigatórios: " + ", ".join(miss))

    def t_list_ad_accounts(email, token, a):
        rows = sb_req("GET", "ads_accounts", params={"email": f"eq.{email}", "platform": "eq.meta",
                      "select": "account_id,name,currency,status,selected", "order": "name.asc"}) or []
        return {"ad_accounts": rows, "note": "Use account_id como ad_account_id nas outras ferramentas."}

    def t_list_pages(email, token, a):
        f = {"fields": "id,name,instagram_business_account{id,username}", "limit": 100}
        d = gcall("GET", "/me/accounts", token, params=f)
        if not d.get("data"):  # Usuário do Sistema: páginas atribuídas
            try:
                d = gcall("GET", "/me/assigned_pages", token, params={"fields": "id,name", "limit": 100})
            except ToolError:
                pass
        return {"pages": d.get("data", [])}

    def t_list_pixels(email, token, a):
        need(a, "ad_account_id")
        row = account_row(email, a["ad_account_id"])
        d = gcall("GET", f"/act_{row['account_id']}/adspixels", token, params={"fields": "id,name,last_fired_time", "limit": 50})
        return {"pixels": d.get("data", [])}

    def t_list_objects(email, token, a):
        need(a, "ad_account_id", "level")
        row = account_row(email, a["ad_account_id"])
        level = a["level"]
        if level not in ("campaigns", "adsets", "ads"):
            raise ToolError("level deve ser campaigns, adsets ou ads.")
        fields = {"campaigns": "id,name,status,effective_status,objective,daily_budget,created_time",
                  "adsets": "id,name,campaign_id,status,effective_status,daily_budget,optimization_goal",
                  "ads": "id,name,adset_id,status,effective_status,creative{id}"}[level]
        d = gcall("GET", f"/act_{row['account_id']}/{level}", token,
                  params={"fields": fields, "limit": min(int(a.get("limit") or 50), 100)})
        return {"currency": row["currency"], "items": d.get("data", []),
                "note": "daily_budget vem em unidade menor da moeda (5000 = 50,00)."}

    def t_get_insights(email, token, a):
        need(a, "ad_account_id")
        row = account_row(email, a["ad_account_id"])
        level = a.get("level") or "campaign"
        if level not in ("account", "campaign", "adset", "ad"):
            raise ToolError("level inválido.")
        params = {"level": level, "limit": 200,
                  "fields": "campaign_name,adset_name,ad_name,spend,impressions,reach,clicks,ctr,cpm,cpc,actions,cost_per_action_type"}
        if a.get("since") and a.get("until"):
            params["time_range"] = json.dumps({"since": a["since"], "until": a["until"]})
        else:
            params["date_preset"] = a.get("date_preset") or "last_7d"
        d = gcall("GET", f"/act_{row['account_id']}/insights", token, params=params)
        return {"currency": row["currency"], "rows": d.get("data", [])}

    def t_create_campaign(email, token, a):
        need(a, "ad_account_id", "name", "objective")
        row = account_row(email, a["ad_account_id"])
        if a["objective"] not in OBJECTIVES:
            raise ToolError("objective deve ser um de: " + ", ".join(OBJECTIVES))
        data = {"name": str(a["name"])[:200], "objective": a["objective"], "status": "PAUSED",
                "special_ad_categories": a.get("special_ad_categories") or [], "buying_type": "AUCTION"}
        if a.get("daily_budget"):
            data["daily_budget"] = to_minor(row["currency"], a["daily_budget"])
            data["bid_strategy"] = a.get("bid_strategy") or "LOWEST_COST_WITHOUT_CAP"
        d = gcall_retry("POST", f"/act_{row['account_id']}/campaigns", token, data, [
            ("is_adset_budget_sharing_enabled", lambda x: {**x, "is_adset_budget_sharing_enabled": False})])
        return {"campaign_id": d.get("id"), "status": "PAUSED"}

    def t_create_adset(email, token, a):
        need(a, "ad_account_id", "campaign_id", "name", "optimization_goal", "targeting")
        row = account_row(email, a["ad_account_id"])
        data = {"name": str(a["name"])[:200], "campaign_id": str(a["campaign_id"]), "status": "PAUSED",
                "optimization_goal": a["optimization_goal"],
                "billing_event": a.get("billing_event") or "IMPRESSIONS",
                "targeting": a["targeting"]}
        if a.get("daily_budget"):
            data["daily_budget"] = to_minor(row["currency"], a["daily_budget"])
            data["bid_strategy"] = a.get("bid_strategy") or "LOWEST_COST_WITHOUT_CAP"
        for k in ("promoted_object", "start_time", "end_time", "destination_type", "dsa_beneficiary", "dsa_payor",
                  "regional_regulated_categories", "regional_regulation_identities", "bid_amount"):
            if a.get(k) not in (None, "", [], {}):
                data[k] = a[k]
        d = gcall_retry("POST", f"/act_{row['account_id']}/adsets", token, data, [
            ("advantage_audience", lambda x: {**x, "targeting": {**x["targeting"], "targeting_automation": {"advantage_audience": 0}}})])
        return {"adset_id": d.get("id"), "status": "PAUSED"}

    def t_create_ad(email, token, a):
        need(a, "ad_account_id", "adset_id", "name", "page_id", "link", "message")
        if not (a.get("image_url") or a.get("image_hash")):
            raise ToolError("Informe image_url (link público https) ou image_hash.")
        row = account_row(email, a["ad_account_id"])
        link = str(a["link"])
        if not link.startswith(("http://", "https://")):
            raise ToolError("link precisa começar com http(s)://")
        link_data = {"link": link, "message": a["message"],
                     "call_to_action": {"type": a.get("call_to_action_type") or "LEARN_MORE", "value": {"link": link}}}
        if a.get("headline"):
            link_data["name"] = a["headline"]
        if a.get("description"):
            link_data["description"] = a["description"]
        if a.get("image_hash"):
            link_data["image_hash"] = a["image_hash"]
        else:
            link_data["picture"] = a["image_url"]
        spec = {"page_id": str(a["page_id"]), "link_data": link_data}
        if a.get("instagram_user_id"):
            spec["instagram_user_id"] = str(a["instagram_user_id"])
        cr = gcall("POST", f"/act_{row['account_id']}/adcreatives", token,
                   {"name": str(a["name"])[:200], "object_story_spec": spec})
        ad = gcall("POST", f"/act_{row['account_id']}/ads", token, {
            "name": str(a["name"])[:200], "adset_id": str(a["adset_id"]),
            "creative": {"creative_id": cr.get("id")}, "status": "PAUSED"})
        return {"ad_id": ad.get("id"), "creative_id": cr.get("id"), "status": "PAUSED"}

    def t_set_status(email, token, a):
        need(a, "object_id", "status")
        oid = str(a["object_id"])
        if not oid.isdigit():
            raise ToolError("object_id inválido.")
        status = str(a["status"]).upper()
        if status not in ("PAUSED", "ACTIVE"):
            raise ToolError("status deve ser PAUSED ou ACTIVE. Não existe ferramenta para apagar.")
        if status == "ACTIVE" and a.get("user_confirmed") is not True:
            raise ToolError("Para ativar, o usuário precisa confirmar explicitamente o gasto diário total. "
                            "Repita o orçamento diário em moeda normal, espere o 'sim' e chame de novo com user_confirmed=true.")
        d = gcall("POST", f"/{oid}", token, {"status": status})
        return {"object_id": oid, "status": status, "success": bool(d.get("success", True))}

    def t_account_overview(email, token, a):
        preset = a.get("date_preset") or "today"
        if preset not in PRESETS:
            raise ToolError("date_preset inválido: " + ", ".join(sorted(PRESETS)))
        return {"preset": preset, "accounts": overview_all(email, token, preset),
                "note": "Uma linha por conta de anúncio selecionada (agrupe por business/BM). spend/revenue na moeda de cada conta."}

    A = {"type": "string"}
    def schema(props, req):
        return {"type": "object", "properties": props, "required": req, "additionalProperties": True}
    ACC = {"type": "string", "description": "account_id retornado por list_ad_accounts (só números)."}
    tools = [
        ("list_ad_accounts", "Lista as contas de anúncio do Meta conectadas pelo usuário no app.", schema({}, []), t_list_ad_accounts),
        ("account_overview", "Visão geral de TODAS as contas de anúncio conectadas (todas as BMs): gasto, resultados, ROAS, status da conta e nº de campanhas ativas no período. date_preset: today, yesterday, last_7d, last_30d. Use para acompanhar o desempenho de hoje.",
         schema({"date_preset": A}, []), t_account_overview),
        ("list_pages", "Lista as Páginas do Facebook (e Instagram ligado) que o usuário pode usar nos anúncios.", schema({}, []), t_list_pages),
        ("list_pixels", "Lista os Pixels da conta de anúncio.", schema({"ad_account_id": ACC}, ["ad_account_id"]), t_list_pixels),
        ("list_objects", "Lista campanhas, conjuntos ou anúncios da conta com status e orçamento. Use para verificar o que foi criado.",
         schema({"ad_account_id": ACC, "level": {"type": "string", "enum": ["campaigns", "adsets", "ads"]}, "limit": {"type": "integer"}}, ["ad_account_id", "level"]), t_list_objects),
        ("get_insights", "Métricas ao vivo do Meta (gasto, impressões, cliques, CTR, CPM, ações). level: account|campaign|adset|ad; date_preset (ex. last_7d, last_30d, yesterday) ou since/until (YYYY-MM-DD).",
         schema({"ad_account_id": ACC, "level": A, "date_preset": A, "since": A, "until": A}, ["ad_account_id"]), t_get_insights),
        ("create_campaign", "Cria uma campanha SEMPRE PAUSADA. daily_budget (opcional) em moeda normal, ex. 10 = 10,00. special_ad_categories: [] salvo categoria regulada.",
         schema({"ad_account_id": ACC, "name": A, "objective": {"type": "string", "enum": OBJECTIVES},
                 "daily_budget": {"type": "number"}, "special_ad_categories": {"type": "array", "items": A}}, ["ad_account_id", "name", "objective"]), t_create_campaign),
        ("create_adset", "Cria um conjunto de anúncios SEMPRE PAUSADO. daily_budget em moeda normal (omita se a campanha tem orçamento). targeting é o objeto do Meta (geo_locations, age_min, age_max, genders, interesses...). Para vendas: optimization_goal OFFSITE_CONVERSIONS + promoted_object {pixel_id, custom_event_type:PURCHASE}.",
         schema({"ad_account_id": ACC, "campaign_id": A, "name": A, "optimization_goal": A, "billing_event": A,
                 "daily_budget": {"type": "number"}, "targeting": {"type": "object"}, "promoted_object": {"type": "object"},
                 "start_time": A, "end_time": A}, ["ad_account_id", "campaign_id", "name", "optimization_goal", "targeting"]), t_create_adset),
        ("create_ad", "Cria o criativo e o anúncio SEMPRE PAUSADO. Imagem por image_url (link público https) ou image_hash. call_to_action_type ex. LEARN_MORE, SHOP_NOW.",
         schema({"ad_account_id": ACC, "adset_id": A, "name": A, "page_id": A, "link": A, "message": A, "headline": A,
                 "description": A, "image_url": A, "image_hash": A, "call_to_action_type": A, "instagram_user_id": A},
                ["ad_account_id", "adset_id", "name", "page_id", "link", "message"]), t_create_ad),
        ("set_status", "Pausa ou ativa uma campanha, conjunto ou anúncio. Para ACTIVE, o usuário precisa ter confirmado o gasto diário total: só então passe user_confirmed=true. Não existe exclusão.",
         schema({"object_id": A, "status": {"type": "string", "enum": ["PAUSED", "ACTIVE"]}, "user_confirmed": {"type": "boolean"}}, ["object_id", "status"]), t_set_status),
    ]
    handlers = {n: h for n, _, _, h in tools}
    d["mcp"]["tools"] = [{"name": n, "title": n.replace("_", " ").title(), "description": desc, "inputSchema": sch}
                         for n, desc, sch, _ in tools]

    def mcp_call(email, name, args):
        h = handlers.get(name)
        if not h:
            return None
        try:
            need_supabase()
            token, _row = get_token(email)
            if not token and name != "list_ad_accounts":
                raise ToolError("Conta Meta não conectada. Peça ao usuário para abrir o app > Conectar contas de anúncio > Conectar com Facebook.")
            out = h(email, token, args if isinstance(args, dict) else {})
            return {"content": [{"type": "text", "text": json.dumps(out, ensure_ascii=False, default=str)[:20000]}]}
        except ToolError as exc:
            return {"content": [{"type": "text", "text": str(exc)}], "isError": True}
        except HTTPException:
            return {"content": [{"type": "text", "text": "Supabase não configurado no app."}], "isError": True}
        except Exception as exc:
            print(f"[ads-mcp] {name} error: {scrub(str(exc))[:300]}", file=sys.stderr)
            return {"content": [{"type": "text", "text": "Erro inesperado ao falar com o Meta. Tente de novo."}], "isError": True}
    d["mcp"]["call"] = mcp_call

    # ================================================================
    # Assistente de campanha (Fase E): mesma tela web, mesmos handlers do
    # MCP acima (sempre cria PAUSADO) - nao duplica logica nenhuma.
    # ================================================================
    _WRITE_TOOLS = {"create_campaign", "create_adset", "create_ad", "set_status"}

    def write_actions_enabled():
        return os.getenv("WRITE_ACTIONS_ENABLED", "").strip().lower() in ("1", "true", "yes", "on")

    @app.get("/api/ads/wizard/meta")
    def ads_wizard_meta():
        """Dados estaticos para montar o wizard: objetivos validos e se a
        criacao real esta ligada (ve "Fase F - WRITE_ACTIONS_ENABLED")."""
        return {"objectives": OBJECTIVES, "write_actions_enabled": write_actions_enabled()}

    @app.post("/api/ads/wizard/call")
    async def ads_wizard_call(request: Request):
        """Unico ponto de entrada do assistente de campanha pela web.
        Ferramentas de leitura (list_*, get_insights, account_overview) sempre
        funcionam. Ferramentas de escrita (create_campaign, create_adset,
        create_ad, set_status) exigem WRITE_ACTIONS_ENABLED=true no ambiente;
        sem isso, o wizard funciona só em modo leitura/preview, como pedido:
        "inicialmente, todas as integracoes reais devem funcionar em modo de
        leitura". Campanhas e conjuntos nascem SEMPRE pausados (ver t_create_*
        acima); so set_status pode ativar, e exige user_confirmed=true."""
        need_supabase()
        email = request.state.user_email
        body = await request.json()
        name = str(body.get("tool") or "")
        args = body.get("args") or {}
        if name in _WRITE_TOOLS and not write_actions_enabled():
            raise HTTPException(403, "write_actions_disabled")
        out = mcp_call(email, name, args)
        if out is None:
            raise HTTPException(404, "unknown_tool")
        text = (out.get("content") or [{}])[0].get("text", "")
        if out.get("isError"):
            raise HTTPException(400, text[:200])
        try:
            return json.loads(text)
        except ValueError:
            return {"result": text}
