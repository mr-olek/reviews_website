from __future__ import annotations

import logging
import os
import random
import uuid

from bs4 import BeautifulSoup

from .base import BaseScraper

_ADJECTIVES = [
    'Big', 'Tiny', 'Blue', 'Red', 'Happy', 'Grumpy', 'Sneaky', 'Fluffy',
    'Brave', 'Lazy', 'Spicy', 'Chilly', 'Wild', 'Calm', 'Swift', 'Clumsy',
    'Bouncy', 'Fuzzy', 'Mighty', 'Sleepy', 'Dizzy', 'Funky', 'Shiny', 'Dusty',
]
_ANIMALS = [
    'Baboon', 'Penguin', 'Panda', 'Narwhal', 'Capybara', 'Quokka', 'Axolotl',
    'Platypus', 'Wombat', 'Toucan', 'Lemur', 'Meerkat', 'Tapir', 'Okapi',
    'Alpaca', 'Manatee', 'Blobfish', 'Gecko', 'Flamingo', 'Armadillo',
]

def _random_username() -> str:
    return f"{random.choice(_ADJECTIVES)}{random.choice(_ANIMALS)}{random.randint(1, 999)}"

logger = logging.getLogger(__name__)

# Russian keywords that must appear in a review for it to be about that breed.
# Checked against the raw (untranslated) Russian body text.
BREED_KEYWORDS: dict[str, list[str]] = {
    'Labrador Retriever':         ['лабрадор'],
    'German Shepherd':            ['овчарк', 'немецк'],
    'Golden Retriever':           ['голден', 'золотист', 'ретривер'],
    'French Bulldog':             ['французск', 'бульдог'],
    'Bulldog':                    ['английск', 'бульдог'],
    'Poodle':                     ['пудел'],
    'Beagle':                     ['бигл'],
    'Rottweiler':                 ['ротвейлер'],
    'German Shorthaired Pointer': ['курцхаар', 'краткошерст', 'дратхаар'],
    'Dachshund':                  ['такс'],
    'Maine Coon':                 ['мейн', 'мэйн'],
    'Persian':                    ['персидск'],
    'Ragdoll':                    ['рэгдол', 'регдол'],
    'Siamese':                    ['сиамск'],
    'British Shorthair':          ['британск'],
    'Abyssinian':                 ['абиссинск'],
    'Scottish Fold':              ['вислоух', 'шотландск'],
    'Sphynx':                     ['сфинкс'],
    'Bengal':                     ['бенгальск'],
    'Russian Blue':               ['русская голуб', 'голубая кошк'],
    'Norwegian Forest Cat':       ['норвежск'],
    'Burmese':                    ['бурманск'],
    'Devon Rex':                  ['девон'],
    'American Shorthair':         ['американск'],
    'Exotic Shorthair':           ['экзотическ'],
    'Birman':                     ['бирманск', 'священная бирм'],
    'Tonkinese':                  ['тонкинск'],
    'Himalayan':                  ['гималайск'],
    'Turkish Angora':             ['турецк', 'ангор'],
    'Chartreux':                  ['шартрез', 'картезианск'],
}


def _is_relevant(text_ru: str, breed_name: str) -> bool:
    """Return True if the Russian text mentions keywords for this breed."""
    keywords = BREED_KEYWORDS.get(breed_name, [])
    if not keywords:
        return True  # unknown breed — allow through
    text_lower = text_ru.lower()
    return any(kw in text_lower for kw in keywords)


# Maps English breed name → (kind, lapkins-slug)
LAPKINS_SLUG: dict[str, tuple[str, str]] = {
    # Dogs
    'Labrador Retriever':          ('dog', 'labrador'),
    'German Shepherd':             ('dog', 'nemetskaya-ovcharka'),
    'Golden Retriever':            ('dog', 'zolotisty-retriver'),
    'French Bulldog':              ('dog', 'frantsuzskiy-buldog'),
    'Bulldog':                     ('dog', 'angliiskiy-buldog'),
    'Poodle':                      ('dog', 'pudel'),
    'Beagle':                      ('dog', 'bigl'),
    'Rottweiler':                  ('dog', 'rotveyler'),
    'German Shorthaired Pointer':  ('dog', 'nemetskiy-kratkhaar'),
    'Dachshund':                   ('dog', 'taksa'),
    # Cats
    'Maine Coon':                  ('cat', 'meyn-kun'),
    'Persian':                     ('cat', 'persidskaya-koshka'),
    'Ragdoll':                     ('cat', 'regdoll'),
    'Siamese':                     ('cat', 'siamskaya-koshka'),
    'British Shorthair':           ('cat', 'britanskaya-korotkosherstnaya'),
    'Abyssinian':                  ('cat', 'abissinskaya-koshka'),
    'Scottish Fold':               ('cat', 'shotlandskaya-visloukhaya-koshka'),
    'Sphynx':                      ('cat', 'sfinks-kanadskiy'),
    'Bengal':                      ('cat', 'bengalskaya-koshka'),
    'Russian Blue':                ('cat', 'russkaya-golubaya'),
    'Norwegian Forest Cat':        ('cat', 'norvezhskaya-lesnaya-koshka'),
    'Burmese':                     ('cat', 'burmanskaya-koshka'),
    'Devon Rex':                   ('cat', 'devon-reks'),
    'American Shorthair':          ('cat', 'amerikanskaya-korotkosherstnaya'),
    'Exotic Shorthair':            ('cat', 'ekzoticheskaya-korotkosherstnaya'),
    'Birman':                      ('cat', 'svyashchennaya-birma'),
    'Tonkinese':                   ('cat', 'tonkinskaya-koshka'),
    'Himalayan':                   ('cat', 'gimalaiskaya-koshka'),
    'Turkish Angora':              ('cat', 'turetskaya-angora'),
    'Chartreux':                   ('cat', 'kartezianskaya-koshka'),
}


class LapkinsScraper(BaseScraper):
    site_name = 'lapkins'
    base_url = 'https://lapkins.ru'

    def scrape_reviews(self, subject_name: str, breed_type: str = '') -> list[dict]:
        entry = LAPKINS_SLUG.get(subject_name)
        if not entry:
            logger.info(f"[lapkins] no slug for '{subject_name}', skipping")
            return []

        kind, slug = entry
        listing_url = f'{self.base_url}/{kind}/{slug}/otzivi/'
        logger.info(f"[lapkins] listing: {listing_url}")

        resp = self._get(listing_url)
        if resp is None:
            return []

        soup = BeautifulSoup(resp.text, 'lxml')
        cards = soup.select('div.forum-prew')
        if not cards:
            logger.debug(f"[lapkins] no review cards for '{subject_name}'")
            return []

        reviews = []
        for card in cards:
            if len(reviews) >= self.max_reviews:
                break
            review = self._parse_card(card, kind, slug, subject_name)
            if review:
                reviews.append(review)

        logger.info(f"[lapkins] found {len(reviews)} reviews for '{subject_name}'")
        return reviews

    @staticmethod
    def _review_id(href: str) -> str | None:
        """Extract numeric ID from a lapkins review slug like /dog/labrador/otzivi/grifon-29624/"""
        import re
        m = re.search(r'-(\d+)/?$', href)
        return m.group(1) if m else None

    def _parse_card(self, card, kind: str, breed_slug: str, subject_name: str = '') -> dict | None:
        try:
            link_el = card.select_one('a.fh')
            if not link_el:
                return None
            href = link_el.get('href', '')

            # Filter out reviews that don't belong to this breed page.
            # On lapkins, ALL hrefs on a breed page share the same /<kind>/<slug>/ prefix,
            # so we cannot distinguish by URL prefix. Instead, we use the numeric review ID
            # as a normalized dedup key and rely on the DB unique constraint to discard
            # cross-breed duplicates when they are encountered later.
            review_id = self._review_id(href)
            if not review_id:
                return None

            # Normalized canonical URL — breed-independent, used for DB dedup
            canonical_url = f'{self.base_url}/review/{review_id}'
            # Full URL for fetching the review page (uses the current breed context)
            full_url = self.base_url + href if href.startswith('/') else href

            title = link_el.get_text(strip=True)
            if not title:
                return None

            author = _random_username()

            # Rating: count filled stars
            filled = card.select('div.otz-reit i.r-yes')
            rating = max(1, min(5, len(filled))) if filled else 3

            # Always fetch the full review page for clean body text and full-size image
            snippet_ru = ''
            image_url = None
            full = self._fetch_full_review(full_url)
            if full:
                title = full.get('title') or title
                snippet_ru = full.get('body') or ''
                image_url = full.get('image_url')

            # Fall back to listing snippet if full page had no body
            if not snippet_ru:
                body_el = card.select_one('div.forum-text')
                snippet_ru = body_el.get_text(strip=True) if body_el else ''

            if not snippet_ru:
                return None

            # Discard reviews that don't mention this breed (lapkins mixes all breeds)
            check_text = (title + ' ' + snippet_ru).lower()
            if subject_name and not _is_relevant(check_text, subject_name):
                logger.debug(f"[lapkins] skipping off-topic review '{title[:40]}' for '{subject_name}'")
                return None

            snippet = snippet_ru

            return {
                'title': title,
                'body': snippet,
                'rating': rating,
                'author_name': author,
                'original_url': canonical_url,
                'source_site': self.site_name,
                'original_date': None,  # dates are relative ("Месяц назад")
                'image_url': image_url,
            }
        except Exception as e:
            logger.debug(f"[lapkins] parse error: {e}")
            return None

    def _fetch_full_review(self, url: str) -> dict | None:
        resp = self._get(url)
        if not resp:
            return None
        soup = BeautifulSoup(resp.text, 'lxml')

        title_el = soup.select_one('h1')
        title = title_el.get_text(strip=True) if title_el else ''

        # Body is in div.pet-inside, after the "Отзыв" label
        body = ''
        pet_inside = soup.select_one('div.pet-inside')
        if pet_inside:
            text = pet_inside.get_text(separator='\n', strip=True)
            idx = text.find('Отзыв')
            if idx >= 0:
                body = text[idx + 5:].strip()
            else:
                body = text.strip()

        # Full-size image: prefer /upload/main/ originals, accept large resize_cache
        image_url = None
        if pet_inside:
            candidates = []
            for img in pet_inside.find_all('img'):
                src = img.get('src') or img.get('data-src', '')
                if not src or 'iblock' in src:
                    continue
                if '/upload/main/' in src:
                    image_url = self._abs_url(src)
                    break
                if '/upload/' in src and ('1024' in src or '800' in src or 'resize_cache' not in src):
                    candidates.append(src)
            if not image_url and candidates:
                image_url = self._abs_url(candidates[0])

        return {'title': title, 'body': body, 'image_url': image_url} if (body or image_url) else None

    def _abs_url(self, src: str) -> str:
        if src.startswith('//'):
            return 'https:' + src
        if src.startswith('/'):
            return self.base_url + src
        return src

    def download_image(self, image_url: str, upload_dir: str) -> str | None:
        try:
            resp = self.session.get(image_url, timeout=15)
            if resp.status_code != 200 or len(resp.content) < 5000:
                return None
            ct = resp.headers.get('content-type', '')
            if 'png' in ct:
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
            logger.debug(f"[lapkins] image download failed {image_url}: {e}")
            return None
