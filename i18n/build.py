#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera as configs traduzidas a partir de configs/meta-ads.json (EN, fonte).

Uso:
    python3 i18n/build.py

Para cada idioma em meta.SUPPORTED_LANGS:
  - EN: injeta messages/ui_strings/languages/lang dentro da própria
    configs/meta-ads.json (sem alterar os demais campos).
  - Demais idiomas: clona a config EN, aplica o dicionário T por caminho
    (deep-set), injeta messages/ui_strings/languages/lang e grava
    configs/meta-ads-<lang>.json.

Rodar de novo é seguro e idempotente.
"""
import copy
import importlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CONFIGS_DIR = os.path.join(ROOT, "configs")
SOURCE = os.path.join(CONFIGS_DIR, "meta-ads.json")

sys.path.insert(0, HERE)
import meta as meta_mod  # noqa: E402


def _step(cur, part):
    """Um passo de descida: índice numérico, chave de dict, ou id em lista."""
    if isinstance(cur, list):
        if part.isdigit():
            return cur[int(part)]
        for el in cur:
            if isinstance(el, dict) and el.get("id") == part:
                return el
        raise KeyError(f"id '{part}' não encontrado na lista")
    return cur[part]


def deep_set(obj, path, value):
    parts = path.split(".")
    cur = obj
    for part in parts[:-1]:
        cur = _step(cur, part)
    last = parts[-1]
    if isinstance(cur, list):
        cur[int(last)] = value
    else:
        cur[last] = value


def deep_get(obj, path):
    cur = obj
    for part in path.split("."):
        cur = _step(cur, part)
    return cur


def enrich(cfg, lang, mod):
    cfg["lang"] = lang
    cfg["languages"] = meta_mod.LANGUAGES
    cfg["messages"] = mod.MESSAGES
    cfg["ui_strings"] = mod.UI
    cfg["base_system"] = meta_mod.BASE_SYSTEM[lang]
    return cfg


def main():
    with open(SOURCE, "r", encoding="utf-8") as f:
        base = json.load(f)

    languages = meta_mod.SUPPORTED_LANGS
    written = []
    for lang in languages:
        mod = importlib.import_module(f"t_{lang}")

        if lang == "en":
            cfg = enrich(copy.deepcopy(base), lang, mod)
            out = SOURCE
        else:
            cfg = copy.deepcopy(base)
            for path, value in mod.T.items():
                cur_val = deep_get(cfg, path)
                if not isinstance(cur_val, str):
                    raise TypeError(f"{path}: esperado str, veio {type(cur_val)}")
                deep_set(cfg, path, value)
            enrich(cfg, lang, mod)
            out = os.path.join(CONFIGS_DIR, f"meta-ads-{lang}.json")

        with open(out, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
            f.write("\n")
        written.append(out)
        print(f"[ok] {lang}: {out}")

    print(f"\n{len(written)} configs escritas.")


if __name__ == "__main__":
    main()
