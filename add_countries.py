#!/usr/bin/env python3
"""Seed Countries category with top 60 most popular countries and reviews."""
import os, sys, random, time, requests
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Category, SubCategory, Subject, Review

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
SESSION = requests.Session()
SESSION.headers['User-Agent'] = 'Mozilla/5.0 (compatible; VerdictlyBot/1.0)'

# ---------------------------------------------------------------------------
# 60 countries: (Display Name, slug, Wikipedia article for image)
# Ukraine first, Russia excluded
# ---------------------------------------------------------------------------
COUNTRIES = [
    ('Ukraine',               'ukraine',               'Ukraine'),
    ('France',                'france',                'France'),
    ('Spain',                 'spain',                 'Spain'),
    ('United States',         'united-states',         'United States'),
    ('China',                 'china',                 'China'),
    ('Italy',                 'italy',                 'Italy'),
    ('Turkey',                'turkey',                'Turkey'),
    ('Mexico',                'mexico',                'Mexico'),
    ('Thailand',              'thailand',              'Thailand'),
    ('Germany',               'germany',               'Germany'),
    ('United Kingdom',        'united-kingdom',        'United Kingdom'),
    ('Japan',                 'japan',                 'Japan'),
    ('Greece',                'greece',                'Greece'),
    ('Austria',               'austria',               'Austria'),
    ('Malaysia',              'malaysia',              'Malaysia'),
    ('Portugal',              'portugal',              'Portugal'),
    ('Canada',                'canada',                'Canada'),
    ('Poland',                'poland',                'Poland'),
    ('Netherlands',           'netherlands',           'Netherlands'),
    ('United Arab Emirates',  'united-arab-emirates',  'United Arab Emirates'),
    ('Brazil',                'brazil',                'Brazil'),
    ('South Korea',           'south-korea',           'South Korea'),
    ('India',                 'india',                 'India'),
    ('Australia',             'australia',             'Australia'),
    ('Switzerland',           'switzerland',           'Switzerland'),
    ('Indonesia',             'indonesia',             'Indonesia'),
    ('Morocco',               'morocco',               'Morocco'),
    ('Croatia',               'croatia',               'Croatia'),
    ('Czech Republic',        'czech-republic',        'Czech Republic'),
    ('Hungary',               'hungary',               'Hungary'),
    ('Vietnam',               'vietnam',               'Vietnam'),
    ('Argentina',             'argentina',             'Argentina'),
    ('Egypt',                 'egypt',                 'Egypt'),
    ('Belgium',               'belgium',               'Belgium'),
    ('Singapore',             'singapore',             'Singapore'),
    ('Peru',                  'peru',                  'Peru'),
    ('Colombia',              'colombia',              'Colombia'),
    ('Saudi Arabia',          'saudi-arabia',          'Saudi Arabia'),
    ('South Africa',          'south-africa',          'South Africa'),
    ('Kenya',                 'kenya',                 'Kenya'),
    ('New Zealand',           'new-zealand',           'New Zealand'),
    ('Ireland',               'ireland',               'Ireland'),
    ('Norway',                'norway',                'Norway'),
    ('Iceland',               'iceland',               'Iceland'),
    ('Sweden',                'sweden',                'Sweden'),
    ('Denmark',               'denmark',               'Denmark'),
    ('Cuba',                  'cuba',                  'Cuba'),
    ('Philippines',           'philippines',           'Philippines'),
    ('Jordan',                'jordan',                'Jordan'),
    ('Israel',                'israel',                'Israel'),
    ('Tanzania',              'tanzania',              'Tanzania'),
    ('Nepal',                 'nepal',                 'Nepal'),
    ('Sri Lanka',             'sri-lanka',             'Sri Lanka'),
    ('Maldives',              'maldives',              'Maldives'),
    ('Cambodia',              'cambodia',              'Cambodia'),
    ('Romania',               'romania',               'Romania'),
    ('Albania',               'albania',               'Albania'),
    ('Serbia',                'serbia',                'Serbia'),
    ('Georgia',               'georgia-country',       'Georgia (country)'),
    ('Hong Kong',             'hong-kong',             'Hong Kong'),
]

# ---------------------------------------------------------------------------
# Review templates — travel experiences
# ---------------------------------------------------------------------------
REVIEW_TEMPLATES = [
    {
        'title': 'An absolutely unforgettable trip',
        'body': "Visited {name} for {n} days and it exceeded every expectation. The {highlight} alone was worth the journey. People were warm and welcoming, food was incredible. Already planning my return trip. Highly recommend to anyone.",
        'rating': 5,
    },
    {
        'title': 'One of the best travel experiences of my life',
        'body': "I've travelled to many countries but {name} stands out. The combination of {highlight}, history, and culture is unlike anywhere else. Spent {n} days and wished I had booked for longer. An absolute must-visit.",
        'rating': 5,
    },
    {
        'title': 'Beautiful country, friendly people',
        'body': "{name} completely won me over. Locals were some of the friendliest I've encountered anywhere. The {highlight} is stunning and the local cuisine is something special. {n} days wasn't nearly enough.",
        'rating': 5,
    },
    {
        'title': 'Great destination with a few caveats',
        'body': "{name} is a fantastic place to visit but {challenge} can be frustrating for first-time visitors. Once you get past that, the {highlight} and overall experience are genuinely impressive. Do your research before going.",
        'rating': 4,
    },
    {
        'title': 'Exceeded my expectations completely',
        'body': "Honestly didn't know much about {name} before visiting but a friend recommended it. After {n} days I understand why. The {highlight} is world-class and the value for money is excellent. Pleasantly surprised.",
        'rating': 5,
    },
    {
        'title': 'Rich history and stunning scenery',
        'body': "As a history lover, {name} was paradise. Every corner has a story — ancient sites, monuments, museums. The {highlight} kept me in awe throughout my {n}-day stay. A deeply rewarding destination for curious travellers.",
        'rating': 5,
    },
    {
        'title': 'Good trip, not without its issues',
        'body': "Spent {n} days in {name} and had a mostly positive experience. The {highlight} was genuinely impressive but {challenge} dampened things slightly. Would still recommend it but manage your expectations going in.",
        'rating': 4,
    },
    {
        'title': 'The food alone is worth the trip',
        'body': "I went to {name} primarily for the food and was not disappointed. Every meal was an adventure. Beyond the cuisine, the {highlight} adds incredible visual richness to the experience. Came back several kilos heavier, no regrets.",
        'rating': 5,
    },
    {
        'title': 'A hidden gem that deserves more visitors',
        'body': "{name} doesn't always get the attention it deserves on the travel circuit. But the {highlight} rivals anything in more famous destinations. Fewer crowds and better value make it an ideal choice for savvy travellers.",
        'rating': 5,
    },
    {
        'title': 'Challenging but rewarding',
        'body': "{name} isn't the easiest destination — {challenge} can test your patience. But the rewards are real. The {highlight} and genuine cultural immersion you get here is hard to replicate elsewhere. Push through the difficulties.",
        'rating': 4,
    },
    {
        'title': 'Would return in a heartbeat',
        'body': "There are countries you visit once and countries you keep returning to. {name} is the latter for me. The {highlight}, the atmosphere, the people — everything draws you back. Booked my third visit before the second was over.",
        'rating': 5,
    },
    {
        'title': 'Perfect for a {n}-day break',
        'body': "{name} is ideal for a shorter trip. In {n} days you can take in the highlights without feeling rushed. The {highlight} is compact enough to explore thoroughly. Great option for long weekend or week-long getaways.",
        'rating': 4,
    },
    {
        'title': 'Stunning natural landscapes',
        'body': "The natural beauty of {name} is genuinely breathtaking. The {highlight} is unlike anything I'd seen before. Spent most of my {n} days outdoors just absorbing the scenery. If you love nature travel, this belongs on your list.",
        'rating': 5,
    },
    {
        'title': 'Great value for money',
        'body': "{name} offers incredible value compared to more touristy destinations. Your money goes far here — quality accommodation, food, and experiences at a fraction of the cost. The {highlight} only adds to the appeal.",
        'rating': 5,
    },
    {
        'title': 'Culture shock in the best way',
        'body': "Visiting {name} pushed me out of my comfort zone and I loved it. The {highlight} and daily rhythms of life here are so different from home. Came back with a broader worldview and a lot of great stories.",
        'rating': 5,
    },
    {
        'title': 'Busy but worth it',
        'body': "Popular tourist spots in {name} can be crowded, especially around {highlight}. But even with the crowds the experience is worthwhile. Go early, be patient, and you'll be rewarded with memories that last a lifetime.",
        'rating': 4,
    },
    {
        'title': 'Not quite what I expected',
        'body': "I had very high expectations for {name} based on photos and reviews. The {highlight} is impressive but {challenge} was more of an issue than anticipated. Still a good trip, just tempered my expectations for next time.",
        'rating': 3,
    },
    {
        'title': 'Safety was better than I feared',
        'body': "I had concerns about visiting {name} after reading some negative reports. In reality I felt comfortable and safe throughout my {n}-day stay. The {highlight} was wonderful and locals were genuinely helpful. Don't let fear stop you.",
        'rating': 4,
    },
    {
        'title': 'The people made it special',
        'body': "What I'll remember most about {name} isn't the {highlight} or the food — it's the people. Locals went out of their way to help, share stories, and make me feel welcome. That human connection is irreplaceable.",
        'rating': 5,
    },
    {
        'title': 'A perfect honeymoon destination',
        'body': "We chose {name} for our honeymoon and it was absolutely perfect. Romantic atmosphere, stunning {highlight}, incredible food. The {n} days flew by. Couldn't have asked for a better start to married life.",
        'rating': 5,
    },
    {
        'title': 'Great for solo travellers',
        'body': "Visited {name} solo for {n} days and felt completely at ease. The {highlight} is easy to navigate independently and I met fellow travellers easily. One of the more welcoming countries I've solo-tripped in.",
        'rating': 5,
    },
    {
        'title': 'Family-friendly and accessible',
        'body': "Travelled to {name} with two young kids and it worked really well. The {highlight} kept everyone entertained and facilities were good. A few {challenge} moments but nothing that ruined the trip. Would go back as a family.",
        'rating': 4,
    },
    {
        'title': 'Overrated in my opinion',
        'body': "Spent {n} days in {name} and while {highlight} is genuinely impressive, I felt the country gets more hype than it deserves. {challenge} was a persistent issue and I've had more enjoyable trips elsewhere at similar cost.",
        'rating': 3,
    },
    {
        'title': 'Off the beaten path and loving it',
        'body': "Chose {name} because I wanted something different from the usual tourist trail. The {highlight} delivered something genuinely unique. Felt like a real explorer rather than just another tourist. Highly recommend for adventurous travellers.",
        'rating': 5,
    },
]

HIGHLIGHTS = [
    'architecture', 'coastline', 'mountain scenery', 'ancient ruins', 'vibrant street life',
    'national parks', 'old town', 'beaches', 'cultural heritage', 'cityscape',
    'traditional villages', 'historic monuments', 'natural wonders', 'local markets',
    'countryside', 'temples and shrines', 'desert landscapes', 'island scenery',
]
CHALLENGES = [
    'the language barrier', 'navigating public transport', 'tourist crowds',
    'the summer heat', 'bureaucratic visa requirements', 'finding budget accommodation',
    'the traffic in cities', 'inconsistent signage for tourists',
]

FIRST_NAMES = [
    'Emma', 'Liam', 'Olivia', 'Noah', 'Ava', 'Ethan', 'Sophia', 'Mason',
    'Isabella', 'James', 'Mia', 'Logan', 'Charlotte', 'Lucas', 'Amelia',
    'Jackson', 'Harper', 'Aiden', 'Evelyn', 'Sebastian', 'Abigail', 'Mateo',
    'Emily', 'Jack', 'Elizabeth', 'Owen', 'Sofia', 'Henry', 'Avery', 'Samuel',
    'Ella', 'Elijah', 'Madison', 'Daniel', 'Scarlett', 'Benjamin', 'Victoria',
    'Aria', 'Dylan', 'Grace', 'Michael', 'Chloe', 'Jayden', 'Penelope', 'Ryan',
    'Marcus', 'Diana', 'Derek', 'Priya', 'Kenji', 'Fatima', 'Carlos', 'Ingrid',
    'Takashi', 'Miriam', 'Stefan', 'Yuki', 'Ahmed', 'Natalia', 'Pierre', 'Leila',
]


def random_author():
    return random.choice(FIRST_NAMES)


def make_review(name, tmpl):
    n = random.randint(5, 21)
    title = tmpl['title'].format(name=name, n=n)
    body = tmpl['body'].format(
        name=name,
        n=n,
        highlight=random.choice(HIGHLIGHTS),
        challenge=random.choice(CHALLENGES),
    )
    return title, body, tmpl['rating']


# ---------------------------------------------------------------------------
# Wikipedia image helpers
# ---------------------------------------------------------------------------
def wiki_image(title, width=600):
    try:
        r = SESSION.get('https://en.wikipedia.org/w/api.php', params={
            'action': 'query', 'titles': title, 'prop': 'pageimages',
            'pithumbsize': width, 'format': 'json',
        }, timeout=12)
        pages = r.json()['query']['pages']
        page = next(iter(pages.values()))
        return page.get('thumbnail', {}).get('source')
    except Exception:
        return None


def commons_search(query, width=600):
    try:
        r = SESSION.get('https://commons.wikimedia.org/w/api.php', params={
            'action': 'query', 'list': 'search',
            'srsearch': f'filetype:bitmap {query}',
            'srnamespace': 6, 'srlimit': 5, 'format': 'json',
        }, timeout=12)
        for result in r.json().get('query', {}).get('search', []):
            r2 = SESSION.get('https://commons.wikimedia.org/w/api.php', params={
                'action': 'query', 'titles': result['title'],
                'prop': 'imageinfo', 'iiprop': 'url',
                'iiurlwidth': width, 'format': 'json',
            }, timeout=10)
            page = next(iter(r2.json()['query']['pages'].values()))
            iis = page.get('imageinfo', [])
            if iis and iis[0].get('thumburl'):
                return iis[0]['thumburl']
    except Exception as e:
        print(f'    commons error: {e}')
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
                print('    rate limited, sleeping 30s...')
                time.sleep(30)
        except Exception as e:
            print(f'    download error: {e}')
            time.sleep(3)
    return False


def fetch_image(name, wiki_title=None):
    url = wiki_image(wiki_title or name)
    if not url:
        url = commons_search(name)
    return url


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    app = create_app()
    with app.app_context():
        # Category
        cat = Category.query.filter_by(slug='countries').first()
        if not cat:
            cat = Category(name='Countries', slug='countries', icon='🌍',
                           description='Explore and review countries from around the world.')
            db.session.add(cat)
            db.session.flush()
            print(f'Created category: {cat.name}')

            img_url = wiki_image('World map')
            if not img_url:
                img_url = wiki_image('Earth')
            if img_url:
                ext = img_url.split('.')[-1].split('?')[0].lower()
                if ext not in ('jpg', 'jpeg', 'png', 'webp', 'gif'):
                    ext = 'jpg'
                fname = f'countries-category.{ext}'
                dest = os.path.join(STATIC_DIR, 'images', 'uploads', 'categories', fname)
                if download(img_url, dest):
                    cat.image_path = f'images/uploads/categories/{fname}'
                    print('  category image saved')
            db.session.commit()
        else:
            print(f'Category exists: {cat.name}')

        # Subcategory
        sc = SubCategory.query.filter_by(category_id=cat.id, slug='all-countries').first()
        if not sc:
            sc = SubCategory(category_id=cat.id, name='All Countries', slug='all-countries')
            db.session.add(sc)
            db.session.flush()

            img_url = wiki_image('Tourism')
            if not img_url:
                img_url = wiki_image('Travel')
            if img_url:
                ext = img_url.split('.')[-1].split('?')[0].lower()
                if ext not in ('jpg', 'jpeg', 'png', 'webp', 'gif'):
                    ext = 'jpg'
                fname = f'countries-all-countries.{ext}'
                dest = os.path.join(STATIC_DIR, 'images', 'uploads', 'subcategories', fname)
                if download(img_url, dest):
                    sc.image_path = f'images/uploads/subcategories/{fname}'
                    print('  subcategory image saved')
            db.session.commit()
            print('Created subcategory: All Countries')
        else:
            print('Subcategory exists: All Countries')

        total_subjects = 0
        total_reviews = 0

        for country_name, country_slug, wiki_title in COUNTRIES:
            subj = Subject.query.filter_by(subcategory_id=sc.id, slug=country_slug).first()
            if subj:
                print(f'  Skipping {country_name} (exists)')
                continue

            subj = Subject(subcategory_id=sc.id, name=country_name, slug=country_slug)
            db.session.add(subj)
            db.session.flush()

            # Image
            img_url = fetch_image(country_name, wiki_title)
            if img_url:
                ext = img_url.split('.')[-1].split('?')[0].lower()
                if ext not in ('jpg', 'jpeg', 'png', 'webp', 'gif'):
                    ext = 'jpg'
                fname = f'countries-{country_slug}.{ext}'
                dest = os.path.join(STATIC_DIR, 'images', 'uploads', 'subjects', fname)
                if download(img_url, dest):
                    subj.image_path = f'images/uploads/subjects/{fname}'
                    print(f'  img ok: {country_name}')
                else:
                    print(f'  no img: {country_name}')
            else:
                print(f'  no img: {country_name}')
            time.sleep(0.8)

            # Reviews
            from datetime import datetime, timedelta
            target = random.randint(12, 30)
            used_titles = set()
            reviews_added = 0
            shuffled = REVIEW_TEMPLATES[:]
            random.shuffle(shuffled)

            for tmpl in shuffled * 2:
                if reviews_added >= target:
                    break
                title, body, base_rating = make_review(country_name, tmpl)
                if title in used_titles:
                    continue
                used_titles.add(title)
                rating = max(1, min(5, base_rating + random.choice([-1, 0, 0, 0, 1])))
                days_ago = random.randint(1, 730)
                rev = Review(
                    subject_id=subj.id,
                    title=title,
                    body=body,
                    rating=rating,
                    author_name=random_author(),
                    source_site='sample',
                    original_date=datetime.utcnow() - timedelta(days=days_ago),
                    is_published=True,
                )
                db.session.add(rev)
                reviews_added += 1

            subj.update_stats()
            total_subjects += 1
            total_reviews += reviews_added
            print(f'  {country_name}: {reviews_added} reviews')

        db.session.commit()
        print(f'\nDone. {total_subjects} countries, {total_reviews} reviews.')


if __name__ == '__main__':
    main()
