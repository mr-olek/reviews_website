#!/usr/bin/env python3
"""Seed Sports category with 20 individual sports and reviews."""
import os, sys, random, time, requests, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Category, SubCategory, Subject, Review

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
SESSION = requests.Session()
SESSION.headers['User-Agent'] = 'Mozilla/5.0 (compatible; VerdictlyBot/1.0)'

# ---------------------------------------------------------------------------
# 20 sports: (Display Name, slug, Wikipedia article for image)
# ---------------------------------------------------------------------------
SPORTS = [
    ('Muay Thai',            'muay-thai',          'Muay Thai'),
    ('Brazilian Jiu-Jitsu',  'brazilian-jiu-jitsu','Brazilian jiu-jitsu'),
    ('Karate',               'karate',             'Karate'),
    ('Boxing',               'boxing',             'Boxing'),
    ('MMA',                  'mma',                'Mixed martial arts'),
    ('Judo',                 'judo',               'Judo'),
    ('Kickboxing',           'kickboxing',         'Kickboxing'),
    ('Wrestling',            'wrestling',          'Wrestling'),
    ('Taekwondo',            'taekwondo',          'Taekwondo'),
    ('Weightlifting',        'weightlifting',      'Olympic weightlifting'),
    ('Powerlifting',         'powerlifting',       'Powerlifting'),
    ('CrossFit',             'crossfit',           'CrossFit'),
    ('Bodybuilding',         'bodybuilding',       'Bodybuilding'),
    ('Rock Climbing',        'rock-climbing',      'Sport climbing'),
    ('Swimming',             'swimming',           'Swimming (sport)'),
    ('Running',              'running',            'Running'),
    ('Cycling',              'cycling',            'Cycling'),
    ('Tennis',               'tennis',             'Tennis'),
    ('Basketball',           'basketball',         'Basketball'),
    ('Yoga',                 'yoga',               'Yoga'),
]

# ---------------------------------------------------------------------------
# Review templates
# ---------------------------------------------------------------------------
REVIEW_TEMPLATES = [
    {
        'title': 'Life-changing experience',
        'body': "I've been training {name} for {n} months now and it has genuinely changed my life. My fitness, discipline, and confidence have all improved massively. The {benefit} alone makes it worth it. Can't recommend it enough to anyone at any {level} level.",
        'rating': 5,
    },
    {
        'title': 'Best fitness decision I ever made',
        'body': "Started {name} as a way to get fit and ended up completely hooked. The {benefit} is incredible and I've met some amazing people in the community. If you're on the fence, just try a beginner class — you'll be surprised.",
        'rating': 5,
    },
    {
        'title': 'Steep learning curve but worth it',
        'body': "{name} is not easy to pick up. The {challenge} kept me frustrated for the first {n} months. But once it clicks, it really clicks. Now I look forward to every session. Stick with it past the initial hurdle.",
        'rating': 4,
    },
    {
        'title': 'Great community, great workout',
        'body': "What surprised me most about {name} is the community. Everyone at my gym is supportive and encouraging. The workout itself delivers serious {benefit} results. I've trained for {n} months and progressed faster than I expected.",
        'rating': 5,
    },
    {
        'title': 'Gear costs add up fast',
        'body': "Love {name} but be aware that {gear} can get expensive. Once you're past the beginner phase you'll want quality equipment and it's not cheap. That said, the {benefit} you get makes it feel worthwhile in the long run.",
        'rating': 4,
    },
    {
        'title': 'Found my passion sport',
        'body': "I tried a lot of different activities before discovering {name}. Nothing else has stuck like this. After {n} months of consistent training I can see real improvement in my {benefit}. This is my sport now.",
        'rating': 5,
    },
    {
        'title': 'Good instructor makes all the difference',
        'body': "My first {name} coach was fine but not great. Switched gyms after {n} months and the new instructor completely transformed my understanding of the sport. If you're not progressing, try a different coach before quitting.",
        'rating': 4,
    },
    {
        'title': 'Excellent for mental health',
        'body': "{name} has done wonders for my mental health. The focus required during training means I completely forget about daily stresses. After a session I feel calm and clear-headed. The {benefit} is almost secondary at this point.",
        'rating': 5,
    },
    {
        'title': 'Competed for the first time',
        'body': "After {n} months of training I entered my first {name} competition. Didn't win but the experience was incredible. Competing gives you a totally different perspective on your training and highlights exactly where you need to improve.",
        'rating': 5,
    },
    {
        'title': 'Discipline carries into daily life',
        'body': "The discipline I've learned from {name} has improved every area of my life. Getting up early for training, sticking to a routine, pushing through {challenge} — it all translates. I'm more productive and focused in general.",
        'rating': 5,
    },
    {
        'title': 'Not for everyone',
        'body': "{name} requires a genuine commitment. The {challenge} is real and some people quit after a few weeks. If you go in expecting quick results you'll be disappointed. But if you embrace the process, the rewards are substantial.",
        'rating': 3,
    },
    {
        'title': 'Solid workout, slow progress',
        'body': "I enjoy {name} and the {benefit} is real, but progress feels slow at my {level} stage. I train three times a week and improvements are incremental. Maybe I need to train more, or maybe I just need more patience.",
        'rating': 3,
    },
    {
        'title': 'Great for overall fitness',
        'body': "I don't care about competing — I do {name} purely for fitness. After {n} months my strength, endurance, and flexibility are all significantly better. It's a full-body workout that keeps things interesting and engaging.",
        'rating': 5,
    },
    {
        'title': 'Struggled with the {challenge} at first',
        'body': "{name} looked straightforward when I watched videos online. In practice the {challenge} was much harder to grasp than expected. My coach was patient and I eventually got it, but expect it to take real time and repetition.",
        'rating': 4,
    },
    {
        'title': 'Amazing stress relief',
        'body': "After a stressful day at work I head to {name} training and everything resets. There's something about the intensity and focus it requires that clears the mind completely. Highly recommend it as a stress management tool.",
        'rating': 5,
    },
    {
        'title': 'Injury set me back',
        'body': "I was making great progress in {name} until a minor injury put me out for six weeks. Looking back I was probably training too hard, too soon. Take the time to learn proper technique first — it pays off in injury prevention.",
        'rating': 3,
    },
    {
        'title': 'Transformed my body in months',
        'body': "The physical transformation from {name} training has been dramatic. After {n} months of consistent training and eating well, I'm stronger and leaner than I've ever been. The {benefit} results speak for themselves.",
        'rating': 5,
    },
    {
        'title': 'Worth every penny',
        'body': "Yes, the {gear} and gym membership cost money, but what you get in return is extraordinary. The {benefit}, the skills, the community — {name} delivers real value. I've spent money on worse things with far less return.",
        'rating': 5,
    },
    {
        'title': 'Recommend for all ages',
        'body': "I started {name} at 45 and felt out of place at first. But the gym has people of all ages and the coach adjusts training to each person's level. It's never too late to start. The {benefit} has been real for me.",
        'rating': 5,
    },
    {
        'title': 'Keeps getting better',
        'body': "After {n} months of {name} I can say the sport keeps revealing new layers. Every time I think I've got a handle on it, there's more to learn. That depth keeps training fresh and engaging. Never bored, always improving.",
        'rating': 5,
    },
    {
        'title': 'Mixed feelings after a year',
        'body': "A year into {name} and I have mixed feelings. The {benefit} is real and I enjoy training, but the {challenge} is frustrating. I'm probably a {level} practitioner now but feel like I should be further along. Maybe that's just how it goes.",
        'rating': 3,
    },
    {
        'title': 'Perfect beginner sport',
        'body': "I was completely new to sport when I tried {name}. My gym had a beginner programme that made everything accessible. The coaches broke down the basics clearly and built up my confidence over {n} months. Great place to start.",
        'rating': 5,
    },
]

BENEFITS = [
    'cardiovascular fitness', 'strength gain', 'flexibility improvement',
    'coordination and balance', 'mental toughness', 'fat loss',
    'stress relief', 'body composition improvement', 'core strength',
]
CHALLENGES = [
    'technical footwork', 'proper breathing technique', 'timing and rhythm',
    'grip strength requirement', 'body mechanics', 'managing exhaustion',
    'learning to spar', 'maintaining correct form under fatigue',
]
GEAR_LIST = [
    'gloves and protective gear', 'proper shoes and clothing', 'equipment fees',
    'gym membership costs', 'competition entry fees', 'specialist equipment',
]
LEVELS = ['beginner', 'intermediate', 'intermediate-to-advanced', 'all-level']

FIRST_NAMES = [
    'Emma', 'Liam', 'Olivia', 'Noah', 'Ava', 'Ethan', 'Sophia', 'Mason',
    'Isabella', 'James', 'Mia', 'Logan', 'Charlotte', 'Lucas', 'Amelia',
    'Jackson', 'Harper', 'Aiden', 'Evelyn', 'Sebastian', 'Abigail', 'Mateo',
    'Emily', 'Jack', 'Elizabeth', 'Owen', 'Sofia', 'Henry', 'Avery', 'Samuel',
    'Ella', 'Elijah', 'Madison', 'Daniel', 'Scarlett', 'Benjamin', 'Victoria',
    'Aria', 'Dylan', 'Grace', 'Michael', 'Chloe', 'Jayden', 'Penelope', 'Ryan',
    'Marcus', 'Diana', 'Derek', 'Priya', 'Kenji', 'Fatima', 'Carlos', 'Ingrid',
]


def random_author():
    return random.choice(FIRST_NAMES)


def make_review(name, tmpl):
    n = random.randint(2, 18)
    title = tmpl['title'].format(name=name, challenge=random.choice(CHALLENGES))
    body = tmpl['body'].format(
        name=name,
        n=n,
        benefit=random.choice(BENEFITS),
        challenge=random.choice(CHALLENGES),
        gear=random.choice(GEAR_LIST),
        level=random.choice(LEVELS),
    )
    return title, body, tmpl['rating']


# ---------------------------------------------------------------------------
# Wikipedia image helpers (identical to add_plants.py)
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
        cat = Category.query.filter_by(slug='sports').first()
        if not cat:
            cat = Category(name='Sports', slug='sports', icon='🏅',
                           description='Discover and review individual sports and fitness disciplines.')
            db.session.add(cat)
            db.session.flush()
            print(f'Created category: {cat.name}')

            # Category image from Wikipedia "Sport" article
            img_url = wiki_image('Sport')
            if img_url:
                ext = img_url.split('.')[-1].split('?')[0].lower()
                if ext not in ('jpg', 'jpeg', 'png', 'webp', 'gif'):
                    ext = 'jpg'
                fname = f'sports-category.{ext}'
                dest = os.path.join(STATIC_DIR, 'images', 'uploads', 'categories', fname)
                if download(img_url, dest):
                    cat.image_path = f'images/uploads/categories/{fname}'
                    print(f'  category image saved')
            db.session.commit()
        else:
            print(f'Category exists: {cat.name}')

        # Create or get subcategory
        sc = SubCategory.query.filter_by(category_id=cat.id, slug='all-sports').first()
        if not sc:
            sc = SubCategory(category_id=cat.id, name='All Sports', slug='all-sports')
            db.session.add(sc)
            db.session.commit()
            print('Created subcategory: All Sports')
        else:
            print('Subcategory exists: All Sports')

        total_subjects = 0
        total_reviews = 0

        for sport_name, sport_slug, wiki_title in SPORTS:
            subj = Subject.query.filter_by(subcategory_id=sc.id, slug=sport_slug).first()
            if subj:
                print(f'  Skipping {sport_name} (exists)')
                continue

            subj = Subject(subcategory_id=sc.id, name=sport_name, slug=sport_slug)
            db.session.add(subj)
            db.session.flush()

            # Download subject image
            img_url = fetch_image(sport_name, wiki_title)
            if img_url:
                ext = img_url.split('.')[-1].split('?')[0].lower()
                if ext not in ('jpg', 'jpeg', 'png', 'webp', 'gif'):
                    ext = 'jpg'
                fname = f'sports-{sport_slug}.{ext}'
                dest = os.path.join(STATIC_DIR, 'images', 'uploads', 'subjects', fname)
                if download(img_url, dest):
                    subj.image_path = f'images/uploads/subjects/{fname}'
                    print(f'  img ok: {sport_name}')
                else:
                    print(f'  no img: {sport_name}')
            else:
                print(f'  no img: {sport_name}')
            time.sleep(0.8)

            # Add reviews
            from datetime import datetime, timedelta
            target = random.randint(12, 30)
            used_titles = set()
            reviews_added = 0
            shuffled = REVIEW_TEMPLATES[:]
            random.shuffle(shuffled)

            for tmpl in shuffled * 2:
                if reviews_added >= target:
                    break
                title, body, base_rating = make_review(sport_name, tmpl)
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
            print(f'  {sport_name}: {reviews_added} reviews')

        db.session.commit()
        print(f'\nDone. {total_subjects} subjects, {total_reviews} reviews.')


if __name__ == '__main__':
    main()
