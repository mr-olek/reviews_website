from __future__ import annotations

import logging
import os
import uuid

logger = logging.getLogger(__name__)

HF_MODEL = "black-forest-labs/FLUX.1-schnell"


def _build_prompt(subject_name: str, review_title: str = '', review_body: str = '') -> str:
    """Build a short image prompt for a pet breed review photo."""
    # Use up to 60 chars of title/body as context
    context = (review_title or review_body or '')[:60].strip()
    if context:
        return f"A happy {subject_name} dog or cat, professional pet photo, {context}, natural lighting, high quality"
    return f"A happy {subject_name} dog or cat, professional pet photo, natural lighting, high quality"


def generate_review_image(
    subject_name: str,
    upload_dir: str,
    api_key: str,
    review_title: str = '',
    review_body: str = '',
) -> str | None:
    """
    Generate a review image using Hugging Face Inference API (FLUX.1-schnell).
    Returns a relative static path like 'images/uploads/reviews/<uuid>.jpg', or None on failure.
    """
    if not api_key:
        logger.warning("HF_API_KEY not set — skipping image generation")
        return None

    try:
        import requests

        prompt = _build_prompt(subject_name, review_title, review_body)
        headers = {"Authorization": f"Bearer {api_key}"}
        payload = {"inputs": prompt}

        resp = requests.post(
            f"https://router.huggingface.co/hf-inference/models/{HF_MODEL}",
            headers=headers,
            json=payload,
            timeout=60,
        )

        if resp.status_code != 200:
            logger.warning(f"[image_gen] HF API returned {resp.status_code}: {resp.text[:200]}")
            return None

        content_type = resp.headers.get("content-type", "")
        if "image" not in content_type:
            logger.warning(f"[image_gen] unexpected content-type: {content_type}")
            return None

        if len(resp.content) < 5000:
            logger.warning(f"[image_gen] image too small ({len(resp.content)} bytes), skipping")
            return None

        ext = "webp" if "webp" in content_type else "jpg"
        filename = f"{uuid.uuid4().hex}.{ext}"
        os.makedirs(upload_dir, exist_ok=True)
        filepath = os.path.join(upload_dir, filename)
        with open(filepath, "wb") as f:
            f.write(resp.content)

        logger.info(f"[image_gen] generated {filename} for '{subject_name}'")
        return f"images/uploads/reviews/{filename}"

    except Exception as e:
        logger.warning(f"[image_gen] generation failed for '{subject_name}': {e}")
        return None


def generate_subject_image(
    subject_name: str,
    category: str,
    subject_slug: str,
    images_dir: str,
    client=None,
    model: str = '',
) -> str | None:
    """Stub — subject images are uploaded manually via admin."""
    logger.info(f"Image generation skipped for {subject_name} (use admin to upload subject images)")
    return None
