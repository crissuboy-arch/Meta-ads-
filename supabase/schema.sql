-- Ofensiva TrÃ¡fego IA — Tracking storage (Supabase)
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

-- App user accounts (login & password). Passwords are PBKDF2 hashes,
-- never plain text.
create table if not exists public.app_users (
  id uuid primary key default gen_random_uuid(),
  email text unique not null,
  pass_hash text not null,
  created_at timestamptz not null default now()
);

alter table public.app_users enable row level security;

-- Buyers: who may download the Claude package. Filled by the Hotmart webhook
-- (POST /api/webhooks/hotmart). Only the service_role key can read/write.
create table if not exists public.app_buyers (
  email text primary key,
  status text not null default 'active',
  updated_at timestamptz not null default now()
);

alter table public.app_buyers enable row level security;

-- MCP access keys (one per buyer). Only the SHA-256 hash of the key is stored.
create table if not exists public.mcp_keys (
  key_hash text primary key,
  email text not null,
  created_at timestamptz not null default now()
);
create index if not exists mcp_keys_email_idx on public.mcp_keys (email);

alter table public.mcp_keys enable row level security;


-- Contas de anúncios conectadas (Meta Ads). Token guardado CRIPTOGRAFADO.
create table if not exists public.ads_connections (
  email text not null,
  platform text not null default 'meta',
  fb_user_id text not null default '',
  name text not null default '',
  token_enc text not null,
  expires_at bigint,
  created_at timestamptz not null default now(),
  primary key (email, platform)
);
create table if not exists public.ads_accounts (
  email text not null,
  platform text not null default 'meta',
  account_id text not null,
  name text not null default '',
  currency text not null default '',
  status text not null default '',
  selected boolean not null default false,
  last_sync bigint,
  primary key (email, platform, account_id)
);
create table if not exists public.ads_insights (
  email text not null,
  platform text not null default 'meta',
  account_id text not null,
  day date not null,
  campaign_id text not null default '',
  campaign_name text not null default '',
  spend numeric not null default 0,
  impressions bigint not null default 0,
  clicks bigint not null default 0,
  ctr numeric not null default 0,
  purchases numeric not null default 0,
  purchase_value numeric not null default 0,
  primary key (email, platform, account_id, day, campaign_id)
);
create index if not exists ads_insights_day_idx on public.ads_insights (email, day desc);
alter table public.ads_connections enable row level security;
alter table public.ads_accounts enable row level security;
alter table public.ads_insights enable row level security;

-- Nome do Business Manager (BM) de cada conta de anúncio
alter table public.ads_accounts add column if not exists business text not null default '';
