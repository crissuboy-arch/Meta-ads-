# Roadmap

## v1.0 ✅ Atual

App Factory funcional com 8 apps, CLI generator, app switcher e skill system.

## v1.1 — Qualidade e Seguranca

- [ ] Tratamento de erro robusto em `list_configs()` (bare except)
- [ ] Validacao de schema JSON na inicializacao (evitar runtime crash com config malformada)
- [ ] SSRF protection expandida (RFC 1918, DNS resolution)
- [ ] Timeouts e limites via config em vez de hardcoded
- [ ] Testes unitarios para `config.py` e `create_app.py`

## v1.2 — Experiencia do Usuario

- [ ] Modo escuro / claro configuravel
- [ ] Exportar conversa (PDF, TXT)
- [ ] Templates de prompt customizaveis pelo usuario
- [ ] Preview de upload antes de analisar
- [ ] Indicadores de progresso mais precisos (progresso real em vez de random)

## v1.3 — Performance e Infra

- [ ] Streaming SSE assincrono (atualmente bloqueia event loop com chamadas sync)
- [ ] Cache de config com TTL configuravel
- [ ] Logger estruturado em vez de print/console.log
- [ ] Rate limiting por app
- [ ] Health check endpoint com metricas

## v2.0 — Multi-Tenant e Colaboracao

- [ ] Autenticacao (API keys por usuario)
- [ ] Historico de conversas por usuario
- [ ] Compartilhamento de analises
- [ ] Webhooks para automacao
- [ ] Plugin system (skills como pacotes instalaveis)

## Futuro

- [ ] Interface de admin web para criar/editar apps (sem CLI)
- [ ] Marketplace de skills (comunidade)
- [ ] Integracao com Meta/Google/TikTok APIs para dados reais
- [ ] Multi-idioma nativo (i18n)
- [ ] App mobile (PWA ou nativo)
