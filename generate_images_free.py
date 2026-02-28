"""
Fetch real breed photos from TheDogAPI and TheCatAPI — completely free, no key needed.

Usage:
  python3 generate_images_free.py           # all subjects
  python3 generate_images_free.py --id 1    # specific subject id
"""
from __future__ import annotations

import argparse
import logging
import os
import time

import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

CAT_API = 'https://api.thecatapi.com/v1'

# Wikipedia page titles for each breed (for the Wikipedia image API)
WIKI_TITLES = {
    'Labrador Retriever': 'Labrador_Retriever',
    'German Shepherd': 'German_Shepherd',
    'Golden Retriever': 'Golden_Retriever',
    'French Bulldog': 'French_Bulldog',
    'Bulldog': 'Bulldog',
    'Poodle': 'Poodle',
    'Beagle': 'Beagle',
    'Rottweiler': 'Rottweiler',
    'German Shorthaired Pointer': 'German_Shorthaired_Pointer',
    'Dachshund': 'Dachshund',
    'British Shorthair': 'British_Shorthair',
}

WIKI_HEADERS = {
    'User-Agent': 'PetReviewsBot/1.0 (educational project; contact@example.com)',
    'Accept': 'application/json',
}

CAT_HEADERS = {'x-api-key': ''}


def fetch_wikipedia_image(breed_name: str) -> str | None:
    """Fetch the main image for a breed from Wikipedia's REST API."""
    title = WIKI_TITLES.get(breed_name, breed_name.replace(' ', '_'))
    url = f'https://en.wikipedia.org/api/rest_v1/page/summary/{title}'
    try:
        r = requests.get(url, headers=WIKI_HEADERS, timeout=15)
        r.raise_for_status()
        data = r.json()
        # Prefer originalimage, fall back to thumbnail
        img = data.get('originalimage') or data.get('thumbnail')
        return img['source'] if img else None
    except Exception as e:
        logger.debug(f"Wikipedia API error for {breed_name}: {e}")
        return None


def fetch_catapi_image(breed_name: str) -> str | None:
    """Fetch breed image from TheCatAPI (free, no key required)."""
    try:
        r = requests.get(
            f'{CAT_API}/breeds/search',
            params={'q': breed_name},
            headers=CAT_HEADERS,
            timeout=10,
        )
        r.raise_for_status()
        breeds = r.json()
        if not breeds:
            return None
        ref_img = breeds[0].get('reference_image_id')
        if ref_img:
            img_r = requests.get(f'{CAT_API}/images/{ref_img}', headers=CAT_HEADERS, timeout=10)
            if img_r.status_code == 200:
                return img_r.json().get('url')
        breed_id = breeds[0].get('id')
        img_r = requests.get(
            f'{CAT_API}/images/search',
            params={'breed_ids': breed_id, 'limit': 1},
            headers=CAT_HEADERS,
            timeout=10,
        )
        results = img_r.json()
        return results[0].get('url') if results else None
    except Exception as e:
        logger.debug(f"CatAPI error for {breed_name}: {e}")
        return None


def fetch_breed_image_url(breed_name: str, animal_type: str) -> str | None:
    if animal_type == 'Cats':
        url = fetch_catapi_image(breed_name)
        if url:
            return url
    # Wikipedia works for both dogs and cats as fallback
    return fetch_wikipedia_image(breed_name)


BROWSER_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://en.wikipedia.org/',
}


def download_image(url: str, filepath: str) -> bool:
    try:
        r = requests.get(url, timeout=60, stream=True, headers=BROWSER_HEADERS)
        r.raise_for_status()
        with open(filepath, 'wb') as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
        return os.path.getsize(filepath) > 5000
    except Exception as e:
        logger.debug(f"Download failed: {e}")
        return False


def generate_image(subject_name: str, subject_slug: str, animal_type: str, images_dir: str) -> str | None:
    os.makedirs(images_dir, exist_ok=True)

    # Try jpg then png extension
    for ext in ('jpg', 'png', 'jpeg'):
        filepath = os.path.join(images_dir, f"{subject_slug}.{ext}")
        if os.path.exists(filepath) and os.path.getsize(filepath) > 5000:
            logger.info(f"  skip {subject_name} (exists)")
            return f"images/generated/{subject_slug}.{ext}"

    logger.info(f"  fetching: {subject_name}…")

    image_url = fetch_breed_image_url(subject_name, animal_type)
    if not image_url:
        logger.warning(f"  no image found for {subject_name}")
        return None

    # Determine extension from URL
    ext = 'jpg'
    if '.png' in image_url:
        ext = 'png'
    elif '.jpeg' in image_url:
        ext = 'jpeg'

    filepath = os.path.join(images_dir, f"{subject_slug}.{ext}")
    if download_image(image_url, filepath):
        size = os.path.getsize(filepath)
        logger.info(f"  ✓ {subject_name} ({size // 1024}KB) ← {image_url[:60]}…")
        return f"images/generated/{subject_slug}.{ext}"
    else:
        logger.warning(f"  ✗ download failed for {subject_name}")
        return None


def run(subject_id: int | None = None):
    from app import create_app, db
    from app.models import Subject

    app = create_app('development')
    images_dir = app.config['IMAGES_DIR']

    with app.app_context():
        if subject_id:
            subjects = [Subject.query.get(subject_id)]
        else:
            subjects = Subject.query.order_by(Subject.id).all()

        logger.info(f"Fetching breed images for {len(subjects)} subjects (TheDogAPI / TheCatAPI)…")

        for subj in subjects:
            animal_type = subj.subcategory.name if subj.subcategory else 'Dogs'
            path = generate_image(subj.name, subj.slug, animal_type, images_dir)
            if path:
                subj.image_path = path
                db.session.commit()
            time.sleep(1)

        logger.info("Done.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', type=int, help='Subject ID (default: all)')
    args = parser.parse_args()
    run(args.id)
