-- Adiciona "reach" (alcance) a ads_insights, necessario para calcular
-- frequencia (impressoes / alcance). Run once in Supabase SQL Editor.

alter table public.ads_insights
  add column if not exists reach bigint not null default 0;
