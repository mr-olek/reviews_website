from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)


def generate_subject_image(
    subject_name: str,
    category: str,
    subject_slug: str,
    images_dir: str,
    client=None,
    model: str = '',
) -> str | None:
    """
    Placeholder: Claude does not generate images.
    Returns None — subject pages show a placeholder icon instead.
    To enable images, integrate a separate image service (e.g. Stability AI).
    """
    logger.info(f"Image generation skipped for {subject_name} (Claude doesn't generate images)")
    return None
