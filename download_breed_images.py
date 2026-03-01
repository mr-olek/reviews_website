"""
Download breed images from Wikipedia for subjects that have no image_path.
Uses the Wikipedia API to find the main article image.
"""
from __future__ import annotations
import os
import time
import uuid
import logging
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

SESSION = requests.Session()
SESSION.headers.update({'User-Agent': 'BreedImageFetcher/1.0 (petreviews; educational)'})

# Wikipedia article titles per breed (some need explicit names to get the right article)
WIKI_TITLES = {
    # Batch 1 dogs
    'Siberian Husky': 'Siberian Husky',
    'Border Collie': 'Border Collie',
    'Australian Shepherd': 'Australian Shepherd',
    'Boxer': 'Boxer (dog)',
    'Yorkshire Terrier': 'Yorkshire Terrier',
    'Shih Tzu': 'Shih Tzu',
    'Doberman Pinscher': 'Dobermann',
    'Chihuahua': 'Chihuahua (dog)',
    'Cavalier King Charles Spaniel': 'Cavalier King Charles Spaniel',
    'Bernese Mountain Dog': 'Bernese Mountain Dog',
    # Batch 1 cats
    'Munchkin': 'Munchkin cat',
    'Siberian': 'Siberian cat',
    'Turkish Van': 'Turkish Van',
    'Cornish Rex': 'Cornish Rex',
    'Balinese': 'Balinese cat',
    'Somali': 'Somali cat',
    'Egyptian Mau': 'Egyptian Mau',
    'Manx': 'Manx cat',
    'Selkirk Rex': 'Selkirk Rex',
    'Savannah': 'Savannah cat',
    # Batch 2 dogs
    'Akita': 'Akita (dog)',
    'Alaskan Malamute': 'Alaskan Malamute',
    'Basset Hound': 'Basset Hound',
    'Belgian Malinois': 'Belgian Malinois',
    'Bichon Frise': 'Bichon Frise',
    'Bloodhound': 'Bloodhound',
    'Boston Terrier': 'Boston Terrier',
    'Bull Terrier': 'Bull Terrier',
    'Cane Corso': 'Cane Corso',
    'Cocker Spaniel': 'American Cocker Spaniel',
    'Dalmatian': 'Dalmatian (dog)',
    'English Springer Spaniel': 'English Springer Spaniel',
    'Great Dane': 'Great Dane',
    'Great Pyrenees': 'Great Pyrenees',
    'Greyhound': 'Greyhound',
    'Havanese': 'Havanese dog',
    'Irish Setter': 'Irish Setter',
    'Irish Wolfhound': 'Irish Wolfhound',
    'Jack Russell Terrier': 'Jack Russell Terrier',
    'Maltese': 'Maltese dog',
    'Mastiff': 'Mastiff',
    'Miniature Schnauzer': 'Miniature Schnauzer',
    'Newfoundland': 'Newfoundland dog',
    'Old English Sheepdog': 'Old English Sheepdog',
    'Papillon': 'Papillon (dog)',
    'Pembroke Welsh Corgi': 'Pembroke Welsh Corgi',
    'Pomeranian': 'Pomeranian (dog)',
    'Portuguese Water Dog': 'Portuguese Water Dog',
    'Rhodesian Ridgeback': 'Rhodesian Ridgeback',
    'Saint Bernard': 'Saint Bernard (dog)',
    'Samoyed': 'Samoyed (dog)',
    'Scottish Terrier': 'Scottish Terrier',
    'Shetland Sheepdog': 'Shetland Sheepdog',
    'Shiba Inu': 'Shiba Inu',
    'Soft Coated Wheaten Terrier': 'Soft-coated Wheaten Terrier',
    'Staffordshire Bull Terrier': 'Staffordshire Bull Terrier',
    'Vizsla': 'Vizsla',
    'Weimaraner': 'Weimaraner',
    'West Highland White Terrier': 'West Highland White Terrier',
    'Whippet': 'Whippet',
    # Batch 2 cats
    'American Bobtail': 'American Bobtail',
    'American Curl': 'American Curl',
    'Bombay': 'Bombay cat',
    'British Longhair': 'British Longhair',
    'Burmilla': 'Burmilla',
    'Chausie': 'Chausie',
    'Colorpoint Shorthair': 'Colorpoint Shorthair',
    'Cymric': 'Cymric (cat)',
    'European Shorthair': 'European Shorthair',
    'Havana Brown': 'Havana Brown',
    'Japanese Bobtail': 'Japanese Bobtail',
    'Khao Manee': 'Khao Manee',
    'Korat': 'Korat',
    'LaPerm': 'LaPerm',
    'Lykoi': 'Lykoi',
    'Nebelung': 'Nebelung',
    'Ocicat': 'Ocicat',
    'Oriental Shorthair': 'Oriental Shorthair',
    'Peterbald': 'Peterbald',
    'Pixiebob': 'Pixiebob',
    'Ragamuffin': 'Ragamuffin cat',
    'Scottish Straight': 'Scottish Fold',
    'Serengeti': 'Serengeti cat',
    'Singapura': 'Singapura (cat)',
    'Snowshoe': 'Snowshoe cat',
    'Sokoke': 'Sokoke',
    'Toyger': 'Toyger',
    'Tiffanie': 'Asian Semi-longhair',
    'Ukrainian Levkoy': 'Ukrainian Levkoy',
    'York Chocolate': 'York Chocolate',
}


def get_wiki_image_url(title: str) -> str | None:
    """Return the URL of the main image for a Wikipedia article."""
    params = {
        'action': 'query',
        'titles': title,
        'prop': 'pageimages',
        'pithumbsize': 800,
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
                # Get higher resolution version
                src = src.replace('/220px-', '/800px-').replace('/200px-', '/800px-')
                # Replace any NNNpx- pattern with 800px-
                import re
                src = re.sub(r'/\d+px-', '/800px-', src)
                return src
    except Exception as e:
        logger.warning(f"Wiki API error for '{title}': {e}")
    return None


def download_image(url: str, dest_path: str) -> bool:
    """Download image to dest_path. Returns True on success."""
    try:
        resp = SESSION.get(url, timeout=20)
        if resp.status_code != 200:
            logger.warning(f"HTTP {resp.status_code} for {url}")
            return False
        content = resp.content
        if len(content) < 5000:
            logger.warning(f"Image too small ({len(content)} bytes): {url}")
            return False
        with open(dest_path, 'wb') as f:
            f.write(content)
        return True
    except Exception as e:
        logger.warning(f"Download error {url}: {e}")
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
            wiki_title = WIKI_TITLES.get(subj.name)
            if not wiki_title:
                logger.info(f"No wiki title configured for '{subj.name}', skipping")
                continue

            logger.info(f"Fetching image for {subj.name} ('{wiki_title}')…")
            img_url = get_wiki_image_url(wiki_title)
            if not img_url:
                logger.warning(f"  No image found for '{subj.name}'")
                continue

            logger.info(f"  URL: {img_url}")

            ext = img_url.split('.')[-1].split('?')[0].lower()
            if ext not in ('jpg', 'jpeg', 'png', 'webp'):
                ext = 'jpg'

            filename = f"{subj.slug}.{ext}"
            dest = os.path.join(upload_dir, filename)

            if download_image(img_url, dest):
                rel_path = f"images/uploads/subjects/{filename}"
                subj.image_path = rel_path
                db.session.commit()
                logger.info(f"  Saved: {rel_path}")
            else:
                logger.warning(f"  Failed to download image for '{subj.name}'")

            time.sleep(0.5)

        logger.info("Done.")


if __name__ == '__main__':
    main()
