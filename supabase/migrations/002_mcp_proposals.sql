-- MCP approval-gate audit log (Meta Ads Expert PRO, Fase 2).
-- Run once in Supabase: SQL Editor -> paste -> Run.
-- RLS on, no public policies: only the service_role key (server-side) can
-- read/write. Never store ad-account tokens here — only action metadata.

create table if not exists public.mcp_proposals (
  id text primary key,
  action text not null,
  params jsonb not null default '{}'::jsonb,
  summary text not null default '',
  status text not null default 'pending'
    check (status in ('pending','approved','executed','rejected','failed')),
  requested_by text not null default 'claude',
  result jsonb,
  created_at bigint not null,
  decided_at bigint
);
create index if not exists mcp_proposals_status_idx
  on public.mcp_proposals (status, created_at desc);

alter table public.mcp_proposals enable row level security;
