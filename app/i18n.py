"""Lightweight i18n helpers for Verdictly."""
from __future__ import annotations

import json as _json
import os
from flask import session

LANGUAGES: dict[str, dict] = {
    'en': {'name': 'English',    'flag': '🇬🇧'},
    'uk': {'name': 'Ukrainian',  'flag': '🇺🇦'},
    'de': {'name': 'German',     'flag': '🇩🇪'},
    'fr': {'name': 'French',     'flag': '🇫🇷'},
    'es': {'name': 'Spanish',    'flag': '🇪🇸'},
}

_trans: dict[str, dict] = {}


def load_translations(app=None) -> None:
    """Load all translation JSON files into memory."""
    base = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'translations')
    for code in LANGUAGES:
        path = os.path.join(base, f'{code}.json')
        if os.path.exists(path):
            with open(path, encoding='utf-8') as f:
                _trans[code] = _json.load(f)


def get_lang() -> str:
    return session.get('lang', 'en')


def t(key: str, **kwargs) -> str:
    """Translate a UI key like 'ui.home'. Falls back to English."""
    lang = get_lang()
    parts = key.split('.')
    def _lookup(data):
        val = data
        for p in parts:
            if isinstance(val, dict):
                val = val.get(p)
            else:
                return None
        return val

    value = _lookup(_trans.get(lang, {})) or _lookup(_trans.get('en', {})) or key
    if kwargs:
        for k, v in kwargs.items():
            value = value.replace('{' + k + '}', str(v))
    return value


def t_cat(slug: str, field: str = 'name', fallback: str = '') -> str:
    """Translate a category field. Returns fallback (e.g. DB name) if missing."""
    lang = get_lang()
    cats = _trans.get(lang, {}).get('categories', {})
    val = cats.get(slug, {}).get(field)
    if val is None:
        cats_en = _trans.get('en', {}).get('categories', {})
        val = cats_en.get(slug, {}).get(field)
    return val or fallback


def t_subcat(slug: str, field: str = 'name', fallback: str = '') -> str:
    """Translate a subcategory field. Returns fallback if missing."""
    lang = get_lang()
    subcats = _trans.get(lang, {}).get('subcategories', {})
    val = subcats.get(slug, {}).get(field)
    if val is None:
        subcats_en = _trans.get('en', {}).get('subcategories', {})
        val = subcats_en.get(slug, {}).get(field)
    return val or fallback


def get_trans(obj, field: str, lang: str = None) -> str:
    """
    Return the translated value of a DB model field for the current language.
    Falls back to the original English DB value if translation is unavailable.
    obj.translations is a JSON TEXT column: {lang: {field: value}}
    """
    if lang is None:
        lang = get_lang()
    original = getattr(obj, field, '') or ''
    if lang == 'en':
        return original
    try:
        trans = _json.loads(obj.translations or '{}')
        val = trans.get(lang, {}).get(field)
        if val:
            return val
    except Exception:
        pass
    return original
