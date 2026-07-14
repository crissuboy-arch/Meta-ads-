BRANDING = {
    "app_name": "Meta Ads Expert PRO",
    "short_name": "Expert PRO",
    "logo_text": "ForgeHub AI",
    "tagline": "ForgeHub AI",
    "company": "ForgeHub AI",
    "copyright": "ForgeHub AI",
    "support_email": "suporte@forgehub.ai",
    "site": "https://forgehub.ai",
    "primary_color": "#2563EB",
    "secondary_color": "#1D4ED8",
    "accent_color": "#3B82F6",
    "gold_color": "#F6C453",
    "plan_name": "Professional",
    "plan_badge": "PRO",
    "favicon_emoji": "\u26A1",
}

SIDEBAR_ITEMS = {
    "menu": [
        {"id": "dashboard", "label": "Dashboard", "icon": "\U0001F4CA"},
    ],
    "plataformas": [
        {"id": "criar-campanha", "label": "Meta Ads", "icon": "\U0001F4C8"},
        {"id": "google-ads", "label": "Google Ads", "icon": "\U0001F310"},
        {"id": "tiktok-ads", "label": "TikTok Ads", "icon": "\U0001F4F9"},
    ],
    "criacao": [
        {"id": "criar-publico", "label": "P\u00FAblicos", "icon": "\U0001F3AF"},
        {"id": "criar-copy", "label": "Copywriting", "icon": "\u270D\uFE0F"},
        {"id": "criar-criativos", "label": "Criativos", "icon": "\U0001F3A8"},
        {"id": "criar-lp", "label": "Landing Pages", "icon": "\U0001F4E2"},
    ],
    "otimizacao": [
        {"id": "remarketing", "label": "Remarketing", "icon": "\U0001F504"},
        {"id": "funis", "label": "Funis", "icon": "\U0001F9F0"},
        {"id": "auditoria", "label": "Auditoria", "icon": "\U0001F50D"},
        {"id": "escalar", "label": "Escalar", "icon": "\U0001F680"},
    ],
    "analytics": [
        {"id": "analytics", "label": "Analytics", "icon": "\U0001F4CA"},
        {"id": "pixel", "label": "Pixel", "icon": "\U0001F4E1"},
        {"id": "conversoes", "label": "Convers\u00F5es", "icon": "\u2705"},
    ],
    "automacoes": [
        {"id": "automacoes", "label": "Automa\u00E7\u00F5es", "icon": "\u2699\uFE0F"},
    ],
}

SIDEBAR_CATEGORIES = [
    {"label": "Menu", "key": "menu"},
    {"label": "Plataformas", "key": "plataformas"},
    {"label": "Cria\u00E7\u00E3o", "key": "criacao"},
    {"label": "Otimiza\u00E7\u00E3o", "key": "otimizacao"},
    {"label": "Analytics", "key": "analytics"},
    {"label": "Automa\u00E7\u00F5es", "key": "automacoes"},
]

ACTION_BUTTONS = [
    {"id": "criar-campanha", "label": "Criar Campanha", "icon": "\U0001F680"},
    {"id": "criar-publico", "label": "Criar P\u00FAblico", "icon": "\U0001F3AF"},
    {"id": "criar-copy", "label": "Criar Copy", "icon": "\u270D\uFE0F"},
    {"id": "criar-criativos", "label": "Criar Criativos", "icon": "\U0001F3A8"},
    {"id": "escalar", "label": "Escalar", "icon": "\U0001F4C8"},
    {"id": "criar-lp", "label": "Criar Landing Page", "icon": "\U0001F4E2"},
    {"id": "criar-app", "label": "Criar Aplicativo", "icon": "\U0001F4F1"},
    {"id": "melhorar-ebook", "label": "Melhorar Ebook", "icon": "\U0001F4D6"},
    {"id": "auditoria", "label": "Auditoria Completa", "icon": "\U0001F50D"},
]

PLATFORM_PATTERNS = [
    (r"(shopify|myshopify)\.", "Shopify"),
    (r"hotmart\.", "Hotmart"),
    (r"kiwify\.", "Kiwify"),
    (r"eduzz\.", "Eduzz"),
    (r"monetizze\.", "Monetizze"),
    (r"wordpress\.", "WordPress"),
    (r"lovable\.", "Lovable"),
    (r"flutterflow\.", "FlutterFlow"),
    (r"bubble\.io", "Bubble"),
    (r"github\.", "GitHub"),
    (r"drive\.google\.", "Google Drive"),
    (r"supabase\.", "Supabase"),
    (r"canva\.", "Canva"),
    (r"woocommerce", "WooCommerce"),
    (r"checkout\.", "Checkout"),
    (r"pay\.", "Checkout"),
    (r"pagamento", "Checkout"),
    (r"app\.", "Aplicativo"),
]

PRODUCT_TYPE_KEYWORDS = {
    "infoproduto": ["infoproduto", "curso online", "ebook", "digital"],
    "curso": ["curso", "aula", "treinamento", "forma\u00E7\u00E3o", "m\u00F3dulo"],
    "mentoria": ["mentoria", "mentor", "coaching", "acompanhamento"],
    "ebook": ["ebook", "livro digital", "guia", "manual"],
    "aplicativo": ["app", "aplicativo", "mobile", "ios", "android"],
    "saas": ["saas", "assinatura", "mensalidade", "plano", "software"],
    "loja": ["loja", "ecommerce", "shop", "comprar", "carrinho"],
    "clinica": ["cl\u00EDnica", "m\u00E9dico", "consulta", "sa\u00FAde"],
    "advocacia": ["advogado", "escrit\u00F3rio", "jur\u00EDdico", "direito"],
    "restaurante": ["restaurante", "delivery", "comida", "card\u00E1pio"],
    "estetica": ["est\u00E9tica", "beleza", "procedimento", "harmoniza\u00E7\u00E3o"],
    "odontologia": ["dentista", "odontologia", "sorriso", "implante"],
    "academia": ["academia", "personal", "treino", "muscula\u00E7\u00E3o"],
    "imobiliaria": ["imobili\u00E1ria", "im\u00F3vel", "apartamento", "casa"],
    "consultoria": ["consultoria", "consultor", "empresarial"],
    "marketplace": ["marketplace", "an\u00FAncio", "classificados"],
    "ferramenta": ["ferramenta", "plataforma", "dashboard"],
    "lead_magnet": ["lead magnet", "isca digital", "gratuito", "download"],
    "workshop": ["workshop", "oficina", "presencial", "evento"],
    "comunidade": ["comunidade", "membership", "grupo exclusivo"],
    "assinatura": ["assinatura", "recorrente", "mensalidade", "plano"],
}
