#!/usr/bin/env python3
"""
ForgeHub AI - App Factory
Cria um novo aplicativo em segundos.

Uso:
    python create_app.py <nome-do-app>
    python create_app.py <nome-do-app> --template meta-ads

Exemplo:
    python create_app.py relacionamento
    python create_app.py nutricao --template copywriter
"""

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).parent


TEMPLATE_JSON = """{
    "app_id": "__APP_ID__",
    "branding": {
        "app_name": "__APP_NAME__",
        "short_name": "__APP_SHORT__",
        "logo_text": "ForgeHub AI",
        "tagline": "ForgeHub AI",
        "company": "ForgeHub AI",
        "copyright": "ForgeHub AI",
        "support_email": "suporte@forgehub.ai",
        "site": "https://forgehub.ai",
        "plan_name": "Professional",
        "plan_badge": "PRO",
        "favicon_emoji": "\\u26A1",
        "assistant_name": "__APP_ASSISTANT__"
    },
    "colors": {
        "primary": "#2563EB",
        "secondary": "#1D4ED8",
        "accent": "#3B82F6",
        "gold": "#F6C453",
        "bg_deep": "#08142E",
        "bg": "#0B1E3C",
        "bg_mid": "#0F2447",
        "bg_light": "#1A3359"
    },
    "models": {
        "default": "meta/llama-3.1-70b-instruct",
        "vision": "meta/llama-3.2-90b-vision-instruct",
        "expert_underlying": "meta/llama-3.1-70b-instruct"
    },
    "skill": "__APP_ID__.md",
    "expert_name": "__APP_EXPERT__",
    "hero": {
        "title": "Bem-vindo ao __APP_NAME__",
        "highlight": "impulsionado por IA",
        "subtitle": "Use a inteligencia artificial para criar, analisar e otimizar seus resultados.",
        "floats": [
            {"label": "Performance", "value": "2x", "color": "gold"},
            {"label": "Resultados", "value": "+45%", "color": "green"},
            {"label": "Eficiencia", "value": "3x"},
            {"label": "ROI", "value": "280%", "color": "green"}
        ]
    },
    "dashboard_metrics": [
        {"label": "Performance", "value": "2.5x", "color": "gold", "trend": "up", "trend_value": "15%"},
        {"label": "Resultados", "value": "+45%", "trend": "up", "trend_value": "8%"},
        {"label": "Eficiencia", "value": "3x", "trend": "up", "trend_value": "12%"},
        {"label": "Conversoes", "value": "89", "color": "green"},
        {"label": "Sessoes", "value": "2.4K"},
        {"label": "Taxa", "value": "4.2%"}
    ],
    "sidebar": {
        "categories": [
            {"label": "Menu", "key": "menu"},
            {"label": "Ferramentas", "key": "ferramentas"},
            {"label": "Analise", "key": "analise"}
        ],
        "items": {
            "menu": [
                {"id": "dashboard", "label": "Dashboard", "icon": "\\uD83D\\uDCCA"}
            ],
            "ferramentas": [
                {"id": "ferramenta-1", "label": "Ferramenta 1", "icon": "\\u2699\\uFE0F"},
                {"id": "ferramenta-2", "label": "Ferramenta 2", "icon": "\\uD83D\\uDEE0\\uFE0F"}
            ],
            "analise": [
                {"id": "analisar", "label": "Analisar", "icon": "\\uD83D\\uDD0D"},
                {"id": "otimizar", "label": "Otimizar", "icon": "\\uD83D\\uDE80"}
            ]
        }
    },
    "tools": [
        {"id": "ferramenta-1", "icon": "\\u2699\\uFE0F", "label": "Ferramenta 1", "desc": "Descricao da ferramenta principal."},
        {"id": "ferramenta-2", "icon": "\\uD83D\\uDEE0\\uFE0F", "label": "Ferramenta 2", "desc": "Descricao da segunda ferramenta."},
        {"id": "analisar", "icon": "\\uD83D\\uDD0D", "label": "Analisar", "desc": "Analise completa com recomendacoes."},
        {"id": "otimizar", "icon": "\\uD83D\\uDE80", "label": "Otimizar", "desc": "Otimizacao baseada em dados."}
    ],
    "imports": [
        {"id": "import-imagem", "icon": "\\uD83D\\uDCF7", "label": "Upload de Imagem"},
        {"id": "import-pdf", "icon": "\\uD83D\\uDCC4", "label": "Upload de PDF"},
        {"id": "import-lp", "icon": "\\uD83C\\uDF10", "label": "Site / URL"}
    ],
    "import_tags": ["Produto", "Publico", "Oferta", "Estrategia", "Resultado"],
    "niches": [
        {"id": "nicho-1", "icon": "\\uD83C\\uDFCD\\uFE0F", "label": "Nicho 1"},
        {"id": "nicho-2", "icon": "\\u2728", "label": "Nicho 2"},
        {"id": "nicho-3", "icon": "\\u2696\\uFE0F", "label": "Nicho 3"},
        {"id": "nicho-4", "icon": "\\uD83C\\uDFE5", "label": "Nicho 4"}
    ],
    "action_buttons": [
        {"id": "ferramenta-1", "label": "Ferramenta 1", "icon": "\\u2699\\uFE0F"},
        {"id": "ferramenta-2", "label": "Ferramenta 2", "icon": "\\uD83D\\uDEE0\\uFE0F"},
        {"id": "analisar", "label": "Analisar", "icon": "\\uD83D\\uDD0D"},
        {"id": "otimizar", "label": "Otimizar", "icon": "\\uD83D\\uDE80"}
    ],
    "uploads": {
        "image": true,
        "pdf": true,
        "screenshot": false,
        "url": true
    },
    "url_analysis": {
        "types": [
            {"id": "lp", "label": "Site", "icon": "\\uD83C\\uDF10"}
        ],
        "platform_patterns": [],
        "product_type_keywords": {}
    },
    "system_prompts": {
        "image": "Voce e um analista especialista.\\nAnalise a imagem e extraia todas as informacoes disponiveis.",
        "pdf": "Voce e um analista especialista analisando um PDF.",
        "screenshot": "",
        "url": {
            "lp": "Voce e um especialista analisando um site."
        }
    },
    "prompts": {
        "dashboard": "Voce e o assistente do __APP_NAME__. Como posso ajudar hoje?",
        "ferramenta-1": "TODO: Personalize este prompt para a ferramenta 1.",
        "ferramenta-2": "TODO: Personalize este prompt para a ferramenta 2.",
        "analisar": "TODO: Personalize este prompt para analise.",
        "otimizar": "TODO: Personalize este prompt para otimizacao.",
        "import-imagem": "TODO: Personalize o prompt para upload de imagem.",
        "import-pdf": "TODO: Personalize o prompt para upload de PDF.",
        "import-lp": "TODO: Personalize o prompt para analise de URL.",
        "nicho-1": "Voce e um consultor especializado em Nicho 1.",
        "nicho-2": "Voce e um consultor especializado em Nicho 2.",
        "nicho-3": "Voce e um consultor especializado em Nicho 3.",
        "nicho-4": "Voce e um consultor especializado em Nicho 4."
    }
}"""

TEMPLATE_SKILL = """# {expert_name}

Voc\u00ea \u00e9 um especialista em {app_name}.

## Regras

1. Seja consultivo: fa\u00e7a perguntas antes de dar respostas completas
2. Pergunte uma coisa de cada vez
3. Use linguagem t\u00e9cnica mas acess\u00edvel
4. Sempre valide o entendimento antes de prosseguir
5. Ofere\u00e7a exemplos pr\u00e1ticos quando relevante

## Comportamento

- Inicie a conversa se apresentando e perguntando qual o objetivo do usu\u00e1rio
- N\u00e3o gere planos completos sem antes entender o contexto
- Ap\u00f3s entender o cen\u00e1rio, ofere\u00e7a an\u00e1lise detalhada
- Pergunte se o usu\u00e1rio deseja implementar as recomenda\u00e7\u00f5es
"""


def to_title(slug):
    return slug.replace("-", " ").title()


def generate_app(name, template=None):
    app_id = name.lower().strip().replace(" ", "-")
    app_name = to_title(name) + " Expert PRO" if not name.endswith("PRO") else to_title(name)
    app_short = to_title(name) + " PRO"
    app_assistant = to_title(name) + " AI"
    app_expert = to_title(name) + " Expert"

    print(f"\n  Criando aplicativo: {app_name} ({app_id})")
    print(f"  {'=' * 40}")

    # --- config ---
    cfg_str = TEMPLATE_JSON
    replacements = {
        "__APP_ID__": app_id,
        "__APP_NAME__": app_name,
        "__APP_SHORT__": app_short,
        "__APP_ASSISTANT__": app_assistant,
        "__APP_EXPERT__": app_expert,
    }
    for k, v in replacements.items():
        cfg_str = cfg_str.replace(k, v)
    cfg = json.loads(cfg_str)
    cfg["app_id"] = app_id

    if template and template != "default":
        template_path = ROOT / "configs" / f"{template}.json"
        if template_path.is_file():
            with open(template_path, "r", encoding="utf-8") as f:
                tmpl = json.load(f)
            cfg = tmpl.copy()
            cfg["app_id"] = app_id
            cfg["branding"]["app_name"] = app_name
            cfg["branding"]["short_name"] = app_short
            cfg["branding"]["assistant_name"] = app_assistant
            cfg["skill"] = f"{app_id}.md"
            cfg["expert_name"] = app_expert
            print(f"  Template base: {template}.json")

    config_path = ROOT / "configs" / f"{app_id}.json"
    if config_path.is_file():
        resp = input(f"  [!] configs/{app_id}.json ja existe. Sobrescrever? (s/N): ")
        if resp.lower() != "s":
            print("  Cancelado.")
            return False

    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)
    print(f"  [OK] configs/{app_id}.json")

    # --- skill ---
    skill_path = ROOT / "skills" / f"{app_id}.md"
    if skill_path.is_file():
        resp = input(f"  [!] skills/{app_id}.md ja existe. Sobrescrever? (s/N): ")
        if resp.lower() != "s":
            print("  Skill mantida.")
        else:
            with open(skill_path, "w", encoding="utf-8") as f:
                f.write(TEMPLATE_SKILL.format(expert_name=app_expert, app_name=app_name))
            print(f"  [OK] skills/{app_id}.md")
    else:
        with open(skill_path, "w", encoding="utf-8") as f:
            f.write(TEMPLATE_SKILL.format(expert_name=app_expert, app_name=app_name))
        print(f"  [OK] skills/{app_id}.md")

    # --- assets ---
    assets_dir = ROOT / "assets" / app_id
    assets_dir.mkdir(parents=True, exist_ok=True)
    readme_asset = assets_dir / "README.md"
    if not readme_asset.is_file():
        with open(readme_asset, "w", encoding="utf-8") as f:
            f.write(f"# {app_name}\n\nAssets espec\u00edficos do aplicativo.\n")
    print(f"  [OK] assets/{app_id}/")

    # --- apps dir placeholder ---
    apps_dir = ROOT / "apps" / app_id
    apps_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n  {'=' * 40}")
    print(f"  App criado com sucesso!")
    print(f"  Para testar: export APP_ID={app_id} && uvicorn app_core:create_app --reload")
    print(f"  Ou selecione no frontend pelo seletor de apps.\n")
    return True


def list_apps():
    configs_dir = ROOT / "configs"
    if not configs_dir.is_dir():
        print("  Nenhum app encontrado.")
        return
    apps = sorted(configs_dir.glob("*.json"))
    if not apps:
        print("  Nenhum app encontrado.")
        return
    print(f"\n  Aplicativos disponiveis ({len(apps)}):")
    print(f"  {'=' * 40}")
    for fpath in apps:
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
            name = data.get("branding", {}).get("app_name", fpath.stem)
            print(f"  * {fpath.stem:20s}  {name}")
        except Exception:
            print(f"  * {fpath.stem:20s}  (erro ao ler)")
    print()


def show_help():
    print(__doc__)


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] in ("--help", "-h", "help"):
        show_help()
        sys.exit(0)

    if sys.argv[1] == "list":
        list_apps()
        sys.exit(0)

    name = sys.argv[1]
    template = "default"
    if "--template" in sys.argv:
        idx = sys.argv.index("--template")
        if idx + 1 < len(sys.argv):
            template = sys.argv[idx + 1]

    generate_app(name, template if template != "default" else None)
