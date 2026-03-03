from __future__ import annotations

import json
import logging
import re
from typing import Optional

logger = logging.getLogger(__name__)

LANG_NAMES = {
    'uk': 'Ukrainian',
    'de': 'German',
    'fr': 'French',
    'es': 'Spanish',
}


def _extract_json(text: str) -> dict:
    """Extract JSON from Claude's response (handles markdown code fences)."""
    # Strip markdown fences if present
    text = re.sub(r'^```(?:json)?\s*', '', text.strip(), flags=re.MULTILINE)
    text = re.sub(r'\s*```$', '', text.strip(), flags=re.MULTILINE)
    return json.loads(text.strip())


def process_review(raw_review: dict, client, model: str = 'claude-sonnet-4-6') -> Optional[dict]:
    """
    Translate + paraphrase a review from Russian to English using Claude.
    Returns processed review dict or None on failure.
    """
    title = raw_review.get('title', '')
    body = raw_review.get('body', '')

    if not title or not body:
        return None

    prompt = f"""You are a professional translator and editor.

I have a review originally written in Russian (or another language). Please:
1. Translate it to natural, fluent English
2. Lightly paraphrase it to make it unique while preserving the original meaning and sentiment
3. Keep the same overall structure and tone (positive/negative/neutral)
4. Do NOT change the star rating or factual content

Return a JSON object with exactly these fields:
- "title": translated and paraphrased title
- "body": translated and paraphrased review body

Original title: {title}

Original body:
{body}

Return only valid JSON, no markdown, no extra text."""

    try:
        message = client.messages.create(
            model=model,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}],
        )
        content = message.content[0].text
        result = _extract_json(content)

        if not result.get('title') or not result.get('body'):
            logger.warning("process_review: missing title or body in response")
            return None

        return {**raw_review, 'title': result['title'], 'body': result['body']}
    except Exception as e:
        logger.error(f"process_review failed: {e}")
        return None


def process_reviews_batch(reviews: list[dict], client, model: str = 'claude-sonnet-4-6') -> list[dict]:
    processed = []
    for i, review in enumerate(reviews):
        logger.info(f"Processing review {i + 1}/{len(reviews)}")
        result = process_review(review, client, model)
        if result:
            processed.append(result)
    return processed


def translate_with_google(
    items: list[dict],
    target_lang: str,
    fields: list[str],
) -> dict[int, dict]:
    """
    Translate specified fields using Google Translate (free, no API key).
    Falls back to original text on any per-field error.
    """
    try:
        from deep_translator import GoogleTranslator
    except ImportError:
        logger.warning("deep-translator not installed; skipping Google fallback")
        return {}

    # Build flat list of (item_id, field, text) to translate in one batch call
    flat_texts = []
    flat_keys = []
    for item in items:
        for f in fields:
            text = (item.get(f) or '').strip()
            flat_texts.append(text or ' ')   # empty string breaks the API
            flat_keys.append((item['id'], f))

    try:
        translator = GoogleTranslator(source='en', target=target_lang)
        # Split into chunks of 128 to avoid rate limits
        chunk_size = 128
        translated_flat = []
        for i in range(0, len(flat_texts), chunk_size):
            chunk = flat_texts[i:i + chunk_size]
            translated_flat.extend(translator.translate_batch(chunk))
    except Exception as e:
        logger.error(f"translate_with_google failed for lang={target_lang}: {e}")
        return {}

    result: dict[int, dict] = {}
    for (item_id, field), translated in zip(flat_keys, translated_flat):
        result.setdefault(item_id, {})[field] = translated or ''
    return result


def translate_texts_batch(
    items: list[dict],
    target_lang: str,
    fields: list[str],
    client,
    model: str = 'claude-haiku-4-5-20251001',
) -> dict[int, dict]:
    """
    Translate specified fields of items to target_lang in one API call.

    items: list of dicts, each must have 'id' plus the specified fields.
    Returns: {id: {field: translated_value}}
    """
    lang_name = LANG_NAMES.get(target_lang, target_lang)

    input_items = []
    for item in items:
        entry = {'id': item['id']}
        for f in fields:
            entry[f] = item.get(f) or ''
        input_items.append(entry)

    prompt = (
        f"Translate the following content from English to {lang_name}. "
        "Preserve tone, meaning, formatting, and newlines (especially in list fields).\n"
        "Return a JSON array with the same structure — same 'id' values, all text fields translated.\n\n"
        f"Input:\n{json.dumps(input_items, ensure_ascii=False)}\n\n"
        "Return only a valid JSON array, no markdown."
    )

    try:
        message = client.messages.create(
            model=model,
            max_tokens=8000,
            messages=[{"role": "user", "content": prompt}],
        )
        result = _extract_json(message.content[0].text)
        if isinstance(result, list):
            return {
                item['id']: {f: item.get(f, '') for f in fields}
                for item in result
                if isinstance(item, dict) and 'id' in item
            }
        return {}
    except Exception as e:
        logger.error(f"translate_texts_batch failed for lang={target_lang}: {e}")
        return {}
