-- Additive only. Existing users, app_buyers, tracking and credentials untouched.
create table public.hubla_entitlements (
  invoice_id text primary key,
  email text not null,
  product_id text not null,
  version bigint not null check(version >= 0),
  status text not null check(status in ('paid','refunded')),
  updated_at timestamptz not null default now()
);
create index hubla_entitlements_active_email on public.hubla_entitlements(email) where status='paid';
create table public.hubla_receipts (
  delivery_id text primary key,
  payload_hash text not null,
  received_at timestamptz not null default now()
);
alter table public.hubla_entitlements enable row level security;
alter table public.hubla_receipts enable row level security;
revoke all on public.hubla_entitlements, public.hubla_receipts from public, anon, authenticated;
grant select,insert,update on public.hubla_entitlements, public.hubla_receipts to service_role;

create function public.hubla_apply_event(p_delivery_id text, p_hash text,
  p_invoice_id text, p_email text, p_product_id text, p_version bigint, p_status text)
returns void language plpgsql security invoker set search_path='' as $$
declare stored_hash text; old_row public.hubla_entitlements;
begin
  if p_status not in ('paid','refunded') or p_version < 0
     or p_email <> lower(trim(p_email)) or length(p_email)>254
     or p_email !~ '^[^[:space:]@]+@[^[:space:]@]+\.[^[:space:]@]+$'
     or p_hash !~ '^[0-9a-f]{64}$' then
    raise exception 'invalid_hubla_event';
  end if;
  -- Receipt and entitlement are committed together; cross-instance safe.
  insert into public.hubla_receipts(delivery_id,payload_hash)
    values(p_delivery_id,p_hash) on conflict do nothing;
  if not found then
    select payload_hash into stored_hash from public.hubla_receipts where delivery_id=p_delivery_id;
    if stored_hash is distinct from p_hash then raise exception 'hubla_receipt_conflict'; end if;
    return;
  end if;
  perform pg_catalog.pg_advisory_xact_lock(pg_catalog.hashtextextended(p_invoice_id, 9700));
  select * into old_row from public.hubla_entitlements where invoice_id=p_invoice_id for update;
  if found then
    if old_row.email <> p_email or old_row.product_id <> p_product_id then
      raise exception 'hubla_invoice_owner_conflict';
    end if;
    -- A refunded invoice cannot be replayed into a fresh paid entitlement.
    if old_row.status='refunded' or old_row.version>p_version then return; end if;
    if old_row.version=p_version and p_status<>'refunded' then return; end if;
  end if;
  insert into public.hubla_entitlements(invoice_id,email,product_id,version,status)
    values(p_invoice_id,p_email,p_product_id,p_version,p_status)
    on conflict(invoice_id) do update set version=excluded.version,status=excluded.status,updated_at=now();
end $$;
revoke all on function public.hubla_apply_event(text,text,text,text,text,bigint,text) from public,anon,authenticated;
grant execute on function public.hubla_apply_event(text,text,text,text,text,bigint,text) to service_role;
