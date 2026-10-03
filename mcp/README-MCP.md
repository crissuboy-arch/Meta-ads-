# MCP da Meta — teste com R$ 50 (Fase 1 + 2)

Servidor MCP que deixa o Claude ler sua conta de anúncios e **propor**
ações (criar campanha, conjunto, pausar/ativar) — nada executa sem você
dizer "sim" no chat. O token da Meta nunca sai da sua máquina.

## O que só você faz (eu não tenho como)

### 1. Criar o app na Meta (10 min, uma vez só)
1. Abra developers.facebook.com → **Meus apps** → **Criar app** → tipo **Negócios**.
2. No painel do app: **Adicionar produto** → **API de Marketing**.
3. Em **Ferramentas** → **Graph API Explorer**:
   - Selecione seu app, clique em **Gerar token de acesso**,
     marque `ads_read` e `ads_management`.
   - Clique em **Abrir no Graph API Explorer** e troque para token de longa
     duração (botão "i" do token → **Estender**). Dura ~60 dias.
4. Anote o **ID da sua conta de anúncios** (só números):
   Gerenciador de Anúncios → canto superior → ID da conta.

### 2. Configurar o .env (na SUA máquina)
```bash
cd ~/workspace/Meta-ads-   # ou onde você clonou o repo
cp mcp/.env.example mcp/.env
nano mcp/.env              # cole o token, o ID da conta e as chaves do Supabase
```
> ⚠️ O token vai SÓ nesse arquivo. Nunca no chat, nunca no git
> (o `.gitignore` já bloqueia `mcp/.env`).

### 3. Criar a tabela de auditoria no Supabase (2 min, uma vez só)
Supabase → **SQL Editor** → cole o conteúdo de
`supabase/migrations/002_mcp_proposals.sql` → **Run**.

### 4. Conectar o Claude Code ao MCP
```bash
claude mcp add meta-ads-pro -- /caminho/para/Meta-ads-/mcp/.venv/bin/python /caminho/para/Meta-ads-/mcp/server.py
```
Depois é só conversar: *"lista minhas campanhas"*, *"mostra o insights da
conta nos últimos 30 dias"*.

## Como funciona a trava de segurança

- Ferramentas de **leitura** (`list_campaigns`, `list_adsets`, `get_insights`)
  rodam livres — não gastam nada, não mudam nada.
- **Não existe** ferramenta de escrita direta. O único caminho é:
  1. `propose_action` → grava a proposta como *pending* (Supabase ou arquivo
     local) e devolve um resumo em português claro.
  2. Você lê o resumo e diz **"sim, executa"** (ou "não").
  3. `approve_proposal` → executa UMA vez. Proposta decidida nunca roda de novo.
- Campanhas são **sempre criadas PAUSADAS**. Ativar exige outra aprovação.
- Tudo fica registrado em `list_proposals` (auditoria: pending/executed/rejected/failed).

## Roteiro do teste de R$ 50

1. **Fase 1 (R$ 0):** só leitura. Peça insights da conta e confirme que os
   números batem com o Gerenciador de Anúncios.
2. **Fase 2:** peça para *propor* a campanha de teste (ex: R$ 10/dia,
   objetivo vendas, direcionando para a página `/sales`). Revise a proposta,
   aprove → campanha nasce **pausada**.
3. **Fase 3:** revise tudo no Gerenciador de Anúncios e só então aprove
   `set_status` → ACTIVE. Acompanhe 5 dias, R$ 50 no total.
4. Regras de kill automático (tipo "pausa se CPA > X") ficam para DEPOIS —
   com R$ 50 qualquer regra mata a campanha no aprendizado.

## Testes do módulo

```bash
mcp/.venv/bin/python -m pytest mcp/tests/ -q   # 10 testes, tudo mockado
```

## Lições aprendidas (teste real, 2026-10-03)
1. **API v21 exige `is_adset_budget_sharing_enabled`** (True/False) em campanhas
   SEM orçamento próprio (ABO). Sem isso, erro 100:4834011.
2. **Conjuntos: espelhar a estrutura de um que funciona.** Nesta conta, foi
   preciso `bid_strategy: LOWEST_COST_WITHOUT_CAP` explícito (sem ele, erro
   100:2490487 pedindo bid_amount).
3. **Campanha CBO + conjunto via API falhou** (100:1815857). ABO funcionou.
   Para testes, ABO espelhando conjunto existente é o caminho.
4. **Criativo com identidade da Página exige:** página atribuída à conta de
   anúncios no Gerenciador de Negócios (Contas de anúncios → Adicionar ativos
   → Páginas). Sem isso, erro 200:1815199. Propagação pode levar minutos.
5. **ID da página ≠ URL do perfil.** O ID usável da API vem de
   `GET /me/accounts` (aqui: Meta Ads Expert PRO = 352558807930156).
6. **Token via arquivo** (`tokemads.txt`): a usuária envia, o script lê UMA
   vez, usa e **apaga imediatamente**. Evita erros de transcrição em tokens
   longos. Nunca commitar.
7. **Criativo (object_story_spec) exige `pages_manage_posts`.** O link_data cria
   um post nao-publicado (dark post) NA pagina — `pages_manage_ads` sozinho
   nao basta (erro 200:1815199). Token precisa de: ads_read, ads_management,
   pages_manage_ads E pages_manage_posts.
8. **App precisa estar LIVE (modo publico).** Criar criativos (dark posts na
   Pagina) via API com app em desenvolvimento falha: 100:1885183 "deve estar
   em modo publico". Caminho: developers.facebook.com → app → alternar de
   "Em desenvolvimento" para "Live" (pode pedir URL de privacidade, icone,
   categoria). Como admin do app, as permissoes concedidas continuam
   funcionando para o proprio uso.
9. **MODO LIVE: cuidado!** Criar o POST do criativo via API exige app Live
   (erro 100:1885183). MAS a doc oficial avisa: em modo Live, permissoes NAO
   aprovadas no App Review param de funcionar — INCLUSIVE para o admin do app.
   Ou seja: virar Live sem App Review QUEBRA tudo (campanha, conjunto etc.).
   Caminho completo p/ Live: basic settings (privacy URL, icone 1024, email,
   terms, data deletion) + Business Verification + App Review
   (ads_read, ads_management, pages_manage_ads, pages_manage_posts) ~1-2 sem.
   ATALHO: publicar o post criativo manualmente na Pagina e usar
   `object_story_id` (post existente) no criativo — nao cria post via API,
   nao exige Live.
10. **Pagina de empresa some do /me/accounts sem `business_management`.**
    Depois de adicionar a Pagina ao Business Manager, o token de usuaria
    precisa de `business_management` para listar a pagina e obter o page
    token. Sem isso: /me/accounts nao retorna a pagina; /published_posts
    exige page token (#210); /posts da 190/2069032 (user token onde page
    token e exigido). Set completo do token: ads_read, ads_management,
    pages_manage_ads, pages_manage_posts, pages_show_list,
    pages_read_engagement, business_management (+ public_profile).
11. **object_story_id exige o ID real do post** (pageid_postid da API, via
    /published_posts com page token). IDs "construidos" (ex.: fbid da foto)
    dao 100:1487472 Invalid parameter.
12. **Conta precisa de acesso ao PIXEL.** Criar anuncio em conjunto com
    Purchase falha (200:1815045 "A conta nao tem acesso ao pixel") se o pixel
    nao estiver atribuido a conta de anuncios no BM (Fontes de dados →
    Pixels → Adicionar ativos → Contas de anuncios). O conjunto aceita o
    pixel na criacao, mas o ANUNCIO valida o acesso.
13. **/published_posts: usar fields minimos.** Com `fields=id,message,...`
    pode dar erro #12 deprecate; com chamada minima (sem fields ou so id)
    funciona e retorna os IDs reais (pageid_postid).
14. **Criativos de posts existentes funcionam em dev mode**
    (create_adcreative_from_post). Os 3 posts viraram 3 criativos + 3 ads.

## TESTE ATIVO (2026-10-03)
- Campanha ABO 120251379447600183: ACTIVE
- Conjunto 120251379454920183 (US Broad 18+, R$10/dia, Purchase): ACTIVE
- 3 ads (120251381146820183, ...147310183, ...148030183): ACTIVE
- Orcamento: R$60 (~6 dias a R$10/dia). Tudo via MCP (propose->approve).
- Campanha CBO inicial 120251379377400183 segue pausada (arquivar depois).
