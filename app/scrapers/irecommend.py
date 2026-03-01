from __future__ import annotations

import logging
import os
import re
import uuid
from datetime import datetime

from bs4 import BeautifulSoup

from .base import BaseScraper
from .ru_names import to_irecommend_slug

logger = logging.getLogger(__name__)


def _parse_date(text: str) -> datetime | None:
    if not text:
        return None
    text = text.strip()
    m = re.match(r'(\d{2})\.(\d{2})\.(\d{4})', text)
    if m:
        try:
            return datetime(int(m.group(3)), int(m.group(2)), int(m.group(1)))
        except ValueError:
            pass
    return None


class IRecommendScraper(BaseScraper):
    site_name = 'irecommend'
    base_url = 'https://irecommend.ru'

    def scrape_reviews(self, subject_name: str, breed_type: str = '') -> list[dict]:
        slug = to_irecommend_slug(subject_name)
        if not slug:
            logger.info(f"[irecommend] no slug for '{subject_name}', skipping")
            return []

        breed_url = f'{self.base_url}/content/{slug}'
        logger.info(f"[irecommend] breed page: {breed_url}")

        reviews = []
        page = 0

        while len(reviews) < self.max_reviews:
            url = breed_url if page == 0 else f'{breed_url}?page={page}'
            resp = self._get(url)
            if resp is None:
                break

            soup = BeautifulSoup(resp.text, 'lxml')
            items = soup.select('div.smTeaser, div.teaser-item, article.node-review')
            if not items:
                logger.debug(f"[irecommend] no items on page {page} for '{subject_name}'")
                break

            for item in items:
                review = self._parse_item(item)
                if review:
                    reviews.append(review)
                if len(reviews) >= self.max_reviews:
                    break

            next_btn = soup.select_one('li.pager-next a, a.pager-next, a[rel="next"]')
            if not next_btn:
                break
            page += 1

        logger.info(f"[irecommend] found {len(reviews)} reviews for '{subject_name}'")
        return reviews

    def _parse_item(self, item) -> dict | None:
        try:
            link_el = item.select_one('a.reviewTextSnippet, a[href*="/content/"]')
            if not link_el:
                return None
            href = link_el.get('href', '')
            url = href if href.startswith('http') else self.base_url + href

            title_el = item.select_one('div.reviewTitle, h2, h3')
            title = title_el.get_text(strip=True) if title_el else link_el.get_text(strip=True)
            title = re.sub(r'\s+', ' ', title).strip()

            body_el = item.select_one('span.reviewTeaserText, a.reviewTextSnippet')
            body_snippet = body_el.get_text(strip=True) if body_el else ''

            author = 'Anonymous'
            original_date = None
            header_text = item.get_text(separator=' ', strip=True)
            date_m = re.search(r'(\d{2}\.\d{2}\.\d{4})', header_text)
            if date_m:
                original_date = _parse_date(date_m.group(1))
            author_el = item.select_one('a[href*="/user/"], .username, .author-name')
            if author_el:
                author = author_el.get_text(strip=True)
            elif date_m:
                before_date = header_text[:date_m.start()].strip()
                if before_date:
                    author = before_date.split()[-1] if before_date.split() else 'Anonymous'

            rating = 3
            rating_m = re.search(r'\b([1-5])\b(?=\s*/\s*5)', header_text)
            if rating_m:
                rating = int(rating_m.group(1))
            else:
                filled = item.select('.star-on, .fivestar-widget-static-vote .on, span.on')
                if filled:
                    rating = max(1, min(5, len(filled)))

            # Extract thumbnail image URL from the review card
            image_url = self._extract_card_image(item)

            # Fetch full review page for body + full-size image
            if not body_snippet or len(body_snippet) < 50 or not image_url:
                full = self._fetch_full_review(url)
                if full:
                    title = full.get('title') or title
                    body_snippet = full.get('body') or body_snippet
                    if not image_url:
                        image_url = full.get('image_url')

            if not body_snippet or not title:
                return None

            return {
                'title': title,
                'body': body_snippet,
                'rating': rating,
                'author_name': author,
                'original_url': url,
                'source_site': self.site_name,
                'original_date': original_date,
                'image_url': image_url,
            }
        except Exception as e:
            logger.debug(f"[irecommend] parse error: {e}")
            return None

    def _extract_card_image(self, item) -> str | None:
        """Extract the first thumbnail image URL from a review card."""
        for container in item.select('div.review-previews-imgs, div.reviewImages, div.reviewPhoto'):
            for img in container.find_all('img'):
                src = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
                if src and self._is_review_image(src):
                    return self._abs_url(src)
        return None

    def _fetch_full_review(self, url: str) -> dict | None:
        resp = self._get(url)
        if not resp:
            return None
        soup = BeautifulSoup(resp.text, 'lxml')

        title_el = soup.select_one('h1.page-header, h1.title, h1')
        title = title_el.get_text(strip=True) if title_el else ''
        title = re.sub(r'\s*—\s*отзыв\s*$', '', title).strip()

        body_el = soup.select_one(
            '.views-field-teaser.reviewText, .field-name-body, div.description, article .field-items'
        )
        body = body_el.get_text(separator='\n', strip=True) if body_el else ''

        # Extract first image from the review body
        image_url = None
        search_scope = body_el or soup
        for img in search_scope.find_all('img'):
            src = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
            if src and self._is_review_image(src):
                image_url = self._abs_url(src)
                break

        return {'title': title, 'body': body, 'image_url': image_url} if (body or image_url) else None

    def _is_review_image(self, src: str) -> bool:
        """Return True if URL looks like a user-uploaded review image."""
        skip = ('logo', 'icon', 'avatar', 'star', 'favicon', 'sprite', 'banner', 'themes/')
        return not any(s in src.lower() for s in skip)

    def _abs_url(self, src: str) -> str:
        if src.startswith('//'):
            return 'https:' + src
        if src.startswith('/'):
            return self.base_url + src
        return src

    def download_image(self, image_url: str, upload_dir: str) -> str | None:
        """Download an image to upload_dir, return relative static path."""
        try:
            resp = self.session.get(image_url, timeout=15)
            if resp.status_code != 200 or len(resp.content) < 5000:
                return None
            ct = resp.headers.get('content-type', '')
            if 'jpeg' in ct or 'jpg' in ct:
                ext = 'jpg'
            elif 'png' in ct:
                ext = 'png'
            elif 'webp' in ct:
                ext = 'webp'
            else:
                ext = 'jpg'
            filename = f"{uuid.uuid4().hex}.{ext}"
            os.makedirs(upload_dir, exist_ok=True)
            with open(os.path.join(upload_dir, filename), 'wb') as f:
                f.write(resp.content)
            return f"images/uploads/reviews/{filename}"
        except Exception as e:
            logger.debug(f"[irecommend] image download failed {image_url}: {e}")
            return None
