#!/usr/bin/env python3
"""Fix car brand images (were logos) and fill in missing model images.
Usage: python3 fix_car_images.py
"""
import os, sys, time, requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

# Brand images: use a specific car model article to get an actual car photo
BRAND_IMAGE_FIXES = {
    'toyota':        'Toyota Camry',
    'ford':          'Ford Mustang',
    'bmw':           'BMW 3 Series',
    'honda':         'Honda Civic',
    'chevrolet':     'Chevrolet Corvette',
    'mercedes-benz': 'Mercedes-Benz S-Class',
    'audi':          'Audi Q5',
    'volkswagen':    'Volkswagen Golf',
    'hyundai':       'Hyundai Tucson',
    'kia':           'Kia Telluride',
    'nissan':        'Nissan GT-R',
    'subaru':        'Subaru WRX',
    'mazda':         'Mazda MX-5',
    'jeep':          'Jeep Wrangler',
    'tesla':         'Tesla Model S',
    'porsche':       'Porsche 911',
    'dodge':         'Dodge Challenger',
    'ram':           'Ram 1500',
    'gmc':           'GMC Sierra',
    'lexus':         'Lexus IS',
    'volvo':         'Volvo XC60',
    'land-rover':    'Range Rover',
    'genesis':       'Genesis GV80',
    'mini':          'Mini Cooper',
    'cadillac':      'Cadillac Escalade',
}

# Model images that were missing or wrong — (slug, wiki_title)
MODEL_IMAGE_FIXES = [
    ('f-150',       'Ford F-150'),
    ('bronco',      'Ford Bronco'),
    ('brz',         'Subaru BRZ'),
    ('gladiator',   'Jeep Gladiator'),
    ('ram-1500',    'Ram 1500'),
    ('ram-2500',    'Ram 2500'),
    ('ram-trx',     'Ram 1500 TRX'),
    ('sierra-1500', 'GMC Sierra'),
    ('yukon',       'GMC Yukon'),
    ('canyon',      'GMC Canyon'),
    ('clubman',     'Mini Clubman'),
]


def get_wiki_image(title, width=600):
    try:
        r = requests.get('https://en.wikipedia.org/w/api.php', params={
            'action': 'query', 'titles': title, 'prop': 'pageimages',
            'pithumbsize': width, 'format': 'json',
        }, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        pages = r.json()['query']['pages']
        page = next(iter(pages.values()))
        return page.get('thumbnail', {}).get('source')
    except Exception:
        return None


def download(url, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    for attempt in range(3):
        try:
            r = requests.get(url, timeout=20, headers={'User-Agent': 'Mozilla/5.0'})
            if r.status_code == 200:
                with open(dest, 'wb') as f:
                    f.write(r.content)
                return True
            elif r.status_code == 429:
                print('    rate limited, sleeping 15s...')
                time.sleep(15)
        except Exception as e:
            print(f'    error: {e}')
            time.sleep(2)
    return False


def fix_brand(slug, wiki_title):
    dest = os.path.join(STATIC_DIR, 'images', 'uploads', 'subcategories', f'cars-{slug}.jpg')
    # Always re-download brand images (they were logos)
    url = get_wiki_image(wiki_title)
    if url:
        if download(url, dest):
            print(f'  ✓ brand {slug} → {wiki_title}')
            return True
    print(f'  ✗ brand {slug} — no image from "{wiki_title}"')
    return False


def fix_model(slug, wiki_title):
    dest = os.path.join(STATIC_DIR, 'images', 'uploads', 'subjects', f'cars-{slug}.jpg')
    if os.path.exists(dest):
        # Re-download to ensure it's not a logo/wrong image
        os.remove(dest)
    url = get_wiki_image(wiki_title)
    if url:
        if download(url, dest):
            print(f'  ✓ model {slug} → {wiki_title}')
            return True
    print(f'  ✗ model {slug} — no image from "{wiki_title}"')
    return False


if __name__ == '__main__':
    print('Fixing brand images...')
    for slug, wiki in BRAND_IMAGE_FIXES.items():
        fix_brand(slug, wiki)
        time.sleep(0.4)

    print('\nFixing model images...')
    for slug, wiki in MODEL_IMAGE_FIXES:
        fix_model(slug, wiki)
        time.sleep(0.4)

    print('\nDone.')
