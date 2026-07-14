# Template Base - Novo Aplicativo

Copie esta pasta como ponto de partida para seu novo app.

## Estrutura

```
seu-app/
├── configs/
│   └── seu-app.json          # Configuração completa do app
├── skills/
│   └── seu-app.md            # System prompt do especialista
├── static/
│   └── index.html            # Frontend (não precisa modificar)
├── templates/
│   └── ...                   # (opcional) templates do app
├── app_core.py               # Backend (não precisa modificar)
├── config.py                 # Carregador de config (não precisa modificar)
└── .env                      # Suas chaves de API
```

## Arquivos que você PRECISA criar

### `configs/seu-app.json`
Configuração completa do aplicativo. Copie de `configs/meta-ads.json` e modifique:
- `branding`: nome, logo, cores
- `colors`: paleta de cores
- `skill`: nome do arquivo .md em skills/
- `sidebar`: menus laterais
- `tools`: ferramentas principais
- `imports`: tipos de upload disponíveis
- `prompts`: sistema de perguntas consultivas
- `system_prompts`: prompts para upload de imagem, PDF, URL
- `action_buttons`: botões rápidos pós-análise
- `uploads`: quais uploads habilitar

### `skills/seu-app.md`
System prompt do especialista. Este conteúdo é injetado como `system` em toda conversa.

## Para executar

```bash
# Escolher qual app rodar
export APP_ID=seu-app

# Iniciar
python run.py
# ou
uvicorn app_core:app --reload
```

## Em <5 minutos você cria um app novo:

1. `cp configs/meta-ads.json configs/meu-app.json`
2. Editar branding, colors, skill
3. `cp skills/pro.md skills/meu-app.md`
4. Editar o system prompt do especialista
5. `export APP_ID=meu-app && python run.py`
6. Pronto.
