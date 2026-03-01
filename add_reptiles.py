"""
Add a Reptiles subcategory to Animals with 5 species, reviews, and images.
Safe to run multiple times — skips existing records.

Usage:
  python3 add_reptiles.py
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
    'Scaly', 'Sunny', 'Bold', 'Sleek', 'Swift', 'Fierce', 'Cool', 'Dusty',
    'Spiky', 'Calm', 'Bright', 'Sharp', 'Lazy', 'Clever', 'Wild',
]
_ANIMALS = [
    'Scale', 'Spike', 'Claw', 'Fang', 'Tail', 'Tongue', 'Basker', 'Crawler',
    'Shade', 'Burrow', 'Ridge', 'Ember', 'Dusk', 'Glow', 'Slither',
]


def _rnd_name(rng: random.Random) -> str:
    return f"{rng.choice(_ADJECTIVES)}{rng.choice(_ANIMALS)}{rng.randint(10, 99)}"


REPTILE_DATA: dict[str, dict] = {
    'Bearded Dragon': {
        'slug': 'bearded-dragon',
        'wiki_title': 'Bearded dragon',
        'description': (
            'The bearded dragon is one of the most popular pet lizards in the world, '
            'celebrated for its docile temperament, expressive "beard" display, and tolerance of handling. '
            'Native to the arid Australian outback, they thrive in properly heated and lit vivaria and can live 10–15 years with good care.'
        ),
        'pros': [
            'Extremely docile and tolerant of handling — great for beginners',
            'Expressive and interactive — responds to owners over time',
            'Hardy and relatively disease-resistant with proper husbandry',
            'Fascinating diet variety (insects + vegetables)',
            'Long lifespan of 10–15 years',
        ],
        'cons': [
            'Requires UVB lighting and a basking spot of 38–42°C',
            'Vivarium and setup costs are significant upfront',
            'Needs live insects (dubia roaches, crickets) regularly',
            'Vet care requires a specialist reptile vet',
        ],
        'reviews': [
            (5, 'Best reptile pet by a mile', 'I\'ve kept many reptiles over the years and my bearded dragon Draco is far and away the most rewarding. He runs to the front of his vivarium when I enter the room, climbs onto my arm for warmth, and seems genuinely happy being handled. His beard display when he watches TV is hilarious — he thinks the screen is a rival male. If you\'re new to reptiles, start with a beardie. You won\'t regret it.'),
            (5, 'Completely changed how I feel about reptiles', 'I always thought reptiles were cold and unresponsive until I got a bearded dragon. My beardie Sunny recognises my voice, perks up when I approach, and settles into my lap contentedly for evening cuddles. She even seems to enjoy watching Netflix — she tilts her head at the screen. The setup cost was real but absolutely worth it. She\'s been healthy for four years with zero issues.'),
            (4, 'Get the setup right from day one', 'Bearded dragons are brilliant pets but only if their husbandry is correct. I made early mistakes with temperatures and UVB output that caused a minor health issue. Once I invested in a proper T5 HO UVB tube, a quality thermostat, and learned to gut-load feeder insects, everything improved dramatically. Research thoroughly before you set up — it saves money and stress in the long run.'),
            (5, 'Great with children', 'My bearded dragon has been a wonderful pet for our family with children aged 8 and 11. He\'s patient, never aggressive, and loves the warmth of their hands. The kids have learned so much about biology, nutrition (he eats bugs AND salad), and habitat through caring for him. He\'s been with us five years and is in perfect health. A remarkable ambassador for reptile keeping.'),
            (4, 'Surprisingly interactive for a lizard', 'I expected a bearded dragon to be passive and uninterested in humans. I was completely wrong. Mine bobs her head at me, waves (an actual wave gesture — it\'s a submission display but it looks adorable), and comes to be picked up. She flattens herself out on my chest to absorb warmth and sometimes falls asleep there. Bearded dragons are genuinely interactive in a way that surprises most new reptile keepers.'),
            (3, 'Wonderful pet but expensive setup', 'My bearded dragon is lovely but the initial cost was substantial — quality vivarium, T5 HO UVB fixture, ceramic heat emitter, quality thermostat, and furnishings came to a significant investment. Then there\'s the ongoing cost of live insects and fresh vegetables daily. Budget carefully before committing. The animal itself is wonderful, but reptile keeping isn\'t cheap if done correctly.'),
            (5, 'My most fascinating pet ever', 'Bearded dragons exhibit the most interesting behaviours of any pet I\'ve kept. The arm-waving, head-bobbing, beard displays, colour changes (darker when cold or stressed, brighter when healthy), and glass-surfing are endlessly fascinating to observe and learn to interpret. My beardie Blaze is 8 years old, still healthy, and still surprises me with new behaviours. An extraordinary animal.'),
            (4, 'Calm and manageable, even for kids', 'I was nervous about getting a reptile as a first exotic pet, but my bearded dragon has been the ideal introduction. He\'s never bitten, scratched, or struggled when held. He does need daily feeding and vivarium checks but the routine is satisfying rather than burdensome. He waves at me every morning which genuinely never gets old. Highly recommend for first-time reptile keepers.'),
            (5, 'Healthy with proper care — 12 years and counting', 'My bearded dragon is 12 years old and still going strong. Proper husbandry — correct temperatures, high-quality UVB, varied diet of gut-loaded insects and fresh greens, annual vet check-ups — keeps reptiles healthy for a very long time. She shed perfectly last month and still has a great appetite. A testament to what good reptile care can achieve. Wonderful animals.'),
        ],
    },
    'Leopard Gecko': {
        'slug': 'leopard-gecko',
        'wiki_title': 'Leopard gecko',
        'description': (
            'The leopard gecko is arguably the most popular gecko species kept in captivity, '
            'prized for its beautiful spotted pattern, manageable size, and gentle, easy-going temperament. '
            'Unlike many lizards, they do not require UVB lighting (though it\'s beneficial), '
            'making their setup more forgiving for beginners. They are nocturnal and live 15–20 years in captivity.'
        ),
        'pros': [
            'Beginner-friendly — no UVB strictly required',
            'Calm, rarely aggressive, and easy to handle',
            'Beautiful spotted/patterned appearance in many morphs',
            'Quiet and odourless — ideal for flat living',
            'Exceptionally long-lived (15–20 years)',
        ],
        'cons': [
            'Nocturnal — most active in the evening and night',
            'Requires live insects (mealworms, crickets, dubia roaches)',
            'Cannot regrow tail bone if tail is dropped — only cartilage regrows',
            'Cold-blooded — needs a thermal gradient in the enclosure',
        ],
        'reviews': [
            (5, 'Perfect beginner reptile', 'My leopard gecko was my gateway into reptile keeping and he\'s been an ideal introduction. He\'s calm, curious, and has learned to walk onto my hand voluntarily. The setup was straightforward and affordable compared to larger reptiles. He hunts mealworms with the most focused, intense expression — hilarious to watch. He\'s been healthy for six years with zero vet visits beyond check-ups. Brilliant first reptile.'),
            (5, 'Beautiful and surprisingly interactive', 'Leopard geckos have far more personality than I expected. My gecko Spots comes to the front of her enclosure when she hears me, investigates everything I put in her tank, and occasionally licks my hand as if to taste the world. The range of colour morphs available is extraordinary — I went with a tangerine morph and she\'s absolutely stunning. A wonderful, low-maintenance reptile pet.'),
            (4, 'Calm and easy, great for nervous first-timers', 'I was nervous about keeping a reptile for the first time but my leopard gecko has been perfect. He\'s never tried to escape or shown any aggression. I handle him for 15 minutes most evenings and he just explores my hands calmly. The setup is simpler than most reptiles — a 60cm tank with undertank heating and hides is the basic requirement. Very manageable for a beginner.'),
            (5, 'Live 15-20 years — proper long-term companion', 'My leopard gecko is 14 years old. Fourteen years. She\'s still healthy, active at night, and has the same curious personality she\'s always had. The long lifespan of this species is one of their best features — you genuinely develop a lasting relationship over the years. She\'s survived three house moves and seems completely unfazed by life. An extraordinary, enduring companion.'),
            (4, 'Evening activity is really fun to watch', 'As a night owl myself, having a nocturnal pet works perfectly. My gecko comes alive around 8–9pm, starts exploring her vivarium, hunting, and climbing. I set her tank up near my desk so I can watch her while I work in the evenings. She\'s graceful, quick, and fascinating to observe. The only downside is the need for live insects — I maintain a mealworm colony to keep costs down.'),
            (3, 'Live food is the main challenge', 'Leopard geckos need live insects and won\'t consistently eat dead prey. Maintaining a feeder insect supply (I use mealworms and crickets) adds a layer of management I wasn\'t fully prepared for. The insects themselves need feeding and housing. Once the routine is established it\'s fine, but new owners should factor in the ongoing live food requirement. The gecko herself is wonderful — calm, healthy, and beautiful.'),
            (5, 'Stunning morphs available', 'The variety of leopard gecko morphs (colour and pattern mutations) is extraordinary. I have a blizzard morph that is almost completely white with pale lavender undertones — she looks otherworldly. Beyond the aesthetics she\'s calm, healthy, and has been a fantastic pet for eight years. If you appreciate beautiful animals, leopard geckos have some of the most spectacular captive-bred colour variations of any reptile.'),
            (4, 'Ideal apartment reptile', 'Living in a flat, I needed a quiet, compact, low-odour pet. My leopard gecko ticks every box. He\'s silent, produces minimal waste, his 60cm tank fits neatly on a shelf, and he doesn\'t smell at all with weekly spot cleans. He\'s been with me four years and has brought so much joy. The evening activity is genuinely relaxing to watch — far better than anything on TV.'),
        ],
    },
    'Ball Python': {
        'slug': 'ball-python',
        'wiki_title': 'Ball python',
        'description': (
            'The ball python is the most commonly kept pet snake in the world, '
            'named for its defensive habit of curling into a tight ball when threatened. '
            'They are docile, slow-moving, and available in hundreds of captive-bred colour morphs. '
            'Adults typically reach 1.2–1.5m and live 20–30 years with proper care, making them a serious long-term commitment.'
        ),
        'pros': [
            'Docile and calm — rarely aggressive',
            'Slow-moving and manageable to handle',
            'Hundreds of colour and pattern morphs available',
            'Incredibly long-lived (20–30 years)',
            'Feed on frozen/thawed mice or rats — no live prey needed',
        ],
        'cons': [
            'Can go on feeding strikes for weeks or months — stressful for new keepers',
            'Require carefully maintained temperature and humidity',
            'Long lifespan means a decades-long commitment',
            'Some people uncomfortable with snake ownership',
        ],
        'reviews': [
            (5, 'The most chill reptile I\'ve ever kept', 'My ball python is the most relaxed, easy-going animal imaginable. She barely moves during the day (they\'re nocturnal), but in the evening she explores my arms, drapes herself across my shoulders, and seems completely unbothered by handling. She\'s never struck, musked, or shown any aggression in three years. Feed her a frozen rat every 7–10 days, maintain humidity, and she asks for nothing else. Perfect.'),
            (5, 'Changed my mind about snakes entirely', 'I was terrified of snakes until a friend let me hold their ball python. The warm, dry, smooth scales and the calm, curious way it explored my arm completely reframed how I thought about snakes. I got my own within a month. Three years on, I have two and they\'re my favourite pets. Ball pythons make excellent ambassadors for snake keeping — they\'re gentle, beautiful, and endlessly fascinating.'),
            (4, 'Feeding strikes can be nerve-wracking', 'Ball pythons are wonderful but feeding strikes are a real thing. My snake refused food for 14 weeks in winter, which I later learned is common during the cooler months. Once I raised the hot spot temperature and improved humidity, she resumed eating. New keepers need to understand this behaviour is normal and not immediately a veterinary emergency. Do your research — feeding strikes cause unnecessary panic in unprepared owners.'),
            (5, 'Stunning morphs at every price point', 'The variety of ball python morphs is extraordinary — I have a pastel spider morph with gold and white patterning that draws gasps every time people see her. The captive breeding industry produces new morphs every year. You can get beautiful ball pythons at accessible prices or invest in rare, high-end morphs depending on your budget. Beyond the looks, they\'re wonderfully easy-going snakes.'),
            (4, 'Great for adults, not for impatient people', 'Ball pythons are brilliant pets but require patience. They hide for days at a time (especially after feeding or during shedding), can go weeks without eating, and are most active when you\'re asleep. If you want a pet you can display constantly, a ball python isn\'t it. If you enjoy observing secretive, beautiful animals on their own schedule, they\'re magnificent. I love mine dearly but manage my expectations.'),
            (3, 'Humidity management is harder than expected', 'Ball pythons require 60–80% humidity, which is genuinely challenging in a dry climate. I went through three different enclosure setups before achieving consistent humidity levels. A well-sealed tub enclosure with humid substrate finally solved the problem. Before getting a ball python, research enclosure options thoroughly — cheap glass vivariums with front ventilation are often unsuitable without significant modification.'),
            (5, 'My 20-year companion', 'My ball python turned 20 this year and is still in perfect health, eating well, and shedding cleanly. Twenty years is a serious relationship with an animal. She was hatched in 2005, has been with me through three homes, a marriage, and raising children. The kids grew up with her and respect her completely. A ball python purchased today could genuinely still be with you in 2045. An extraordinary commitment that rewards in kind.'),
            (4, 'Frozen prey is a genuine advantage', 'Unlike many reptiles, ball pythons readily accept frozen/thawed rodents, which removes all the ethical concerns and management headaches of live prey. I order frozen feeder rats online in bulk and thaw them as needed. No live animal storage, no risk to the snake from struggling prey, and complete diet control. The snake herself doesn\'t care — she strikes frozen prey with the same enthusiasm as anything else.'),
        ],
    },
    'Corn Snake': {
        'slug': 'corn-snake',
        'wiki_title': 'Corn snake',
        'description': (
            'The corn snake is widely regarded as the ideal beginner snake — '
            'it is slender, manageable in size (1–1.5m), docile, and easy to care for. '
            'Native to the southeastern United States, corn snakes are excellent climbers and come in a dazzling array of captive-bred colour morphs. '
            'They live 15–20 years and are forgiving of minor husbandry imperfections.'
        ),
        'pros': [
            'Widely considered the best beginner snake',
            'Docile and rarely bites even when young',
            'Slender and manageable — not intimidating to handle',
            'Wide range of beautiful colour morphs',
            'Forgiving of minor husbandry variations',
        ],
        'cons': [
            'Escape artists — enclosure must be completely secure',
            'Nocturnal and secretive — often hidden during the day',
            'Require frozen/thawed mice regularly',
            'Long lifespan (15–20 years) — a significant commitment',
        ],
        'reviews': [
            (5, 'The perfect beginner snake — no question', 'Corn snakes have a well-earned reputation as the ideal beginner reptile. My first snake was a corn snake at 16 years old and she\'s now 12 years old, healthy, and as curious as ever. She\'s never bitten me, never struck defensively, and handles beautifully. Feed her a frozen mouse every 10–14 days, keep humidity moderate, and she\'s the most low-maintenance, rewarding pet imaginable. Start with a corn snake.'),
            (5, 'Stunning colours, great personality', 'My amelanistic corn snake is a cascade of orange, red, and white that looks almost unreal. The captive-bred morph variety is incredible — I spent weeks choosing my favourite. Beyond the looks, she has a wonderful exploratory personality, investigating every new environment with her tongue flickering constantly. She\'s been with me seven years and every handling session is a pleasure.'),
            (4, 'Escape artist — get a secure enclosure', 'Corn snakes are notorious escape artists and my first snake confirmed this. She found a gap in the lid of her first enclosure within a week and disappeared for three days before I found her behind the bookcase. I immediately upgraded to a purpose-built reptile enclosure with clip-lock lids. Since then, zero escapes in five years. The snake herself is wonderful — just take escape-proofing seriously before you bring one home.'),
            (5, 'Great introduction to snake keeping for the whole family', 'My teenage children were interested in snakes and a corn snake was the perfect introduction. It\'s slender enough not to be intimidating, completely docile, and handles beautifully. Both my kids now handle it confidently and have learned so much about reptile biology. Our corn snake is four years old, healthy, and has never shown any aggression. A brilliant family reptile for anyone curious about snakes.'),
            (4, 'Nocturnal but fun to watch at dusk', 'Corn snakes are most active around dusk and dawn, which works well for me. I sit near her enclosure in the evenings and watch her explore, climb, and flick her tongue at everything. It\'s surprisingly meditative. She comes out of her hide as the lights dim and explores for hours. During the day she\'s curled in her hide, which can disappoint some owners — just understand this is normal snake behaviour.'),
            (3, 'Went off food for two months', 'My corn snake had a feeding strike for eight weeks in late autumn. I later learned this is very common — corn snakes from temperate climates often go through a natural cooling period. Once I slightly lowered enclosure temperatures and waited, she resumed eating enthusiastically. The two months of anxiety were unnecessary — it\'s completely normal but nobody told me beforehand. Research the natural feeding cycle before panicking.'),
            (5, 'Long-lived and consistently lovely', 'My corn snake is 15 years old and still going strong. She sheds cleanly, eats regularly (though less frequently than she used to), and is as gentle as ever. The 15–20 year lifespan is one of the great pleasures of corn snake keeping — you develop a genuine long-term bond. She\'s lived through three house moves and remained completely calm throughout. A wonderful, enduring reptile companion.'),
            (4, 'Affordable and accessible', 'Corn snakes are among the most accessible pet snakes. The animals themselves are reasonably priced, standard captive-bred morphs are widely available, and the setup costs are far lower than larger reptiles like boa constrictors. A 90cm enclosure (they rarely exceed 1.5m), basic heat mat, thermostat, and hides is all you really need. For anyone curious about snake keeping, corn snakes offer the full experience without the complexity.'),
        ],
    },
    'Blue-Tongued Skink': {
        'slug': 'blue-tongued-skink',
        'wiki_title': 'Blue-tongued skink',
        'description': (
            'Blue-tongued skinks are large, robust lizards named for their striking blue tongues, '
            'which they display as a defence mechanism against predators. '
            'Native to Australia and Indonesia, they are among the most docile and handleable of all pet lizards, '
            'with an omnivorous diet and a lifespan of 15–20 years.'
        ),
        'pros': [
            'Exceptionally docile — one of the calmest pet lizards',
            'Omnivorous — variety of foods including vegetables, fruits, and protein',
            'Impressive blue tongue display is fascinating to see',
            'Hardy and forgiving of beginner husbandry mistakes',
            'Long lifespan of 15–20 years',
        ],
        'cons': [
            'Large adult size (45–60cm) requires a substantial vivarium',
            'Need UVB lighting and a thermal gradient',
            'Requires varied diet — more complex feeding than insect-only reptiles',
            'Specialist reptile vet required for health care',
        ],
        'reviews': [
            (5, 'Absolutely love this species', 'Blue-tongued skinks are the best kept secret in the reptile hobby. Mine is calm, handleable, and genuinely seems to tolerate (maybe even enjoy) human interaction. The blue tongue display when she\'s startled is genuinely spectacular — a flash of vivid blue that would startle any predator. She eats a varied diet of lean protein, vegetables, and occasional fruit, which makes feeding enjoyable. An extraordinary lizard.'),
            (5, 'The most handleable lizard I\'ve kept', 'I\'ve kept bearded dragons, blue-tongues, and monitor lizards, and my blue-tongued skink is by far the easiest to handle. She barely reacts to being picked up, sits calmly on my lap, and investigates my hands with her tongue. She has never bitten, scratched, or tried to escape in three years of ownership. If you want a handleable, impressive lizard that\'s manageable for beginners, nothing beats a blue-tongue.'),
            (4, 'Omnivorous diet is complex but rewarding', 'Blue-tongued skinks eat a varied omnivorous diet — vegetables, fruits, lean meats, dog food (high-quality), insects — which requires more thought than an insect-only reptile. I rotate vegetables, add protein sources, and offer fruit as an occasional treat. Getting the diet right takes research, but it\'s actually enjoyable to vary their meals. My skink has a genuine food vocabulary: she comes immediately for blueberries but turns her nose up at bitter greens.'),
            (5, 'Fascinates every visitor', 'Every time someone visits, they end up fascinated by my blue-tongued skink. The vivid blue tongue display when she\'s curious (not even defensive — she does it when exploring) stops people in their tracks. She\'s calm enough to pass around for handling and patient with people who\'ve never held a lizard. She\'s been a wonderful ambassador for reptile keeping — more people have overcome their reptile fears through meeting her than any other animal I\'ve kept.'),
            (4, 'Big enclosure needed — plan ahead', 'Blue-tongued skinks grow to 45–60cm as adults and need a large vivarium — minimum 120cm × 60cm, ideally larger. I started with a smaller enclosure for my juvenile and had to upgrade, which involved extra cost. Buy the adult-sized enclosure from the start — it\'s more economical. Once properly housed, my skink has thrived. She uses every corner of her vivarium and is clearly more active with the additional space.'),
            (3, 'Finding a good vet is challenging', 'Blue-tongued skinks require specialist reptile veterinary care. I had to drive 40 minutes to find a vet experienced with skinks. This is a real consideration before getting any exotic reptile — check that you have access to specialist care before committing. My skink has been healthy, but knowing a good reptile vet is available before you need one is essential. The animal itself is wonderful, but do your preparatory homework.'),
            (5, 'Heavy, warm, and wonderfully calm', 'What I love most about my blue-tongued skink is the weight of her — she\'s 450g and feels substantial and warm when she settles on my arm. Unlike delicate geckos or snakes, she feels robust and secure. She explores slowly and methodically, investigating everything with her flickering blue tongue. After four years she recognises my voice and comes to be let out every evening. A truly exceptional reptile companion.'),
            (4, 'Longer-lived than most realise', 'Blue-tongued skinks live 15–20 years in captivity. Mine is 11 years old, still active, still eating well, and still the same curious personality. The long lifespan is both a joy and a commitment — you\'re taking on a 15–20 year responsibility when you get a blue-tongue. Factor this in carefully. But the relationship that develops over a decade and more with such an intelligent, responsive reptile is genuinely special.'),
        ],
    },
}


def get_wiki_image(title: str, size: int = 500) -> str | None:
    params = {
        'action': 'query',
        'titles': title,
        'prop': 'pageimages',
        'pithumbsize': size,
        'format': 'json',
    }
    try:
        resp = SESSION.get('https://en.wikipedia.org/w/api.php', params=params, timeout=15)
        if resp.status_code == 429:
            logger.warning('Wikipedia 429, sleeping 5s...')
            time.sleep(5)
            resp = SESSION.get('https://en.wikipedia.org/w/api.php', params=params, timeout=15)
        data = resp.json()
        for page in data.get('query', {}).get('pages', {}).values():
            src = page.get('thumbnail', {}).get('source')
            if src:
                return re.sub(r'/\d+px-', f'/{size}px-', src)
    except Exception as e:
        logger.warning(f'Wiki API error for {title!r}: {e}')
    return None


def try_commons_image(query: str, size: int = 500) -> str | None:
    params = {
        'action': 'query',
        'list': 'search',
        'srsearch': query,
        'srnamespace': 6,
        'srlimit': 5,
        'format': 'json',
    }
    try:
        resp = SESSION.get('https://commons.wikimedia.org/w/api.php', params=params, timeout=15)
        if resp.status_code == 429:
            time.sleep(5)
            resp = SESSION.get('https://commons.wikimedia.org/w/api.php', params=params, timeout=15)
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
            logger.warning(f'HTTP {resp.status_code} for {url}')
            return False
        content = resp.content
        if len(content) < 3000:
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

        sub = SubCategory.query.filter_by(category_id=animals_cat.id, slug='reptiles').first()
        if not sub:
            sub = SubCategory(category_id=animals_cat.id, name='Reptiles', slug='reptiles')
            db.session.add(sub)
            db.session.flush()
            logger.info("Created Reptiles subcategory")
        else:
            logger.info("Reptiles subcategory already exists")

        total_reviews = 0
        for name, data in REPTILE_DATA.items():
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
                img_url = get_wiki_image(data['wiki_title']) or try_commons_image(f"{name} pet reptile")
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
            slate_url = get_wiki_image('Bearded dragon') or try_commons_image('pet reptile lizard')
            if slate_url:
                dest = os.path.join(defaults_dir, 'reptiles.jpg')
                if download_image(slate_url, dest):
                    sub.image_path = 'images/defaults/reptiles.jpg'
                    logger.info("Saved Reptiles slate image")
            time.sleep(2)

        db.session.commit()
        logger.info(f"\nDone. {len(REPTILE_DATA)} reptile species, {total_reviews} reviews.")


if __name__ == '__main__':
    main()
