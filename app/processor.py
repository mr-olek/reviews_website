from __future__ import annotations

import json
import logging
import re
from typing import Optional

logger = logging.getLogger(__name__)


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
