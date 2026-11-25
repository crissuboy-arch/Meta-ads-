-- Adiciona o provedor Anthropic (Claude) e contadores de uso em ai_providers.
-- Run once in Supabase: SQL Editor -> paste -> Run.

alter table public.ai_providers
  drop constraint if exists ai_providers_provider_check;
alter table public.ai_providers
  add constraint ai_providers_provider_check
  check (provider in ('gemini', 'openai', 'openrouter', 'anthropic'));

alter table public.ai_providers
  add column if not exists calls_count integer not null default 0;
alter table public.ai_providers
  add column if not exists last_used_at timestamptz;
