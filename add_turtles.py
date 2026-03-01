"""
Add a Turtles & Tortoises subcategory to Animals with 4 species, reviews, and images.
Safe to run multiple times — skips existing records.

Usage:
  python3 add_turtles.py
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
    'Slow', 'Ancient', 'Wise', 'Calm', 'Steady', 'Rocky', 'Mossy', 'Sunlit',
    'Sandy', 'Shelly', 'Domed', 'Muddy', 'Basking', 'Gentle', 'Patient',
]
_ANIMALS = [
    'Shell', 'Dome', 'Paddle', 'Bask', 'Clamp', 'Plod', 'Wade', 'Dip',
    'Crest', 'Pond', 'Bank', 'Slide', 'Rock', 'Marsh', 'Drift',
]


def _rnd_name(rng: random.Random) -> str:
    return f"{rng.choice(_ADJECTIVES)}{rng.choice(_ANIMALS)}{rng.randint(10, 99)}"


TURTLE_DATA: dict[str, dict] = {
    'Red-Eared Slider': {
        'slug': 'red-eared-slider',
        'wiki_title': 'Red-eared slider',
        'description': (
            'The red-eared slider is the most popular pet turtle in the world, '
            'named for the distinctive red stripe behind each eye. '
            'Semi-aquatic, they require both water for swimming and a dry basking area with UVB lighting. '
            'With proper care they live 20–40 years and grow to 20–30cm — a serious long-term commitment.'
        ),
        'pros': [
            'Widely available and well-understood in terms of care',
            'Active and entertaining to watch while swimming',
            'Recognise their owners and respond to feeding time',
            'Robust and hardy with correct husbandry',
            'Can live 20–40 years — a true long-term companion',
        ],
        'cons': [
            'Require a large aquatic setup (minimum 200L for adults)',
            'Need powerful filtration — messy eaters',
            'Long lifespan requires multi-decade commitment',
            'Can carry Salmonella — hygiene essential especially with children',
        ],
        'reviews': [
            (5, 'My 15-year companion and still going strong', 'My red-eared slider has been with me for 15 years and is still as active and alert as ever. She recognises me (or at least my food) and swims eagerly to the front of her tank at mealtimes. Watching her bask under the UV lamp is meditative. The setup was a significant investment — large tank, powerful filter, UV and basking lights — but she\'s required virtually no vet care in 15 years. A wonderfully long-lived pet.'),
            (5, 'Fascinating to watch daily', 'I never tire of watching my red-eared sliders. They swim, bask, interact with each other, and seem genuinely aware of their environment. Mine have learned that a tap on the glass means food and come gliding over immediately. The red stripe on their heads is beautifully vivid. Turtle keeping requires commitment to water quality, but the reward is a fascinating, long-lived pet unlike any other.'),
            (4, 'Filtration is critical — invest in a good filter', 'Red-eared sliders are messy and a powerful filter is non-negotiable. I learned this the hard way with a cheap filter that couldn\'t handle the bioload of two adult turtles. Cloudy, smelly water and one mildly ill turtle later, I invested in a proper external canister filter rated for three times the tank volume. The difference was immediate. Good filtration means clear water, happy turtles, and far less maintenance.'),
            (4, 'Long commitment — plan accordingly', 'Before getting red-eared sliders please understand the commitment. These turtles live 20–40 years. I got mine as tiny 5cm hatchlings that cost very little — they are now 22cm adults in a 400L tank. The cute hatchlings grow into substantial animals requiring significant resources. I love them dearly but I wish I\'d understood the adult size and lifespan properly before starting. Research thoroughly.'),
            (5, 'Great for patient, dedicated keepers', 'Red-eared sliders are not a pet you set up and ignore. They reward careful attention to water quality, temperature, UV provision, and diet variety. When you get all that right, they thrive visibly — brighter colours, active behaviour, and excellent health. My oldest slider is 18 years old and still in perfect condition. The dedication is real but so is the reward of a healthy, thriving turtle that will outlive most pets.'),
            (3, 'Salmonella hygiene is real', 'Red-eared sliders are wonderful turtles but the Salmonella risk is real and must be managed. Wash hands thoroughly after handling turtles or touching tank water. Never let turtles near food preparation areas. Young children should be supervised. None of this is difficult — it\'s just consistent hygiene — but families with young children should be fully aware before getting aquatic turtles. My turtles are healthy and well-managed; just don\'t underestimate the hygiene requirements.'),
            (4, 'Intelligent and responsive', 'People underestimate turtle intelligence. My red-eared sliders know my routine — they start swimming to the feeding area before I even reach for the food container. They also have distinct personalities: one is bold and interactive, the other shy and observant. After 12 years I can tell when they\'re healthy, when they\'re cold, and when they want to be left alone. Turtles reward careful observation.'),
            (5, 'Mesmerising to watch', 'There is something deeply calming about watching turtles. My red-eared sliders glide through their tank with such effortless grace — extending their limbs, surfacing for air, basking under the lamp in a state of perfect contentment. I spend time just watching them most evenings. They\'re living art. Setting up a proper turtle habitat is expensive, but the result is the most beautiful and tranquil home aquarium imaginable.'),
        ],
    },
    'Russian Tortoise': {
        'slug': 'russian-tortoise',
        'wiki_title': 'Russian tortoise',
        'description': (
            'The Russian tortoise (also known as the Horsfield\'s tortoise) is one of the most popular pet tortoises, '
            'appreciated for its manageable size (15–20cm), relative hardiness, and active personality. '
            'Native to the arid steppes of Central Asia, they tolerate cool temperatures better than Mediterranean species '
            'and are considered an excellent choice for first-time tortoise keepers.'
        ),
        'pros': [
            'Manageable adult size (15–20cm)',
            'Hardy and tolerates cooler temperatures better than other species',
            'Active and personable — will come to greet owners',
            'Good starter tortoise species for beginners',
            'Can be kept outdoors in temperate climates during summer',
        ],
        'cons': [
            'Require hibernation (brumation) in winter — careful management needed',
            'Strictly herbivorous — no protein, careful diet management required',
            'Need outdoor space or very large indoor setup',
            'Live 40–50+ years — an exceptional long-term commitment',
        ],
        'reviews': [
            (5, 'My 20-year tortoise companion', 'My Russian tortoise has been with me for 20 years and is reportedly only in mid-life. She bobs to the front of her enclosure when she sees me, has favourite foods (dandelions and clover), and shows distinct disapproval when her lettuce isn\'t fresh. Tortoises are deeply underestimated as companion animals — they have personality, preferences, and genuine character. Twenty years in and I adore her completely.'),
            (5, 'Perfect size for indoor keeping', 'Russian tortoises top out at 15–20cm, which makes them the perfect size for indoor keeping without requiring a shed or a huge garden. My enclosure is a 120cm × 60cm wooden vivarium with a UV panel and thermostat — a manageable footprint. She grazes on fresh weeds from the garden daily and is in excellent health at 8 years old. The perfect tortoise for keepers without large outdoor space.'),
            (4, 'Hibernation requires confidence', 'Russian tortoises require annual hibernation and getting this right requires research and nerve. My tortoise hibernates in a fridge (controlled temperature hibernation) from November to February. The first time was nerve-wracking — is she too cold? Too warm? Is she breathing? Two years on I\'m completely confident in the process and she wakes up in spring with renewed energy. But do proper research before hibernating a tortoise for the first time.'),
            (5, 'Active and full of character', 'Russian tortoises are far more active than their reputation suggests. Mine potters around her enclosure constantly, investigates new objects, and has a very clear daily routine. She\'s assertive about mealtimes — she will ram her food dish if food is late. She has favourite basking spots, favourite foods, and makes clear when she\'s had enough handling. A genuinely characterful animal.'),
            (4, 'Diet research is essential', 'Russian tortoise diet is more complex than it looks. They\'re strict herbivores requiring high-fibre, low-protein, calcium-rich diet — dandelions, plantain, clover, tortoise-safe wildflowers. Many shop-bought vegetables are inappropriate. I grow weeds specifically for my tortoise now. The investment in diet research is worth it — my tortoise has beautiful shell growth and excellent health after 6 years. Get the diet right from day one.'),
            (3, 'Multi-decade commitment is serious', 'Russian tortoises live 40–50+ years. I got mine 15 years ago and have come to terms with the fact that she will outlive me unless I live to 90. I\'ve arranged for her care in my will. This sounds extreme but it\'s a genuine responsibility that prospective tortoise owners should think about. She\'s a wonderful animal and I love her dearly — just be honest with yourself about a 50-year commitment before getting a tortoise.'),
            (5, 'Hardy and forgiving for beginners', 'Russian tortoises are often recommended to beginners because they tolerate a wider temperature range than Mediterranean species, are less prone to respiratory infections in imperfect conditions, and are generally more robust. My first tortoise was a Russian and she thrived despite my early mistakes in husbandry. She\'s 10 years old, healthy, and still teaching me things about tortoise keeping. An excellent entry point to the hobby.'),
            (4, 'Loves outdoor time in summer', 'One of the best things about keeping a Russian tortoise is outdoor time in summer. I set up a secure outdoor pen on warm days and she transforms — grazing enthusiastically on clover and dandelions, basking in natural sunlight, and exploring at surprising speed. The UV from real sunlight is irreplaceable. She\'s noticeably more alert and active after outdoor sessions than after days inside. Weather permitting, outdoor time is enormously beneficial.'),
        ],
    },
    "Hermann's Tortoise": {
        'slug': 'hermanns-tortoise',
        'wiki_title': "Hermann's tortoise",
        'description': (
            "Hermann's tortoise is one of the most beloved pet tortoise species in Europe, "
            'native to the Mediterranean region. They are known for their attractive domed shells '
            'with yellow and black patterning, active and inquisitive personality, and manageable adult size (15–25cm). '
            'They live 50–100 years, making them potentially multi-generational family pets.'
        ),
        'pros': [
            'Attractive domed shell with beautiful yellow and black markings',
            'Active and inquisitive personality',
            'Well-established care requirements — extensive keeper community',
            'Suitable for Mediterranean-style outdoor enclosures in mild climates',
            'Extremely long-lived — potentially outlives owners',
        ],
        'cons': [
            'Very long lifespan (50–100 years) — multi-generational commitment',
            'Require hibernation in winter',
            'Need outdoor space for optimal health in temperate climates',
            'Strict herbivorous diet — no fruit or protein',
        ],
        'reviews': [
            (5, 'A living heirloom', 'My Hermann\'s tortoise is 35 years old and was already an adult when I received her from my aunt. She could live another 50 years. There is something profound about caring for an animal that has its own history, that has outlived owners, and that will likely outlive me too. She\'s healthy, active, and still surprises me with her character after all these years. A genuine living heirloom — plan for her future carefully.'),
            (5, 'Most beautiful tortoise species', 'Hermann\'s tortoises have some of the most beautiful shells of any tortoise species — vivid yellow and black patterning that remains striking even in older animals. My 12-year-old Hermann has a perfect, smooth, naturally-patterned shell that people ask to photograph. Beyond the aesthetics, she\'s inquisitive and active, grazes enthusiastically in the garden, and has a distinct daily personality. A magnificent animal.'),
            (4, 'Outdoor keeping in summer is spectacular', 'My Hermann\'s tortoise has a large outdoor pen for the warmer months with a varied selection of tortoise-safe plants, natural basking areas, and a hide. Watching her graze, bask, and explore outdoors in natural sunlight is wonderful. She grows faster and is visibly happier outdoors than indoors. For anyone in a mild climate, outdoor keeping (with appropriate security and temperature monitoring) transforms tortoise husbandry.'),
            (5, 'Comes running for dandelions', 'My Hermann\'s tortoise has learned that the yellow flowers of dandelions are a favourite treat. Whenever I pick dandelions from the garden she hears the rustle and comes trundling over at surprising speed. For an animal reputedly slow, she can move quickly when motivated. Her enthusiasm for food is endearing and her preferences are very distinct — she loves clover and dandelions, tolerates plantain, and decisively refuses anything she dislikes.'),
            (4, 'Hibernation management is important', 'Hermann\'s tortoises must hibernate — attempting to keep them active year-round causes health problems. I dry-hibernate mine in a cool garage (8–12°C) from November to March in a box of substrate. The first winter was nerve-wracking but she woke up in spring perfectly healthy and immediately demanded food. Correct hibernation is achievable with research but requires commitment. Join a tortoise keeper forum for guidance — experienced keepers are invaluable.'),
            (3, '50-100 years is not a metaphor', 'People read "50-100 year lifespan" and intellectually understand it, but emotionally underestimate it. My Hermann\'s is 18 years old and I\'m already thinking about who will care for her when I\'m too old. She will likely outlive everyone in my immediate family. I\'ve updated my will to arrange for her care. This is not morbid — it\'s responsible tortoise ownership. Magnificent animals, but their longevity demands real planning.'),
            (5, 'Perfect Mediterranean garden tortoise', 'I have a large garden with a dedicated tortoise enclosure — planted with appropriate herbs, clover, plantain, and safe wildflowers. My Hermann\'s tortoise has lived outdoors (with an insulated indoor heated section for cool nights) for eight years. She\'s in perfect health, has beautiful shell growth, and is visibly thriving. For anyone with suitable outdoor space, Hermann\'s are the ideal garden tortoise.'),
            (4, 'Engaging and surprisingly social', 'Tortoises have a reputation for being solitary and dull, which my Hermann\'s has comprehensively disproved. She patrols her enclosure purposefully, investigates anything new, and has distinct preferences and dislikes. She will come to greet me at the garden fence and follow me around if I enter her area. Whether this is food-association or genuine recognition, I\'ve come to believe she is aware of me specifically. Remarkable animals.'),
        ],
    },
    'Sulcata Tortoise': {
        'slug': 'sulcata-tortoise',
        'wiki_title': 'African spurred tortoise',
        'description': (
            'The sulcata (African spurred tortoise) is the third-largest tortoise species in the world, '
            'with adults reaching 70–90cm and weighing 45–100kg. '
            'Native to the Sahel region of Africa, they are powerful, long-lived (70–100 years), and require '
            'substantial outdoor space with warm temperatures. They are beautiful but are frequently surrendered to rescues '
            'by owners who underestimated their adult size.'
        ),
        'pros': [
            'Impressive and magnificent animals',
            'Extremely long-lived (70–100+ years)',
            'Gentle and generally placid temperament',
            'Fascinating to observe — powerful and prehistoric in character',
            'Bond strongly with consistent caregivers',
        ],
        'cons': [
            'Enormous adult size (up to 100kg) — requires dedicated large outdoor space',
            'Need warm climate or heated outdoor enclosure year-round',
            'Cannot hibernate — require warm temperatures continuously',
            'Powerful enough to destroy fencing and garden structures',
            'Frequently surrendered to rescues due to underestimated adult requirements',
        ],
        'reviews': [
            (5, 'The most magnificent animal I\'ve ever kept', 'My sulcata tortoise is 18 years old and weighs 45kg. She is the most magnificent, prehistoric-looking animal — watching her graze slowly across the garden or lower her head to investigate something is like having a living dinosaur. She\'s gentle, recognises her caregivers, and has never shown aggression. Keeping a sulcata properly requires genuine resources and commitment, but the experience is like nothing else in the animal world.'),
            (4, 'Research adult size BEFORE buying a hatchling', 'Sulcata hatchlings are adorable 5cm tortoises that cost very little and seem manageable. They are not. In ten years mine went from fitting in my palm to weighing 30kg and demolishing my fence. Please research adult sulcata size before buying a hatchling. The number of surrendered sulcatas in rescues is heartbreaking. That said, with the right space and resources, they are extraordinary animals.'),
            (5, 'Warm climate essential', 'I live in southern Spain which is ideal for sulcata keeping. My tortoise lives entirely outdoors year-round in a large secure enclosure. He grazes constantly, basks extensively, and is visibly thriving in the warm climate. Sulcatas cannot be cold — they need consistently warm temperatures. For keepers in temperate climates, maintaining appropriate warmth for a 70kg tortoise in winter is a significant challenge and cost. Know your climate before committing.'),
            (4, 'Genuinely bonds with caregivers', 'People assume tortoises are unaware of their owners. My sulcata has disproved this entirely over 15 years. She knows my voice, my routine, and comes to the gate of her enclosure when she hears me approach in the morning. She tolerates handling from me willingly but is more cautious with strangers. The relationship that develops over years of consistent, respectful care is genuine and deeply rewarding.'),
            (3, 'Massive commitment — be honest with yourself', 'I love my sulcata but I am honest that I underestimated the commitment. He now weighs 60kg, requires a shed with heating for cool nights, eats enormous quantities of hay and fresh weeds daily, and has broken through two fences. The cost and physical demands are substantial. He\'s a wonderful animal and I\'m committed to his lifelong care, but I encourage anyone considering a sulcata to visit an adult in a rescue first. See what you\'re committing to.'),
            (5, 'Prehistoric and awe-inspiring', 'Watching a fully grown sulcata tortoise is awe-inspiring. The sheer scale of the animal — the domed shell, the wrinkled neck, the powerful legs — feels ancient and magnificent. My 25-year-old female weighs 55kg and moves with unhurried authority through her enclosure. Guests who visit specifically to see her invariably stand in silence for the first minute, just absorbing the presence of such an extraordinary creature. Nothing quite prepares you for a full-grown sulcata.'),
            (4, 'Long-lived — arrange for their future', 'Sulcatas live 70–100 years. I am 52 and my sulcata may well outlive me. I have arranged for her continued care in my estate planning and identified a tortoise sanctuary that will take her if needed. This is not optional — responsible sulcata ownership requires thinking about what happens to your tortoise in 30 years. It\'s a sobering but necessary part of committing to one of these extraordinary animals.'),
            (5, 'The right animal for the right keeper', 'Sulcata tortoises are not for everyone — they need space, warmth, strength (they are powerful animals), and multi-decade commitment. But for the right keeper with the right setup, they are the most rewarding reptile imaginable. My sulcata is 20 years old, in magnificent health, and a source of constant wonder. He eats from my hand, allows me to clean his shell, and seems genuinely content in his large, warm outdoor enclosure. An extraordinary privilege to keep.'),
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

        sub = SubCategory.query.filter_by(category_id=animals_cat.id, slug='turtles-tortoises').first()
        if not sub:
            sub = SubCategory(category_id=animals_cat.id, name='Turtles & Tortoises', slug='turtles-tortoises')
            db.session.add(sub)
            db.session.flush()
            logger.info("Created Turtles & Tortoises subcategory")
        else:
            logger.info("Turtles & Tortoises subcategory already exists")

        total_reviews = 0
        for name, data in TURTLE_DATA.items():
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
                img_url = get_wiki_image(data['wiki_title']) or try_commons_image(f"{name} pet")
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
            slate_url = get_wiki_image("Hermann's tortoise") or try_commons_image('pet tortoise turtle')
            if slate_url:
                dest = os.path.join(defaults_dir, 'turtles-tortoises.jpg')
                if download_image(slate_url, dest):
                    sub.image_path = 'images/defaults/turtles-tortoises.jpg'
                    logger.info("Saved Turtles & Tortoises slate image")
            time.sleep(2)

        db.session.commit()
        logger.info(f"\nDone. {len(TURTLE_DATA)} turtle/tortoise species, {total_reviews} reviews.")


if __name__ == '__main__':
    main()
