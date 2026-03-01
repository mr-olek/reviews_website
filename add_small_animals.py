"""
Add a Small Animals subcategory to Animals with 5 species, reviews, and images.
Safe to run multiple times — skips existing records.

Usage:
  python3 add_small_animals.py
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
    'Happy', 'Fluffy', 'Curious', 'Tiny', 'Fuzzy', 'Cozy', 'Bouncy',
    'Snuggly', 'Speedy', 'Brave', 'Lucky', 'Cheeky', 'Plump', 'Jolly', 'Sweet',
]
_ANIMALS = [
    'Paw', 'Whisker', 'Cheek', 'Pouch', 'Fluff', 'Nibble', 'Squeak',
    'Wheel', 'Burrow', 'Nest', 'Tuft', 'Chin', 'Dust', 'Ear', 'Snout',
]


def _rnd_name(rng: random.Random) -> str:
    return f"{rng.choice(_ADJECTIVES)}{rng.choice(_ANIMALS)}{rng.randint(10, 99)}"


SMALL_ANIMAL_DATA: dict[str, dict] = {
    'Syrian Hamster': {
        'slug': 'syrian-hamster',
        'wiki_title': 'Golden hamster',
        'description': (
            'The Syrian hamster (also called the golden hamster) is the most popular hamster species kept as a pet, '
            'known for its charming chubby cheek pouches and docile temperament when hand-raised from a young age. '
            'Strictly solitary animals, they must be housed alone and are naturally nocturnal — most active in the evening and night.'
        ),
        'pros': [
            'Docile and easy to handle when socialised young',
            'Low-maintenance and inexpensive to keep',
            'Large enough to handle without the fragility of dwarf hamsters',
            'Entertaining to watch — love their wheels, tunnels, and food caching',
            'Good starter pet for responsible older children',
        ],
        'cons': [
            'Nocturnal — mostly active at night when you may be asleep',
            'Short lifespan of 2–3 years',
            'Must be kept alone — will fight other hamsters to the death',
            'Wheel noise can be disruptive at night',
        ],
        'reviews': [
            (5, 'Perfect first pet', 'My Syrian hamster Biscuit was my first pet and an absolute joy. She was tame from the day I brought her home, learned to take treats from my hand within a week, and would sit contentedly in my palm for evening cuddles. Her cheek pouches stuffed with food are the funniest thing I\'ve ever seen. At just 2.5 years her lifespan was heartbreakingly short, but the memories are wonderful.'),
            (5, 'Entertaining and adorable', 'Syrian hamsters are endlessly entertaining. My hamster Peanut spends his evenings running on his wheel, rearranging his bedding, and caching food in elaborate little piles. He knows my smell and comes to the front of his cage when I approach. The fact that he lives 2–3 years does sting, but within that time he becomes a real companion. Highly recommend for anyone wanting a low-maintenance but engaging pet.'),
            (4, 'Great but set up the cage properly', 'I cannot stress enough how important a proper cage setup is for Syrian hamsters. They need at minimum a 100cm × 50cm enclosure with deep bedding to burrow. My first setup was too small and my hamster was stressed and bar-chewing constantly. Once I upgraded to a proper tank with 30cm of substrate, the transformation was remarkable — calm, happy, and endlessly busy burrowing. Get the setup right from day one.'),
            (5, 'So much personality in a tiny package', 'People underestimate how much personality hamsters have. My Syrian hamster has distinct moods, favourite foods, and a hilarious habit of reorganising his cage overnight. He even has a bedtime routine where he stuffs his pouches, goes to his burrow, and won\'t come out again until evening. He\'s never bitten me and seems genuinely happy to be handled in the evenings. A brilliant little pet.'),
            (4, 'Night owl — plan accordingly', 'Syrian hamsters are genuinely nocturnal, which caught me off guard. My hamster barely stirs during the day and comes alive around 9–10pm. If you go to bed early this could be frustrating, especially as the wheel is quite loud. I ended up putting a silent spinner wheel in which helped enormously. In terms of personality and tamability, he\'s excellent — just be prepared for the nocturnal lifestyle.'),
            (3, 'Short lifespan is emotionally hard', 'Syrian hamsters are lovely pets, but the short lifespan (my hamster lived 2 years and 4 months) is genuinely hard. He was healthy and happy right up to the end, which I\'m grateful for, but saying goodbye after such a short time was devastating. I knew this going in, but knowing and experiencing it are different things. If you can cope with a short-lived pet, they are wonderful — just emotionally prepare yourself.'),
            (5, 'My children\'s perfect first pet', 'We got a Syrian hamster for our 10-year-old and it was an excellent choice. Old enough to handle gently, the hamster is big enough to hold without being as delicate as dwarf varieties. Our daughter learned responsibility, empathy, and patience through caring for him. He lived 2 years and 8 months and was healthy throughout. The whole experience was genuinely educational and joyful.'),
            (4, 'Very tame with regular handling', 'The key to a tame Syrian hamster is consistent gentle handling from a young age. I spent 15 minutes each evening sitting with my hamster and letting her explore my hands. Within three weeks she was completely relaxed and would fall asleep in my palm. She never bit and always seemed pleased to be out. Very rewarding to tame a hamster — it just takes patience and consistency.'),
        ],
    },
    'Dwarf Hamster': {
        'slug': 'dwarf-hamster',
        'wiki_title': 'Dwarf hamster',
        'description': (
            'Dwarf hamsters — including the Russian Campbell, Winter White, and Roborovski varieties — are tiny, '
            'fast-moving little animals that are endlessly entertaining to watch. '
            'Some species can cohabit in same-sex pairs if introduced young, but they are faster and more challenging to handle than Syrian hamsters.'
        ),
        'pros': [
            'Tiny and incredibly cute',
            'Some species can be kept in same-sex pairs for companionship',
            'Very active and fun to watch',
            'Smaller cage footprint than Syrians',
            'Longer lifespan than Syrians in some species (up to 3–4 years)',
        ],
        'cons': [
            'Very fast and difficult to handle — prone to escaping',
            'More nippy than Syrians, especially if startled',
            'Not ideal for young children due to fragility and speed',
            'Needs very secure enclosure with small bar spacing',
        ],
        'reviews': [
            (5, 'Tiny but endlessly entertaining', 'My two Roborovski dwarf hamsters are the most entertaining animals I\'ve ever kept. They zoom around their enclosure at incredible speed, play-fight, groom each other, and perform the funniest acrobatics on their wheel. Handling them is challenging — they\'re incredibly fast — but watching them is pure joy. Perfect desk pets if you work from home.'),
            (4, 'Hilarious to watch, tricky to handle', 'I bought dwarf hamsters expecting to handle them like a Syrian, which was a mistake. They\'re lightning-fast and very wary of being picked up. Once I accepted them as "look but don\'t touch" pets and focused on building a rich enclosure for them to explore, my enjoyment shot up. They\'re genuinely fascinating animals to observe. Just adjust your expectations around handling.'),
            (3, 'Not for young children', 'I got dwarf hamsters for my 7-year-old, which in hindsight was too young for this particular species. They\'re extremely fast and easily dropped, and one escaped within the first week. Thankfully we found her. The hamsters themselves are healthy and active, but the speed and fragility make them unsuitable for young children. I\'d recommend Syrians for kids and dwarf hamsters for teenagers or adults.'),
            (5, 'Russian Winter Whites are adorable', 'My Russian Winter White dwarf hamsters are the most adorable little animals. In winter they turn partially white (hence the name) which is just magical. They\'re slightly calmer than Roborovskis and my pair has tolerated gentle handling reasonably well. They eat together, sleep in a big pile, and squeak adorably when exploring. I spend far too long just watching them live their little lives.'),
            (4, 'Pairs are wonderful company for each other', 'Keeping a same-sex pair of Campbell\'s dwarf hamsters has been brilliant. They groom each other, sleep in a huddle, and seem genuinely happier together than solitary hamsters I\'ve kept previously. There was one minor scuffle in the first week, but they settled quickly and have been inseparable since. Note: not all dwarf species can be safely paired — do your research on the specific variety.'),
            (5, 'Great for watching, enchanting little animals', 'I set up a large bin cage for my two Roborovskis with lots of substrate, tunnels, and foraging opportunities. Watching them borrow and cache food is like having a tiny nature documentary in my room. They\'ve never bitten me (though I handle them rarely), seem stress-free, and are in excellent health after 18 months. For anyone who loves observing animals, dwarf hamsters are perfect.'),
            (4, 'Surprisingly long-lived', 'My Campbell\'s dwarf hamster is 3 years and 2 months old, which is longer than I expected for a hamster. She\'s slowed down a bit but still potters around her cage daily and eats well. Dwarf hamsters can outlive Syrians if kept in good conditions. She\'s never been ill and the only vet visits were routine check-ups. A healthy, happy, and surprisingly long-lived little pet.'),
            (3, 'Escaped twice — cage needs to be escape-proof', 'Dwarf hamsters are extraordinary escape artists. Mine got through what I thought was a secure bar-spacing gap and went missing for two days before I found her behind the washing machine. I switched to an aquarium-style tank with a mesh lid and the problem was solved. Just be very aware of cage security — dwarf hamsters can squeeze through tiny gaps and navigate their way around any enclosure with weaknesses.'),
        ],
    },
    'Guinea Pig': {
        'slug': 'guinea-pig',
        'wiki_title': 'Guinea pig',
        'description': (
            'Guinea pigs (also called cavies) are highly social, vocal, and gentle small animals that make wonderful pets for families. '
            'They should always be kept in pairs or groups as they are herd animals that become lonely and stressed in isolation. '
            'With a lifespan of 5–7 years and a huge range of sounds — from wheeks and purrs to rumbles and chutts — they are endlessly communicative and engaging companions.'
        ),
        'pros': [
            'Highly social and vocal — communicates with a wide range of sounds',
            'Gentle and rarely bite — excellent with children',
            'Longer lifespan (5–7 years) than most small pets',
            'Very rewarding to bond with — come running when they hear you',
            'Wide variety of breeds and coat types',
        ],
        'cons': [
            'Must be kept in pairs or groups — cannot live alone',
            'Need a very large enclosure (minimum 120cm × 60cm for a pair)',
            'Require fresh hay, pellets, and fresh vegetables daily',
            'Vet care can be costly as exotic animals',
        ],
        'reviews': [
            (5, 'The best small pets I\'ve ever owned', 'I have three guinea pigs and they have been the most rewarding small animals I\'ve ever kept. The wheek they make when they hear the fridge open is the most joyful sound. They run to the front of their enclosure when they see me and purr when stroked. Keeping them in a group means they\'re never lonely and you get to watch the fascinating social dynamics between them. Absolutely wonderful animals.'),
            (5, 'Perfect family pet', 'Guinea pigs have been a revelation for our family. Our kids (aged 6, 9, and 12) all interact with them brilliantly. The guinea pigs are gentle, don\'t scratch or bite, and are tolerant of careful children. They wheek excitedly when the children come home from school. They\'re messier than hamsters but far more interactive and emotionally rewarding. We\'ve had them three years and cannot imagine life without them.'),
            (4, 'Vocal and full of character', 'What surprised me most about guinea pigs is how vocal they are. My two cavies have a sound for everything — a wheek for excitement, a purr for contentment, a low rumble when displeased, a chutter when curious. Learning to read their sounds has been genuinely fascinating. They\'re intelligent animals with distinct personalities and preferences. One loves being stroked, the other prefers being left alone but wheeking loudly for treats.'),
            (5, 'Come running when they hear your voice', 'After only two weeks my guinea pigs learned to associate my voice with treats and attention. Now they sprint across their enclosure whenever I enter the room and wheek loudly until I acknowledge them. The bond that develops with guinea pigs is unlike anything I\'ve experienced with other small pets. They actively seek out human interaction in a way that hamsters and gerbils simply don\'t.'),
            (4, 'Needs a bigger cage than you think', 'Before getting guinea pigs, please research their space requirements. The tiny pet shop cages are completely inadequate — a pair of guinea pigs needs at least 120cm × 60cm of floor space, and more is better. Many owners build C&C (coroplast and grid) cages which are much more suitable. Once my piggies had proper space, they started popcorning (joyful jumping) and zooming, which told me they were finally happy.'),
            (5, 'Gentle and perfect for nervous children', 'My daughter was nervous around animals but has completely blossomed with our guinea pigs. They\'re gentle, predictable, and don\'t make sudden movements or loud noises. She gently pets them during lap time and they purr contentedly. The experience has built her confidence enormously. Guinea pigs are exceptional for children who are nervous or sensory-sensitive because they\'re so calm and communicative.'),
            (3, 'Expensive vet care for exotic animals', 'Guinea pigs are lovely pets but be aware that vet care is expensive. As "exotic" animals, not all vets see them, and those that do charge specialist rates. My guinea pig needed dental work (a common issue in the breed) which cost significantly more than a dog would for the same procedure. I love my piggies dearly but I wish I\'d factored in exotic vet costs when budgeting. Find a specialist vet before you get guinea pigs.'),
            (4, 'Popcorning is the most joyful thing to witness', 'Guinea pigs express happiness through "popcorning" — sudden random jumps into the air. The first time I saw my piggies do this after I expanded their enclosure, I laughed out loud. It\'s the most joyful, silly behaviour. Once you\'ve witnessed popcorning you understand completely why guinea pig owners are so enthusiastic. Happy guinea pigs are an absolute delight.'),
            (5, 'Six years and still going strong', 'My guinea pig Pepper is six years old and still wheeks enthusiastically for her daily bell pepper (hence the name). She\'s slower than she was but has been in excellent health her whole life. The 5–7 year lifespan is a real advantage over shorter-lived small pets — you get to develop a genuine long-term relationship. She knows my voice, my routine, and my smell. Utterly irreplaceable.'),
        ],
    },
    'Chinchilla': {
        'slug': 'chinchilla',
        'wiki_title': 'Chinchilla',
        'description': (
            'Chinchillas are native to the Andes mountains of South America and are prized for their extraordinarily dense, '
            'impossibly soft fur — with up to 60 hairs per follicle. '
            'They are active, intelligent, and can live 10–15 years with proper care, making them a long-term commitment. '
            'They require dust baths for coat maintenance and are sensitive to heat above 24°C.'
        ),
        'pros': [
            'Incredibly soft fur — the densest of any land animal',
            'Long lifespan (10–15 years) for a small pet',
            'Clean and virtually odourless',
            'Fascinating and acrobatic — love to jump and explore',
            'Hypoallergenic for many allergy sufferers',
        ],
        'cons': [
            'Sensitive to heat — must be kept below 24°C (75°F)',
            'Require dust baths 2–3 times per week',
            'Crepuscular/nocturnal — most active at dawn and dusk',
            'Need large multi-level enclosures to jump and climb',
            'Can be skittish and take time to socialise',
        ],
        'reviews': [
            (5, 'The softest animal on the planet', 'No description does chinchilla fur justice until you feel it. It is genuinely, impossibly soft — like touching a cloud. My chinchilla has been with me for eight years and every day I still marvel at his fur. Beyond the coat, he\'s intelligent, acrobatic, and entertaining. He leaps between levels of his cage with gymnastic precision and has a playful, curious personality. A long-lived and deeply rewarding pet.'),
            (5, 'Worth every bit of preparation', 'Chinchillas take some preparation — you need to understand the temperature requirements, dust baths, proper diet, and enclosure needs before bringing one home. But get all that right and you have an extraordinary pet. Mine is 10 years old, healthy, and still as active as ever. He\'s bonded deeply to me and chatters softly when I approach his cage. The commitment pays off enormously over a decade of companionship.'),
            (4, 'Temperature control is critical', 'Chinchillas cannot tolerate heat. My apartment struggles in summer and I had to install a dedicated air conditioning unit to keep his space at 18–22°C. Once I sorted the temperature control, everything else fell into place. He\'s been in perfect health for five years. But please, if you live somewhere hot or don\'t have reliable air conditioning, reconsider — heat can kill chinchillas quickly.'),
            (5, 'The dust baths are the best part', 'Watching a chinchilla take a dust bath is one of the most joyful things in pet keeping. They roll and wiggle in the dust with such pure enthusiasm and their coat comes out perfectly fluffed. My chinchilla gets two baths a week and performs an excited little spin whenever I bring the bath out. He\'s been with me seven years and I genuinely cannot imagine life without him.'),
            (4, 'Long-lived and deeply rewarding', 'I\'ve had my chinchilla for 12 years and counting. That alone tells you what a commitment (and joy) chinchilla ownership can be. He\'s slower than he was but still jumps around his cage and grooms himself fastidiously. The long lifespan means the bond you develop is genuinely deep — he knows my voice, my routine, and comes out of his sleeping spot when he hears me every morning.'),
            (3, 'Beautiful but took months to settle', 'My chinchilla was extremely skittish for the first six months. She would bark (yes, they bark) and flee whenever I approached. Patient, consistent interaction — sitting nearby, talking softly, offering treats at arm\'s length — gradually built trust. She\'s much calmer now at 3 years old, but the early period required real patience. Chinchillas are worth the effort but don\'t expect an immediately tame pet.'),
            (5, 'Virtually odourless and incredibly clean', 'One of the best things about chinchillas is that they are essentially odourless. The cage needs cleaning, but the animals themselves have no smell whatsoever. Combined with the hypoallergenic fur, they\'re ideal for allergy sufferers like me. My partner has cat allergies but has no reaction to our chinchilla at all. A beautiful, clean, and fascinating pet.'),
            (4, 'Need a large multi-level cage', 'Chinchillas are incredibly agile and need space to jump. The standard small animal cages sold in pet shops are completely inadequate. I built a custom multi-level cage (180cm tall, 90cm wide) with wooden shelves and ropes, and the difference in my chinchilla\'s behaviour was immediate — constant jumping, exploring, and playing. Please invest in proper housing; a confined chinchilla is an unhappy one.'),
            (5, 'My most rewarding small pet ever', 'I\'ve kept rabbits, guinea pigs, and hamsters over the years, but my chinchillas are in a different league. The combination of intelligence, acrobatics, and extraordinary softness, combined with a 10–15 year lifespan, makes them the most rewarding small pet I\'ve experienced. My pair are inseparable, groom each other daily, and both come out enthusiastically for their evening dust baths. Truly exceptional animals.'),
        ],
    },
    'Gerbil': {
        'slug': 'gerbil',
        'wiki_title': 'Gerbil',
        'description': (
            'Gerbils are small, active, and highly social rodents that are native to the desert regions of Mongolia. '
            'They are best kept in same-sex pairs or small groups and are known for their endless curiosity, burrowing behaviour, '
            'and remarkably gentle nature — they rarely bite even when startled. '
            'With a lifespan of 3–5 years, they make engaging and entertaining pets.'
        ),
        'pros': [
            'Social and curious — love to explore and burrow',
            'Rarely bite — gentle and suitable for older children',
            'Active during the day as well as at night',
            'Low odour compared to mice and rats',
            'Entertaining to watch, especially when burrowing',
        ],
        'cons': [
            'Short lifespan of 3–5 years',
            'Need to be kept in pairs — lonely alone',
            'Very fast and can be difficult to handle',
            'Need deep substrate for burrowing (minimum 20cm)',
        ],
        'reviews': [
            (5, 'The friendliest small rodents I\'ve kept', 'I\'ve had mice, hamsters, and rats, and my gerbils are the friendliest of all. They\'ve never bitten me despite being handled frequently, and they actively come to investigate my hand when I put it in their enclosure. Watching them burrow and rearrange their substrate is endlessly fascinating. They\'re also diurnal enough to be active when I\'m home, unlike hamsters who sleep all day.'),
            (5, 'Perfect pets for the whole family', 'Our two gerbils Sage and Pepper have been a wonderful addition to the family. They\'re active during daytime, easy to watch, and gentle enough for our 10-year-old to handle (supervised). The burrowing is the best part — they excavate complex tunnel systems and rearrange everything overnight. They\'re rarely aggressive and have never drawn blood despite frequent handling. Brilliant small pets.'),
            (4, 'Much better in pairs', 'I started with one gerbil (bad idea) and got a second after doing more research. The transformation was remarkable — the solo gerbil had been slightly lethargic and repetitive in his behaviour. Once bonded with a companion, both gerbils became active, playful, and engaged. Always get gerbils in pairs — they groom each other, sleep together, and seem genuinely happier with companionship.'),
            (5, 'The burrowing is magical to watch', 'I set up a large bin cage with 30cm of substrate for my gerbils and watching them excavate it has been one of the best things about keeping small pets. They have an intricate tunnel system and rearrange everything constantly. When I add fresh substrate they spend hours digging and reorganising. Gerbils need proper burrowing opportunities to be happy — a bare-floored cage is cruel and dull for them.'),
            (4, 'Active during the day — a huge plus', 'Unlike hamsters, my gerbils are active during daylight hours, which means I actually get to see them behave naturally. They have a pattern of active bursts followed by short rest periods throughout the day. It\'s like watching a tiny nature documentary. The fact that they\'re active when I\'m home makes them far more rewarding than nocturnal pets that are asleep every time I want to interact.'),
            (3, 'Shorter lifespan than expected', 'My first gerbil passed at 2 years and 8 months, which I found surprisingly short. After researching I found 2–4 years is average for gerbils, though some reach 5. It\'s shorter than I\'d hoped for the level of attachment I\'d developed. The second gerbil died from loneliness shortly after (always get three so one never ends up alone when bonded pairs die). The animals themselves are wonderful — just be prepared for a shorter relationship than with guinea pigs or chinchillas.'),
            (5, 'Low-odour and clean pets', 'Gerbils come from desert environments and have very concentrated urine, which means they produce minimal odour compared to mice or rats. My gerbils\' cage needs cleaning weekly but doesn\'t smell between cleans. They\'re fastidious about their bathroom spot which makes spot-cleaning easy. Combined with their gentle nature and entertaining behaviour, the low odour makes them exceptionally easy to live with.'),
            (4, 'Curious about everything', 'The curiosity of gerbils is one of their best traits. Whenever I put something new in their enclosure — a tube, a cardboard box, a new hide — they investigate it immediately and thoroughly. They seem to genuinely enjoy novelty and enrichment. I rotate their toys and add new substrate smells regularly to keep them stimulated. Active, curious, and full of personality — wonderful small pets.'),
            (5, 'Great introduction to rodent keeping', 'Gerbils were my first rodents and they set a wonderful precedent. They\'re gentle enough for beginners, active enough to be rewarding, and forgiving of early mistakes in husbandry (as long as the basics are right). My pair of Mongolian gerbils are 3 years old now and still as active and curious as when I got them at 8 weeks. I\'d recommend gerbils to anyone curious about keeping small rodents.'),
        ],
    },
}


def get_wiki_image(title: str, size: int = 500) -> str | None:
    """Return thumbnail URL from Wikipedia pageimages API."""
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
            logger.warning('Wikipedia 429 rate limit, sleeping 5s...')
            time.sleep(5)
            resp = SESSION.get('https://en.wikipedia.org/w/api.php', params=params, timeout=15)
        data = resp.json()
        pages = data.get('query', {}).get('pages', {})
        for page in pages.values():
            src = page.get('thumbnail', {}).get('source')
            if src:
                src = re.sub(r'/\d+px-', f'/{size}px-', src)
                return src
    except Exception as e:
        logger.warning(f'Wiki API error for {title!r}: {e}')
    return None


def try_commons_image(query: str, size: int = 500) -> str | None:
    """Search Wikimedia Commons for an image matching the query."""
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
        data = resp.json()
        results = data.get('query', {}).get('search', [])
        for result in results:
            title = result.get('title', '')
            if not title.startswith('File:'):
                continue
            ext = title.rsplit('.', 1)[-1].lower()
            if ext not in ('jpg', 'jpeg', 'png', 'webp'):
                continue
            info_params = {
                'action': 'query',
                'titles': title,
                'prop': 'imageinfo',
                'iiprop': 'url|thumburl',
                'iiurlwidth': size,
                'format': 'json',
            }
            info_resp = SESSION.get('https://commons.wikimedia.org/w/api.php', params=info_params, timeout=15)
            info_data = info_resp.json()
            for page in info_data.get('query', {}).get('pages', {}).values():
                infos = page.get('imageinfo', [])
                if infos and infos[0].get('thumburl'):
                    return infos[0]['thumburl']
    except Exception as e:
        logger.warning(f'Commons search error for {query!r}: {e}')
    return None


def download_image(url: str, dest_path: str) -> bool:
    """Download an image to dest_path. Returns True on success."""
    try:
        resp = SESSION.get(url, timeout=20)
        if resp.status_code == 429:
            logger.warning('429 rate limit on download, sleeping 5s...')
            time.sleep(5)
            resp = SESSION.get(url, timeout=20)
        if resp.status_code != 200:
            logger.warning(f'HTTP {resp.status_code} for {url}')
            return False
        content = resp.content
        if len(content) < 3000:
            logger.warning(f'Image too small ({len(content)} bytes): {url}')
            return False
        with open(dest_path, 'wb') as f:
            f.write(content)
        return True
    except Exception as e:
        logger.warning(f'Download error for {url}: {e}')
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

        # Create or fetch Small Animals subcategory
        small_sub = SubCategory.query.filter_by(
            category_id=animals_cat.id, slug='small-animals'
        ).first()
        if not small_sub:
            small_sub = SubCategory(
                category_id=animals_cat.id,
                name='Small Animals',
                slug='small-animals',
            )
            db.session.add(small_sub)
            db.session.flush()
            logger.info("Created Small Animals subcategory")
        else:
            logger.info("Small Animals subcategory already exists")

        total_reviews = 0
        for name, data in SMALL_ANIMAL_DATA.items():
            slug = data['slug']

            subj = Subject.query.filter_by(
                subcategory_id=small_sub.id, slug=slug
            ).first()
            if not subj:
                subj = Subject(
                    subcategory_id=small_sub.id,
                    name=name,
                    slug=slug,
                )
                db.session.add(subj)
                db.session.flush()
                logger.info(f"  + Subject: {name}")
            else:
                logger.info(f"  ~ Subject exists: {name}")

            subj.description = data['description']
            subj.pros = '\n'.join(data['pros'])
            subj.cons = '\n'.join(data['cons'])

            # Seed reviews
            rng = random.Random(hash(name) % 100000)
            all_reviews = data['reviews']
            count = rng.randint(5, 10)
            chosen = rng.sample(all_reviews, min(count, len(all_reviews)))

            added = 0
            for i, (rating, title, body) in enumerate(chosen):
                url_key = f"sample-{slug}-{i}"
                exists = Review.query.filter_by(original_url=url_key).first()
                if exists:
                    continue
                author = _rnd_name(rng)
                review = Review(
                    subject_id=subj.id,
                    rating=rating,
                    title=title,
                    body=body,
                    author_name=author,
                    source_site='sample',
                    is_published=True,
                    original_url=url_key,
                )
                db.session.add(review)
                added += 1
            total_reviews += added
            subj.update_stats()
            logger.info(f"    Added {added} reviews for {name}")

            # Download subject image
            if not subj.image_path:
                logger.info(f"  Fetching image for {name}...")
                img_url = get_wiki_image(data['wiki_title'])
                if not img_url:
                    img_url = try_commons_image(name)
                if img_url:
                    ext = img_url.rsplit('.', 1)[-1].split('?')[0].lower()
                    if ext not in ('jpg', 'jpeg', 'png', 'webp'):
                        ext = 'jpg'
                    dest = os.path.join(upload_dir, f"{slug}.{ext}")
                    if download_image(img_url, dest):
                        subj.image_path = f"images/uploads/subjects/{slug}.{ext}"
                        logger.info(f"    Saved image: {subj.image_path}")
                    else:
                        logger.warning(f"    Failed to download image for {name}")
                else:
                    logger.warning(f"    No image found for {name}")
                time.sleep(2)

        # Download subcategory slate image
        if not small_sub.image_path:
            logger.info("Fetching Small Animals slate image...")
            slate_url = get_wiki_image('Guinea pig')
            if not slate_url:
                slate_url = try_commons_image('pet small animal rodent')
            if slate_url:
                dest = os.path.join(defaults_dir, 'small-animals.jpg')
                if download_image(slate_url, dest):
                    small_sub.image_path = 'images/defaults/small-animals.jpg'
                    logger.info("  Saved Small Animals slate image")
                else:
                    logger.warning("  Failed to download Small Animals slate image")
            else:
                logger.warning("  No slate image found for Small Animals")
            time.sleep(2)

        db.session.commit()
        logger.info(f"\nDone. Added {len(SMALL_ANIMAL_DATA)} small animal species and {total_reviews} reviews.")


if __name__ == '__main__':
    main()
