#!/usr/bin/env python3
"""Seed Plants & Garden category with 20 plant types, specific varieties, and reviews."""
import os, sys, random, time, requests, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Category, SubCategory, Subject, Review

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
SESSION = requests.Session()
SESSION.headers['User-Agent'] = 'Mozilla/5.0 (compatible; VerdictlyBot/1.0)'

# ---------------------------------------------------------------------------
# 20 plant types → specific varieties
# ---------------------------------------------------------------------------
PLANT_DATA = [
    ('Roses', 'roses', [
        'Peace', 'Mr. Lincoln', 'Queen Elizabeth', 'Iceberg', 'New Dawn',
        'Double Delight', 'Black Baccara', 'Julia Child',
    ]),
    ('Succulents', 'succulents', [
        'Echeveria', 'Aloe Vera', 'Jade Plant', 'Haworthia',
        'String of Pearls', 'Ghost Plant', 'Panda Plant', 'Hen and Chicks',
    ]),
    ('Cacti', 'cacti', [
        'Saguaro', 'Prickly Pear', 'Christmas Cactus', 'Barrel Cactus',
        'Bunny Ears Cactus', 'Moon Cactus', 'Golden Barrel', 'Organ Pipe Cactus',
    ]),
    ('Herbs', 'herbs', [
        'Basil', 'Rosemary', 'Mint', 'Thyme',
        'Oregano', 'Cilantro', 'Chives', 'Sage',
    ]),
    ('Orchids', 'orchids', [
        'Phalaenopsis', 'Dendrobium', 'Cattleya', 'Oncidium',
        'Cymbidium', 'Vanda', 'Miltoniopsis', 'Zygopetalum',
    ]),
    ('Ferns', 'ferns', [
        'Boston Fern', 'Maidenhair Fern', "Bird's Nest Fern", 'Staghorn Fern',
        'Lady Fern', 'Ostrich Fern', 'Kimberly Queen Fern', 'Sword Fern',
    ]),
    ('Vegetables', 'vegetables', [
        'Tomato', 'Bell Pepper', 'Zucchini', 'Cucumber',
        'Kale', 'Spinach', 'Carrot', 'Sweet Corn',
    ]),
    ('Fruit Trees', 'fruit-trees', [
        'Apple Tree', 'Lemon Tree', 'Cherry Tree', 'Peach Tree',
        'Avocado Tree', 'Fig Tree', 'Mango Tree', 'Plum Tree',
    ]),
    ('Tropical Plants', 'tropical-plants', [
        'Bird of Paradise', 'Monstera Deliciosa', 'Heliconia', 'Banana Plant',
        'Anthurium', 'Plumeria', 'Bromeliad', 'Traveller\'s Palm',
    ]),
    ('Bonsai', 'bonsai', [
        'Japanese Maple Bonsai', 'Juniper Bonsai', 'Ficus Bonsai', 'Pine Bonsai',
        'Azalea Bonsai', 'Chinese Elm Bonsai', 'Cherry Blossom Bonsai', 'Wisteria Bonsai',
    ]),
    ('Wildflowers', 'wildflowers', [
        'Sunflower', 'Purple Coneflower', 'Black-eyed Susan', 'Cosmos',
        'California Poppy', 'Foxglove', 'Lupine', 'Meadow Sage',
    ]),
    ('Bamboo', 'bamboo', [
        'Lucky Bamboo', 'Golden Bamboo', 'Black Bamboo', 'Giant Bamboo',
        'Arrow Bamboo', 'Fargesia Bamboo', 'Heavenly Bamboo', 'Buddha Belly Bamboo',
    ]),
    ('Palms', 'palms', [
        'Areca Palm', 'Majesty Palm', 'Kentia Palm', 'Date Palm',
        'Queen Palm', 'Pygmy Date Palm', 'Windmill Palm', 'Sago Palm',
    ]),
    ('Vines & Climbers', 'vines-climbers', [
        'Wisteria', 'Jasmine', 'Clematis', 'Honeysuckle',
        'Passionflower', 'Morning Glory', 'Virginia Creeper', 'Climbing Hydrangea',
    ]),
    ('Bulbs', 'bulbs', [
        'Tulip', 'Daffodil', 'Hyacinth', 'Asiatic Lily',
        'Gladiolus', 'Crocus', 'Allium', 'Camassia',
    ]),
    ('Shrubs', 'shrubs', [
        'Lavender', 'Boxwood', 'Holly', 'Azalea',
        'Hydrangea', 'Rose of Sharon', 'Forsythia', 'Butterfly Bush',
    ]),
    ('Aquatic Plants', 'aquatic-plants', [
        'Water Lily', 'Lotus', 'Cattail', 'Water Hyacinth',
        'Hornwort', 'Anacharis', 'Pickerelweed', 'Blue Flag Iris',
    ]),
    ('Air Plants', 'air-plants', [
        'Tillandsia Ionantha', 'Tillandsia Xerographica', 'Tillandsia Stricta',
        'Tillandsia Bulbosa', 'Tillandsia Caput-Medusae', 'Tillandsia Capitata',
        'Tillandsia Brachycaulos', 'Tillandsia Andreana',
    ]),
    ('Houseplants', 'houseplants', [
        'Pothos', 'Snake Plant', 'ZZ Plant', 'Peace Lily',
        'Spider Plant', 'Rubber Plant', 'Monstera Adansonii', 'Chinese Evergreen',
    ]),
    ('Trees', 'trees', [
        'Japanese Maple', 'Magnolia', 'Cherry Blossom', 'Weeping Willow',
        'Dogwood', 'Redbud', 'Crepe Myrtle', 'Silver Birch',
    ]),
]

# ---------------------------------------------------------------------------
# Review templates
# ---------------------------------------------------------------------------
REVIEW_TEMPLATES = [
    {
        'title': 'Absolutely love this plant!',
        'body': "I've had {name} for about {n} months now and it's been a joy. Really easy to care for once you understand its needs. The growth has been steady and it looks beautiful in my {location}. Highly recommend for {level} gardeners.",
        'rating': 5,
    },
    {
        'title': 'Great addition to my garden',
        'body': "Bought {name} on a whim and couldn't be happier. It settled in quickly and has been thriving ever since. The {quality} is just stunning. Only thing to watch is {care_tip}. Would definitely buy again.",
        'rating': 5,
    },
    {
        'title': 'Beautiful but needs attention',
        'body': "{name} is gorgeous when it's happy, but it does need some specific care. I've learned that {care_tip} is crucial. Once I got the conditions right it rewarded me with {result}. Worth the effort for sure.",
        'rating': 4,
    },
    {
        'title': 'Solid plant, very reliable',
        'body': "This is my third {name} and each one has performed well. It's reliable, hardy, and just does its thing without much fuss. Perfect for {level} gardeners who want something dependable.",
        'rating': 4,
    },
    {
        'title': 'Surprised by how fast it grows',
        'body': "I expected slow growth from {name} but it has really taken off. In just {n} weeks it had already established itself nicely. Loving the {quality}. Great value for the price.",
        'rating': 5,
    },
    {
        'title': 'Took a while to settle in',
        'body': "{name} went through a bit of transplant shock at first — lost a few leaves and looked sad for a couple weeks. But once it adapted it started growing steadily. Now it looks great in my {location}. Patience pays off.",
        'rating': 4,
    },
    {
        'title': 'Mixed experience overall',
        'body': "I've had {name} for {n} months. Some periods it looks amazing, other times it struggles. I think the key is {care_tip}. When it's happy it's really beautiful, but getting there can be hit or miss.",
        'rating': 3,
    },
    {
        'title': 'Perfect for beginners',
        'body': "As someone new to gardening I was nervous about {name} but it's been super forgiving. Even when I forgot to water it for a week it bounced back. The {quality} makes it a real showstopper. Can't recommend it enough.",
        'rating': 5,
    },
    {
        'title': 'Not as easy as I expected',
        'body': "{name} looked so nice at the nursery but at home it's been a challenge. I've read everything I can about {care_tip} and still struggle at times. It does have moments of beauty but requires more effort than I anticipated.",
        'rating': 3,
    },
    {
        'title': 'Stunning when in bloom',
        'body': "When {name} blooms it is absolutely breathtaking. The {quality} is beyond compare. The rest of the year it's a nice green plant, but those weeks of flowering make it all worthwhile. Already ordered another one.",
        'rating': 5,
    },
    {
        'title': 'Great for indoor spaces',
        'body': "Been keeping {name} indoors for {n} months and it's doing wonderfully. It adapts well to indoor light conditions and doesn't drop leaves all over the place. The {quality} brightens up the whole room.",
        'rating': 5,
    },
    {
        'title': 'Hardy and drought-tolerant',
        'body': "{name} has survived everything I've thrown at it — missed waterings, temperature swings, even a bit of neglect. It's one of the toughest plants in my collection. Ideal if you want something low-maintenance.",
        'rating': 4,
    },
    {
        'title': 'Fragrance is incredible',
        'body': "I planted {name} mainly for the fragrance and it has not disappointed. Every time I walk past it in the {location} the scent is just wonderful. Beyond the smell, the {quality} is also very attractive.",
        'rating': 5,
    },
    {
        'title': 'Grows well in containers',
        'body': "I don't have much outdoor space so I grow {name} in pots and it works brilliantly. As long as you remember {care_tip} it thrives in containers just as well as in the ground. Great for balconies and patios.",
        'rating': 4,
    },
    {
        'title': 'Pest problems were an issue',
        'body': "My {name} got attacked by pests in the first season which was frustrating. After treating and taking care of {care_tip} it recovered well. Now it's healthy and looks great. Just be vigilant about checking for pests early.",
        'rating': 3,
    },
    {
        'title': 'Exceeded all my expectations',
        'body': "I bought {name} without much research and was blown away. The {quality} is spectacular and it grows faster than I expected. It's become the centerpiece of my {location}. Will be buying more varieties of this plant family.",
        'rating': 5,
    },
    {
        'title': 'Good but takes patience',
        'body': "{name} is a slow starter — for the first {n} months I wondered if it would ever take off. But then it suddenly hit its stride and now it's flourishing. Definitely worth the wait if you can be patient.",
        'rating': 4,
    },
    {
        'title': 'A real statement plant',
        'body': "Everyone who visits comments on my {name}. The {quality} is just so unique and eye-catching. It's become a real talking point. Takes a bit of know-how around {care_tip} but totally worth it.",
        'rating': 5,
    },
    {
        'title': 'Decent, nothing spectacular',
        'body': "My {name} is fine — it grows, it looks okay, it doesn't cause problems. But I was hoping for a bit more drama or impact. Maybe I haven't found the perfect spot for it yet. It's a solid {level}-level plant.",
        'rating': 3,
    },
    {
        'title': 'Would not buy again',
        'body': "{name} has been a disappointment. It never really thrived despite my attempts at {care_tip}. Lost more leaves than it grew and eventually gave up on me. Maybe I just got a weak specimen from the nursery.",
        'rating': 2,
    },
    {
        'title': 'Thrives with minimal care',
        'body': "I travel a lot and worried {name} wouldn't survive my absences. It's proven incredibly resilient — a slow-release feed and a deep water before I leave and it's fine for weeks. Perfect for busy plant lovers.",
        'rating': 5,
    },
    {
        'title': 'Beautiful foliage year-round',
        'body': "What I love about {name} is that it looks good in every season. The {quality} changes subtly through the year but it always has something going on visually. A truly reliable garden performer.",
        'rating': 4,
    },
    {
        'title': 'Fast results, very satisfying',
        'body': "Started from a small cutting and within {n} months had a full, healthy {name}. The {quality} has been consistently impressive. Great to see such quick progress — very satisfying for an impatient gardener like me.",
        'rating': 5,
    },
    {
        'title': 'Attracts pollinators',
        'body': "Since planting {name} my garden has been buzzing with bees and butterflies. The ecological benefit is as great as the visual one. The {quality} draws in pollinators all season long. Fantastic addition to any wildlife-friendly garden.",
        'rating': 5,
    },
    {
        'title': 'Struggled in my climate',
        'body': "{name} is beautiful but I live in a colder region and it has really struggled through winter. I've had to bring it inside and provide supplemental lighting. If you're in a warmer climate you'll probably have a much easier time.",
        'rating': 3,
    },
]

LOCATIONS = ['living room', 'garden', 'balcony', 'conservatory', 'back garden', 'patio', 'windowsill', 'greenhouse']
QUALITIES = ['leaf texture', 'flower color', 'fragrance', 'architectural shape', 'vibrant color', 'delicate blooms', 'lush foliage']
CARE_TIPS = [
    'watering consistency', 'good drainage', 'bright indirect light', 'regular feeding',
    'humidity levels', 'pruning after flowering', 'protecting from frost', 'well-draining soil',
]
LEVELS = ['beginner', 'intermediate', 'experienced', 'all-level']
RESULTS = [
    'abundant blooms', 'lush new growth', 'a stunning display', 'a dramatic size increase',
    'beautiful new leaves', 'a full bushy shape', 'vibrant flowers all season',
]

FIRST_NAMES = [
    'Emma', 'Liam', 'Olivia', 'Noah', 'Ava', 'Ethan', 'Sophia', 'Mason',
    'Isabella', 'James', 'Mia', 'Logan', 'Charlotte', 'Lucas', 'Amelia',
    'Jackson', 'Harper', 'Aiden', 'Evelyn', 'Sebastian', 'Abigail', 'Mateo',
    'Emily', 'Jack', 'Elizabeth', 'Owen', 'Sofia', 'Henry', 'Avery', 'Samuel',
    'Ella', 'Elijah', 'Madison', 'Daniel', 'Scarlett', 'Benjamin', 'Victoria',
    'Aria', 'Dylan', 'Grace', 'Michael', 'Chloe', 'Jayden', 'Penelope', 'Ryan',
]


def slugify(text):
    return re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', text.lower())).strip('-')


def random_author():
    return random.choice(FIRST_NAMES)


def make_review(name, tmpl):
    n = random.randint(2, 14)
    body = tmpl['body'].format(
        name=name,
        n=n,
        location=random.choice(LOCATIONS),
        quality=random.choice(QUALITIES),
        care_tip=random.choice(CARE_TIPS),
        level=random.choice(LEVELS),
        result=random.choice(RESULTS),
    )
    return tmpl['title'], body, tmpl['rating']


# ---------------------------------------------------------------------------
# Wikipedia image helpers
# ---------------------------------------------------------------------------
def wiki_image(title, width=500):
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


def commons_search(query, width=500):
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
        # Create or get category
        cat = Category.query.filter_by(slug='plants').first()
        if not cat:
            cat = Category(name='Plants & Garden', slug='plants', icon='🌿',
                           description='Discover and review plants for your home and garden.')
            db.session.add(cat)
            db.session.commit()
            print(f'Created category: {cat.name}')
        else:
            print(f'Category exists: {cat.name}')

        total_subjects = 0
        total_reviews = 0

        for subcat_name, subcat_slug, varieties in PLANT_DATA:
            sc = SubCategory.query.filter_by(category_id=cat.id, slug=subcat_slug).first()
            if sc:
                print(f'  Skipping {subcat_name} (exists)')
                continue

            sc = SubCategory(category_id=cat.id, name=subcat_name, slug=subcat_slug)
            db.session.add(sc)
            db.session.flush()

            # Download subcategory image
            print(f'\nCreated: {subcat_name}')
            img_url = fetch_image(subcat_name)
            if img_url:
                ext = img_url.split('.')[-1].split('?')[0].lower()
                if ext not in ('jpg', 'jpeg', 'png', 'webp', 'gif'):
                    ext = 'jpg'
                fname = f'plants-{subcat_slug}.{ext}'
                dest = os.path.join(STATIC_DIR, 'images', 'uploads', 'subcategories', fname)
                if download(img_url, dest):
                    sc.image_path = f'images/uploads/subcategories/{fname}'
                    print(f'  subcategory image saved')
            time.sleep(1)

            for variety in varieties:
                variety_slug = slugify(variety)
                subj_slug = f'{subcat_slug}-{variety_slug}'

                subj = Subject.query.filter_by(subcategory_id=sc.id, slug=subj_slug).first()
                if subj:
                    continue

                subj = Subject(subcategory_id=sc.id, name=variety, slug=subj_slug)
                db.session.add(subj)
                db.session.flush()

                # Download subject image
                img_url = fetch_image(variety)
                if img_url:
                    ext = img_url.split('.')[-1].split('?')[0].lower()
                    if ext not in ('jpg', 'jpeg', 'png', 'webp', 'gif'):
                        ext = 'jpg'
                    fname = f'plants-{subj_slug}.{ext}'
                    dest = os.path.join(STATIC_DIR, 'images', 'uploads', 'subjects', fname)
                    if download(img_url, dest):
                        subj.image_path = f'images/uploads/subjects/{fname}'
                        print(f'    img: {variety}')
                    else:
                        print(f'    no img: {variety}')
                else:
                    print(f'    no img: {variety}')
                time.sleep(0.8)

                # Add reviews
                target = random.randint(12, 35)
                used_titles = set()
                from datetime import datetime, timedelta
                reviews_added = 0
                shuffled = REVIEW_TEMPLATES[:]
                random.shuffle(shuffled)

                for tmpl in shuffled * 2:
                    if reviews_added >= target:
                        break
                    title, body, base_rating = make_review(variety, tmpl)
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

            db.session.commit()
            print(f'  committed {subcat_name}')

        print(f'\nDone. {total_subjects} subjects, {total_reviews} reviews.')


if __name__ == '__main__':
    main()
