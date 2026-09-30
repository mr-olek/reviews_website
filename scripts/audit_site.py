"""Read-only audit of the catalogue using an isolated database copy."""
import json
import os
import sys
from collections import Counter
from pathlib import Path
from html.parser import HTMLParser

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import create_app
from app.models import Category, SubCategory, Subject, Review


class Assets(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        value = attrs.get('src') if tag in ('img', 'script') else attrs.get('href') if tag == 'link' else None
        if value and value.startswith('/static/'):
            self.paths.add(value.split('?', 1)[0])


app = create_app('production')
app.config['TESTING'] = True
client = app.test_client()
with app.app_context():
    categories = {c.id: c.slug for c in Category.query.all()}
    subcategories = {s.id: f'/{categories[s.category_id]}/{s.slug}/' for s in SubCategory.query.all()}
    subjects = {s.id: subcategories[s.subcategory_id] + s.slug + '/' for s in Subject.query.all()}
    reviews = Review.query.filter_by(is_published=True).with_entities(Review.id, Review.subject_id).all()
    # Every subject's first review; --all-reviews expands to every review.
    chosen = {}
    for review_id, subject_id in reviews:
        chosen.setdefault(subject_id, review_id)
    review_paths = ([subjects[s] + str(r) + '/' for r, s in reviews] if '--all-reviews' in sys.argv
                    else [subjects[s] + str(r) + '/' for s, r in chosen.items()])
paths = ['/', '/robots.txt', '/sitemap.xml', '/llms.txt', '/admin/login']
paths += ['/' + s + '/' for s in categories.values()]
paths += list(subcategories.values()) + list(subjects.values()) + review_paths
counts = Counter()
failures = []
assets = set()
for i, path in enumerate(paths, 1):
    try:
        response = client.get(path)
        counts[response.status_code] += 1
        if response.status_code != 200:
            failures.append({'path': path, 'status': response.status_code})
        elif response.mimetype == 'text/html':
            parser = Assets()
            parser.feed(response.get_data(as_text=True))
            assets.update(parser.paths)
    except Exception as exc:
        failures.append({'path': path, 'error': str(exc)})
    if i % 500 == 0:
        print(f'Checked {i}/{len(paths)} pages; failures={len(failures)}', flush=True)
missing_assets = []
for path in sorted(assets):
    if not (Path(app.static_folder) / path.removeprefix('/static/')).is_file():
        missing_assets.append(path)
result = {'pages': len(paths), 'statuses': dict(counts), 'failures': failures,
          'assets': len(assets), 'missing_assets': missing_assets}
Path('/tmp/verdictly-audit.json').write_text(json.dumps(result, indent=2))
print(json.dumps(result, indent=2), flush=True)
sys.exit(bool(failures))
