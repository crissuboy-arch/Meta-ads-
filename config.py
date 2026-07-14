import json
import os
from pathlib import Path

ROOT = Path(__file__).parent

def load_config(app_id=None):
    if app_id is None:
        app_id = os.getenv("APP_ID", "meta-ads")
    config_path = ROOT / "configs" / f"{app_id}.json"
    if not config_path.is_file():
        raise FileNotFoundError(
            f"Configuracao nao encontrada: {config_path}. "
            f"Crie o arquivo configs/{app_id}.json ou ajuste a variavel APP_ID."
        )
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def list_configs():
    configs_dir = ROOT / "configs"
    configs = []
    if configs_dir.is_dir():
        for fpath in sorted(configs_dir.glob("*.json")):
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                configs.append({
                    "app_id": data.get("app_id", fpath.stem),
                    "app_name": data.get("branding", {}).get("app_name", fpath.stem),
                    "description": data.get("hero", {}).get("subtitle", ""),
                    "icon": data.get("branding", {}).get("favicon_emoji", ""),
                    "color": data.get("colors", {}).get("primary", "#2563EB"),
                })
            except Exception:
                pass
    return configs

_active_config = None

def get_active_config():
    global _active_config
    if _active_config is None:
        _active_config = load_config()
    return _active_config

def reload_config():
    global _active_config
    _active_config = load_config()
    return _active_config

CONFIG = get_active_config()
BRANDING = CONFIG.get("branding", {})
SIDEBAR_ITEMS = CONFIG.get("sidebar", {}).get("items", {})
SIDEBAR_CATEGORIES = CONFIG.get("sidebar", {}).get("categories", [])
ACTION_BUTTONS = CONFIG.get("action_buttons", [])
PLATFORM_PATTERNS = CONFIG.get("url_analysis", {}).get("platform_patterns", [])
PRODUCT_TYPE_KEYWORDS = CONFIG.get("url_analysis", {}).get("product_type_keywords", {})
PROMPTS = CONFIG.get("prompts", {})
SYSTEM_PROMPTS = CONFIG.get("system_prompts", {})
UPLOADS = CONFIG.get("uploads", {})
TOOLS = CONFIG.get("tools", [])
IMPORTS = CONFIG.get("imports", [])
NICHES = CONFIG.get("niches", [])
DASHBOARD_METRICS = CONFIG.get("dashboard_metrics", [])
HERO = CONFIG.get("hero", {})
COLORS = CONFIG.get("colors", {})
IMPORT_TAGS = CONFIG.get("import_tags", [])
MODELS = CONFIG.get("models", {})
URL_TYPES = CONFIG.get("url_analysis", {}).get("types", [])
