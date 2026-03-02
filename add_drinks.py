#!/usr/bin/env python3
"""Seed Drinks category with Alcoholic and Non-Alcoholic subcategories."""
import os, sys, random, time, requests
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Category, SubCategory, Subject, Review

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
SESSION = requests.Session()
SESSION.headers['User-Agent'] = 'Mozilla/5.0 (compatible; VerdictlyBot/1.0)'

# ---------------------------------------------------------------------------
# Drinks: (Display Name, slug, Wikipedia article for image)
# ---------------------------------------------------------------------------
ALCOHOLIC = [
    ('Whiskey',        'whiskey',        'Whisky'),
    ('Red Wine',       'red-wine',       'Red wine'),
    ('Beer',           'beer',           'Beer'),
    ('Vodka',          'vodka',          'Vodka'),
    ('Gin',            'gin',            'Gin'),
    ('Rum',            'rum',            'Rum'),
    ('Tequila',        'tequila',        'Tequila'),
    ('Champagne',      'champagne',      'Champagne'),
    ('Craft Beer',     'craft-beer',     'Craft beer'),
    ('Sake',           'sake',           'Sake'),
    ('Mezcal',         'mezcal',         'Mezcal'),
    ('Bourbon',        'bourbon',        'Bourbon whiskey'),
    ('White Wine',     'white-wine',     'White wine'),
    ('Rosé Wine',      'rose-wine',      'Rosé'),
    ('Cognac',         'cognac',         'Cognac'),
    ('Absinthe',       'absinthe',       'Absinthe'),
    ('Cider',          'cider',          'Cider'),
    ('Port Wine',      'port-wine',      'Port wine'),
    ('Prosecco',       'prosecco',       'Prosecco'),
    ('Hard Seltzer',   'hard-seltzer',   'Hard seltzer'),
]

NON_ALCOHOLIC = [
    ('Coffee',         'coffee',         'Coffee'),
    ('Green Tea',      'green-tea',      'Green tea'),
    ('Espresso',       'espresso',       'Espresso'),
    ('Matcha',         'matcha',         'Matcha'),
    ('Orange Juice',   'orange-juice',   'Orange juice'),
    ('Lemonade',       'lemonade',       'Lemonade'),
    ('Sparkling Water','sparkling-water','Carbonated water'),
    ('Kombucha',       'kombucha',       'Kombucha'),
    ('Smoothie',       'smoothie',       'Smoothie'),
    ('Cold Brew',      'cold-brew',      'Cold brew coffee'),
    ('Chai Latte',     'chai-latte',     'Masala chai'),
    ('Coconut Water',  'coconut-water',  'Coconut water'),
    ('Herbal Tea',     'herbal-tea',     'Herbal tea'),
    ('Milkshake',      'milkshake',      'Milkshake'),
    ('Iced Tea',       'iced-tea',       'Iced tea'),
    ('Turmeric Latte', 'turmeric-latte', 'Turmeric latte'),
    ('Hot Chocolate',  'hot-chocolate',  'Hot chocolate'),
    ('Energy Drink',   'energy-drink',   'Energy drink'),
    ('Kefir',          'kefir',          'Kefir'),
    ('Ginger Beer',    'ginger-beer',    'Ginger beer'),
]

# ---------------------------------------------------------------------------
# Review templates
# ---------------------------------------------------------------------------
ALCOHOLIC_TEMPLATES = [
    {
        'title_tmpl': 'My go-to {name} — worth every penny',
        'body_tmpl': "I've been a {name} drinker for years and this category never gets old. The depth of flavour you get from a well-made {name} is genuinely hard to explain to someone who hasn't tried it. I tend to drink it {style} and find that's when it shows its best character.\n\nThe {note} is what sets a great {name} apart from a mediocre one. Once you start noticing it you can't stop. If you're new to {name}, start simple and take your time — there's a lot to discover.",
        'rating': 5,
    },
    {
        'title_tmpl': 'Converted to {name} after years of avoiding it',
        'body_tmpl': "I resisted {name} for a long time based on a bad early experience. Then a friend insisted I try a properly made version served {style} and everything changed. The {note} I'd missed the first time was suddenly the point.\n\nBeen drinking it regularly for about six months now and find myself actively seeking out interesting producers and styles. The rabbit hole is deep. Highly recommend giving it a second chance if your first experience was poor.",
        'rating': 5,
    },
    {
        'title_tmpl': 'Great for occasions, honest about the cost',
        'body_tmpl': "Quality {name} sits at the premium end of my drinks budget and that's fine — it's an occasion drink for me. Served {style} at the right moment it's hard to beat. The {note} on a well-chosen bottle is extraordinary.\n\nThat said, the price variation in this category is wild. You absolutely get what you pay for at the top end, but the sweet spot for everyday drinking is easier to find than the marketing suggests. Do your research before spending serious money.",
        'rating': 4,
    },
    {
        'title_tmpl': 'The perfect drink for a slow evening',
        'body_tmpl': "{name} has become my slow-evening ritual. Served {style}, no distractions, and you start to notice things — the {note}, the way it develops in the glass. It's a drink that rewards attention in a way most don't.\n\nI've introduced a few friends to proper {name} and the reaction is always the same: surprise that something they'd written off could be this interesting. Start with something accessible and work from there.",
        'rating': 5,
    },
    {
        'title_tmpl': 'Decent {name} — not life-changing but solid',
        'body_tmpl': "Tried this {name} on recommendation and it's a solid choice without being exceptional. Served {style} as suggested. The {note} is present but not as pronounced as in more premium examples.\n\nFor regular drinking it's good value. For a special occasion I'd go a step up. It's the kind of {name} you'd be happy to find at a bar but wouldn't specifically seek out to buy a bottle. Three and a half stars rounded to four.",
        'rating': 4,
    },
    {
        'title_tmpl': 'Overpriced for what it delivers',
        'body_tmpl': "I expected more from this {name} given the price point and the hype around the category. Served {style} as recommended. The {note} was underwhelming compared to bottles at half the price I've enjoyed.\n\nThe premium end of this market has a lot of marketing attached to it that doesn't translate to taste. I'm not saying all expensive {name} is overrated — I've had transcendent examples — but this particular tier didn't justify the spend for me.",
        'rating': 2,
    },
    {
        'title_tmpl': 'A gateway drink that opened a whole world',
        'body_tmpl': "My first serious {name} was a gift and it genuinely opened a new chapter in how I think about drinking. The complexity — especially the {note} — was unlike anything I'd experienced. Served {style} by the person who gave it, with an explanation of what I was tasting.\n\nThat experience sent me down a path of exploration that's still ongoing. There are entire regions, styles, and producers I haven't touched yet. The category rewards curiosity like few others.",
        'rating': 5,
    },
    {
        'title_tmpl': 'Perfect for cocktails, different story neat',
        'body_tmpl': "I use {name} primarily in cocktails and it excels in that role — the {note} comes through in a mixed drink in ways that complement rather than dominate. Served neat {style} it's fine but not where it shines for me personally.\n\nIf you're building a home bar, having a quality {name} is essential. Just think about whether you're buying it for mixing or sipping — the best choices for each aren't always the same bottle.",
        'rating': 4,
    },
]

NON_ALCOHOLIC_TEMPLATES = [
    {
        'title_tmpl': 'My daily ritual — {name} done properly',
        'body_tmpl': "I've made {name} part of my morning routine and it's transformed how I start the day. The key is the {detail} — that's the part most people rush and where the whole thing lives or dies. Prepared {style} it takes maybe five minutes and the result is worth every second.\n\nThe {benefit} is real and consistent. I've tried cutting it out for a week and immediately noticed the absence. Not in a dependency way — more like a quality-of-morning way. Genuinely recommend building the ritual around it.",
        'rating': 5,
    },
    {
        'title_tmpl': 'Converted to {name} — never going back',
        'body_tmpl': "I switched to {name} as part of a broader lifestyle change and it's been one of the easiest wins. The {benefit} was noticeable within a couple of weeks. Prepared {style} it's genuinely enjoyable, not just functional.\n\nThe {detail} matters more than you'd think — the difference between a mediocre and a great {name} comes down to sourcing and preparation. Once you find your method, the consistency is satisfying. Wouldn't swap it.",
        'rating': 5,
    },
    {
        'title_tmpl': 'Decent everyday drink, nothing transcendent',
        'body_tmpl': "I drink {name} most days and it does exactly what it needs to. Prepared {style} it's pleasant and the {benefit} is noticeable. The {detail} could be better — I've had more impressive versions elsewhere — but for a reliable daily drink it delivers.\n\nNot everything needs to be a revelation. This is a solid, dependable choice that fits into a routine without demanding too much attention. Four stars for exactly what it is.",
        'rating': 4,
    },
    {
        'title_tmpl': '{name} at its best — how to get there',
        'body_tmpl': "There's a big gap between bad {name} and great {name} and it's mostly about {detail}. Prepared {style} with care, the result is something genuinely special — the {benefit} is pronounced and the experience is noticeably better than the everyday version.\n\nI spent some time learning proper technique and it paid dividends immediately. Once you know what good looks like you can't go back to cutting corners. Worth the small investment in knowledge.",
        'rating': 5,
    },
    {
        'title_tmpl': 'Overhyped — good but not worth the obsession',
        'body_tmpl': "There's a lot of enthusiasm around {name} that I find slightly excessive. It's a good drink — prepared {style} it's genuinely pleasant and the {benefit} is real. But the {detail} that enthusiasts obsess over makes less difference to the final result than they suggest.\n\nI enjoy it regularly but don't feel the need to turn it into a hobby. Some drinks reward deep investment; for most people, a solid everyday approach to {name} delivers 90% of the benefit for 10% of the effort.",
        'rating': 3,
    },
    {
        'title_tmpl': 'Morning game-changer — {name} properly made',
        'body_tmpl': "I used to start the day badly. Switching to properly made {name} prepared {style} changed things in ways I didn't fully predict. The {benefit} is the obvious part. What I didn't expect was the ritual aspect — having something that requires a bit of attention and care sets the right tone for the morning.\n\nThe {detail} is where most people go wrong. Once you get that right everything else follows. Genuinely one of the better small habits I've built.",
        'rating': 5,
    },
    {
        'title_tmpl': 'Good cold, great warm — {name} across seasons',
        'body_tmpl': "I drink {name} year-round but the experience changes significantly with the seasons. In summer prepared {style} over ice it's refreshing and the {benefit} is immediate. In winter served warm the {detail} becomes more prominent and the comfort factor is high.\n\nVersatility is underrated in a drink. The fact that {name} works across contexts — morning, afternoon, social, solo — means it earns its place in any regular rotation. Gets better the more you learn about it.",
        'rating': 4,
    },
    {
        'title_tmpl': 'Didn\'t expect to love {name} this much',
        'body_tmpl': "I picked up {name} reluctantly — my doctor suggested it and I was sceptical. Prepared {style} the first time I thought it was fine but nothing special. By the second week I was actively looking forward to it.\n\nThe {benefit} is real. The {detail} surprised me — there's more going on in a well-prepared {name} than it appears. I now genuinely enjoy it rather than just tolerating it, which is better than I expected when I started.",
        'rating': 5,
    },
]

ALCOHOLIC_TEMPLATES += [
    {
        'title_tmpl': '{name} — {n} years in and still discovering new things',
        'body_tmpl': "After {n} years of drinking {name} I'm still finding bottles that surprise me. The category has more depth than it's given credit for by people who haven't explored it properly. Served {style} at its best, the {note} continues to evolve in interesting directions.\n\nMy advice to anyone starting out: don't get too attached to one producer or style early on. The range is the point.",
        'rating': 5,
    },
    {
        'title_tmpl': 'Brought a bottle of {name} to a dinner party — huge hit',
        'body_tmpl': "Took a bottle of {name} to a dinner party where nobody had thought much about it before. Served it {style} after the meal and it sparked a genuine conversation. The {note} did the work — once people noticed it they couldn't stop asking questions.\n\nThere's something satisfying about introducing people to a drink category properly. Three of the guests have since bought their own bottles.",
        'rating': 5,
    },
    {
        'title_tmpl': 'Tried {n} different {name} brands — here is what I found',
        'body_tmpl': "Over the past year I've tried {n} different expressions of {name}, ranging from entry-level to premium. My conclusion: the {note} is the most reliable indicator of quality across price points. Served {style}, the differences are pronounced and educational.\n\nThe best value wasn't the most expensive. There's a sweet spot in the middle range where quality and price align well. Happy to share specifics if anyone asks.",
        'rating': 4,
    },
    {
        'title_tmpl': 'Finally understand what the fuss about {name} is',
        'body_tmpl': "I spent years not getting {name}. Tried it a few times, found it fine, moved on. Then I had it served {style} by someone who knew what they were doing and the {note} landed differently. Something clicked.\n\nSince then I've been actively exploring the category and find it more rewarding than almost anything else in my drinks cabinet. The learning curve is real but so is the payoff on the other side.",
        'rating': 5,
    },
    {
        'title_tmpl': 'Honest {name} review from someone who drinks it weekly',
        'body_tmpl': "I drink {name} roughly once a week and have done for {n} years. Not a connoisseur, just someone who enjoys it consistently. Served {style} after work it provides a reliable wind-down that nothing else quite replicates. The {note} is comforting in its familiarity.\n\nI'm not here to persuade anyone. I just think more people would enjoy it if they approached it without preconceptions.",
        'rating': 4,
    },
    {
        'title_tmpl': 'The regional differences in {name} are fascinating',
        'body_tmpl': "One of the things I love about {name} is the regional variation. The same category produced in different parts of the world tastes completely different. The {note} shifts dramatically depending on origin, and served {style} those differences are most apparent.\n\nIf you've only tried one style, you've barely scratched the surface. The breadth is what makes it an endlessly interesting category.",
        'rating': 5,
    },
    {
        'title_tmpl': 'Not for everyone — but definitely for me',
        'body_tmpl': "{name} has a specific character that isn't universally appealing and I respect that. Some people find the {note} overwhelming. Served {style} it's at its most polarising — full flavour, no hiding.\n\nFor those it clicks with, the payoff is enormous. I'm firmly in that camp and have been for years. If you're on the fence, try it in the right setting with someone who drinks it well.",
        'rating': 4,
    },
    {
        'title_tmpl': 'Started drinking {name} at {n} — wish I had started sooner',
        'body_tmpl': "I came to {name} late — not until I was in my {n}s. Had assumed it wasn't for me based on nothing in particular. A partner's recommendation changed that. Tried it {style} and the {note} was immediately interesting rather than off-putting.\n\nSeveral years on and it's firmly part of how I drink. I don't know why I waited. The lesson is to try things properly before writing them off.",
        'rating': 5,
    },
    {
        'title_tmpl': '{name} in summer versus winter — two completely different drinks',
        'body_tmpl': "Something I've noticed with {name}: the season changes the experience significantly. In summer {style} it's lighter and more refreshing, the {note} sitting differently in warm weather. In winter the same drink served the same way feels richer and more substantial.\n\nI now think about {name} seasonally in a way I didn't used to. It's the same bottle but context transforms it. Worth being aware of if you've only tried it in one season.",
        'rating': 4,
    },
]

NON_ALCOHOLIC_TEMPLATES += [
    {
        'title_tmpl': '{name} has been part of my routine for {n} years',
        'body_tmpl': "I've been drinking {name} daily for {n} years now and it's as much a habit as a preference. Prepared {style} every morning, the {detail} takes maybe a minute of attention and the result is consistently good. The {benefit} has been a constant.\n\nSome habits you keep because you feel you should. This one I keep because I genuinely want to. That's the test.",
        'rating': 5,
    },
    {
        'title_tmpl': 'Switched from coffee to {name} — {n} months on',
        'body_tmpl': "I made the switch from my previous drink to {name} about {n} months ago. The transition was easier than I expected. Prepared {style}, the {detail} keeps it interesting and the {benefit} is noticeably different — better for me personally, though I know results vary.\n\nThe ritual aspect helps. Having something you prepare with a bit of attention does something for the start of a day that a quick grab-and-go doesn't.",
        'rating': 5,
    },
    {
        'title_tmpl': 'The difference between cheap and quality {name} is significant',
        'body_tmpl': "I used to drink whatever {name} was convenient and it was fine. Then I tried a properly sourced version prepared {style} and the gap was immediately obvious. The {detail} at the quality end is in another category. The {benefit} was also more pronounced.\n\nYou don't need to spend a fortune but you do need to care a bit. The bottom of the market in this category genuinely isn't good enough to make the habit worth keeping.",
        'rating': 4,
    },
    {
        'title_tmpl': 'Unexpected depth in {name} — took time to notice',
        'body_tmpl': "I drank {name} for months before I started noticing what was actually going on in it. Once I slowed down and paid attention — prepared {style} rather than rushing — the {detail} became something I actively appreciated. The {benefit} I'd been getting was just part of it.\n\nThere's a difference between drinking something and actually tasting it. {name} rewards the latter more than you'd expect from something so widely consumed.",
        'rating': 5,
    },
    {
        'title_tmpl': 'Made {name} from scratch — completely worth the effort',
        'body_tmpl': "Tried making {name} from scratch rather than buying it ready-made. The {detail} is more involved than the packaged version suggests but the result is genuinely better. Prepared {style} with properly sourced ingredients, the {benefit} is more pronounced and the whole experience is more satisfying.\n\nNot something I do every day — the effort doesn't always justify itself — but for special occasions or when you want to understand what you're drinking, highly worthwhile.",
        'rating': 5,
    },
    {
        'title_tmpl': 'Perfect afternoon drink — {name} done right',
        'body_tmpl': "I've moved {name} from morning to afternoon and it works better for me that way. Prepared {style} around 3pm, the {benefit} carries through the rest of the day rather than the morning. The {detail} I used to rush I now take more time with.\n\nSmall scheduling changes can change a drink entirely. Worth experimenting with when in the day you take something if you feel your relationship with it has gone stale.",
        'rating': 4,
    },
    {
        'title_tmpl': 'Introduced {name} to my whole family — now everyone drinks it',
        'body_tmpl': "I brought {name} to a family gathering as an experiment. Prepared it {style} for everyone with attention to {detail}. Reactions ranged from politely interested to genuinely converted. The {benefit} side of things sparked a separate conversation.\n\nThree family members now drink it regularly. That kind of quiet evangelism is the best recommendation I can give a drink — the kind that happens because people actually enjoyed it.",
        'rating': 5,
    },
    {
        'title_tmpl': '{name} is the most underrated drink in its category',
        'body_tmpl': "People overlook {name} in favour of trendier options and I find it baffling. Prepared {style} with care for {detail}, it delivers {benefit} that the alternatives often promise but underdeliver. It's not flashy but it's consistently excellent.\n\nSometimes the unassuming choice is the right choice. {name} has been a staple in various cultures for good reason and the modern wellness world is only now catching up to what people have known for generations.",
        'rating': 5,
    },
    {
        'title_tmpl': 'Tried {n} versions of {name} — significant quality range',
        'body_tmpl': "Out of curiosity I tried {n} different versions of {name} over a month, varying {detail} each time. The range was significant. Prepared {style} with care at the best end, the {benefit} was pronounced. At the worst end, genuinely mediocre.\n\nThe takeaway: the category isn't uniformly good. Getting to know what makes a version excellent versus average is worth the time. It made me a more intentional consumer rather than just grabbing whatever's available.",
        'rating': 4,
    },
]

ALCOHOLIC_STYLES = ['neat', 'on the rocks', 'with a splash of water', 'in a proper glass at room temperature', 'chilled', 'as a long drink with ice']
ALCOHOLIC_NOTES = ['finish', 'nose', 'complexity on the palate', 'balance between sweetness and bite', 'depth of flavour', 'smooth aftertaste', 'character']
ALCOHOLIC_AGES = [2, 3, 4, 5, 6, 7, 8, 10, 15, 20, 30, 40]

NON_ALCOHOLIC_STYLES = ['hot', 'over ice', 'in the morning', 'as an afternoon ritual', 'cold-brewed', 'traditionally']
NON_ALCOHOLIC_DETAILS = ['quality of the source', 'temperature of preparation', 'brewing time', 'ratio of ingredients', 'freshness of the base ingredient']
NON_ALCOHOLIC_BENEFITS = ['energy without the crash', 'mental clarity', 'sustained focus', 'digestive benefit', 'calm alertness', 'hydration', 'morning clarity']

FIRST_NAMES = [
    'Sarah', 'James', 'Olivia', 'Liam', 'Emma', 'Noah', 'Ava', 'Ethan',
    'Sophia', 'Mason', 'Isabella', 'Logan', 'Charlotte', 'Lucas', 'Amelia',
    'Jackson', 'Mia', 'Aiden', 'Harper', 'Sebastian', 'Emily', 'Jack',
    'Elizabeth', 'Owen', 'Sofia', 'Henry', 'Avery', 'Samuel', 'Ella',
    'Daniel', 'Scarlett', 'Benjamin', 'Victoria', 'Aria', 'Dylan', 'Grace',
    'Michael', 'Chloe', 'Ryan', 'Marcus', 'Diana', 'Priya', 'Kenji',
    'Fatima', 'Carlos', 'Ingrid', 'Takashi', 'Miriam', 'Stefan', 'Leila',
]


def make_alcoholic_review(name, tmpl):
    n = random.choice(ALCOHOLIC_AGES)
    body = tmpl['body_tmpl'].format(
        name=name, n=n,
        style=random.choice(ALCOHOLIC_STYLES),
        note=random.choice(ALCOHOLIC_NOTES),
    )
    title = tmpl['title_tmpl'].format(name=name, n=n)
    rating = max(1, min(5, tmpl['rating'] + random.choice([-1, 0, 0, 0, 1])))
    return title, body, rating


def make_nonalcoholic_review(name, tmpl):
    n = random.randint(2, 12)
    body = tmpl['body_tmpl'].format(
        name=name, n=n,
        style=random.choice(NON_ALCOHOLIC_STYLES),
        detail=random.choice(NON_ALCOHOLIC_DETAILS),
        benefit=random.choice(NON_ALCOHOLIC_BENEFITS),
    )
    title = tmpl['title_tmpl'].format(name=name, n=n)
    rating = max(1, min(5, tmpl['rating'] + random.choice([-1, 0, 0, 0, 1])))
    return title, body, rating


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


def add_reviews(subj, templates, make_fn):
    from datetime import datetime, timedelta
    Review.query.filter_by(subject_id=subj.id, source_site='sample').delete()
    db.session.commit()
    target = random.randint(12, 25)
    used_titles: set = set()
    reviews_added = 0
    shuffled = templates[:]
    random.shuffle(shuffled)
    pool = (shuffled * ((target // len(shuffled)) + 2))[:target * 2]

    for tmpl in pool:
        if reviews_added >= target:
            break
        title, body, rating = make_fn(subj.name, tmpl)
        if title in used_titles:
            continue
        used_titles.add(title)
        days_ago = random.randint(30, 365 * 3)
        rev = Review(
            subject_id=subj.id,
            title=title,
            body=body,
            rating=rating,
            author_name=random.choice(FIRST_NAMES),
            source_site='sample',
            original_date=datetime.utcnow() - timedelta(days=days_ago),
            is_published=True,
        )
        db.session.add(rev)
        reviews_added += 1
    return reviews_added


def seed_subcategory(cat, sc_name, sc_slug, drinks, templates, make_fn):
    sc = SubCategory.query.filter_by(category_id=cat.id, slug=sc_slug).first()
    if not sc:
        sc = SubCategory(category_id=cat.id, name=sc_name, slug=sc_slug)
        db.session.add(sc)
        db.session.flush()
        print(f'Created subcategory: {sc_name}')

        # Subcategory image
        wiki_key = 'Alcoholic drink' if 'alcoholic' in sc_slug and 'non' not in sc_slug else 'Non-alcoholic drink'
        img_url = wiki_image(wiki_key)
        if img_url:
            ext = img_url.split('.')[-1].split('?')[0].lower()
            if ext not in ('jpg', 'jpeg', 'png', 'webp', 'gif'):
                ext = 'jpg'
            fname = f'drinks-{sc_slug}.{ext}'
            dest = os.path.join(STATIC_DIR, 'images', 'uploads', 'subcategories', fname)
            if download(img_url, dest):
                sc.image_path = f'images/uploads/subcategories/{fname}'
                print(f'  subcategory image saved')
        db.session.commit()
    else:
        print(f'Subcategory exists: {sc_name}')

    total_subjects = 0
    total_reviews = 0

    for drink_name, drink_slug, wiki_title in drinks:
        subj = Subject.query.filter_by(subcategory_id=sc.id, slug=drink_slug).first()
        existing = subj is not None
        if not subj:
            subj = Subject(subcategory_id=sc.id, name=drink_name, slug=drink_slug)
        if not existing:
            db.session.add(subj)
        db.session.flush()

        img_url = wiki_image(wiki_title) if not existing else None
        if img_url:
            ext = img_url.split('.')[-1].split('?')[0].lower()
            if ext not in ('jpg', 'jpeg', 'png', 'webp', 'gif'):
                ext = 'jpg'
            fname = f'drinks-{drink_slug}.{ext}'
            dest = os.path.join(STATIC_DIR, 'images', 'uploads', 'subjects', fname)
            if download(img_url, dest):
                subj.image_path = f'images/uploads/subjects/{fname}'
                print(f'  img ok: {drink_name}')
            else:
                print(f'  no img: {drink_name}')
            time.sleep(0.8)

        n = add_reviews(subj, templates, make_fn)
        subj.update_stats()
        total_subjects += 1
        total_reviews += n
        print(f'  {drink_name}: {n} reviews')

    db.session.commit()
    return total_subjects, total_reviews


def main():
    app = create_app()
    with app.app_context():
        cat = Category.query.filter_by(slug='drinks').first()
        if not cat:
            cat = Category(name='Drinks', slug='drinks', icon='🥤',
                           description='Discover and review drinks from around the world.')
            db.session.add(cat)
            db.session.flush()
            print(f'Created category: {cat.name}')

            img_url = wiki_image('Drink')
            if not img_url:
                img_url = wiki_image('Beverage')
            if img_url:
                ext = img_url.split('.')[-1].split('?')[0].lower()
                if ext not in ('jpg', 'jpeg', 'png', 'webp', 'gif'):
                    ext = 'jpg'
                fname = f'drinks-category.{ext}'
                dest = os.path.join(STATIC_DIR, 'images', 'uploads', 'categories', fname)
                if download(img_url, dest):
                    cat.image_path = f'images/uploads/categories/{fname}'
                    print('  category image saved')
            db.session.commit()
        else:
            print(f'Category exists: {cat.name}')

        ts, tr = seed_subcategory(cat, 'Alcoholic', 'alcoholic', ALCOHOLIC,
                                  ALCOHOLIC_TEMPLATES, make_alcoholic_review)
        ts2, tr2 = seed_subcategory(cat, 'Non-Alcoholic', 'non-alcoholic', NON_ALCOHOLIC,
                                    NON_ALCOHOLIC_TEMPLATES, make_nonalcoholic_review)

        print(f'\nDone. {ts + ts2} drinks, {tr + tr2} reviews.')


if __name__ == '__main__':
    main()
