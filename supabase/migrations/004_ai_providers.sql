-- Provedores de IA (Ofensiva TrÃ¡fego IA, redesign-v2).
-- Run once in Supabase: SQL Editor -> paste -> Run.
-- RLS on, no public policies: only the service_role key (server-side) can
-- read/write. API keys are stored encrypted; the API never returns them whole.

create table if not exists public.ai_providers (
  id text primary key,
  owner_email text not null,
  provider text not null
    check (provider in ('gemini', 'openai', 'openrouter')),
  kind text not null
    check (kind in ('text', 'image')),
  role text not null
    check (role in ('primary', 'backup')),
  model text not null default '',
  key_enc text not null,
  key_hint text not null default '',
  active boolean not null default true,
  last_test_ok boolean,
  last_test_at timestamptz,
  created_at timestamptz not null default now(),
  unique (owner_email, kind, role)
);
create index if not exists ai_providers_owner_idx
  on public.ai_providers (owner_email, kind, active);

alter table public.ai_providers enable row level security;
-- no policies: service_role only (server-side).
