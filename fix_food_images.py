#!/usr/bin/env python3
"""Fix wrong/missing food images for specific dishes."""

import os
import time
import urllib.request

STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; FoodImageFixer/1.0; educational)'
}


def wiki_pageimage(title, thumb=600):
    """Return direct image URL from Wikipedia article pageimage."""
    import urllib.parse
    url = (
        'https://en.wikipedia.org/w/api.php'
        f'?action=query&titles={urllib.parse.quote(title)}'
        f'&prop=pageimages&pithumbsize={thumb}&format=json&redirects=1'
    )
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as r:
        data = __import__('json').loads(r.read())
    pages = data.get('query', {}).get('pages', {})
    for page in pages.values():
        thumb_data = page.get('thumbnail', {})
        if thumb_data:
            return thumb_data.get('source')
    return None


def commons_search(query, skip_keywords=None, max_results=20):
    """Search Wikimedia Commons for an image, return first matching URL."""
    import urllib.parse, json
    skip_keywords = skip_keywords or []
    url = (
        'https://commons.wikimedia.org/w/api.php'
        f'?action=query&list=search&srnamespace=6'
        f'&srsearch={urllib.parse.quote(query)}&srlimit={max_results}&format=json'
    )
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())
    results = data.get('query', {}).get('search', [])
    for item in results:
        title = item['title']  # e.g. "File:Foo.jpg"
        fname = title.replace('File:', '')
        if skip_keywords and any(k.lower() in fname.lower() for k in skip_keywords):
            continue
        img_url = commons_file_url(fname)
        if img_url:
            return img_url
    return None


def commons_file_url(filename):
    """Get direct URL for a Commons file via imageinfo API."""
    import urllib.parse, json
    title = f'File:{filename}'
    url = (
        'https://commons.wikimedia.org/w/api.php'
        f'?action=query&titles={urllib.parse.quote(title)}'
        f'&prop=imageinfo&iiprop=url&format=json'
    )
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
        pages = data.get('query', {}).get('pages', {})
        for page in pages.values():
            info = page.get('imageinfo', [])
            if info:
                return info[0].get('url')
    except Exception:
        pass
    return None


def download(url, dest_path, retries=3):
    """Download url to dest_path. Returns file size or 0 on failure."""
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=20) as r:
                if r.status == 429:
                    print(f'  Rate limited, sleeping 30s...')
                    time.sleep(30)
                    continue
                data = r.read()
            if len(data) < 5000:
                return 0
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            with open(dest_path, 'wb') as f:
                f.write(data)
            return len(data)
        except Exception as e:
            if '429' in str(e):
                print(f'  Rate limited (exception), sleeping 30s...')
                time.sleep(30)
            elif attempt < retries - 1:
                time.sleep(3)
    return 0


def update_db(subject_slug, new_image_path):
    """Update Subject.image_path in the DB."""
    from app import create_app, db
    from app.models import Subject
    app = create_app()
    with app.app_context():
        s = Subject.query.filter_by(slug=subject_slug).first()
        if s:
            s.image_path = new_image_path
            db.session.commit()
            return True
    return False


def fix(subject_slug, dest_filename, strategies, skip_keywords=None):
    """Try each strategy until one works. strategies = list of (type, value) tuples."""
    dest_path = os.path.join(STATIC_DIR, 'images', 'uploads', 'subjects', dest_filename)
    print(f'\n{subject_slug} → {dest_filename}')

    img_url = None
    for stype, sval in strategies:
        try:
            if stype == 'wiki':
                img_url = wiki_pageimage(sval)
            elif stype == 'commons_search':
                img_url = commons_search(sval, skip_keywords=skip_keywords)
            elif stype == 'commons_file':
                img_url = commons_file_url(sval)
            elif stype == 'direct':
                img_url = sval

            if img_url:
                print(f'  Found via {stype}: {img_url[:80]}...' if len(img_url) > 80 else f'  Found via {stype}: {img_url}')
                size = download(img_url, dest_path)
                if size > 0:
                    # Determine extension from URL
                    ext = img_url.split('?')[0].rsplit('.', 1)[-1].lower()
                    if ext not in ('jpg', 'jpeg', 'png', 'gif', 'webp'):
                        ext = 'jpg'
                    if not dest_filename.endswith(f'.{ext}'):
                        # Need different extension
                        new_filename = dest_filename.rsplit('.', 1)[0] + f'.{ext}'
                        new_path = os.path.join(STATIC_DIR, 'images', 'uploads', 'subjects', new_filename)
                        os.rename(dest_path, new_path)
                        dest_path = new_path
                        dest_filename = new_filename
                    rel_path = f'images/uploads/subjects/{dest_filename}'
                    updated = update_db(subject_slug, rel_path)
                    print(f'  OK ({size:,}b) → DB updated: {updated}')
                    return True
                else:
                    print(f'  Download failed/too small, trying next strategy...')
                    img_url = None
        except Exception as e:
            print(f'  {stype} error: {e}')
            img_url = None

        time.sleep(1)

    print(f'  FAILED - no working image found')
    return False


def main():
    fixes = [
        # BeaverTail (Canadian pastry)
        ('canadian-beavertail', 'food-canadian-beavertail.jpg', [
            ('wiki', 'BeaverTails'),
            ('commons_search', 'BeaverTails pastry food Canada'),
            ('commons_search', 'BeaverTail fried dough pastry'),
            ('commons_file', 'BeaverTails-pastry.jpg'),
        ], ['hut', 'stand', 'stall', 'shop', 'market', 'kiosk']),

        # Colombian Lechona (whole stuffed pig)
        ('colombian-lechona', 'food-colombian-lechona.jpg', [
            ('wiki', 'Lechona'),
            ('commons_search', 'Lechona colombiana pork stuffed'),
            ('commons_search', 'Lechona food Colombia'),
            ('commons_file', 'Lechona.jpg'),
        ], []),

        # Nepalese Bara (lentil pancake)
        ('nepalese-bara', 'food-nepalese-bara.jpg', [
            ('wiki', 'Bara (food)'),
            ('commons_search', 'Bara Nepalese lentil pancake food'),
            ('commons_search', 'bara Nepal food dish'),
            ('commons_file', 'Bara,_a_Newari_food.jpg'),
        ], []),

        # Uzbek Lagman (noodle soup)
        ('uzbek-lagman', 'food-uzbek-lagman.jpg', [
            ('wiki', 'Laghman (dish)'),
            ('commons_search', 'Lagman Uzbek noodle soup dish'),
            ('commons_search', 'Laghman noodle Central Asia food'),
            ('commons_file', 'Laghman.jpg'),
        ], []),

        # Uzbek Manti (steamed dumplings)
        ('uzbek-manti', 'food-uzbek-manti.jpg', [
            ('commons_search', 'Uzbek manti steamed dumplings food'),
            ('commons_search', 'Manti dumpling Uzbekistan dish'),
            ('commons_file', 'Manti_Uzbekistan.jpg'),
            ('commons_file', 'Uzbek_manti.jpg'),
        ], ['kayseri', 'turkish', 'armenian', 'baked']),

        # Uzbek Naryn (cold noodle dish)
        ('uzbek-naryn', 'food-uzbek-naryn.jpg', [
            ('wiki', 'Naryn (dish)'),
            ('commons_search', 'Naryn Uzbek noodle horse meat dish'),
            ('commons_search', 'Naryn Central Asian food dish'),
            ('commons_file', 'Naryn_dish.jpg'),
        ], []),

        # Armenian Manti (baked dumplings)
        ('armenian-manti', 'food-armenian-manti.jpg', [
            ('commons_search', 'Armenian manti baked dumplings food'),
            ('commons_search', 'Manti Armenian dish baked'),
            ('commons_file', 'Armenian_manti.jpg'),
            ('commons_file', 'Manti_Armenian.jpg'),
        ], ['uzbek', 'turkish', 'kayseri']),

        # Azerbaijani Piti (lamb soup)
        ('azerbaijani-piti', 'food-azerbaijani-piti.jpg', [
            ('wiki', 'Piti (food)'),
            ('commons_search', 'Piti Azerbaijani lamb soup dish'),
            ('commons_search', 'Piti stew Azerbaijan food'),
            ('commons_file', 'Piti_azerbaijani.jpg'),
            ('commons_file', 'Piti.jpg'),
        ], []),

        # Burmese Mont Di (fish noodle soup)
        ('burmese-mont-di', 'food-burmese-mont-di.jpg', [
            ('wiki', 'Mont di'),
            ('commons_search', 'Mont di Burmese fish noodle soup'),
            ('commons_search', 'Mont di Myanmar food dish'),
            ('commons_file', 'Mont_di.jpg'),
            ('commons_file', 'Mont-di.jpg'),
        ], []),

        # Norwegian Klippfisk (dried salted cod)
        ('norwegian-klippfisk', 'food-norwegian-klippfisk.jpg', [
            ('wiki', 'Klippfisk'),
            ('commons_search', 'Klippfisk Norwegian dried cod food'),
            ('commons_search', 'Bacalhau dried salted cod dish'),
            ('commons_file', 'Klippfisk.jpg'),
        ], []),

        # Ghanaian Red Red (bean stew with plantain)
        ('ghanaian-red-red', 'food-ghanaian-red-red.jpg', [
            ('wiki', 'Red red'),
            ('commons_search', 'Red red Ghana bean stew fried plantain'),
            ('commons_search', 'Red red West African bean stew dish'),
            ('commons_file', 'Red_red.jpg'),
            ('commons_file', 'Red-red.jpg'),
        ], []),

        # Chilean Empanadas
        ('chilean-empanadas', 'food-chilean-empanadas.jpg', [
            ('wiki', 'Chilean empanada'),
            ('commons_search', 'Chilean empanada de pino food'),
            ('commons_search', 'empanada Chile pastry food dish'),
            ('commons_file', 'Empanada_de_Pino.jpg'),
            ('commons_file', 'Chilean_Empanada.jpg'),
        ], ['colombian', 'argentinian', 'bolivian', 'tucumana']),

        # Bolivian Tucumanas (fried dumplings)
        ('bolivian-tucumanas', 'food-bolivian-tucumanas.jpg', [
            ('wiki', 'Tucumana'),
            ('commons_search', 'Tucumana Bolivian fried dumpling food'),
            ('commons_search', 'Tucumana Bolivia street food dish'),
            ('commons_file', 'Tucumana.jpg'),
            ('commons_file', 'Bolivian_tucumana.jpg'),
        ], []),
    ]

    successes = 0
    for args in fixes:
        subject_slug = args[0]
        dest_filename = args[1]
        strategies = args[2]
        skip_keywords = args[3] if len(args) > 3 else []
        if fix(subject_slug, dest_filename, strategies, skip_keywords):
            successes += 1
        time.sleep(2)

    print(f'\nDone: {successes}/{len(fixes)} fixed')


if __name__ == '__main__':
    main()
