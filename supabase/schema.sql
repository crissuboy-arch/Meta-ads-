-- Meta Ads Expert PRO — Tracking storage (Supabase)
-- Run once in Supabase: SQL Editor -> paste -> Run.
-- RLS is enabled with no public policies: only the service_role key
-- (used server-side by the app) can read/write. The anon key is blocked.

create table if not exists public.trk_configs (
  key text primary key,
  pixel_id text not null default '',
  token text,
  test_code text not null default '',
  domain text not null default '',
  events jsonb not null default '[]'::jsonb,
  last_test_ok boolean,
  updated_at timestamptz not null default now()
);

create table if not exists public.trk_sales (
  event_id text primary key,
  key text not null,
  ts bigint not null,
  method text not null default 'other',
  record jsonb not null
);
create index if not exists trk_sales_key_ts_idx on public.trk_sales (key, ts desc);

alter table public.trk_configs enable row level security;
alter table public.trk_sales enable row level security;
