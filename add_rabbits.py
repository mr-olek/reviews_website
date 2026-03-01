"""
Add a Rabbits subcategory to Animals with 5 breeds, reviews, and images.
Safe to run multiple times — skips existing records.

Usage:
  python3 add_rabbits.py
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
    'Happy', 'Fluffy', 'Curious', 'Gentle', 'Bouncy', 'Sweet', 'Playful',
    'Snuggly', 'Feisty', 'Brave', 'Lucky', 'Cozy', 'Fuzzy', 'Tiny', 'Jolly',
]
_ANIMALS = [
    'Bunny', 'Rabbit', 'Paw', 'Hop', 'Flop', 'Ear', 'Tail', 'Nose',
    'Whisker', 'Clover', 'Meadow', 'Hutch', 'Burrow', 'Clover', 'Patch',
]


def _rnd_name(rng: random.Random) -> str:
    return f"{rng.choice(_ADJECTIVES)}{rng.choice(_ANIMALS)}{rng.randint(10, 99)}"


RABBIT_DATA: dict[str, dict] = {
    'Holland Lop': {
        'slug': 'holland-lop',
        'wiki_title': 'Holland Lop',
        'description': (
            'The Holland Lop is one of the most popular rabbit breeds in the world, '
            'beloved for its compact body and distinctive floppy ears that frame an adorably round face. '
            'Weighing just 2–4 lbs, they make wonderful indoor companions and thrive with daily out-of-cage time to explore.'
        ),
        'pros': [
            'Compact size makes them ideal for apartments',
            'Extremely affectionate and bonds closely with owners',
            'Adorable lopped ears and round face',
            'Generally calm and easy to handle',
            'Wide variety of colour patterns available',
        ],
        'cons': [
            'Ear canals can trap moisture — regular checks needed',
            'Needs several hours of exercise outside the cage each day',
            'Can be territorial and thump when displeased',
            'Requires a hay-heavy diet and dental monitoring',
        ],
        'reviews': [
            (5, 'My absolute favourite rabbit breed', 'I\'ve owned three Holland Lops over the years and each one has been an absolute joy. They\'re small enough to live comfortably indoors but have huge personalities. My current bunny, Maple, follows me around the apartment and binkies every time I come home. The floppy ears are irresistible. If you\'re looking for a cuddly, manageable rabbit, Holland Lops are perfect. They do need daily free-roam time, but that\'s part of the fun watching them zoom around.'),
            (5, 'Perfect apartment rabbit', 'Living in a one-bedroom flat, I was worried a rabbit might not work, but my Holland Lop proved me completely wrong. She\'s quiet, doesn\'t smell if you clean regularly, and loves lounging next to me while I watch TV. She learned her name within two weeks and comes when called. The compact size means her enclosure fits easily in the living room. Genuinely the best pet decision I\'ve ever made.'),
            (4, 'Wonderful but needs lots of space to run', 'Holland Lops are sweet and docile, but don\'t let that fool you — they need a good 3–4 hours of free time daily. My lop gets grumpy and thumps if he\'s cooped up too long. Once he\'s out though, he\'s the most loving little guy. He nudges my hand for pets and grooms my fingers. Just make sure you rabbit-proof your home well before getting one of these guys.'),
            (5, 'Best first rabbit ever', 'Got my Holland Lop as a first-time rabbit owner. The breed is known to be beginner-friendly and I completely agree. He was relaxed from day one and never bit or scratched me. He took to litter training in about a week. Vet bills have been reasonable — just routine check-ups. The hardest part was learning about proper diet (lots of hay, limited pellets, fresh greens) but there are great resources online.'),
            (4, 'Charming little companion', 'My Holland Lop Biscuit has been with me for three years and is still full of energy. He does the funniest binkies when he\'s happy. He loves to rearrange his hay and move things around his pen, which is endlessly entertaining. Grooming is straightforward — a weekly brush keeps his coat tidy. The only downside is he chews anything within reach, so I\'ve had to be careful with cables and baseboards.'),
            (3, 'Sweet but can be stubborn', 'My Holland Lop has a definite mind of her own. She\'s sweet and loves head rubs, but she also likes to thump and push things over when she doesn\'t get her way. Rabbits have stronger personalities than I expected. She\'s healthy and eats well, but bonding took about two months of patient daily interaction. Worth the effort, but go in with realistic expectations that rabbits aren\'t always lap animals.'),
            (5, 'Love every minute with him', 'From the moment I brought my Holland Lop home he stole my heart. He\'s playful in the mornings, then turns into a sleepy loaf by afternoon. He loves tossing his hay ball around and always comes over to investigate whenever I enter the room. His fur is incredibly soft and his little face is the cutest thing I\'ve ever seen. I recommend Holland Lops to anyone looking for a gentle, manageable pet rabbit.'),
            (4, 'Great with kids, needs supervision', 'We got a Holland Lop for our children (ages 7 and 10) and it\'s been a wonderful experience. The breed is calm enough for kids to handle with guidance, though we always supervise. Our lop loves the kids running around — he binkies and zooms alongside them. Teaching the children to respect the rabbit\'s space has been a great lesson too. Just note they live 8–12 years, so it\'s a long commitment.'),
            (5, 'Melted my heart from day one', 'I wasn\'t a rabbit person until I met a Holland Lop at a rescue. That was the end of that — I adopted her the same day. She was shy at first but within a month she was flopping over for belly rubs and grinding her teeth in contentment when I stroked her. She\'s two years old now and the most charming little creature. Holland Lops genuinely feel like proper companion animals, not just cage pets.'),
            (3, 'Healthy but high-maintenance diet', 'Holland Lops are lovely little rabbits, but I underestimated how important diet is. Unlimited Timothy hay is non-negotiable, pellets should be limited, and fresh greens need rotating. My rabbit developed a GI issue early on from too many pellets, which was a scary and expensive vet visit. Once I got the diet right everything improved. Research the proper diet thoroughly before getting any rabbit — it\'s more nuanced than I expected.'),
        ],
    },
    'Mini Rex': {
        'slug': 'mini-rex',
        'wiki_title': 'Mini Rex',
        'description': (
            'The Mini Rex is prized for its extraordinarily plush, velvety coat that stands upright rather than lying flat, '
            'giving it a wonderfully soft texture unlike any other breed. '
            'Weighing around 3–4.5 lbs, they are calm, friendly, and one of the best rabbit breeds for families with children.'
        ),
        'pros': [
            'Incredibly soft, velvety plush coat',
            'Calm and gentle temperament, great with kids',
            'Medium size — not too fragile, not too large',
            'Relatively low-maintenance grooming compared to long-haired breeds',
            'Wide range of recognised colours',
        ],
        'cons': [
            'Can be shy initially and needs patient socialisation',
            'Coat requires regular brushing to prevent matting',
            'Needs ample space and daily exercise time',
            'Prone to sore hocks if kept on hard surfaces',
        ],
        'reviews': [
            (5, 'The softest animal I\'ve ever touched', 'I bought a Mini Rex purely based on photos and descriptions of the coat — and the reality exceeded every expectation. Running your hands through that velvety fur is genuinely therapeutic. Beyond the coat, my Rex is calm, curious, and has never nipped me once. She comes to the front of her pen when I approach and loves to sit beside me while I work. An absolute gem of a rabbit.'),
            (5, 'Perfect family rabbit', 'We chose a Mini Rex for our family after researching rabbit breeds extensively. The calm temperament is exactly as advertised. Our 9-year-old handles her with confidence (supervised) and the rabbit seems genuinely relaxed around children. She\'s not a hide-in-the-corner type — she explores, binkies, and investigates everything. Litter training took only a few days. We\'re completely smitten.'),
            (4, 'Great beginner rabbit', 'As a first-time rabbit owner, the Mini Rex was an excellent choice. She\'s forgiving of my early mistakes and patient when I misread her body language. The velvety coat is easy to groom — just a quick brush once a week. She did take about six weeks to fully trust me, but now she flops dramatically by my feet whenever I sit on the floor. Rabbits really do have big personalities in small bodies.'),
            (5, 'Calm, curious, and utterly charming', 'My Mini Rex Velvet has been with me for two years and I cannot imagine life without her. She has a distinct daily routine — active and zoomy in the morning, loafy in the afternoons. She loves cardboard to chew and rearrange. Her coat stays beautifully clean with minimal effort. The breed is genuinely as calm and friendly as its reputation suggests.'),
            (4, 'Excellent temperament, needs proper housing', 'Mini Rex rabbits are wonderfully calm, but they do need proper flooring. My rabbit developed mild hock sores on a wire floor (which I immediately replaced with a mat). Once housed correctly she\'s been in perfect health. I\'d strongly advise solid flooring and comfortable bedding from the start. With that sorted, they are exceptional pets — quiet, affectionate, and endlessly entertaining to watch.'),
            (3, 'Sweet but took months to bond', 'My Mini Rex is lovely now, but the bonding process was slow. She hid for the first month and would thump if I approached too quickly. With daily patient interaction — sitting near her, offering treats, talking quietly — she gradually became more confident. Now she hops onto my lap voluntarily. Some rabbits just take more time. If you\'re patient the reward is a wonderfully affectionate companion.'),
            (5, 'Best pet I\'ve ever owned', 'I\'ve had cats, dogs, and hamsters, and my Mini Rex is my favourite pet of all time. The combination of soft velvety fur, expressive body language, and gentle personality is unbeatable. She binkies every evening during free-roam time which is the most joyful thing to watch. She\'s healthy, easy to care for, and full of character. I recommend Mini Rex rabbits without reservation.'),
            (4, 'Quiet and perfect for flat living', 'Living in an apartment I needed a quiet, compact pet. My Mini Rex is ideal — she\'s silent (rabbits don\'t bark or meow), her enclosure fits neatly in the corner, and she\'s easy to clean up after. She gets 3 hours of free-roam time daily and seems perfectly content. She\'s not overly clingy but enjoys company and will hop over for attention when she\'s in the mood.'),
            (5, 'Velvety coat is genuinely special', 'The Mini Rex coat is like nothing else — it doesn\'t lie flat like normal rabbit fur, it stands upright and feels dense and plush. Everyone who meets my rabbit comments on it. Beyond the looks, he\'s a genuinely sweet-natured rabbit who has never shown aggression. He loves exploring cardboard tunnels and foraging for treats hidden in hay. A wonderful, underrated rabbit breed.'),
        ],
    },
    'Lionhead': {
        'slug': 'lionhead-rabbit',
        'wiki_title': 'Lionhead rabbit',
        'description': (
            'The Lionhead rabbit is instantly recognisable by its distinctive wool mane encircling its head, '
            'giving it a striking resemblance to a tiny lion. '
            'Despite their small size (2.5–3.5 lbs), Lionheads are energetic, playful, and form strong bonds with their owners when properly socialised.'
        ),
        'pros': [
            'Unique and beautiful lion-like mane',
            'Playful and energetic, lots of personality',
            'Small size suitable for most living spaces',
            'Bonds strongly with owners once socialised',
            'Available in a wide range of colours',
        ],
        'cons': [
            'Mane requires regular grooming to prevent matting',
            'Can be skittish and takes time to socialise',
            'Small size makes them fragile — not ideal for very young children',
            'Double-mane Lionheads have heavier grooming needs',
        ],
        'reviews': [
            (5, 'The most beautiful rabbit I\'ve ever seen', 'I fell in love with Lionheads the moment I saw one at a rabbit show. The mane is absolutely stunning — my rabbit looks like a tiny, perfect lion. Beyond the looks, she\'s playful and inquisitive and follows me around the room during free-roam time. She took a few weeks to settle in but is now completely comfortable with being handled. An extraordinary little rabbit.'),
            (4, 'Charming but the mane needs attention', 'My Lionhead is wonderful but new owners need to know about grooming. The mane can tangle and mat if not brushed regularly — I do a gentle brush every other day with a small slicker brush. My rabbit actually seems to enjoy it now. Apart from grooming, he\'s been straightforward to care for and has a bubbly, curious personality that makes him a delight to have around.'),
            (5, 'Full of energy and personality', 'Lionheads are absolutely full of character. My rabbit Simba lives up to his name — he\'s bold, curious, and fearless. He binkies across the room, tosses his toys, and has learned to jump up onto the sofa for cuddles. He took about a month to become fully comfortable with handling, but the patience was completely worth it. He\'s never bitten or scratched and is now incredibly affectionate.'),
            (3, 'Beautiful but took a long time to trust us', 'I love my Lionhead, but she was very skittish for the first three months. She would thump and hide if approached too quickly. Slow, patient handling sessions eventually paid off and she\'s much calmer now, but prospective owners should be prepared for a longer bonding period compared to some other breeds. The mane also requires more grooming than I anticipated. Beautiful rabbit though.'),
            (5, 'Perfect small rabbit for experienced owners', 'My second rabbit is a Lionhead and the experience has been brilliant. The breed is energetic and playful in a way that larger breeds aren\'t — they zoom around and leap through tunnels with infectious enthusiasm. The mane is genuinely gorgeous and gets softer as they mature. I\'d recommend Lionheads to anyone who has some rabbit experience and enjoys an active, engaging pet.'),
            (4, 'Adorable and fun to watch', 'There\'s nothing quite like watching a Lionhead binky around the room — the mane bobs in the most endearing way. My rabbit Dandelion is sociable and loves exploring new environments. He investigates every new toy I give him and has a hilarious habit of rearranging his hay pile. Grooming takes about 10 minutes every couple of days, which I\'ve come to enjoy as bonding time.'),
            (5, 'My kids absolutely love him', 'We got a Lionhead for our family and the children (aged 8 and 11) are completely smitten. He\'s playful enough to entertain them but calm enough that supervised handling goes smoothly. The mane is a big hit — the kids think he looks like a fairy tale creature. He\'s healthy, eating well, and has been an excellent addition to our household. Just supervise young children carefully as he is small and fragile.'),
            (4, 'Great personality, check mane regularly', 'Lionheads are wonderful rabbits with big personalities packed into small bodies. My rabbit is curious, playful, and surprisingly bold for such a small breed. The main thing to be aware of is the mane — check it weekly for any matting around the ears and behind the head. A few minutes of gentle brushing prevents any issues. Overall a fantastic breed that I\'d happily recommend.'),
            (3, 'Fun but grooming is more work than expected', 'I chose a Lionhead because the mane looked beautiful in photos. In person, that mane requires real commitment. My rabbit has a double mane and needs brushing every day or it tangles quickly. She also had a small bout of wool block early on (a risk with longhaired rabbits) which needed vet treatment. She\'s healthy and sweet-natured, but do your research on Lionhead grooming before committing to the breed.'),
        ],
    },
    'Dutch Rabbit': {
        'slug': 'dutch-rabbit',
        'wiki_title': 'Dutch rabbit',
        'description': (
            'The Dutch rabbit is one of the oldest and most recognisable rabbit breeds, '
            'distinguished by its characteristic two-tone markings — a white blaze and saddle contrasting with a coloured body. '
            'Active, curious, and intelligent, Dutch rabbits are excellent for beginners and families alike.'
        ),
        'pros': [
            'Classic, striking two-tone markings',
            'Active and curious — entertaining to watch',
            'Good-natured and suitable for beginners',
            'Compact yet sturdy (4–5.5 lbs)',
            'Intelligent and can learn simple tricks',
        ],
        'cons': [
            'More energetic than some breeds — needs plenty of exercise space',
            'Can be nippy if not properly socialised young',
            'Sheds moderately and needs regular brushing',
            'Needs companionship — consider keeping in bonded pairs',
        ],
        'reviews': [
            (5, 'Classic breed, wonderful temperament', 'Dutch rabbits have been popular for a reason — they\'re balanced, friendly, and full of character. My Dutch rabbit Domino has been with me for four years and remains active and curious every single day. He loves exploring, rearranging his toys, and investigating cardboard boxes. The distinctive markings turn heads every time someone visits. A brilliant all-round breed.'),
            (4, 'Great first rabbit for beginners', 'As a first-time rabbit owner I did a lot of research before choosing a Dutch. They\'re widely recommended for beginners and the reputation is well-deserved. My rabbit was easy to litter train and hasn\'t had any health issues in two years. She\'s spirited and active — she needs good free-roam time — but she\'s never aggressive and loves head scratches. A great introduction to rabbit keeping.'),
            (5, 'Intelligent and entertaining', 'I was surprised by how smart my Dutch rabbit is. He learned his name quickly, comes when called, and figured out how to open the simple latch on his enclosure (I had to upgrade it). He loves puzzle feeders and will spend ages working out how to get to a treat. The distinctive markings are beautiful and he gets admired by everyone who visits. A truly engaging pet.'),
            (4, 'Active and fun but needs space', 'Dutch rabbits are more active than I expected. My rabbit needs at least 4 hours of free-roam time to be truly content, and she will thump and rearrange things if kept cooped up. Once she\'s out she\'s brilliant — curious, playful, and will binky enthusiastically across the room. Make sure you have enough space before getting a Dutch; they aren\'t couch potatoes.'),
            (5, 'Wonderful family rabbit', 'We chose a Dutch rabbit for our family after seeing how good-natured they are. Our rabbit Panda is relaxed with our children, doesn\'t bite, and has been a joy to have around. The children have learned so much about animal care through looking after her. She\'s healthy, eats well, and is generally a robust little rabbit. The black-and-white markings are exactly as striking in person as in photos.'),
            (3, 'Can be nippy if not socialised early', 'My Dutch rabbit took a while to fully trust us and went through a nippy phase around three months old. Patient handling and respecting his body language gradually sorted this out. He\'s now four years old and very calm, but the early months required real consistency. Dutch rabbits are wonderful once bonded, but don\'t assume they\'ll be immediately tame — they need socialisation like any rabbit.'),
            (5, 'Healthy, hardy, and fun', 'Dutch rabbits have a reputation for being hardy and my experience confirms it. My rabbit has been in excellent health for six years with only routine vet check-ups. She\'s still active, curious, and enthusiastic about her morning greens. The breed is genuinely low-drama compared to some others I\'ve encountered. Good diet, proper housing, and regular vet checks is all they really need.'),
            (4, 'Great personality in a compact package', 'My Dutch rabbit Splash has a huge personality for such a small animal. He binkies, zooms, climbs on me for attention, and grooms my hand when he\'s in an affectionate mood. The distinctive markings make him look like a little panda. He does shed seasonally and needs brushing more frequently then, but grooming is otherwise minimal. A wonderfully engaging rabbit.'),
            (4, 'Smart and inquisitive', 'Dutch rabbits are noticeably intelligent compared to some other breeds I\'ve kept. My rabbit worked out the layout of the apartment within a week and knows exactly where her food comes from. She nudges me persistently if her morning greens are late. She loves exploring new environments and investigates every new item I bring home. A really rewarding rabbit to keep.'),
        ],
    },
    'Flemish Giant': {
        'slug': 'flemish-giant',
        'wiki_title': 'Flemish Giant rabbit',
        'description': (
            'The Flemish Giant is the largest domestic rabbit breed, with adults often reaching 10 kg (22 lbs) or more. '
            'Despite their imposing size, they are famously gentle, patient, and affectionate — earning the nickname "the gentle giant of rabbits." '
            'They require significantly more space and food than smaller breeds but reward owners with dog-like companionship.'
        ),
        'pros': [
            'Exceptionally gentle and docile temperament',
            'Dog-like personality — bonds deeply with family',
            'Calm and tolerant, excellent with older children',
            'Distinctive impressive size — a real conversation starter',
            'Less prone to startling than smaller, more nervous breeds',
        ],
        'cons': [
            'Requires very large enclosure — at least 3m × 2m minimum',
            'Eats significantly more hay, pellets, and greens than smaller breeds',
            'Shorter lifespan (5–7 years) compared to smaller rabbit breeds',
            'Vet costs and neutering fees higher due to size',
            'Heavy and strong — can be difficult to lift safely',
        ],
        'reviews': [
            (5, 'The most dog-like pet I\'ve ever owned', 'I\'ve had dogs all my life and then got a Flemish Giant and I\'m completely smitten. He comes when called, follows me around the house, and flops at my feet while I watch TV. He\'s calm, relaxed, and utterly gentle despite being the size of a small dog. The only real difference from a dog is the silence — rabbits are whisper-quiet. He\'s been an absolute revelation.'),
            (5, 'Gentle giant is exactly right', 'My Flemish Giant is the most patient, placid animal I\'ve ever encountered. She weighs 9 kg and could easily injure me if she panicked, but she never does. She\'s calm in new environments, tolerant of being picked up (with proper support), and loves lounging beside me for hours. Her size does mean a substantial enclosure and a significant food bill, but the companionship is unmatched.'),
            (4, 'Wonderful but plan for the space and cost', 'Before getting a Flemish Giant, please research the space requirements thoroughly. My rabbit needed a custom-built enclosure to be comfortable. He eats two to three times what a medium rabbit eats. Vet bills are higher. Once you\'ve sorted the practicalities, though, the reward is extraordinary — a huge, gentle, affectionate rabbit who greets you every morning and loves company.'),
            (5, 'My children adore him', 'We have a Flemish Giant named Bernard and he\'s the star of our household. Our kids (aged 8, 11, and 14) all adore him and he tolerates their attention with infinite patience. He\'s calm, gentle, and seems to enjoy the bustle of family life. He has his own dedicated room with a large pen and gets several hours of free time daily. The investment in space and food is absolutely worth it.'),
            (4, 'Incredible companion animal', 'Flemish Giants are truly companion animals — they want to be near people and get mopey if left alone too long. My giant follows me from room to room and nudges me for attention if I ignore him for too long. He\'s the most social rabbit I\'ve owned. The food costs are real (around 3x what a normal rabbit eats) but I budget for it. He\'s worth every penny.'),
            (3, 'Wonderful personality but very demanding of space', 'My Flemish Giant has an amazing personality and I love him dearly, but I wish I\'d fully appreciated the space requirements before getting him. He was miserable in a standard rabbit hutch and I had to completely redesign our spare room into his enclosure. Once he had proper space everything improved. Please research housing thoroughly — a giant rabbit in a small cage is genuinely unkind.'),
            (5, 'Best decision I ever made', 'I adopted a Flemish Giant from a rescue and it\'s the best pet decision of my life. He was a bit nervous at first but blossomed into the most affectionate, curious, personality-filled animal. He binkies when happy (which looks absolutely hilarious at his size), grooms me in return for head rubs, and has learned to knock gently on my bedroom door when he wants attention. Extraordinary animal.'),
            (4, 'Calm and gentle with our elderly relatives', 'We chose a Flemish Giant partly for its calming presence. Our elderly parents visit regularly and the rabbit sits calmly beside them while they stroke his enormous ears. He\'s never startled or bolted around them. His size means he\'s easy to pet without bending down too far. He\'s been therapeutic for everyone in the family. A gentle giant in every sense.'),
            (5, 'Nothing else quite like them', 'There is genuinely no other rabbit breed that matches the Flemish Giant\'s combination of size, gentleness, and personality. Mine weighs 10.5 kg and is the calmest, most affectionate pet imaginable. He greets me at the gate of his pen every morning and flops dramatically for belly rubs in the evening. He\'s healthy and has been since I adopted him at 8 months. Truly a special rabbit.'),
            (3, 'Amazing rabbits but shorter lifespan', 'Flemish Giants are wonderful pets but prospective owners should know about the shorter lifespan. My giant lived to 6.5 years, which is typical for the breed. He was healthy throughout but the goodbye was devastating when his time came. I\'ve since adopted another and cherish every day with him. Magnificent rabbits, but go in knowing the lifespan is shorter than smaller breeds and that\'s genuinely hard.'),
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
        'srnamespace': 6,  # File namespace
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
            # Get the thumbnail URL
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

        # Create or fetch Rabbits subcategory
        rabbits_sub = SubCategory.query.filter_by(
            category_id=animals_cat.id, slug='rabbits'
        ).first()
        if not rabbits_sub:
            rabbits_sub = SubCategory(
                category_id=animals_cat.id,
                name='Rabbits',
                slug='rabbits',
            )
            db.session.add(rabbits_sub)
            db.session.flush()
            logger.info("Created Rabbits subcategory")
        else:
            logger.info("Rabbits subcategory already exists")

        total_reviews = 0
        for name, data in RABBIT_DATA.items():
            slug = data['slug']

            # Create or update subject
            subj = Subject.query.filter_by(
                subcategory_id=rabbits_sub.id, slug=slug
            ).first()
            if not subj:
                subj = Subject(
                    subcategory_id=rabbits_sub.id,
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
                    img_url = try_commons_image(f"{name} rabbit")
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
        if not rabbits_sub.image_path:
            logger.info("Fetching Rabbits slate image...")
            slate_url = get_wiki_image('Domestic rabbit')
            if not slate_url:
                slate_url = try_commons_image('pet rabbit domestic')
            if slate_url:
                dest = os.path.join(defaults_dir, 'rabbits.jpg')
                if download_image(slate_url, dest):
                    rabbits_sub.image_path = 'images/defaults/rabbits.jpg'
                    logger.info("  Saved Rabbits slate image")
                else:
                    logger.warning("  Failed to download Rabbits slate image")
            else:
                logger.warning("  No slate image found for Rabbits")
            time.sleep(2)

        db.session.commit()
        logger.info(f"\nDone. Added {len(RABBIT_DATA)} rabbit breeds and {total_reviews} reviews.")


if __name__ == '__main__':
    main()
