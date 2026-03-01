"""Retry downloading images for breeds that still have no image_path."""
from __future__ import annotations
import os
import re
import time
import logging
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

SESSION = requests.Session()
SESSION.headers.update({'User-Agent': 'BreedImageFetcher/1.0 (petreviews; educational)'})

WIKI_TITLES = {
    'Australian Shepherd': 'Australian Shepherd',
    'Boxer': 'Boxer dog',
    'Doberman Pinscher': 'Dobermann',
    'Bernese Mountain Dog': 'Bernese Mountain Dog',
    'Munchkin': 'Munchkin cat',
    'Cornish Rex': 'Cornish Rex',
    'Somali': 'Somali cat',
    'Egyptian Mau': 'Egyptian Mau',
    'Selkirk Rex': 'Selkirk Rex',
    'Savannah': 'Savannah cat',
    'Chihuahua': 'Chihuahua dog',
}

# Fallback direct URLs for breeds that don't surface via API
DIRECT_URLS = {
    'Boxer': 'https://upload.wikimedia.org/wikipedia/commons/b/b0/BringeBoxer.jpg',
    'Chihuahua': 'https://upload.wikimedia.org/wikipedia/commons/4/4c/Chihuahua1_bvdb.jpg',
}


def get_wiki_image_url(title: str) -> str | None:
    for size in [400, 300, 200]:
        params = {
            'action': 'query',
            'titles': title,
            'prop': 'pageimages',
            'pithumbsize': size,
            'format': 'json',
        }
        try:
            resp = SESSION.get('https://en.wikipedia.org/w/api.php', params=params, timeout=15)
            data = resp.json()
            pages = data.get('query', {}).get('pages', {})
            for page in pages.values():
                thumb = page.get('thumbnail', {})
                src = thumb.get('source')
                if src:
                    return src
        except Exception as e:
            logger.warning(f"Wiki API error for '{title}': {e}")
        time.sleep(1)
    return None


def download_image(url: str, dest_path: str) -> bool:
    for attempt in range(3):
        try:
            resp = SESSION.get(url, timeout=25)
            if resp.status_code == 429:
                wait = 5 * (attempt + 1)
                logger.info(f"  Rate limited, waiting {wait}s…")
                time.sleep(wait)
                continue
            if resp.status_code != 200:
                logger.warning(f"HTTP {resp.status_code} for {url}")
                return False
            content = resp.content
            if len(content) < 5000:
                logger.warning(f"Image too small ({len(content)} bytes)")
                return False
            with open(dest_path, 'wb') as f:
                f.write(content)
            return True
        except Exception as e:
            logger.warning(f"Download error: {e}")
    return False


def main():
    from app import create_app, db
    from app.models import Subject

    app = create_app('development')
    upload_dir = os.path.join('static', 'images', 'uploads', 'subjects')
    os.makedirs(upload_dir, exist_ok=True)

    with app.app_context():
        subjects = Subject.query.filter_by(image_path=None).all()
        logger.info(f"Found {len(subjects)} subjects without images")

        for subj in subjects:
            logger.info(f"Processing {subj.name}…")

            img_url = DIRECT_URLS.get(subj.name)
            if not img_url:
                wiki_title = WIKI_TITLES.get(subj.name, subj.name)
                img_url = get_wiki_image_url(wiki_title)

            if not img_url:
                logger.warning(f"  No image URL found for '{subj.name}'")
                continue

            logger.info(f"  URL: {img_url}")

            ext = img_url.split('.')[-1].split('?')[0].lower()
            if ext not in ('jpg', 'jpeg', 'png', 'webp', 'gif'):
                ext = 'jpg'
            if ext == 'jpeg':
                ext = 'jpg'

            filename = f"{subj.slug}.{ext}"
            dest = os.path.join(upload_dir, filename)

            if download_image(img_url, dest):
                rel_path = f"images/uploads/subjects/{filename}"
                subj.image_path = rel_path
                db.session.commit()
                logger.info(f"  Saved: {rel_path}")
            else:
                logger.warning(f"  Failed to download for '{subj.name}'")

            time.sleep(3)

        logger.info("Done.")


if __name__ == '__main__':
    main()
