-- Biblioteca viva de estruturas de anúncio (Ofensiva Tráfego IA, redesign-v2).
-- Run once in Supabase: SQL Editor -> paste -> Run.
-- RLS on, no public policies: only the service_role key (server-side) can
-- read/write. The app exposes a filtered read API and admin write API.

create table if not exists public.ad_structures (
  id text primary key,
  slug text not null unique,
  name text not null,
  description text not null default '',
  funnel_stage text not null
    check (funnel_stage in ('topo', 'meio', 'fundo')),
  category text not null default '',
  trigger text not null default '',
  placement text,
  cta_options jsonb not null default '[]'::jsonb,
  image_prompt_structure text,
  i18n jsonb not null default '{}'::jsonb,
  active boolean not null default true,
  created_at timestamptz not null default now()
);
create index if not exists ad_structures_stage_idx
  on public.ad_structures (funnel_stage, active);
create index if not exists ad_structures_slug_idx
  on public.ad_structures (slug);

alter table public.ad_structures enable row level security;
-- no policies: service_role only (server-side). Matches 002_mcp_proposals pattern.
