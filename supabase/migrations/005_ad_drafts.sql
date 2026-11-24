-- Rascunhos do Criar anúncio (Ofensiva TrÃ¡fego IA, redesign-v2).
-- Run once in Supabase: SQL Editor -> paste -> Run.
-- RLS on, no public policies: only the service_role key (server-side) can
-- read/write.

create table if not exists public.ad_drafts (
  id text primary key,
  owner_email text not null,
  structure_slug text,
  structure_name text,
  briefing jsonb not null default '{}'::jsonb,
  result jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index if not exists ad_drafts_owner_idx
  on public.ad_drafts (owner_email, updated_at desc);

alter table public.ad_drafts enable row level security;
-- no policies: service_role only (server-side).
