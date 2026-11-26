"""Hubla Webhooks 2.0. Server-only, fail closed; no checkout or campaign writes."""
import hashlib
import hmac
import json
import os
import re

from fastapi import HTTPException, Request


def normalize(body, product_id):
    if not isinstance(body, dict) or body.get('version') != '2.0.0':
        raise ValueError('unsupported_payload')
    kind = body.get('type')
    if kind not in ('invoice.payment_succeeded', 'invoice.refunded'):
        return None
    event = body.get('event')
    if not isinstance(event, dict):
        raise ValueError('invalid_event')
    products = event.get('products')
    if not isinstance(products, list) or not any(
        isinstance(p, dict) and p.get('id') == product_id for p in products
    ):
        return None
    invoice = event.get('invoice') or {}
    user = event.get('user') or {}
    if not isinstance(invoice, dict) or not isinstance(user, dict):
        raise ValueError('invalid_invoice')
    email = str(user.get('email') or '').strip().lower()
    invoice_id = invoice.get('id')
    version = invoice.get('version')
    status = 'paid' if kind == 'invoice.payment_succeeded' else 'refunded'
    if (not isinstance(invoice_id, str) or not 1 <= len(invoice_id) <= 160
            or invoice.get('parentInvoiceId') or type(version) is not int or version < 0
            or invoice.get('status') != status
            or not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', email)
            or len(email) > 254 or invoice.get('currency') != 'BRL'):
        raise ValueError('invalid_invoice')
    if status == 'paid':
        # A launch offer is explicitly configured, never inferred from its name.
        amount = invoice.get('amount') or {}
        if not isinstance(amount, dict) or type(amount.get('totalCents')) is not int or amount['totalCents'] != 9700:
            raise ValueError('unexpected_amount')
    return {'p_invoice_id': invoice_id, 'p_email': email,
            'p_product_id': product_id, 'p_version': version, 'p_status': status}


def register(app, sb_req):
    @app.post('/api/webhooks/hubla')
    async def hubla_webhook(request: Request):
        expected = os.getenv('HUBLA_WEBHOOK_TOKEN', '')
        product_id = os.getenv('HUBLA_PRODUCT_ID', '')
        if not expected or not product_id:
            raise HTTPException(503, 'hubla_not_configured')
        if not hmac.compare_digest(request.headers.get('x-hubla-token', '').encode(), expected.encode()):
            raise HTTPException(401, 'invalid_hubla_token')
        sandbox = request.headers.get('x-hubla-sandbox')
        delivery = request.headers.get('x-hubla-idempotency', '')
        if sandbox not in ('true', 'false') or not 1 <= len(delivery) <= 200:
            raise HTTPException(400, 'invalid_hubla_headers')
        if request.headers.get('x-hubla-delivery-mode') != 'standard':
            raise HTTPException(400, 'hubla_standard_delivery_required')
        raw = await request.body()
        if len(raw) > 262144:
            raise HTTPException(413, 'payload_too_large')
        try:
            body = json.loads(raw)
            normalized = normalize(body, product_id)
        except (ValueError, TypeError):
            raise HTTPException(400, 'invalid_hubla_payload')
        if normalized is None:
            return {'ok': True, 'ignored': True}
        if sandbox == 'true':
            return {'ok': True, 'sandbox': True, 'access_changed': False}
        # No live sale can be consumed silently before commercial validation.
        if os.getenv('HUBLA_LIVE_ACCESS_ENABLED', 'false').lower() != 'true':
            raise HTTPException(503, 'hubla_live_access_disabled')
        if os.getenv('HUBLA_ACCESS_MODEL') != 'one_time':
            raise HTTPException(503, 'hubla_access_model_not_approved')
        normalized.update(p_delivery_id=delivery, p_hash=hashlib.sha256(
            json.dumps(body, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()
        ).hexdigest())
        try:
            sb_req('POST', 'rpc/hubla_apply_event', payload=normalized)
        except Exception:
            # Retryable: no local-file fallback or successful acknowledgement on DB failure.
            raise HTTPException(503, 'hubla_persistence_unavailable')
        return {'ok': True}
