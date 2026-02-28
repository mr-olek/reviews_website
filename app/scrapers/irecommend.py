from __future__ import annotations

import logging
import re
from datetime import datetime
from urllib.parse import quote

from bs4 import BeautifulSoup

from .base import BaseScraper
from .ru_names import to_russian

logger = logging.getLogger(__name__)

MONTH_MAP = {
    'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4,
    'мая': 5, 'июня': 6, 'июля': 7, 'августа': 8,
    'сентября': 9, 'октября': 10, 'ноября': 11, 'декабря': 12,
}


def _parse_date(text: str) -> datetime | None:
    if not text:
        return None
    text = text.strip()
    m = re.match(r'(\d{1,2})\s+(\w+)\s+(\d{4})', text)
    if m:
        day, month_str, year = m.group(1), m.group(2).lower(), m.group(3)
        month = MONTH_MAP.get(month_str)
        if month:
            try:
                return datetime(int(year), month, int(day))
            except ValueError:
                pass
    return None


class IRecommendScraper(BaseScraper):
    site_name = 'irecommend'
    base_url = 'https://irecommend.ru'

    def scrape_reviews(self, subject_name: str, breed_type: str = '') -> list[dict]:
        ru_name = to_russian(subject_name)
        # irecommend search endpoint
        search_url = f'{self.base_url}/search?q={quote(ru_name)}'
        logger.info(f"[irecommend] searching: '{ru_name}' → {search_url}")

        reviews = []
        page = 0

        while len(reviews) < self.max_reviews:
            url = search_url if page == 0 else f'{search_url}&page={page}'
            resp = self._get(url)
            if resp is None:
                break

            soup = BeautifulSoup(resp.text, 'lxml')
            # irecommend search results
            items = soup.select(
                'div.teaser-product, article.node-review, '
                'div.view-content div.views-row, li.search-result'
            )
            if not items:
                logger.debug(f"[irecommend] no items on page {page}")
                break

            for item in items:
                review = self._parse_item(item)
                if review:
                    reviews.append(review)
                if len(reviews) >= self.max_reviews:
                    break

            next_btn = soup.select_one('li.pager-next a, a[rel="next"]')
            if not next_btn:
                break
            page += 1

        logger.info(f"[irecommend] found {len(reviews)} reviews for '{subject_name}'")
        return reviews

    def _parse_item(self, item) -> dict | None:
        try:
            link_el = item.select_one('a[href*="/content/"], h2 a, h3 a, .views-field-title a')
            if not link_el:
                return None
            href = link_el.get('href', '')
            url = href if href.startswith('http') else self.base_url + href

            title = link_el.get_text(strip=True)

            # Rating
            rating = 0
            rating_el = item.select_one('[class*="rating"], [class*="stars"], .field-name-field-rating')
            if rating_el:
                txt = rating_el.get_text()
                m = re.search(r'(\d)', txt)
                if m:
                    rating = int(m.group(1))
            if not rating:
                filled = item.select('.star-on, .filled, i.active')
                rating = len(filled)
            rating = max(1, min(5, rating)) if rating else 3

            author_el = item.select_one('a[href*="/user/"], .username, .views-field-name a')
            author = author_el.get_text(strip=True) if author_el else 'Anonymous'

            date_el = item.select_one('time, span.date, .views-field-created')
            date_text = (
                date_el.get('datetime') or date_el.get_text(strip=True)
                if date_el else ''
            )
            original_date = _parse_date(date_text)

            body_el = item.select_one(
                'div.description, div.field-name-body, .views-field-body, p.review-body'
            )
            body = body_el.get_text(strip=True) if body_el else ''

            if not body or len(body) < 50:
                full = self._fetch_full_review(url)
                if full:
                    title = full.get('title') or title
                    body = full.get('body') or body

            if not body or not title:
                return None

            return {
                'title': title,
                'body': body,
                'rating': rating,
                'author_name': author,
                'original_url': url,
                'source_site': self.site_name,
                'original_date': original_date,
            }
        except Exception as e:
            logger.debug(f"[irecommend] parse error: {e}")
            return None

    def _fetch_full_review(self, url: str) -> dict | None:
        resp = self._get(url)
        if not resp:
            return None
        soup = BeautifulSoup(resp.text, 'lxml')

        title_el = soup.select_one('h1.page-header, h1.title, h1')
        title = title_el.get_text(strip=True) if title_el else ''

        body_el = soup.select_one(
            'div.field-name-body, div.description, article .field-items'
        )
        body = body_el.get_text(separator='\n', strip=True) if body_el else ''

        return {'title': title, 'body': body} if body else None
