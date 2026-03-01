"""
Add a Horses subcategory to Animals with 5 breeds, reviews, and images.
Safe to run multiple times — skips existing records.

Usage:
  python3 add_horses.py
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
    'Bold', 'Swift', 'Brave', 'Noble', 'Wild', 'Free', 'Proud', 'Gallant',
    'Steady', 'Loyal', 'Fierce', 'Graceful', 'Mighty', 'Spirited', 'Gentle',
]
_ANIMALS = [
    'Stride', 'Mane', 'Canter', 'Gallop', 'Hoof', 'Bridle', 'Saddle',
    'Pasture', 'Stallion', 'Mare', 'Foal', 'Trot', 'Crest', 'Flank', 'Gait',
]


def _rnd_name(rng: random.Random) -> str:
    return f"{rng.choice(_ADJECTIVES)}{rng.choice(_ANIMALS)}{rng.randint(10, 99)}"


HORSE_DATA: dict[str, dict] = {
    'Thoroughbred': {
        'slug': 'thoroughbred',
        'wiki_title': 'Thoroughbred',
        'description': (
            'The Thoroughbred is the world\'s preeminent racehorse, bred over centuries in England for speed and stamina. '
            'Known for their lean, athletic build, high spirit, and exceptional athleticism, they excel not only in racing '
            'but also in show jumping, eventing, and dressage. They require experienced handlers and plenty of exercise.'
        ),
        'pros': [
            'Exceptionally athletic and fast — peak performance horses',
            'Intelligent, sensitive, and responsive to skilled riders',
            'Successful in many disciplines beyond racing',
            'Deep bond with experienced riders who earn their trust',
            'Many off-the-track Thoroughbreds (OTTBs) make wonderful second-career horses',
        ],
        'cons': [
            'High-spirited and hot-blooded — not suitable for beginners',
            'Require significant daily exercise and turnout',
            'Prone to certain health issues including gastric ulcers and leg injuries',
            'Can be anxious and sensitive — needs patient, experienced handling',
        ],
        'reviews': [
            (5, 'The most electric horse I\'ve ever ridden', 'My off-the-track Thoroughbred Quicksilver took two years to fully transition from racing to a relaxed amateur competition horse. The patience was worth every moment. He is the most responsive, electric horse I\'ve ever ridden — a feather-touch cue and he responds instantly. He placed second at his first dressage competition last month. OTTBs get a bad reputation for being difficult, but with the right approach they are extraordinary partners.'),
            (5, 'My OTTB changed my riding forever', 'I\'ve ridden warmbloods, cobs, and Iberian horses, but my Thoroughbred taught me to ride with true lightness. He doesn\'t tolerate heavy hands or sloppy aids — he demands precision. That discipline made me a genuinely better rider. He\'s been with me six years, competes in eventing, and still takes my breath away galloping cross-country. A transformative horse.'),
            (4, 'Brilliant but needs experienced handling', 'Thoroughbreds are not beginners\' horses and I say that with deep admiration for the breed. My mare is intelligent, sensitive, and communicates clearly when something is wrong. Getting her ulcer management and turnout routine exactly right took a year of trial and error. Once everything was optimised she blossomed into the most willing, elegant horse. But she would be genuinely dangerous in the wrong hands.'),
            (5, 'Speed is just the beginning', 'What surprises people about Thoroughbreds is how much more there is beyond speed. My gelding has the most refined, expressive movement of any horse I\'ve owned. In the arena he floats. On trails he\'s sensible and curious. He\'s taught me to feel subtleties in movement I never noticed before. People who dismiss the breed as "hot and difficult" are missing one of the most remarkable horses in the world.'),
            (4, 'OTTB adoption is incredibly rewarding', 'I adopted my Thoroughbred from a racing rehoming organisation and the transition process was a genuine journey. He arrived underweight, anxious, and confused by a world without starting gates and crowds. Eight months of careful retraining, correct feeding, and consistent routine turned him into a confident, happy horse. He now competes in showjumping and loves his job. The OTTB adoption journey is real work, but the horse at the end of it is extraordinary.'),
            (3, 'Wonderful horse, significant management needs', 'My Thoroughbred mare is brilliant in so many ways but her management needs are substantial. Gastric ulcers required specialist veterinary intervention. She needs at minimum four hours of turnout daily. She loses condition quickly in winter. She doesn\'t tolerate changes in routine well. I manage all of this willingly because she\'s a remarkable athlete, but prospective Thoroughbred owners should understand the time and cost commitment before taking one on.'),
            (5, 'Nothing compares in the eventing arena', 'I\'ve competed in eventing for fifteen years on various breeds. My Thoroughbred is the best cross-country horse I\'ve ever ridden — bold, honest, and absolutely electric across a course of fences. He reads the terrain instinctively, backs himself at challenging combinations, and comes home with ears pricked. The TB heart — the willingness to give everything — is something the breed carries in its DNA. An extraordinary competition horse.'),
            (4, 'Sensitive and intelligent — demands respect', 'The Thoroughbred is the most sensitive horse I\'ve worked with and I mean that as a profound compliment. My gelding is finely tuned — he responds to breathing, weight, and the subtlest leg position. He also communicates clearly when uncomfortable, anxious, or in pain. Learning to listen to him has made me a genuinely better horsewoman. He\'s not a horse for everyone, but for the right rider he\'s a privilege to own.'),
            (5, 'Fifteen years together — an irreplaceable partnership', 'My Thoroughbred mare has been with me for fifteen years. I bought her as a four-year-old fresh off the track and we\'ve competed through every level of eventing together. She\'s 19 now and retired to hacking and light schooling. The relationship we\'ve built — the trust, the communication, the wordless understanding — is the most meaningful relationship of my riding life. Thoroughbreds give everything. The least you can do is give the same back.'),
        ],
    },
    'Arabian': {
        'slug': 'arabian',
        'wiki_title': 'Arabian horse',
        'description': (
            'The Arabian is one of the oldest horse breeds in the world, developed on the Arabian Peninsula over thousands of years. '
            'Instantly recognisable by their dished face, arched neck, and high tail carriage, '
            'Arabians are renowned for extraordinary endurance, intelligence, and a unique bond with their human companions. '
            'They excel in endurance riding, showing, and as devoted personal mounts.'
        ),
        'pros': [
            'Exceptional stamina — dominant in endurance riding worldwide',
            'Deep intelligence and bond with their person — almost dog-like loyalty',
            'Striking, distinctive beauty unlike any other breed',
            'Naturally efficient metabolisms — often easier to condition than heavier breeds',
            'Long lifespan — often ridden well into their twenties',
        ],
        'cons': [
            'High-spirited and sensitive — not ideal for inexperienced riders',
            'Can be dramatic and spooky in new environments',
            'Require significant mental stimulation — get bored with repetitive work',
            'Metabolic sensitivity — careful diet management needed',
        ],
        'reviews': [
            (5, 'The most beautiful horse on earth', 'I\'ve admired Arabians my entire life and finally bought my first at 35 years old. The reality exceeded every expectation. My mare\'s presence is extraordinary — dished face, enormous dark eyes, arched neck, tail flagged high. But beyond the beauty she has a mind and personality unlike any horse I\'ve encountered. She\'s opinionated, curious, and has bonded to me with an intensity I wasn\'t prepared for. She calls for me every morning.'),
            (5, 'Endurance champion — 10 years competing', 'My Arabian Shaheen has completed over 8,000 competition miles in endurance riding. The breed\'s stamina and metabolic efficiency are genuinely extraordinary — he recovers faster than horses half his age. He\'s 21 now and still competing at 80-mile events. The Arabian endurance community is passionate and knowledgeable, and the breed dominates the sport globally for good reason. An incomparable endurance partner.'),
            (4, 'Brilliant mind, needs stimulation', 'Arabians are not a horse you can park in a field and ignore. My gelding needs daily mental stimulation — varied schooling, trail rides, new challenges. When bored or under-exercised, he becomes creative in ways that test every fence in the field. When properly occupied he\'s the most engaged, willing, and delightful horse. The intelligence that can be challenging is also what makes riding an Arabian so deeply rewarding.'),
            (5, 'Bond unlike any other breed', 'The Arabian\'s relationship with humans is genuinely different from other breeds. My mare follows me around without a lead rope, comes when called from across the field, and has an almost telepathic sensitivity to my emotions. When I\'m stressed she\'s unsettled; when I\'m calm she relaxes. Riding her feels like a conversation rather than a directive. The ancient partnership between Arabian horses and their Bedouin companions produced something genuinely unique in the horse world.'),
            (4, 'Requires an experienced, quiet rider', 'My Arabian cross-trains in dressage and trail riding. He\'s brilliant at both, but requires a confident, quiet rider. He amplifies any tension or uncertainty in the saddle instantly. With correct, calm riding he\'s light, responsive, and a genuine joy. With an anxious or heavy-handed rider he becomes difficult quickly. The breed rewards skilled horsemanship with an exceptional partnership, but punishes poor riding equally efficiently.'),
            (3, 'Spectacular but can be dramatic', 'I love my Arabian unreservedly but I\'m honest that he can be deeply dramatic. A plastic bag three fields away will spin him in circles. A sudden noise brings his tail up and his feet dancing. He\'s never put me on the floor in six years, but he\'s made me work for it on several occasions. With patient, consistent training the spookiness is manageable. But new Arabian owners should be prepared for a horse with a very strong opinion about the world.'),
            (5, 'Long-lived and passionate about life', 'My Arabian is 24 years old and still the most exuberant horse in the yard. He flat-out gallops in from the field every morning, bucks for joy after a good schooling session, and approaches everything with the enthusiasm of a four-year-old. The breed\'s longevity is remarkable — Arabians ridden well into their late twenties are not unusual. He\'s been my main competition horse for 16 years and I intend to hack him into his thirties.'),
            (4, 'Showing Arabians is its own wonderful world', 'Arabian showing — particularly in-hand and native costume classes — is a spectacular, passionate community. My mare is a successful halter horse whose presence in the ring genuinely stops people. Presenting an Arabian in top condition, with her coat gleaming and tail flagged, is one of the most satisfying experiences in the equine world. The breed is shown to its extraordinary beauty and the community of Arabian enthusiasts is among the most dedicated in horse sport.'),
        ],
    },
    'Quarter Horse': {
        'slug': 'quarter-horse',
        'wiki_title': 'American Quarter Horse',
        'description': (
            'The American Quarter Horse is the most popular horse breed in the United States and one of the most versatile in the world. '
            'Named for their unmatched speed over a quarter-mile, they excel in western riding disciplines, ranch work, barrel racing, and trail riding. '
            'Their calm, willing temperament makes them suitable for riders of all experience levels.'
        ),
        'pros': [
            'Extremely versatile — excels in western, ranch, trail, and many other disciplines',
            'Generally calm and sensible temperament — suitable for beginners',
            'Quick to learn and willing to please',
            'Compact, muscular build well-suited to western work',
            'The most registered breed in the world — enormous support community',
        ],
        'cons': [
            'Prone to certain genetic conditions including HYPP and GBED',
            'Can become bored and lazy if not given enough varied work',
            'Heavily muscled individuals can be prone to tying-up (exertional rhabdomyolysis)',
            'Quarter Horse bloodlines vary enormously — research lineage carefully',
        ],
        'reviews': [
            (5, 'The perfect all-around horse', 'My Quarter Horse Dusty has done trail riding, western pleasure, ranch sorting, and barrel racing in the twelve years I\'ve owned him. He switches between disciplines without missing a beat. He\'s been ridden by my teenagers learning to ride, my experienced adult friends at speed across open country, and my elderly neighbour on gentle walks. The versatility and calm temperament of the breed are genuinely unmatched.'),
            (5, 'Best first horse for a beginner', 'I bought my Quarter Horse as a completely green adult beginner and she has been the most patient, forgiving teacher imaginable. She\'s never spooked me off, tolerates my inconsistent aids with good humour, and gets excited for every ride. Three years later I\'m confidently trail riding in the mountains and starting western pleasure lessons. I couldn\'t have asked for a better introduction to horse ownership.'),
            (4, 'Outstanding western performance horse', 'My cutting-bred Quarter Horse has cattle sense that seems to come from deep in his DNA — he anticipates the cow\'s movement almost before I process it. He\'s won consistently in ranch sorting and cutting competitions. The athleticism and quickness of a well-bred working Quarter Horse is extraordinary. Training with experienced western handlers has been essential, but the raw ability was already there in the bloodline.'),
            (5, 'Solid, reliable trail partner', 'My Quarter Horse mare has covered thousands of miles of trail over ten years. She\'s crossed water, navigated mountain terrain, and stood calm while deer crashed through the brush nearby. Her steady, sensible temperament is the foundation of everything. After a long week I can throw a saddle on her and just ride — no drama, no anxiety, just a horse and rider moving through the world together. Invaluable.'),
            (4, 'Incredibly willing — loves to work', 'Quarter Horses genuinely seem to enjoy having a job. My gelding comes to the gate when he sees me carrying the saddle — he wants to work. He tries hard at everything I ask, learns new things quickly, and seems happy and settled when properly occupied. He does need consistent work; a few days off and he has more energy than is comfortable in the arena. Keep him busy and he\'s the perfect horse.'),
            (3, 'Check the bloodlines for genetic conditions', 'My Quarter Horse is wonderful but I wish I\'d researched genetic conditions before buying. Heavy Impressive-bred bloodlines carry HYPP risk. I bought my horse without doing genetic testing and he has N/H HYPP, which requires careful diet management and monitoring. He lives a happy, manageable life, but the condition was avoidable with a genetic test before purchase. Always test Quarter Horses before buying — it\'s inexpensive and could save significant heartache.'),
            (5, 'Barrel racing machine', 'My barrel racing Quarter Horse is the most athletically gifted horse I\'ve owned. She turns barrels with power and precision that comes from years of careful training and natural ability. Her quarter-mile acceleration is breathtaking — you feel the gear-change when she opens up. She\'s competitive at regional level and still improving at nine years old. The working Quarter Horse\'s athleticism for speed events is genuinely spectacular.'),
            (4, 'Great family horse', 'We keep three Quarter Horses for the whole family — myself, my husband, and our children aged 10 and 14. All three are safe enough for the children to handle and exciting enough to keep the adults engaged. The breed\'s range from very quiet to quite athletic means you can find exactly the right individual for each rider. For a family wanting to ride together across different levels, Quarter Horses are ideal.'),
            (5, 'Twenty years and still going', 'My Quarter Horse is 25 years old and still sound and happy. He gets light hacking and arena work two to three times a week and seems to love every minute of it. His calm, sensible nature hasn\'t changed in all the years I\'ve known him. He\'s seen my children learn to ride, my grandchildren take their first sits on a horse, and has never put a foot wrong. An incomparable family heirloom of a horse.'),
        ],
    },
    'Friesian': {
        'slug': 'friesian',
        'wiki_title': 'Friesian horse',
        'description': (
            'The Friesian is a striking Dutch breed, instantly recognisable by its jet-black coat, '
            'flowing mane and tail, feathered lower legs, and powerful yet elegant movement. '
            'Historically used as war horses and carriage horses in the Netherlands, '
            'they are now popular in dressage, driving, film, and as spectacular leisure horses. '
            'They are known for their gentle, willing temperament despite their impressive presence.'
        ),
        'pros': [
            'Breathtaking appearance — black coat, flowing mane, and feathered feet',
            'Gentle, willing temperament despite impressive size',
            'Expressive, elevated gaits — naturally suited to collection',
            'Loyal and people-oriented — love human interaction',
            'Spectacular in dressage, driving, and ceremonial work',
        ],
        'cons': [
            'Prone to several breed-specific health conditions (hydrocephalus, megaoesophagus, dwarfism)',
            'Feathered legs require significant grooming and can harbour skin conditions',
            'Shorter average lifespan than many breeds (~16 years)',
            'KFPS studbook registration important for breeding quality — research lineage',
        ],
        'reviews': [
            (5, 'The most magnificent horse I\'ve ever seen', 'Nothing prepares you for seeing a Friesian in person for the first time. My stallion Nero moves as if he\'s been choreographed — elevated trot, arched neck, mane and tail flowing — and people genuinely stop and stare wherever we go. Beyond the spectacle, he has the most gentle, affectionate nature. He nudges my pockets for treats and grooms my jacket when I\'m tacking him up. A breathtaking animal.'),
            (5, 'My Friesian mare is my dream horse', 'I saved for eight years to buy my Friesian mare and she has exceeded every expectation. She\'s powerful and expressive in the arena, completely calm on trail rides, and the most human-focused horse I\'ve ever owned. She comes to me in the field without being caught, stands perfectly for grooming (which is extensive with all that mane), and has never shown a moment of genuine nastiness. She\'s the horse I\'ve dreamed of since childhood.'),
            (4, 'Grooming commitment is real', 'Friesians are gloriously beautiful and that beauty has a price — grooming. The feathered legs need thorough cleaning and drying after wet weather to prevent mud fever and skin conditions. The mane and tail require regular conditioning to stay untangled and lustrous. My mare gets two to three hours of detailed grooming per week minimum. I enjoy it as bonding time, but prospective Friesian owners must understand the commitment involved.'),
            (5, 'Born to do dressage', 'My Friesian gelding has the most naturally elevated, expressive trot I\'ve encountered. He moves with a natural cadence and suspension that warmbloods trained for years to achieve from birth. His collection is effortless. We\'ve competed successfully through Medium dressage and his passage work is developing beautifully. The Friesian\'s historical training in classical horsemanship is embedded in the breed — you can feel it in every movement.'),
            (4, 'Gentle giant with enormous personality', 'Friesians are large horses (my gelding is 16.3hh and heavily built) but their temperament is surprisingly gentle and people-oriented. He\'s curious about everything and everyone, stands quietly for children to stroke him, and seems to genuinely enjoy the attention he attracts. He does require confident handling — he\'s powerful and can be over-enthusiastic — but he\'s never deliberately dangerous. A wonderful ambassador for the breed.'),
            (3, 'Health issues are a real consideration', 'I love my Friesian unconditionally but the breed\'s health challenges are real. My mare has megaoesophagus (a known Friesian condition) which requires careful management of her feed consistency and presentation. She also has sweet itch affecting her legs. The vet bills have been significant. Research Friesian-specific health conditions thoroughly and find a vet experienced with the breed before committing to ownership.'),
            (5, 'Film-worthy presence that\'s equally lovely in person', 'Friesians appear in countless films and productions because they look extraordinary on camera. My gelding has the same effect in person — people photograph him wherever we go. What they can\'t capture in photos is his personality: the nicker when he sees me, the way he leans into grooming brushes, the enthusiasm he shows for a gallop in open pasture. The presence is real, but the character is what makes him irreplaceable.'),
            (4, 'Driving a Friesian is spectacular', 'I drive my Friesian mare in a traditional Dutch carriage and the combination is simply spectacular. Her elevated, expressive trot and the dramatic black-and-feather aesthetic in harness draws crowds at every show. She\'s a willing and responsive driving horse who has taken to the discipline beautifully. For anyone interested in carriage driving, a Friesian is an extraordinary partner — the breed has centuries of carriage work in its heritage.'),
        ],
    },
    'Shetland Pony': {
        'slug': 'shetland-pony',
        'wiki_title': 'Shetland pony',
        'description': (
            'The Shetland pony is a small, hardy breed originating from the Shetland Islands of Scotland. '
            'Despite standing at just 28–42 inches, they are extraordinarily strong for their size '
            'and have incredible stamina. Famous as children\'s riding ponies and in leadrein classes, '
            'they also have a reputation for formidable personalities — strong-willed and sometimes outwitting their handlers.'
        ),
        'pros': [
            'Hardy and extremely strong for their tiny size',
            'Long lifespan (25–30+ years)',
            'Popular leadrein and starter ponies for young children',
            'Low feeding costs — very easy keepers',
            'Compact and manageable for small spaces and smaller budgets',
        ],
        'cons': [
            'Very strong-willed and can be difficult to handle without firm, consistent management',
            'Prone to laminitis — strict diet control essential',
            'Can develop bad habits quickly if not consistently disciplined',
            'Not suitable for riders much beyond children due to size limitations',
        ],
        'reviews': [
            (5, 'My daughter\'s best friend', 'Our Shetland pony Haggis has been with us for seven years and has taught three of my children to ride. He\'s been patient with wobbling beginners, enthusiastic in leadrein classes, and utterly safe in the most testing situations. He does have a massive personality and has perfected the art of looking innocent while plotting mischief, but he has never put a child in danger. An incomparable children\'s pony.'),
            (5, 'Tiny body, enormous character', 'Shetland ponies have more personality per inch than any animal I\'ve ever encountered. My pony Hamish has distinct opinions about his breakfast timing, his preferred company, and whether today is a day he feels like cooperating. He\'s outwitted every field gate we\'ve had and taught himself to open the feed store door. Managing him requires consistency and humour in equal measure. He\'s brought more laughter to our yard than any full-sized horse.'),
            (4, 'Perfect first pony with proper management', 'Shetland ponies have a reputation for being cheeky and difficult, which is fair — but properly managed from the start, they are excellent children\'s ponies. My pony Angus respects consistent boundaries and is a joy to handle and ride. The problems come when they\'re allowed to develop bad habits. Get a well-handled, correctly trained Shetland and work with an experienced instructor to maintain the standards. Properly done, they\'re wonderful.'),
            (5, 'Never had a sounder, tougher animal', 'My Shetland is 28 years old and still going strong. The breed\'s hardiness is genuinely extraordinary — he\'s never had a lame day in his life, requires minimal veterinary intervention, and thrives on a small amount of hay and adequate pasture. He costs a fraction of a full-sized horse to keep. For families wanting a long-lived companion pony without enormous costs, Shetlands are unbeatable.'),
            (4, 'Laminitis management is critical', 'Shetland ponies are highly prone to laminitis and diet management is non-negotiable. My pony must have restricted grazing (strip grazing in spring and summer), no hard feed, and regular farrier visits. When managed correctly he\'s been sound and healthy for 15 years. One owner before me let him overgraze and he suffered a serious laminitis episode. Learn the dietary requirements before getting a Shetland — it\'s not difficult but it\'s essential.'),
            (3, 'Brilliant ponies, not for soft-hearted handlers', 'Shetland ponies are remarkable animals but they will absolutely take advantage of soft or inconsistent handling. My pony tested every boundary in his first year — barging, nibbling, refusing, gate-crashing. Firm, consistent, fair handling sorted all of it and he\'s now a genuinely good pony. But anyone who gives him an inch finds he takes a field. They\'re not malicious — they\'re simply intelligent enough to figure out what they can get away with.'),
            (5, 'In-hand showing champion', 'My Shetland pony has been champion at our regional breed show three years running. Presented properly — gleaming coat, perfectly pulled mane, correct conformation assessed — he is a spectacular example of the breed. In-hand Shetland showing is a wonderful discipline that showcases the breed\'s compact power and correct type. The Shetland Pony Stud-Book Society is an excellent resource and the showing community is passionate and welcoming.'),
            (4, 'Great companion for larger horses', 'Beyond their role as children\'s riding ponies, Shetlands make wonderful companions for larger horses. My Shetland lives with my mare and has given her the calm, settled companionship that transformed her stable life. He also keeps the yard entertained with his antics. At his age he\'s retired from riding but is a valued full-time companion and yard character. The bond between him and my mare is genuinely touching.'),
            (5, 'Thirty years of joy in a tiny package', 'My Shetland pony is 30 years old this year. He has taught four generations of my family to ride. He\'s been on holiday with us in a borrowed field, appeared in a school nativity play, and been the subject of approximately one thousand children\'s drawings. He costs almost nothing to keep and remains sound and happy. A Shetland pony purchased for a young child can genuinely be a family companion for three decades. Extraordinary value in the most compact package.'),
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

        sub = SubCategory.query.filter_by(category_id=animals_cat.id, slug='horses').first()
        if not sub:
            sub = SubCategory(category_id=animals_cat.id, name='Horses', slug='horses')
            db.session.add(sub)
            db.session.flush()
            logger.info("Created Horses subcategory")
        else:
            logger.info("Horses subcategory already exists")

        total_reviews = 0
        for name, data in HORSE_DATA.items():
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
                img_url = get_wiki_image(data['wiki_title']) or try_commons_image(f"{name} horse breed")
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
            logger.info("Fetching Horses slate image...")
            slate_url = get_wiki_image('Horse') or try_commons_image('horse galloping field')
            if slate_url:
                dest = os.path.join(defaults_dir, 'horses.jpg')
                if download_image(slate_url, dest):
                    sub.image_path = 'images/defaults/horses.jpg'
                    logger.info("  Saved Horses slate image")
            time.sleep(2)

        db.session.commit()
        logger.info(f"\nDone. {len(HORSE_DATA)} horse breeds, {total_reviews} reviews.")


if __name__ == '__main__':
    main()
