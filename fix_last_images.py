#!/usr/bin/env python3
"""Fix last 4 remaining food images."""
import os, time, urllib.request, json, urllib.parse

HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; educational)'}
STATIC = os.path.join(os.path.dirname(__file__), 'static')


def commons_file_url(filename):
    title = 'File:' + filename
    url = ('https://commons.wikimedia.org/w/api.php?action=query&titles='
           + urllib.parse.quote(title) + '&prop=imageinfo&iiprop=url&format=json')
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())
    pages = data.get('query', {}).get('pages', {})
    for page in pages.values():
        info = page.get('imageinfo', [])
        if info:
            return info[0].get('url')
    return None


def download(url, dest):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    if len(data) < 5000:
        return 0
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, 'wb') as f:
        f.write(data)
    return len(data)


def update_db(slug, image_path):
    from app import create_app, db
    from app.models import Subject
    app = create_app()
    with app.app_context():
        s = Subject.query.filter_by(slug=slug).first()
        if s:
            s.image_path = image_path
            db.session.commit()
            return True
    return False


# Direct URLs for each dish
fixes = [
    # Nepalese Bara: use thumbnail version
    ('nepalese-bara', 'food-nepalese-bara.jpg',
     'https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Bara_%2833428%29.jpg/640px-Bara_%2833428%29.jpg'),
    # Uzbek Manti: thumbnail
    ('uzbek-manti', 'food-uzbek-manti.jpg',
     'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Uzbek_Manti_%28bright%29.jpg/640px-Uzbek_Manti_%28bright%29.jpg'),
    # Armenian Manti: direct file
    ('armenian-manti', 'food-armenian-manti.jpg', None),  # will use commons_file_url
    # Bolivian Tucumanas: Salteña
    ('bolivian-tucumanas', 'food-bolivian-tucumanas.jpg',
     'https://upload.wikimedia.org/wikipedia/commons/3/38/Salte%C3%B1a.jpg'),
]

# Get Armenian Manti URL
armenian_url = commons_file_url('Armenian Manti.jpg')
print(f'Armenian Manti URL: {armenian_url}')
# Fill it in
fixes[2] = ('armenian-manti', 'food-armenian-manti.jpg', armenian_url)

for slug, fname, url in fixes:
    dest = os.path.join(STATIC, 'images', 'uploads', 'subjects', fname)
    print(f'\n{slug} → {fname}')
    if not url:
        print('  No URL, skipping')
        continue
    print(f'  {url[:80]}')
    size = download(url, dest)
    if size:
        rel = f'images/uploads/subjects/{fname}'
        ok = update_db(slug, rel)
        print(f'  OK ({size:,}b) DB={ok}')
    else:
        print(f'  Failed')
    time.sleep(2)

print('\nDone')
