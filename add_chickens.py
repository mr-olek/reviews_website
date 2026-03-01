"""
Add a Chickens subcategory to Animals with 4 breeds, reviews, and images.
Safe to run multiple times — skips existing records.

Usage:
  python3 add_chickens.py
"""
from __future__ import annotations

import logging
import os
import random
import re
import time

import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

SESSION = requests.Session()
SESSION.headers.update({
    'User-Agent': 'Mozilla/5.0 (compatible; PetReviewsBot/1.0; educational)'
})

_ADJECTIVES = [
    'Clucky', 'Broody', 'Fluffy', 'Pecky', 'Feisty', 'Happy', 'Sunny',
    'Dusty', 'Cozy', 'Bossy', 'Rowdy', 'Sassy', 'Plump', 'Cheeky', 'Bold',
]
_ANIMALS = [
    'Cluck', 'Hen', 'Coop', 'Roost', 'Scratch', 'Peck', 'Egg', 'Flap',
    'Perch', 'Feather', 'Wattle', 'Comb', 'Grain', 'Yolk', 'Nest',
]


def _rnd_name(rng: random.Random) -> str:
    return f"{rng.choice(_ADJECTIVES)}{rng.choice(_ANIMALS)}{rng.randint(10, 99)}"


CHICKEN_DATA: dict[str, dict] = {
    'Orpington': {
        'slug': 'orpington',
        'wiki_title': 'Orpington chicken',
        'description': (
            'The Orpington is a large, fluffy English breed developed in the 1880s in Orpington, Kent. '
            'Available in buff, black, blue, and white varieties, they are prized for their exceptionally '
            'calm and docile temperament, generous egg-laying, and tendency to go broody. '
            'One of the most beloved backyard chicken breeds in the world.'
        ),
        'pros': [
            'Exceptionally docile and friendly — ideal for children and beginners',
            'Good layers of large brown eggs (3–5 per week)',
            'Tolerant of cold weather due to fluffy, dense feathering',
            'Naturally broody — good for hatching eggs',
            'Calm and easy to handle — won\'t fly over fences',
        ],
        'cons': [
            'Dense feathering can hide external parasites — check regularly',
            'Tend to become overweight without controlled feeding',
            'Fluffy feathering gets muddy in wet conditions',
            'Broodiness reduces egg production when it occurs',
        ],
        'reviews': [
            (5, 'Best backyard chicken breed, full stop', 'I\'ve kept a dozen different chicken breeds over eight years of backyard keeping, and Buff Orpingtons are simply the best all-rounder. Calm enough for my children to pick up without drama, reliably laying large brown eggs, and gorgeous to look at — their warm buff plumage glows in the afternoon light. My girls come running when they see me and will sit on my lap for a stroke. Brilliant birds.'),
            (5, 'My toddler\'s best friends', 'Our three Buff Orpingtons are the gentlest chickens imaginable. My three-year-old walks amongst them daily and they tolerate her curiosity with serene patience. They\'ve never pecked her, never flapped at her, and seem genuinely relaxed with children. The eggs are enormous and a beautiful deep brown. For families with young children wanting backyard chickens, Orpingtons are the obvious choice.'),
            (4, 'Lovely layers who enjoy a cuddle', 'My Orpingtons lay reliably through autumn and winter — something not all breeds manage. They slow down in the shortest days but maintain production better than my Leghorns ever did. More importantly, they\'re extraordinarily friendly. Two of mine fly up onto my arm when I enter the run and one has taken to sitting on my shoulder while I do coop maintenance. Lovely, personable birds with genuine individual characters.'),
            (5, 'Gorgeous, calm, and productive', 'Buff Orpingtons look like living clouds — big, fluffy, warm-golden birds that move around the garden with great dignity. Three of mine provide 4–5 eggs per week between them consistently. They free range happily, never destroy the garden aggressively, and don\'t attempt to fly over our low picket fence. For a low-drama, productive backyard flock, they\'re ideal. My neighbours were initially sceptical about chickens and are now completely won over by their charm.'),
            (4, 'Watch for weight gain', 'Orpingtons love their food and will overeat if given unlimited access to high-calorie feed. Two of my original three became quite round and one developed mobility issues as a result. I now use a measured pellet ration supplemented with fresh greens and their weight and health improved dramatically. They\'re still round and fluffy looking — that\'s the breed — but properly fed they move freely and lay well. Monitor body condition carefully.'),
            (5, 'Perfect broody hens for hatching', 'My Orpington hen Doris has successfully raised three batches of chicks in two years. She\'s the most devoted, determined broody hen — she sits through everything and raises her chicks with fierce protectiveness. Orpingtons\' natural broodiness makes them ideal if you want to hatch eggs and have a hen do all the work. Doris has raised more chicks than my incubator and does a far better job.'),
            (3, 'Heavy feathering in mud is challenging', 'Orpingtons are beautiful, but in a wet British winter their fluffy leg and body feathering becomes a muddy maintenance challenge. After heavy rain their plumage is sodden and they look sorry for themselves. I\'ve improved their run with hardstanding and raised sheltered areas which has helped significantly. They\'re worth the management, but prospective owners in wet climates should plan for mud management before getting Orpingtons.'),
            (4, 'Black Orpingtons are spectacular', 'My Black Orpingtons have beetle-green iridescent plumage in sunlight that is genuinely stunning. They\'re slightly more independent than Buffs in my experience but equally calm and friendly when socialised from chicks. They lay slightly less than Buffs but the eggs are the same beautiful brown. If you want the docile Orpington temperament in a more dramatic colour, the Black variety is exceptional.'),
            (5, 'Eight years and still my favourite breed', 'I\'ve kept Orpingtons continuously for eight years and they remain my favourite backyard breed. I\'ve tried Rhode Island Reds (productive but pushy), Silkies (beautiful but lower layers), and various hybrids (excellent layers but less character). Nothing matches the Orpington combination of docility, productivity, beauty, and personality. My current flock of five hens provides more eggs than my family can eat and endless entertainment in the garden.'),
        ],
    },
    'Silkie': {
        'slug': 'silkie',
        'wiki_title': 'Silkie',
        'description': (
            'The Silkie is one of the most distinctive chicken breeds in the world, '
            'with uniquely soft, silk-like plumage lacking barbicels (the hooks that hold normal feathers together), '
            'giving them a fluffy, fur-like appearance. They also have black skin and bones, blue earlobes, '
            'and five toes instead of the usual four. Silkies are famously docile and strongly broody, '
            'making them beloved backyard pets and surrogate mothers for other breeds\' eggs.'
        ),
        'pros': [
            'Extraordinarily gentle and docile — excellent pet chickens',
            'Beautiful, unique appearance — endlessly admired by visitors',
            'Outstanding broody mothers — will hatch almost any egg',
            'Friendly with children and easy to handle',
            'Available in a wide range of colours',
        ],
        'cons': [
            'Crest feathering can impair vision — check regularly for mites in the crest',
            'Lower egg production than most breeds (2–3 small eggs per week)',
            'Cannot fly to escape predators — need very secure housing',
            'Feathered feet get muddy and damp easily',
        ],
        'reviews': [
            (5, 'Not a chicken — a fluffy cloud with feet', 'The first time someone visits our garden and sees our Silkies, they genuinely don\'t know what they\'re looking at. The silk-like plumage, the crest, the feathered feet — they look like something from a fantasy story. Our four Silkies are the calmest, sweetest animals on the property. The children carry them around like stuffed toys (with our supervision) and they accept it with tranquil dignity. Extraordinary birds.'),
            (5, 'Best broody hens in existence', 'If you want eggs hatched and chicks raised without an incubator, get a Silkie. My hen Minerva has raised four clutches of chicks in three years, including duck eggs and guinea fowl eggs. She sits with monastic dedication for 21 days, raises her chicks with fierce protectiveness, and is back on a nest within weeks. No incubator matches the success rate or the care quality of a committed Silkie broody. They\'re extraordinary surrogate mothers.'),
            (4, 'Lower egg production — know what you\'re getting', 'Silkies are not production layers. My three Silkies average 2 small white/cream eggs per hen per week, which drops further when broody (which is often). They\'re kept as much for their personality and ornamental value as for eggs. If you want maximum egg production, choose a different breed. If you want delightful, handleable, beautiful birds that happen to also lay some eggs, Silkies are wonderful.'),
            (5, 'Children are obsessed with them', 'Our Silkies have converted every child who\'s visited from a chicken sceptic to a devoted fan. They\'re so peculiar-looking and so docile that children who would normally be cautious around birds confidently pick them up and stroke them. Our hen Duchess has been carried by children aged 3 to 13 and never objected. They\'re the ideal first chicken for families and a wonderful way to introduce children to animal husbandry.'),
            (4, 'Crest management needed', 'Silkies with full crests need their vision checked regularly. My hen Beatrice had her crest grow over her eyes in summer and became anxious and flighty as a result — a dramatic change from her usual calm. A gentle trim of the crest feathers around the eyes restored her vision and her personality immediately returned to normal. Check their vision regularly and trim the crest feathers when needed. It takes two minutes and makes a huge difference.'),
            (5, 'Most characterful backyard birds I\'ve kept', 'Five years of Silkie keeping and they remain my favourite flock. Each hen has a distinct personality — Duchess is the bold leader, Pearl is timid but curious, Minerva is perpetually broody and maternal. They interact with each other in ways that are fascinating to observe. They come to greet me every morning, follow me around the garden, and have been caught (on camera) watching TV through the patio door. Endlessly entertaining.'),
            (3, 'Secure housing is essential', 'Silkies cannot fly and their crest feathering limits their peripheral vision — both factors that make them extremely vulnerable to predators. We lost a Silkie to a fox who dug under a run we thought was secure. Since reinforcing with an apron of wire mesh around the entire perimeter and hardware cloth instead of chicken wire, we\'ve had no more losses. Please invest properly in Silkie housing security — their inability to escape makes thorough predator-proofing non-negotiable.'),
            (4, 'Feathered feet need attention in mud', 'The feathered feet of Silkies get very muddy in wet conditions and can develop bumblefoot (a staph infection) if the feet are consistently wet and soiled. I\'ve laid hardstanding and covered areas in their run which has eliminated this problem. Regular foot checks for early signs of swelling or injury are important with feather-footed breeds. With proper housing and management, Silkies are healthy and hardy.'),
        ],
    },
    'Rhode Island Red': {
        'slug': 'rhode-island-red',
        'wiki_title': 'Rhode Island Red',
        'description': (
            'The Rhode Island Red is one of America\'s most successful dual-purpose chicken breeds, '
            'developed in the late 19th century in Rhode Island. '
            'Known for their deep, rich mahogany-red plumage, they are exceptionally productive layers '
            'of large brown eggs, remarkably hardy and disease-resistant, and adaptable to virtually any climate. '
            'The backbone of backyard flocks worldwide.'
        ),
        'pros': [
            'Outstanding egg production — 250–300 large brown eggs per year',
            'Extremely hardy and disease-resistant',
            'Adaptable to any climate — handles cold and heat well',
            'Forages efficiently — reduces feed costs',
            'Long productive laying period',
        ],
        'cons': [
            'Can be assertive and dominant with other breeds in mixed flocks',
            'Roosters can be aggressive — require careful management',
            'Less docile than Orpingtons or Silkies — not ideal lap chickens',
            'Can be persistent diggers — may damage garden beds',
        ],
        'reviews': [
            (5, 'The ultimate backyard egg machine', 'My four Rhode Island Reds lay so reliably that I\'ve never bought eggs since acquiring them three years ago and give away dozens weekly to neighbours. Even through last winter\'s dark months they maintained one egg per hen every day or two. The eggs are large, with deep orange yolks from their enthusiastic foraging. For anyone who wants genuine, consistent egg production from backyard chickens, RIRs are unmatched.'),
            (5, 'Hardy as iron, productive as a factory', 'Rhode Island Reds have an almost legendary reputation for hardiness and it\'s completely deserved. My flock has sailed through an extremely cold winter, a hot summer, and conditions that left softer breeds struggling. No significant health issues in five years beyond routine worming. They forage aggressively, eat efficiently, and convert that into eggs at a remarkable rate. The backbone of a practical backyard flock.'),
            (4, 'Confident birds, not cuddly', 'Rhode Island Reds are confident, assertive birds rather than lap chickens. My girls are friendly with me — they follow me around and eat from my hand — but they won\'t be picked up willingly and won\'t be carried around by children. They\'re practical, efficient birds rather than pets in the Silkie or Orpington sense. If you want egg production above all else, they\'re exceptional. If you want a cuddly bird, look elsewhere.'),
            (5, 'The breed that converted me to chicken keeping', 'My first three chickens were Rhode Island Reds and they\'ve made me a committed backyard keeper for eight years. The reliable eggs, the vigorous health, the active foraging personality — everything about them is honest and dependable. They don\'t have the fluffy charm of Silkies but they have something arguably more valuable: consistent, genuine productivity and durability. They\'ve never let me down.'),
            (4, 'Dominant in mixed flocks — plan your flock carefully', 'Rhode Island Reds are confident and can bully gentler breeds in a mixed flock. I made the mistake of adding Silkies to an established RIR flock and the Silkies were persistently picked on. Separating them or choosing breeds of similar confidence is important. Within a pure RIR flock there\'s a clear pecking order that\'s established quickly and maintained with minimal drama. Just be careful with mixed-breed introductions.'),
            (3, 'Roosters need careful management', 'I kept a Rhode Island Red rooster for a year and he required consistent management to remain approachable. RIR roosters have a reputation for aggression and mine lived up to it — he charged at people (though never the hens\' owners who handled him from day one). He was beautiful and the flock benefited from his protection, but I had to rehome him when our toddler started toddling. If you want a rooster, research cockerel management thoroughly first.'),
            (5, 'Deep mahogany plumage is beautiful', 'Beyond their productivity, Rhode Island Reds are genuinely beautiful birds. The deep mahogany-red plumage with black tail feathers in direct sunlight is stunning — they look like polished mahogany furniture with feathers. In the garden against green grass they\'re a wonderful visual addition. Productive, hardy, and good-looking — the complete backyard chicken.'),
            (4, 'Best foragers in my flock', 'My Rhode Island Reds are by far the best foragers of my mixed flock. They cover the entire garden systematically, consume enormous quantities of insects and greens, and their yolks are deeper orange than any other breed I keep as a result. Free-ranging RIRs produce exceptional eggs and are very economical to keep when they can forage freely. Their activity and enthusiasm for self-feeding makes them the most cost-effective backyard layer I\'ve found.'),
            (5, 'Six years, barely a sick day', 'My Rhode Island Red flock has been with me for six years and the health record is extraordinary. No significant disease issues, no leg problems, no respiratory infections. Routine worming and annual vet checks are all they\'ve needed. The hardiness bred into this dual-purpose American breed is genuinely remarkable. For anyone wanting a low-maintenance, productive backyard flock, Rhode Island Reds are the gold standard.'),
        ],
    },
    'Plymouth Rock': {
        'slug': 'plymouth-rock',
        'wiki_title': 'Plymouth Rock chicken',
        'description': (
            'The Plymouth Rock (commonly called Barred Rock in the barred variety) is a classic American dual-purpose breed '
            'developed in New England in the mid-19th century. '
            'The barred variety — with its distinctive black-and-white striped plumage — is the most widely kept. '
            'Plymouth Rocks are reliable layers of large brown eggs, calm and friendly in temperament, '
            'and excellent foragers, making them one of the most popular backyard chicken breeds in North America.'
        ),
        'pros': [
            'Friendly and calm temperament — more docile than Rhode Island Reds',
            'Good egg production — 200–280 large brown eggs per year',
            'Hardy and adaptable to cold climates',
            'The distinctive barred plumage is visually striking',
            'Dual-purpose breed with good body size',
        ],
        'cons': [
            'Can be assertive in mixed flocks with gentler breeds',
            'Not as prolific as production-bred hybrids',
            'May develop broodiness which reduces laying',
            'Active foragers — need space or strong fencing for gardens',
        ],
        'reviews': [
            (5, 'The perfect backyard chicken', 'Barred Plymouth Rocks are my favourite backyard breed after trying many others. They hit every mark: friendly enough to be genuine pets, productive enough to supply my family with eggs, hardy enough to handle a New England winter, and beautiful enough that visitors admire them. The black-and-white barred pattern is distinctive and handsome. I recommend them universally to anyone starting a backyard flock.'),
            (5, 'Friendlier than Rhode Island Reds, more productive than Silkies', 'I\'ve kept Plymouth Rocks for five years as my compromise between egg production and pet-ability. They\'re friendlier and more handleable than my Rhode Island Reds but lay significantly more eggs than my Silkies. They meet me at the coop door, eat from my hand, and tolerate being picked up reasonably well. The ideal middle ground for a backyard keeper who wants both utility and personality.'),
            (4, 'Reliable layers through winter', 'My Barred Rocks are much more consistent winter layers than many of my other breeds. When my Leghorns and Silkies slow to a trickle in the shortest days, my Rocks maintain respectable production. They seem genuinely cold-hardy and less affected by short day length than I expected. Supplementary lighting in the coop helps, but even without it they outperform most breeds through the dark months.'),
            (5, 'Beautiful black-and-white plumage', 'The barred plumage of Plymouth Rocks is one of the most elegant and distinctive patterns in poultry. The precise black-and-white barring creates a wonderful optical effect in sunlight. In the garden against green grass they\'re a striking sight. My flock of five Barred Rocks gets more compliments from visiting non-chicken people than any other breed I\'ve kept. Productive, friendly, and genuinely attractive birds.'),
            (4, 'Great for children — tolerant and calm', 'My children (aged 7 and 10) handle our Barred Rocks confidently and the hens tolerate it remarkably well. They don\'t love being picked up, but they accept it without panicking. The children collect eggs daily and have learned to interpret the hens\' behaviours — crouch means don\'t approach, relaxed means you can stroke. Plymouth Rocks\' calm nature makes them a good choice for a family flock where children are involved in daily care.'),
            (3, 'Active foragers can be hard on gardens', 'My Barred Rocks are enthusiastic foragers which is wonderful for their health and egg quality, but hard on my vegetable garden. They bulldoze through anything not protected by wire. I\'ve had to net all my raised beds and they routinely scratch up areas I haven\'t protected. They\'re doing what chickens do — just be prepared to fence off anything you want to keep. Free range Rocks are wonderful, but they\'re thorough in their scratching.'),
            (5, 'Heritage breed with real character', 'There\'s something satisfying about keeping a heritage breed with genuine history. Plymouth Rocks were developed in New England in the 1860s and became the most popular farm chicken in America by the early 20th century. My Barred Rocks feel connected to that tradition — honest, productive, adaptable farm birds. They\'re not the most productive modern hybrid, but they have character, beauty, and hardiness that production breeds can\'t match.'),
            (4, 'Excellent first-time keeper birds', 'I chose Barred Plymouth Rocks for my first backyard flock on the advice of an experienced keeper and it was excellent guidance. They\'re forgiving of beginner mistakes in coop management, hardy enough to tolerate minor husbandry errors while you\'re learning, friendly enough that they become genuine pets, and productive enough to keep you supplied with eggs. Two years in I\'ve added other breeds, but my original Rocks are still my favourites.'),
            (5, 'Four years of consistent excellent performance', 'My Barred Rock flock is four years old now and still laying well — slightly fewer eggs than year one, as expected, but consistent and reliable. Their health has been excellent with no significant illness or injury. They free range in the afternoons and have been brilliant about returning to the coop at dusk without encouragement. Easy to keep, easy to manage, genuinely enjoyable birds every single day.'),
        ],
    },
}


def get_wiki_image(title: str, size: int = 500) -> str | None:
    params = {
        'action': 'query', 'titles': title, 'prop': 'pageimages',
        'pithumbsize': size, 'format': 'json',
    }
    try:
        resp = SESSION.get('https://en.wikipedia.org/w/api.php', params=params, timeout=15)
        if resp.status_code == 429:
            logger.warning('Wikipedia 429, sleeping 5s...')
            time.sleep(5)
            resp = SESSION.get('https://en.wikipedia.org/w/api.php', params=params, timeout=15)
        for page in resp.json().get('query', {}).get('pages', {}).values():
            src = page.get('thumbnail', {}).get('source')
            if src:
                return re.sub(r'/\d+px-', f'/{size}px-', src)
    except Exception as e:
        logger.warning(f'Wiki API error for {title!r}: {e}')
    return None


def try_commons_image(query: str, size: int = 500) -> str | None:
    try:
        resp = SESSION.get('https://commons.wikimedia.org/w/api.php', params={
            'action': 'query', 'list': 'search', 'srsearch': query,
            'srnamespace': 6, 'srlimit': 5, 'format': 'json',
        }, timeout=15)
        if resp.status_code == 429:
            time.sleep(5)
            resp = SESSION.get('https://commons.wikimedia.org/w/api.php', params={
                'action': 'query', 'list': 'search', 'srsearch': query,
                'srnamespace': 6, 'srlimit': 5, 'format': 'json',
            }, timeout=15)
        for result in resp.json().get('query', {}).get('search', []):
            title = result.get('title', '')
            if not title.startswith('File:'):
                continue
            ext = title.rsplit('.', 1)[-1].lower()
            if ext not in ('jpg', 'jpeg', 'png', 'webp'):
                continue
            info = SESSION.get('https://commons.wikimedia.org/w/api.php', params={
                'action': 'query', 'titles': title, 'prop': 'imageinfo',
                'iiprop': 'url', 'iiurlwidth': size, 'format': 'json',
            }, timeout=15).json()
            for page in info.get('query', {}).get('pages', {}).values():
                infos = page.get('imageinfo', [])
                if infos:
                    return infos[0].get('thumburl') or infos[0].get('url')
    except Exception as e:
        logger.warning(f'Commons error for {query!r}: {e}')
    return None


def download_image(url: str, dest_path: str) -> bool:
    try:
        resp = SESSION.get(url, timeout=20)
        if resp.status_code == 429:
            logger.warning('429 rate limit, sleeping 5s...')
            time.sleep(5)
            resp = SESSION.get(url, timeout=20)
        if resp.status_code != 200:
            logger.warning(f'HTTP {resp.status_code} for {url}')
            return False
        content = resp.content
        if len(content) < 5000:
            logger.warning(f'Image too small ({len(content)} bytes)')
            return False
        with open(dest_path, 'wb') as f:
            f.write(content)
        return True
    except Exception as e:
        logger.warning(f'Download error: {e}')
        return False


def main() -> None:
    from app import create_app, db
    from app.models import Category, SubCategory, Subject, Review

    app = create_app('development')
    upload_dir = os.path.join('static', 'images', 'uploads', 'subjects')
    defaults_dir = os.path.join('static', 'images', 'defaults')
    os.makedirs(upload_dir, exist_ok=True)
    os.makedirs(defaults_dir, exist_ok=True)

    with app.app_context():
        animals_cat = Category.query.filter_by(slug='animals').first()
        if not animals_cat:
            logger.error("Animals category not found — run seed.py first.")
            return

        sub = SubCategory.query.filter_by(category_id=animals_cat.id, slug='chickens').first()
        if not sub:
            sub = SubCategory(category_id=animals_cat.id, name='Chickens', slug='chickens')
            db.session.add(sub)
            db.session.flush()
            logger.info("Created Chickens subcategory")
        else:
            logger.info("Chickens subcategory already exists")

        total_reviews = 0
        for name, data in CHICKEN_DATA.items():
            slug = data['slug']
            subj = Subject.query.filter_by(subcategory_id=sub.id, slug=slug).first()
            if not subj:
                subj = Subject(subcategory_id=sub.id, name=name, slug=slug)
                db.session.add(subj)
                db.session.flush()
                logger.info(f"  + Subject: {name}")
            else:
                logger.info(f"  ~ Exists: {name}")

            subj.description = data['description']
            subj.pros = '\n'.join(data['pros'])
            subj.cons = '\n'.join(data['cons'])

            rng = random.Random(hash(name) % 100000)
            all_reviews = data['reviews']
            count = rng.randint(5, 10)
            chosen = rng.sample(all_reviews, min(count, len(all_reviews)))

            added = 0
            for i, (rating, title, body) in enumerate(chosen):
                url_key = f"sample-{slug}-{i}"
                if Review.query.filter_by(original_url=url_key).first():
                    continue
                db.session.add(Review(
                    subject_id=subj.id, rating=rating, title=title, body=body,
                    author_name=_rnd_name(rng), source_site='sample',
                    is_published=True, original_url=url_key,
                ))
                added += 1
            total_reviews += added
            subj.update_stats()
            logger.info(f"    {added} reviews for {name}")

            if not subj.image_path:
                logger.info(f"  Fetching image for {name}...")
                img_url = get_wiki_image(data['wiki_title']) or try_commons_image(f"{name} chicken breed")
                if img_url:
                    ext = img_url.rsplit('.', 1)[-1].split('?')[0].lower()
                    if ext not in ('jpg', 'jpeg', 'png', 'webp'):
                        ext = 'jpg'
                    dest = os.path.join(upload_dir, f"{slug}.{ext}")
                    if download_image(img_url, dest):
                        subj.image_path = f"images/uploads/subjects/{slug}.{ext}"
                        logger.info(f"    Image: {subj.image_path}")
                    else:
                        logger.warning(f"    Image download failed for {name}")
                else:
                    logger.warning(f"    No image found for {name}")
                time.sleep(2)

        if not sub.image_path:
            logger.info("Fetching Chickens slate image...")
            slate_url = get_wiki_image('Chicken') or try_commons_image('backyard chickens flock')
            if slate_url:
                dest = os.path.join(defaults_dir, 'chickens.jpg')
                if download_image(slate_url, dest):
                    sub.image_path = 'images/defaults/chickens.jpg'
                    logger.info("  Saved Chickens slate image")
            time.sleep(2)

        db.session.commit()
        logger.info(f"\nDone. {len(CHICKEN_DATA)} chicken breeds, {total_reviews} reviews.")


if __name__ == '__main__':
    main()
