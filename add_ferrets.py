"""
Add a Ferrets subcategory to Animals with 5 ferret types/breeds, reviews, and images.
Safe to run multiple times — skips existing records.

Usage:
  python3 add_ferrets.py
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
    'Bouncy', 'Wriggly', 'Cheeky', 'Fuzzy', 'Sneaky', 'Zippy', 'Mischief',
    'Silly', 'Bold', 'Fluffy', 'Dooky', 'Wobbly', 'Chaos', 'Feisty', 'Wiggly',
]
_ANIMALS = [
    'Dook', 'Noodle', 'Bandit', 'Weasel', 'Chaos', 'Sock', 'Tunnel',
    'Zoom', 'Zoomie', 'Sneak', 'Bounce', 'Squirm', 'Pounce', 'Dash', 'Scout',
]


def _rnd_name(rng: random.Random) -> str:
    return f"{rng.choice(_ADJECTIVES)}{rng.choice(_ANIMALS)}{rng.randint(10, 99)}"


FERRET_DATA: dict[str, dict] = {
    'Sable Ferret': {
        'slug': 'sable-ferret',
        'wiki_title': 'Ferret',
        'description': (
            'The sable ferret is the most common and classic ferret colour pattern, '
            'with dark brown guard hairs, a cream or white undercoat, and a dark mask. '
            'Domesticated ferrets are intelligent, playful, and deeply social — they should be kept in pairs or groups '
            'and form incredibly strong bonds with their owners.'
        ),
        'pros': [
            'Incredibly playful and entertaining — never a dull moment',
            'Form deep bonds with owners and recognise individual people',
            'Intelligent — can learn tricks, navigate obstacle courses',
            'Active and fun during their waking hours',
            'The most expressive and characterful of small pets',
        ],
        'cons': [
            'Must be kept in pairs or groups — miserable alone',
            'Require large multi-level enclosures and significant daily free-roam time',
            'Prone to several health conditions including insulinoma and adrenal disease',
            'Musky scent even after descenting — not for scent-sensitive owners',
            'Short lifespan of 5–8 years',
        ],
        'reviews': [
            (5, 'The most entertaining pets I\'ve ever owned', 'Ferrets are absolute chaos in the most wonderful way. My two sable ferrets perform the "war dance" (a sideways hopping frenzy) when excited, steal every small object they can reach and hide it under the sofa, and chase each other at full speed around the living room during free-roam. They dook (a chuckling sound) constantly when happy. Watching ferrets play is the most entertaining thing in pet keeping. I\'m completely obsessed.'),
            (5, 'Bond like velcro — incredibly affectionate', 'People don\'t realise how affectionate ferrets are. Mine greet me every morning with dooking and dancing, climb up my legs to be held, and fall asleep on my lap for hours. My sable male Bandit seeks me out specifically — he ignores my partner and comes only to me. The bond between a ferret and its person is genuinely special and unlike anything I\'ve experienced with other small animals.'),
            (4, 'Get two or more — they need company', 'My first ferret was a single kit (baby ferret) and while she was sweet, she was clearly lonely during the hours I was at work. I adopted a companion a month later and the transformation was immediate — both ferrets were happier, more active, and more playful. Ferrets must have ferret company. A lone ferret is an unhappy ferret. Always get two minimum and factor in the doubled cost of food, vet care, and housing.'),
            (5, 'Intelligent and trainable', 'Ferrets are far more intelligent than most people give them credit for. My two sable ferrets have learned their names, come when called (most of the time), and one has learned to sit for treats. They understand cause and effect in a sophisticated way — they know which drawer has the treats, which cabinet has their leads, and which sounds mean "free roam time." Their problem-solving is genuinely impressive and endlessly entertaining to observe.'),
            (4, 'Vet health issues are real — budget accordingly', 'Ferrets are prone to several serious health conditions — insulinoma (pancreatic tumour), adrenal disease, and lymphoma are distressingly common in ferrets over 4 years old. My older ferret was diagnosed with insulinoma at 5 and the treatment (medication and diet modification) has given her an extra year of quality life. Ferret vet care is specialist and expensive. Budget for health costs before committing to ferrets.'),
            (3, 'The smell is real', 'I love my ferrets unconditionally, but I\'m honest that the musky ferret smell is real and persistent. Even descented ferrets have a natural musky odour that permeates the room where they live. Regular cage cleaning, frequent bedding changes, and proper diet all help, but the smell doesn\'t disappear. If you\'re scent-sensitive or house-proud, genuinely test your tolerance around ferrets before committing. They\'re worth it to me — but not to everyone.'),
            (5, 'Never stop laughing', 'Three years of ferret ownership and I still laugh every single day. The war dance when they\'re excited, the sideways stumbling when over-stimulated, the dramatic "dead ferret" sleep (so limp and still that new owners panic), the deliberate stealing of specific items to provoke a chase — ferrets are absurdist performance art. My two sable ferrets have brought more joy per day than any pet I\'ve kept. Extraordinary animals.'),
            (4, 'Free-roam time is non-negotiable', 'Ferrets need at least 4 hours of out-of-cage free-roam time daily and will become unhappy and destructive without it. You must ferret-proof any space they use — they can fit through incredibly small gaps, will destroy anything chewable, and will steal and hide anything small enough to carry. Once you\'ve established a safe free-roam area, watching ferrets explore and play is one of the great joys of pet keeping. Just budget time and energy accordingly.'),
        ],
    },
    'Albino Ferret': {
        'slug': 'albino-ferret',
        'wiki_title': 'Ferret',
        'description': (
            'The albino ferret has a completely white coat, pink eyes, and a pink nose — '
            'the result of a lack of melanin pigmentation. '
            'Albino ferrets share the same playful, affectionate personality as all domestic ferrets '
            'and are highly popular due to their striking appearance.'
        ),
        'pros': [
            'Striking white coat and pink eyes — distinctive and beautiful',
            'Same playful, affectionate personality as all ferrets',
            'Highly social and bonds strongly with owners',
            'Entertaining and energetic during active periods',
            'Wide availability as a popular ferret colour variant',
        ],
        'cons': [
            'Pink eyes mean reduced vision in bright light',
            'Same health concerns as all ferrets (insulinoma, adrenal disease)',
            'White coat shows dirt more readily — requires more frequent cleaning',
            'Must be kept in pairs — cannot live alone',
        ],
        'reviews': [
            (5, 'Ghost-like and utterly beautiful', 'My albino ferret is the most striking pet I\'ve ever owned. Completely white with vivid pink eyes, she looks otherworldly — like a tiny ghost dashing around the flat. People are startled when they first see her pink eyes, but she\'s completely healthy and has perfect vision in normal lighting. She\'s as wild and playful as any ferret I\'ve kept, just dramatically more photogenic. She gets more attention than any pet I\'ve ever had.'),
            (4, 'Same personality as any ferret — spectacular looks', 'Albino ferrets aren\'t a distinct breed — the albinism is just a coat colour/eye colour variation. My albino has exactly the same dooking, war-dancing, chaotic personality as my sable ferret. She\'s sociable, mischievous, and incredibly affectionate. The white coat does show dirt more readily and she gets grubby after digging in her substrate, but she\'s so charming that frequent bath time is just another bonding experience.'),
            (5, 'My most affectionate ferret ever', 'I\'ve kept three ferrets over the years and my albino female is the most affectionate. She actively seeks cuddles, falls asleep on my chest, and makes the most expressive dooking sounds when she sees me. Whether albinos are genuinely more cuddly or whether it\'s individual personality I couldn\'t say, but she\'s the snuggliest ferret I\'ve had. The white and pink colouring just adds to her irresistible charm.'),
            (4, 'Pink eyes in bright light — manage lighting', 'Albino ferrets have reduced light tolerance due to their pink eyes (lack of pigment). My ferret avoids very bright areas and prefers the slightly dimmer corners of her enclosure. I avoid placing her habitat in direct sun and keep lighting moderate. In normal indoor conditions she\'s completely comfortable and visually capable. Just be aware that very bright environments may cause her to squint or avoid the area.'),
            (5, 'Turns everyone into a ferret fan', 'I bring my albino ferret to friends\' houses during visits and she converts almost everyone to ferret appreciation. Something about the white coat, the pink eyes, and the dancing, dooking personality combined is irresistible even to people who said they didn\'t like ferrets. She\'s an extraordinary ambassador for the species. After three years I can\'t imagine life without her or her sable companion.'),
            (4, 'Requires same commitment as any ferret', 'An albino ferret requires exactly the same commitment as any other ferret — large enclosure, ferret companion, 4+ hours free-roam daily, specialist vet, and preparation for health costs later in life. The albinism is just colouring. Make sure you\'re committed to ferret keeping in general before choosing an albino specifically — don\'t choose based solely on looks. That said, she is phenomenally beautiful and I\'m completely smitten.'),
            (3, 'Health monitoring is important', 'My albino ferret developed adrenal disease at 4 years old — a common condition in ferrets. The vet placed an implant to manage hormone levels and she\'s been stable for a year. The specialist vet costs were significant. Albinos aren\'t more prone to health issues than other ferrets, but ferrets in general have a high rate of certain conditions. Budget for specialist veterinary care and monitor your ferret\'s health closely as they age.'),
        ],
    },
    'Silver Mitt Ferret': {
        'slug': 'silver-mitt-ferret',
        'wiki_title': 'Ferret',
        'description': (
            'The silver mitt ferret has a silver-grey coat with distinctive white "mitt" markings on all four paws '
            'and often a white bib on the chest. '
            'The silver colour comes from a mix of white and dark guard hairs, giving a beautiful shimmering effect. '
            'Like all domestic ferrets, they are energetic, curious, and deeply social animals.'
        ),
        'pros': [
            'Beautiful silver coat with distinctive white paw markings',
            'Same playful, intelligent personality as all ferrets',
            'Social and bonds deeply with owners',
            'Unique and striking appearance — stand out from common sable and albino',
            'Energetic and entertaining to watch',
        ],
        'cons': [
            'Same health risks as all ferrets (insulinoma, adrenal disease)',
            'Need ferret companion — cannot live alone',
            'Require substantial daily free-roam time',
            'Musky natural scent even in clean ferrets',
        ],
        'reviews': [
            (5, 'Most beautiful ferret colouring I\'ve seen', 'Silver mitt ferrets have the most elegant colouring — the silver-grey body shimmering with the white paw markings is genuinely stunning. My silver mitt boy Frost is absolutely gorgeous and constantly admired. He\'s also a typical ferret in temperament — chaotic, playful, and utterly charming. The silver sheen of his coat in sunlight is like watching a small, mischievous cloud zoom across the floor. Spectacular.'),
            (4, 'Distinctive enough to attract attention', 'Everyone who visits comments on my silver mitt ferret before they even notice the sable. The colouring is striking — silver and white with the defined paw mitts — and very photogenic. She photographs beautifully against any background. Beyond the aesthetics she\'s a typical ferret: energetic, curious, and infuriatingly mischievous. She stole my car keys yesterday and I found them behind the washing machine. Classic ferret behaviour.'),
            (5, 'Best personality of any ferret I\'ve had', 'My silver mitt is hands-down the most interactive ferret I\'ve owned. He dooks every time he sees me, greets me at the cage door, and does his war dance before zooming around the room in joyful frenzy. He learned his name in two weeks and comes reliably. Whether the silver mitt colour correlates with personality I genuinely don\'t know, but he\'s extraordinary. Three years in and he still surprises me daily.'),
            (4, 'Requires ferret-proofing before free-roam', 'Silver mitt or any other ferret — free-roam time requires serious ferret-proofing. My silver mitt found a gap behind the kitchen cabinets in the first week. I\'ve since blocked every gap under 3cm in the free-roam area and do a sweep before every session. Once the space is properly secured, watching him explore, dig, and dook his way around the room is pure joy. Just do the preparation first.'),
            (5, 'Plays brilliantly with companion ferrets', 'My silver mitt and my sable ferret have the most entertaining relationship. They chase each other, perform wrestling matches, do dooking circuits around the sofa, and then collapse in a ferret pile to sleep. The interaction between ferrets is just as entertaining as individual play. Silver mitt\'s distinctive colouring makes it easy to tell them apart in the chaos. Never get just one ferret — the joy of watching two play together is irreplaceable.'),
            (3, 'Vet bills escalated in later years', 'My silver mitt developed both insulinoma and adrenal disease by age 5. Managing both simultaneously required specialist vet visits every three months and ongoing medication. The bills were substantial. I loved him completely and managed both conditions for two years before he passed peacefully at 7. Ferrets are wonderful animals but prospective owners need to understand and budget for the real likelihood of expensive health issues in later years.'),
        ],
    },
    'Panda Ferret': {
        'slug': 'panda-ferret',
        'wiki_title': 'Ferret',
        'description': (
            'The panda ferret has a distinctive white head and shoulders contrasting with a darker body, '
            'giving it a resemblance to a tiny panda. '
            'Combined with its mask and white bib, the panda colouring is one of the most sought-after ferret patterns. '
            'All panda ferrets share the classic ferret personality: mischievous, energetic, and deeply affectionate.'
        ),
        'pros': [
            'Striking panda-like black and white markings',
            'One of the most distinctive and admired ferret colour patterns',
            'Same energetic, affectionate personality as all ferrets',
            'Social and forms strong bonds with owners',
            'Highly entertaining — chaotic energy and dooking joy',
        ],
        'cons': [
            'Panda ferrets can be harder to find from reputable breeders',
            'Same health risks as all ferrets',
            'Require ferret companion and significant free-roam time',
            'White areas of coat show dirt readily',
        ],
        'reviews': [
            (5, 'Looks like a toy that came to life', 'My panda ferret looks so much like a tiny cartoon animal that visitors always do a double-take. The white head against the dark body with the classic ferret mask is just absurdly adorable. She is, of course, completely unaware of this and spends all her time being chaotic, stealing things, and dooking at maximum volume. She\'s the most photographed pet I\'ve ever owned — every picture of her gets an extreme reaction. Completely obsessed.'),
            (5, 'The personality behind the markings', 'Beyond the stunning panda markings my ferret has the most vibrant personality. She\'s the boldest and most curious ferret in my group of three, always the first to investigate new objects and new areas. She dooks constantly and has the most elaborate war dance. The markings drew me to the colour pattern but the personality is what made me fall completely in love. She\'s extraordinary — the markings are the cherry on top.'),
            (4, 'Finding one took some searching', 'Panda ferrets are one of the more sought-after colour patterns and finding one from a reputable breeder took several months of searching. I was adamant about sourcing from a breeder who health-tested their ferrets and socialised kits properly. The wait was completely worth it — my panda girl is confident, healthy, and beautifully socialised. Please don\'t rush the search — a well-bred ferret from a good source is worth waiting for.'),
            (5, 'Brings my whole family together', 'When I introduced my panda ferret to the family, everyone was instantly captivated. The markings are so arresting that people who claimed not to like ferrets were immediately enchanted. He\'s become the centre of family gatherings — we set him up for free-roam and watch him perform. His war dance and dooking produce genuine laughter every time. A panda ferret is social media gold and domestic happiness in equal measure.'),
            (4, 'White areas need regular attention', 'The white portions of my panda ferret\'s coat (the head and shoulders) show every speck of substrate, food, and whatever else she\'s gotten into during free-roam. She\'s beautifully clean immediately after a bath and gloriously grubby within the hour. I\'ve just accepted this as part of panda ferret ownership. The bath sessions are actually lovely bonding time and she tolerates them well. Just know the white patches require more attention than a solid dark ferret.'),
            (3, 'Committed ferret person only', 'Panda ferrets are beautiful and endearing — but they\'re ferrets, with all the commitment that entails. Large enclosure, ferret companion, hours of daily free-roam, ferret-proofing, specialist vet, real health costs in later years. The panda markings might attract people who aren\'t fully prepared for the reality of ferret keeping. Please research ferret care thoroughly before being drawn in purely by the stunning colouring. For committed keepers they\'re magnificent.'),
        ],
    },
    'Angora Ferret': {
        'slug': 'angora-ferret',
        'wiki_title': 'Ferret',
        'description': (
            'The Angora ferret is a long-haired variety of domestic ferret, '
            'with a soft, flowing coat that can reach twice the length of standard ferret fur. '
            'Less common than standard-coated ferrets, they have the same characterful, mischievous personality '
            'but require significantly more grooming to prevent matting and keep the coat healthy.'
        ),
        'pros': [
            'Extraordinarily soft, long, flowing coat',
            'Same playful and affectionate personality as all ferrets',
            'Distinctive and unusual appearance — rarely seen in pet keeping',
            'Grooming sessions become a bonding activity',
            'Same intelligence and trainability as standard ferrets',
        ],
        'cons': [
            'Long coat requires regular grooming — daily during shedding season',
            'More difficult to find from reputable breeders',
            'Coat can matt severely without proper maintenance',
            'Same health risks as all ferrets; often harder to examine skin condition under long fur',
        ],
        'reviews': [
            (5, 'Like a tiny fluffy lion', 'My Angora ferret looks like someone took a regular ferret and added twice as much fur. She\'s absolutely magnificent — flowing coat, expressive face, and the same chaotic ferret energy underneath all that fluff. The coat requires real daily attention, especially around the face and armpits where matting is most likely, but brushing sessions have become wonderful bonding time. She dooks contentedly through the whole grooming process. An extraordinary animal.'),
            (4, 'Grooming is the main commitment', 'Angora ferrets are wonderfully rewarding but the grooming is real. I brush my Angora daily and do a thorough comb-through twice a week. Without this, his coat matts quickly — especially around his neck and face. During shedding season it\'s even more intensive. He tolerates it well and even seems to enjoy it, but prospective Angora owners need to commit to daily grooming as non-negotiable. Skip it and you\'ll be dealing with painful matts.'),
            (5, 'Found one through a specialist breeder — worth every effort', 'Angora ferrets are much rarer than standard ferrets and finding a reputable breeder took significant research and patience. I sourced mine from a specialist ferret breeder who showed me both parents and the health history of the line. The result is a beautifully socialised, healthy Angora who has been in perfect health for four years. Don\'t rush the search for an Angora — the rarity makes vetting the source even more important.'),
            (4, 'Gets more grooming attention than I do', 'I honestly spend more time on my Angora ferret\'s coat than on my own hair. Daily brush, twice-weekly detailed comb, occasional gentle trim around the feet and face to prevent the fur dragging in litter. It\'s a meaningful time commitment. That said, grooming time with my Angora has become my favourite part of the day. She purrs (ferret teeth-chattering contentment sound) through the whole process and relaxes completely. Highly therapeutic for both of us.'),
            (5, 'The most beautiful small animal I\'ve ever seen', 'I\'ve kept a wide range of small animals over the years and my Angora ferret is simply the most beautiful. The long, silky coat paired with the typical ferret mask and the wild ferret energy underneath is extraordinary. She attracts more attention and admiration than any animal I\'ve ever kept. Beyond the aesthetics she\'s as mischievous, curious, and affectionate as any ferret — the long fur is nature\'s extravagance applied to an already wonderful animal.'),
            (3, 'Harder to spot skin issues under all that fur', 'One challenge specific to Angora ferrets is that health monitoring is more difficult. Signs of skin conditions, adrenal disease (hair loss is a common early sign in standard ferrets), or injuries can be hidden under the long coat. I\'ve learned to do thorough parting and skin checks during grooming sessions. My vet (who specialises in ferrets) is also careful to part the coat during examinations. Be aware that the beautiful coat requires extra health vigilance.'),
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
                'iiprop': 'thumburl', 'iiurlwidth': size, 'format': 'json',
            }, timeout=15).json()
            for page in info.get('query', {}).get('pages', {}).values():
                infos = page.get('imageinfo', [])
                if infos and infos[0].get('thumburl'):
                    return infos[0]['thumburl']
    except Exception as e:
        logger.warning(f'Commons error for {query!r}: {e}')
    return None


def download_image(url: str, dest_path: str) -> bool:
    try:
        resp = SESSION.get(url, timeout=20)
        if resp.status_code == 429:
            time.sleep(5)
            resp = SESSION.get(url, timeout=20)
        if resp.status_code != 200:
            return False
        content = resp.content
        if len(content) < 3000:
            return False
        with open(dest_path, 'wb') as f:
            f.write(content)
        return True
    except Exception as e:
        logger.warning(f'Download error: {e}')
        return False


# Specific image URLs for each ferret type (Wikipedia 'Ferret' gives a sable photo — use it for sable,
# then use Commons searches for the other colour variants)
FERRET_COMMONS_QUERIES = {
    'Sable Ferret': 'sable ferret pet',
    'Albino Ferret': 'albino ferret white pink eyes',
    'Silver Mitt Ferret': 'silver ferret pet',
    'Panda Ferret': 'panda ferret pet',
    'Angora Ferret': 'angora ferret long hair',
}


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

        sub = SubCategory.query.filter_by(category_id=animals_cat.id, slug='ferrets').first()
        if not sub:
            sub = SubCategory(category_id=animals_cat.id, name='Ferrets', slug='ferrets')
            db.session.add(sub)
            db.session.flush()
            logger.info("Created Ferrets subcategory")
        else:
            logger.info("Ferrets subcategory already exists")

        total_reviews = 0
        for name, data in FERRET_DATA.items():
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
                # Try specific Commons query for this ferret colour type
                commons_query = FERRET_COMMONS_QUERIES.get(name, 'pet ferret')
                img_url = try_commons_image(commons_query)
                if not img_url:
                    img_url = get_wiki_image(data['wiki_title'])
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
            slate_url = try_commons_image('ferret pet playing') or get_wiki_image('Ferret')
            if slate_url:
                dest = os.path.join(defaults_dir, 'ferrets.jpg')
                if download_image(slate_url, dest):
                    sub.image_path = 'images/defaults/ferrets.jpg'
                    logger.info("Saved Ferrets slate image")
            time.sleep(2)

        db.session.commit()
        logger.info(f"\nDone. {len(FERRET_DATA)} ferret types, {total_reviews} reviews.")


if __name__ == '__main__':
    main()
