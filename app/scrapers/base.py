from __future__ import annotations

import time
import logging
from abc import ABC, abstractmethod
from typing import Optional

logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """Abstract base class for all scrapers."""

    site_name: str = ''
    base_url: str = ''

    def __init__(self, delay: float = 2.0, max_reviews: int = 20):
        self.delay = delay
        self.max_reviews = max_reviews
        self.session = self._make_session()

    def _make_session(self):
        import requests
        session = requests.Session()
        session.headers.update({
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/120.0.0.0 Safari/537.36'
            ),
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        })
        return session

    def _get(self, url: str, **kwargs) -> Optional[object]:
        """GET with error handling and rate limiting."""
        try:
            time.sleep(self.delay)
            resp = self.session.get(url, timeout=15, **kwargs)
            resp.raise_for_status()
            return resp
        except Exception as e:
            logger.warning(f"[{self.site_name}] GET {url} failed: {e}")
            return None

    @abstractmethod
    def scrape_reviews(self, subject_name: str, breed_type: str = '') -> list[dict]:
        """
        Scrape reviews for a given subject.

        Returns list of dicts with keys:
          - title: str
          - body: str
          - rating: int (1-5)
          - author_name: str
          - original_url: str
          - source_site: str
          - original_date: datetime | None
        """
        pass
