#!/usr/bin/env python3
"""Downloads year-specific images for every car model+year subject.
Searches Wikimedia Commons for "{year} {brand} {model}", falls back to
the existing shared model image if nothing found.

Usage: python3 fix_car_year_images.py
"""
import os, sys, time, requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Category, SubCategory, Subject

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
SESSION = requests.Session()
SESSION.headers['User-Agent'] = 'Mozilla/5.0 (compatible; VerdictlyBot/1.0)'


def commons_search_image(query, width=500):
    """Search Commons for query, return thumbnail URL of best result."""
    try:
        r = SESSION.get('https://commons.wikimedia.org/w/api.php', params={
            'action': 'query', 'list': 'search',
            'srsearch': f'filetype:bitmap {query}',
            'srnamespace': 6, 'srlimit': 5, 'format': 'json',
        }, timeout=15)
        results = r.json().get('query', {}).get('search', [])
        for result in results:
            file_title = result['title']
            r2 = SESSION.get('https://commons.wikimedia.org/w/api.php', params={
                'action': 'query', 'titles': file_title,
                'prop': 'imageinfo', 'iiprop': 'url',
                'iiurlwidth': width, 'format': 'json',
            }, timeout=10)
            pages = r2.json()['query']['pages']
            page = next(iter(pages.values()))
            iis = page.get('imageinfo', [])
            if iis:
                url = iis[0].get('thumburl')
                if url:
                    return url
    except Exception as e:
        print(f'    commons error: {e}')
    return None


def wiki_image(title, width=500):
    """Wikipedia pageimages API — fast single-article lookup."""
    try:
        r = SESSION.get('https://en.wikipedia.org/w/api.php', params={
            'action': 'query', 'titles': title, 'prop': 'pageimages',
            'pithumbsize': width, 'format': 'json',
        }, timeout=10)
        pages = r.json()['query']['pages']
        page = next(iter(pages.values()))
        return page.get('thumbnail', {}).get('source')
    except Exception:
        return None


def download(url, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    for attempt in range(3):
        try:
            r = SESSION.get(url, timeout=20)
            if r.status_code == 200:
                with open(dest, 'wb') as f:
                    f.write(r.content)
                return True
            elif r.status_code == 429:
                print('    rate limited, sleeping 20s...')
                time.sleep(20)
        except Exception as e:
            print(f'    download error: {e}')
            time.sleep(3)
    return False


# For some models, Wikipedia has generation-specific articles keyed by year range.
# Map (brand_slug, model_slug, year) → wikipedia title for precision.
GENERATION_WIKI = {
    # Toyota
    ('toyota', 'camry', range(2021, 2025)): 'Toyota Camry (XV70)',
    ('toyota', 'camry', range(2025, 2026)): 'Toyota Camry (XV80)',
    ('toyota', 'corolla', range(2021, 2026)): 'Toyota Corolla (E210)',
    ('toyota', 'rav4', range(2021, 2026)):   'Toyota RAV4 (XA50)',
    ('toyota', 'highlander', range(2021, 2026)): 'Toyota Highlander (XU70)',
    ('toyota', 'tacoma', range(2021, 2025)): 'Toyota Tacoma (N300)',
    ('toyota', 'tacoma', range(2025, 2026)): 'Toyota Tacoma (N400)',
    ('toyota', 'prius', range(2021, 2023)):  'Toyota Prius (XW50)',
    ('toyota', 'prius', range(2023, 2026)):  'Toyota Prius (XW60)',
    # Ford
    ('ford', 'f-150', range(2021, 2026)):    'Ford F-150 (fourteenth generation)',
    ('ford', 'mustang', range(2021, 2024)):  'Ford Mustang (sixth generation)',
    ('ford', 'mustang', range(2024, 2026)):  'Ford Mustang (seventh generation)',
    ('ford', 'bronco', range(2021, 2026)):   'Ford Bronco (sixth generation)',
    ('ford', 'explorer', range(2021, 2026)): 'Ford Explorer (sixth generation)',
    # BMW
    ('bmw', '3-series', range(2021, 2026)):  'BMW 3 Series (G20)',
    ('bmw', '5-series', range(2021, 2025)):  'BMW 5 Series (G30)',
    ('bmw', '5-series', range(2025, 2026)):  'BMW 5 Series (G60)',
    ('bmw', 'x3', range(2021, 2025)):        'BMW X3 (G01)',
    ('bmw', 'x5', range(2021, 2026)):        'BMW X5 (G05)',
    ('bmw', 'm3', range(2021, 2026)):        'BMW M3 (G80)',
    # Honda
    ('honda', 'civic', range(2021, 2022)):   'Honda Civic (tenth generation)',
    ('honda', 'civic', range(2022, 2026)):   'Honda Civic (eleventh generation)',
    ('honda', 'accord', range(2021, 2023)):  'Honda Accord (tenth generation)',
    ('honda', 'accord', range(2023, 2026)):  'Honda Accord (eleventh generation)',
    ('honda', 'cr-v', range(2021, 2023)):    'Honda CR-V (fifth generation)',
    ('honda', 'cr-v', range(2023, 2026)):    'Honda CR-V (sixth generation)',
    # Mercedes-Benz
    ('mercedes-benz', 'c-class', range(2021, 2022)): 'Mercedes-Benz W205',
    ('mercedes-benz', 'c-class', range(2022, 2026)): 'Mercedes-Benz W206',
    ('mercedes-benz', 's-class', range(2021, 2026)): 'Mercedes-Benz W223',
    # Tesla
    ('tesla', 'model-3', range(2021, 2024)): 'Tesla Model 3',
    ('tesla', 'model-3', range(2024, 2026)): 'Tesla Model 3 (second generation)',
    ('tesla', 'model-y', range(2021, 2026)): 'Tesla Model Y',
    ('tesla', 'model-s', range(2021, 2026)): 'Tesla Model S (second generation)',
    # Hyundai
    ('hyundai', 'elantra', range(2021, 2026)): 'Hyundai Elantra (CN7)',
    ('hyundai', 'tucson', range(2021, 2026)):  'Hyundai Tucson (NX4)',
    ('hyundai', 'ioniq-5', range(2022, 2026)): 'Hyundai Ioniq 5',
    # Kia
    ('kia', 'sportage', range(2021, 2023)): 'Kia Sportage (QL)',
    ('kia', 'sportage', range(2023, 2026)): 'Kia Sportage (NQ5)',
    ('kia', 'ev6', range(2022, 2026)):       'Kia EV6',
    # Subaru
    ('subaru', 'outback', range(2021, 2026)): 'Subaru Outback (sixth generation)',
    ('subaru', 'wrx', range(2021, 2023)):    'Subaru WRX (VA)',
    ('subaru', 'wrx', range(2023, 2026)):    'Subaru WRX (VB)',
    # Mazda
    ('mazda', 'cx-5', range(2021, 2026)):   'Mazda CX-5 (KF)',
    # Jeep
    ('jeep', 'wrangler', range(2021, 2026)): 'Jeep Wrangler (JL)',
    ('jeep', 'grand-cherokee', range(2021, 2022)): 'Jeep Grand Cherokee (WK2)',
    ('jeep', 'grand-cherokee', range(2022, 2026)): 'Jeep Grand Cherokee (WL)',
    ('jeep', 'gladiator', range(2021, 2026)): 'Jeep Gladiator (JT)',
    # Porsche
    ('porsche', '911', range(2021, 2026)):   'Porsche 992',
    ('porsche', 'cayenne', range(2021, 2026)): 'Porsche Cayenne (9YA)',
    ('porsche', 'taycan', range(2021, 2026)): 'Porsche Taycan',
    # Dodge
    ('dodge', 'charger', range(2021, 2026)): 'Dodge Charger (LX)',
    ('dodge', 'challenger', range(2021, 2026)): 'Dodge Challenger (LC)',
    # RAM
    ('ram', 'ram-1500', range(2021, 2026)):  'Ram 1500 (DT)',
    # Volvo
    ('volvo', 'xc60', range(2021, 2026)):   'Volvo XC60 (U)',
    ('volvo', 'xc90', range(2021, 2026)):   'Volvo XC90 (SPA)',
    # Land Rover
    ('land-rover', 'range-rover', range(2021, 2022)): 'Range Rover (fourth generation)',
    ('land-rover', 'range-rover', range(2022, 2026)): 'Range Rover (fifth generation)',
    ('land-rover', 'defender', range(2021, 2026)): 'Land Rover Defender (L663)',
}


def get_generation_wiki(brand_slug, model_slug, year):
    for (b, m, yr), title in GENERATION_WIKI.items():
        if b == brand_slug and m == model_slug and year in yr:
            return title
    return None


def main():
    app = create_app('development')
    with app.app_context():
        cat = Category.query.filter_by(slug='cars').first()
        if not cat:
            print('Cars category not found')
            return

        total = 0
        found = 0
        fallback = 0

        for sc in SubCategory.query.filter_by(category_id=cat.id).order_by('name').all():
            print(f'\n{sc.name}:')
            for subj in sc.subjects.order_by('name').all():
                tail = subj.slug.rsplit('-', 1)[-1]
                if not (tail.isdigit() and len(tail) == 4):
                    continue
                year = int(tail)
                model_slug = subj.slug.rsplit('-', 1)[0]  # e.g. 'camry'
                model_name = subj.name.rsplit(' ', 1)[0]  # e.g. 'Camry'
                full_name = f'{sc.name} {model_name}'
                total += 1

                year_img_rel = f'images/uploads/subjects/cars-{subj.slug}.jpg'
                year_img_dest = os.path.join(STATIC_DIR, year_img_rel)

                # Already downloaded — just ensure DB is updated
                if os.path.exists(year_img_dest):
                    if subj.image_path != year_img_rel:
                        subj.image_path = year_img_rel
                    found += 1
                    continue

                url = None

                # 1. Try generation-specific Wikipedia article
                gen_title = get_generation_wiki(sc.slug, model_slug, year)
                if gen_title:
                    url = wiki_image(gen_title)
                    if url:
                        print(f'  {subj.name}: wiki gen "{gen_title}"')

                # 2. Try Commons search for year-specific photo
                if not url:
                    query = f'{year} {full_name}'
                    url = commons_search_image(query)
                    if url:
                        print(f'  {subj.name}: commons "{query}"')
                    time.sleep(1)

                if url and download(url, year_img_dest):
                    subj.image_path = year_img_rel
                    found += 1
                else:
                    # Fall back: use existing shared model image
                    model_img_rel = f'images/uploads/subjects/cars-{model_slug}.jpg'
                    if subj.image_path != model_img_rel:
                        subj.image_path = model_img_rel
                    fallback += 1
                    if not url:
                        print(f'  {subj.name}: using shared model image')

                time.sleep(0.5)

            db.session.commit()
            print(f'  committed {sc.name}')

        print(f'\nDone. {total} subjects: {found} unique images, {fallback} fallbacks.')


if __name__ == '__main__':
    main()
