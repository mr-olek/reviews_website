#!/usr/bin/env python3
"""Adds more car brands — Chinese EVs and other popular brands.
Usage: python3 add_more_cars.py
"""
import os, sys, time, random, requests
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Category, SubCategory, Subject, Review

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

_ADJ = ['Big','Tiny','Blue','Red','Happy','Grumpy','Sneaky','Fluffy','Brave','Lazy',
        'Spicy','Chilly','Wild','Calm','Swift','Clumsy','Bouncy','Fuzzy','Mighty','Sleepy']
_ANI = ['Baboon','Penguin','Panda','Narwhal','Capybara','Quokka','Axolotl','Platypus',
        'Wombat','Toucan','Lemur','Meerkat','Tapir','Okapi','Alpaca','Manatee',
        'Blobfish','Gecko','Flamingo','Armadillo']
def _rname(): return f"{random.choice(_ADJ)}{random.choice(_ANI)}{random.randint(1,999)}"

YEARS = [2021, 2022, 2023, 2024, 2025]

# (model_name, slug, wiki_title, description, start_year)
BRANDS = [
    # ── Chinese brands ──────────────────────────────────────────────────────────
    {
        'name': 'BYD', 'slug': 'byd', 'wiki': 'BYD Atto 3',
        'models': [
            ('Atto 3',   'atto-3',   'BYD Atto 3',    'Compact all-electric SUV — BYD\'s global breakthrough model with impressive range and value.', 2022),
            ('Han',      'han',      'BYD Han',        'BYD\'s flagship electric sedan — long range, rapid charging, and a premium cabin.', 2021),
            ('Tang',     'tang',     'BYD Tang',       'Large electric/PHEV SUV with 7 seats and supercar-grade acceleration.', 2021),
            ('Seal',     'seal',     'BYD Seal',       'Sporty all-electric sedan built on BYD\'s e-Platform 3.0 with CTB battery tech.', 2022),
            ('Dolphin',  'dolphin',  'BYD Dolphin',    'Affordable and fun compact EV hatchback with playful styling and 250+ km range.', 2021),
            ('Song Plus', 'song-plus','BYD Song Plus',  'Best-selling PHEV/EV SUV in China — spacious, efficient, and feature-rich.', 2021),
        ],
    },
    {
        'name': 'NIO', 'slug': 'nio', 'wiki': 'NIO ET5',
        'models': [
            ('ES6',  'es6',  'NIO ES6',  'Premium midsize electric SUV with NIO\'s unique battery-swap capability.', 2023),
            ('ES8',  'es8',  'NIO ES8',  'Large 6 or 7-seat electric SUV — NIO\'s flagship family vehicle.', 2021),
            ('ET5',  'et5',  'NIO ET5',  'Midsize electric sedan that takes on the Tesla Model 3 with a compelling package.', 2022),
            ('ET7',  'et7',  'NIO ET7',  'NIO\'s flagship luxury electric sedan with up to 1,000 km range on 150 kWh battery.', 2022),
            ('EC6',  'ec6',  'NIO EC6',  'Sleek coupe-SUV electric with sporty roofline and NIO\'s full smart tech suite.', 2021),
        ],
    },
    {
        'name': 'Li Auto', 'slug': 'li-auto', 'wiki': 'Li Auto L9',
        'models': [
            ('L9',   'l9',   'Li Auto L9',   'Flagship 6-seat EREV SUV — Li Auto\'s most capable and luxurious family vehicle.', 2022),
            ('L8',   'l8',   'Li Auto L8',   '6-seat extended-range electric SUV, the heart of the Li Auto family lineup.', 2022),
            ('L7',   'l7',   'Li Auto L7',   '5-seat EREV performance SUV that combines sportiness with long-distance capability.', 2023),
            ('L6',   'l6',   'Li Auto L6',   'Entry EREV SUV bringing Li Auto\'s technology to a more accessible price point.', 2024),
        ],
    },
    {
        'name': 'Xpeng', 'slug': 'xpeng', 'wiki': 'Xpeng G6',
        'models': [
            ('P7',   'p7',   'Xpeng P7',   'Smart electric sedan with advanced XNGP autonomous driving — a true Tesla rival.', 2021),
            ('G6',   'g6',   'Xpeng G6',   'Sleek midsize electric SUV on the SEPA 2.0 platform with 800V fast charging.', 2023),
            ('G9',   'g9',   'Xpeng G9',   'Large electric SUV with Xpeng\'s most advanced smart driving system.', 2022),
            ('X9',   'x9',   'Xpeng X9',   'Flagship 7-seat electric MPV with exceptional interior space and smart tech.', 2024),
            ('P5',   'p5',   'Xpeng P5',   'Affordable smart electric sedan with LiDAR-based autonomous driving capability.', 2021),
        ],
    },
    {
        'name': 'MG Motor', 'slug': 'mg-motor', 'wiki': 'MG4 EV',
        'models': [
            ('MG4',      'mg4',      'MG4 EV',      'Award-winning compact electric hatchback — excellent value and impressive dynamics.', 2022),
            ('ZS EV',    'zs-ev',    'MG ZS',       'Popular compact electric SUV — the EV that brought affordable range to the masses.', 2021),
            ('HS',       'hs',       'MG HS',       'Stylish midsize SUV available as PHEV — spacious and feature-packed at competitive pricing.', 2021),
            ('MG5',      'mg5',      'MG5',         'Practical electric estate/wagon with long range and family-friendly practicality.', 2021),
            ('Cyberster', 'cyberster','MG Cyberster', 'Head-turning electric roadster that revives the classic MG spirit for the EV era.', 2023),
        ],
    },
    {
        'name': 'Haval', 'slug': 'haval', 'wiki': 'Haval H6',
        'models': [
            ('H6',     'h6',     'Haval H6',     'China\'s best-selling SUV — reliable, well-equipped, and available as a hybrid.', 2021),
            ('Jolion',  'jolion', 'Haval Jolion',  'Stylish compact crossover with hybrid options and a tech-forward interior.', 2021),
            ('H9',     'h9',     'Haval H9',     'Body-on-frame SUV built for serious off-road adventures with 7-seat capacity.', 2021),
            ('Dargo',   'dargo',  'Haval Dargo',   'Off-road oriented crossover with rugged styling and available PHEV powertrain.', 2021),
        ],
    },
    {
        'name': 'Chery', 'slug': 'chery', 'wiki': 'Chery Tiggo 8',
        'models': [
            ('Tiggo 7 Pro',  'tiggo-7-pro',  'Chery Tiggo 7 Pro',  'Comfortable midsize SUV with strong powertrains and premium interior quality.', 2021),
            ('Tiggo 8 Pro',  'tiggo-8-pro',  'Chery Tiggo 8',      'Large family SUV with 3-row seating and a generous feature list for the price.', 2021),
            ('Tiggo 4 Pro',  'tiggo-4-pro',  'Chery Tiggo 4',      'Compact SUV bringing modern design and tech to an entry-level price point.', 2022),
            ('Arrizo 6',     'arrizo-6',     'Chery Arrizo 6',     'Stylish compact sedan with sporty character and impressive value.', 2021),
        ],
    },
    {
        'name': 'Zeekr', 'slug': 'zeekr', 'wiki': 'Zeekr 001',
        'models': [
            ('001',  'zeekr-001', 'Zeekr 001',  'High-performance electric shooting brake — Geely\'s premium EV with supercar acceleration.', 2021),
            ('009',  'zeekr-009', 'Zeekr 009',  'Flagship luxury electric MPV — the world\'s most powerful electric van.', 2022),
            ('X',    'zeekr-x',   'Zeekr X',    'Compact electric crossover combining Zeekr performance with city-friendly dimensions.', 2023),
            ('007',  'zeekr-007', 'Zeekr 007',  'Premium electric sedan with 800V platform and exceptional efficiency.', 2024),
        ],
    },
    {
        'name': 'Hongqi', 'slug': 'hongqi', 'wiki': 'Hongqi HS5',
        'models': [
            ('H5',   'h5',   'Hongqi H5',   'Luxury midsize sedan blending Chinese heritage with modern premium comfort.', 2021),
            ('HS5',  'hs5',  'Hongqi HS5',  'Premium midsize SUV — the aspirational choice for Chinese luxury buyers.', 2021),
            ('E-HS9','e-hs9','Hongqi E-HS9','Flagship luxury electric SUV with 6 or 7 seats and ultra-premium appointments.', 2021),
            ('H9',   'hq-h9','Hongqi H9',   'Ultra-luxury full-size saloon that challenges Bentley and Rolls-Royce on Chinese roads.', 2021),
        ],
    },
    {
        'name': 'Geely', 'slug': 'geely', 'wiki': 'Geely Coolray',
        'models': [
            ('Coolray',   'coolray',  'Geely Coolray',   'Sporty compact SUV with turbocharged engine and eye-catching coupe-like design.', 2021),
            ('Azkarra',   'azkarra',  'Geely Azkarra',   'Compact hybrid SUV — Geely\'s answer to fuel-efficient family motoring.', 2021),
            ('Okavango',  'okavango', 'Geely Okavango',  'Three-row hybrid SUV offering genuine space and fuel efficiency for families.', 2021),
            ('Emgrand',   'emgrand',  'Geely Emgrand',   'Popular compact sedan — reliable, affordable, and widely available globally.', 2021),
        ],
    },
    {
        'name': 'AITO', 'slug': 'aito', 'wiki': 'Aito M7',
        'models': [
            ('M5',  'm5',  'Aito M5',  'HUAWEI-backed EREV SUV blending impressive tech with strong driving range.', 2022),
            ('M7',  'm7',  'Aito M7',  'Large 6-seat EREV SUV with HUAWEI\'s HarmonyOS cockpit and DRES powertrain.', 2022),
            ('M9',  'm9',  'Aito M9',  'Flagship luxury EREV SUV — AITO\'s most ambitious and feature-laden model.', 2023),
        ],
    },
    {
        'name': 'Ora', 'slug': 'ora', 'wiki': 'Ora Good Cat',
        'models': [
            ('Good Cat',   'good-cat',   'Ora Good Cat',   'Retro-styled electric city car with quirky character and impressive efficiency.', 2021),
            ('Funky Cat',  'funky-cat',  'Ora Funky Cat',  'Playful compact EV with distinctive design and practical everyday range.', 2022),
            ('Lightning Cat','lightning-cat','Ora Lightning Cat','Performance-oriented electric coupe with GT styling and spirited dynamics.', 2022),
        ],
    },

    # ── Other popular brands ─────────────────────────────────────────────────────
    {
        'name': 'Alfa Romeo', 'slug': 'alfa-romeo', 'wiki': 'Alfa Romeo Giulia (952)',
        'models': [
            ('Giulia',   'giulia',  'Alfa Romeo Giulia (952)',  'The Italian sports sedan — beautiful, driver-focused, and unlike anything else.', 2021),
            ('Stelvio',  'stelvio', 'Alfa Romeo Stelvio',       'An SUV that drives like a sports car — the most driver-focused crossover money can buy.', 2021),
            ('Tonale',   'tonale',  'Alfa Romeo Tonale',        'Compact PHEV crossover bringing Alfa Romeo style to the premium compact segment.', 2022),
        ],
    },
    {
        'name': 'Mitsubishi', 'slug': 'mitsubishi', 'wiki': 'Mitsubishi Outlander',
        'models': [
            ('Outlander',     'outlander',     'Mitsubishi Outlander',      'Redesigned three-row SUV with bold styling, standard PHEV option, and generous space.', 2022),
            ('Eclipse Cross', 'eclipse-cross', 'Mitsubishi Eclipse Cross',  'A stylish compact SUV/crossover with PHEV powertrain and a coupe-like roofline.', 2021),
            ('ASX',           'asx',           'Mitsubishi ASX',            'Compact crossover recently refreshed with a new platform and Renault underpinnings.', 2023),
            ('Pajero Sport',  'pajero-sport',  'Mitsubishi Pajero Sport',   'Body-on-frame SUV built for genuine off-road capability with 7-seat comfort.', 2021),
        ],
    },
    {
        'name': 'Acura', 'slug': 'acura', 'wiki': 'Acura TLX',
        'models': [
            ('TLX',  'tlx',  'Acura TLX',  'Honda\'s premium sport sedan with sharp styling, Type S performance variant, and SH-AWD.', 2021),
            ('MDX',  'mdx',  'Acura MDX',  'Three-row luxury SUV — Acura\'s flagship offering with superb ride quality.', 2022),
            ('RDX',  'rdx',  'Acura RDX',  'Sporty compact luxury SUV with a unique landscape touchpad and available Type S.', 2021),
            ('Integra', 'integra', 'Acura Integra (DC6)', 'The iconic nameplate returns as a premium sport compact with a manual option.', 2023),
        ],
    },
    {
        'name': 'Lincoln', 'slug': 'lincoln', 'wiki': 'Lincoln Aviator',
        'models': [
            ('Nautilus',  'nautilus',  'Lincoln Nautilus',  'A refined midsize luxury SUV with a serene interior and QuietFlight design.', 2021),
            ('Aviator',   'aviator',   'Lincoln Aviator',   'Three-row luxury SUV with available plug-in hybrid and stunning interior.', 2021),
            ('Navigator', 'navigator', 'Lincoln Navigator', 'Full-size luxury SUV icon — the most opulent American SUV available.', 2021),
            ('Corsair',   'corsair',   'Lincoln Corsair',   'Compact luxury SUV with available plug-in hybrid and class-leading quiet ride.', 2021),
        ],
    },
    {
        'name': 'Buick', 'slug': 'buick', 'wiki': 'Buick Enclave',
        'models': [
            ('Enclave',   'enclave',   'Buick Enclave',   'Three-row luxury crossover with Buick\'s signature QuietTuning and comfortable ride.', 2021),
            ('Encore GX', 'encore-gx', 'Buick Encore GX', 'Compact luxury crossover with a well-appointed interior and user-friendly tech.', 2021),
            ('Envision',  'envision',  'Buick Envision',  'Midsize luxury crossover bridging the gap with a balanced blend of comfort and tech.', 2021),
            ('Envista',   'envista',   'Buick Envista',   'Subcompact luxury crossover bringing Buick refinement to the entry level.', 2023),
        ],
    },
    {
        'name': 'Polestar', 'slug': 'polestar', 'wiki': 'Polestar 2',
        'models': [
            ('Polestar 2', 'polestar-2', 'Polestar 2', 'Volvo\'s performance EV brand — the Model 3 rival with Scandinavian minimalism and superb build.', 2021),
            ('Polestar 3', 'polestar-3', 'Polestar 3', 'A luxury performance electric SUV sharing its platform with the Volvo EX90.', 2023),
            ('Polestar 4', 'polestar-4', 'Polestar 4', 'Electric performance SUV-coupe without a rear window — bold, fast, and efficient.', 2024),
        ],
    },
    {
        'name': 'Rivian', 'slug': 'rivian', 'wiki': 'Rivian R1T',
        'models': [
            ('R1T', 'r1t', 'Rivian R1T', 'The world\'s first all-electric adventure pickup truck — powerful, capable, and genuinely fun.', 2022),
            ('R1S', 'r1s', 'Rivian R1S', 'Electric adventure SUV with 3 rows, immense off-road ability, and exceptional range.', 2022),
            ('R2',  'r2',  'Rivian R2',  'Rivian\'s more affordable electric SUV bringing adventure capability to a wider audience.', 2025),
        ],
    },
    {
        'name': 'Suzuki', 'slug': 'suzuki', 'wiki': 'Suzuki Jimny',
        'models': [
            ('Jimny',   'jimny',   'Suzuki Jimny',   'Cult-status micro off-roader — tiny footprint, ladder-frame chassis, and genuine 4x4 ability.', 2021),
            ('Vitara',  'vitara',  'Suzuki Vitara',  'Compact crossover with mild hybrid efficiency and available AllGrip four-wheel drive.', 2021),
            ('Swift',   'swift',   'Suzuki Swift',   'An award-winning compact hatchback — light, fun, efficient, and reliable.', 2021),
            ('S-Cross', 's-cross', 'Suzuki S-Cross', 'Practical compact SUV with full hybrid option and Suzuki\'s AllGrip AWD system.', 2021),
        ],
    },
    {
        'name': 'Isuzu', 'slug': 'isuzu', 'wiki': 'Isuzu D-Max',
        'models': [
            ('D-Max',   'd-max',   'Isuzu D-Max',    'The working-class pickup hero — indestructible, torquey diesel, and globally proven.', 2021),
            ('MU-X',    'mu-x',    'Isuzu MU-X',     'A body-on-frame SUV derived from the D-Max with 7 seats and genuine off-road credentials.', 2021),
        ],
    },
]

REVIEW_POOL = [
    (5, "Absolutely love it — couldn't be happier",
     "Picked up my {year} {car} and have zero complaints. Build quality is exceptional, the technology is genuinely impressive, and it puts a smile on my face every commute. Real-world range exceeds what I expected. Highly recommend."),
    (5, "Best purchase I've ever made",
     "I've owned many cars and the {year} {car} is comfortably the best. Interior feels genuinely premium, the powertrain is whisper-quiet, and the tech works intuitively. Minor gripe is wind noise at motorway speeds but that's it."),
    (5, "Exceeded every expectation",
     "After 18 months with my {year} {car}, not a single unplanned visit to the dealer. The safety features have already helped me avoid two incidents on the motorway. Comfortable on long journeys, easy to park in town. Outstanding."),
    (5, "Worth every penny",
     "The {year} {car} has more than justified the price. The refinement difference vs my old car is immediately obvious. Cruising at motorway speed is serene, tech is useful not gimmicky, and running costs are lower than expected."),
    (5, "Three years in — still impressed",
     "45,000 miles, zero mechanical issues. Everything works as it did on day one, resale is holding up brilliantly. If you want reliable long-term ownership, look no further."),
    (5, "EV convert — never going back",
     "The {year} {car} converted me to electric. Charging at home overnight means I never visit a petrol station. The instant torque makes every journey enjoyable, and the running cost savings are remarkable."),
    (5, "Chinese engineering has arrived",
     "I was sceptical about a Chinese brand, but the {year} {car} genuinely surprised me. The fit and finish is excellent, the tech is class-leading, and the value for money is extraordinary. European rivals should be worried."),
    (5, "Family road trip approved",
     "1,200 miles in our {year} {car} with two kids and a dog. Boot swallowed everything, rear space genuinely comfortable, and the kids fell asleep before we left the city. Ultimate family car endorsement."),
    (4, "Really good — a few niggles but nothing major",
     "Excellent car overall. Strong points: ride quality, interior space, standard tech. Weak points: slightly fiddly touchscreen and some hard plastic in places. Neither is a dealbreaker. Would buy again without hesitation."),
    (4, "Great daily driver, small gripes",
     "Eight months in — efficiency, comfort, and how it handles city traffic are all impressive. My gripes are that rear legroom is tight for taller adults and the auto hesitates occasionally. Minor issues in an otherwise excellent package."),
    (4, "Solid choice — does most things very well",
     "Hits the sweet spot for me. Refined on the motorway, economical for commuting, practical for family duties. Only gripe is the infotainment system slow to connect to phone on start-up. Build quality noticeably better than my previous car."),
    (4, "Impressed after 12 months",
     "I was sceptical when ordering — felt like I was playing it safe. A year in, I'm genuinely impressed. More refined than expected, comfortable over long distances, nothing unexpected has gone wrong."),
    (4, "Surprisingly fun to drive",
     "Bought for practicality, expected dull. Wrong. The chassis is genuinely sorted — precise steering, good body control, and real eagerness. Makes you look forward to driving rather than dreading it."),
    (4, "Excellent value for the spec",
     "Mid-spec was the sweet spot. Heated seats, wireless CarPlay, blind-spot monitoring all standard. Build quality feels honest and durable. Nothing showy or fragile. Exactly what I needed."),
    (4, "Tech is impressive, reliability TBD",
     "The {year} {car} offers genuinely impressive technology — the driver assistance systems are class-leading and the infotainment is intuitive. Taking one star off as it's still too early to judge long-term reliability."),
    (3, "Decent, but not outstanding",
     "Solid car that does its job competently without exciting me. Ride comfortable, easy to drive. However, interior materials feel a step below the price point and the engine is noisy when pushed. Reliable but not class-leading."),
    (3, "Mixed feelings after six months",
     "Excited at purchase, reality more subdued. Positives: generous space, good economy. Negatives: touchscreen occasionally freezes, rear wiper smears in light rain, lane-keeping is too aggressive. Not bad but needs polish."),
    (3, "Good but expected more",
     "Competent, reliable, comfortable. But 'competent' isn't what you want when spending this much. A few hard plastic panels at this price point, engine note is unpleasant when pushed. Test the competition before committing."),
    (3, "Average — wouldn't buy again",
     "Functional but underwhelming. Ride is fine, economy acceptable, reliable enough. But every time I get in I feel I settled. Looking at alternatives for my next purchase."),
    (2, "Disappointed — reliability let me down",
     "Bought on strong reviews and brand reputation. Ongoing electronic issues: infotainment crashed twice, lane-keeping triggered unexpectedly three times. Dealer slow to acknowledge these as known issues. The car itself drives fine but reliability soured everything."),
    (2, "Quality control issues from day one",
     "Factory fit-and-finish issues right off the lot — a door seal that whistles at speed, dashboard rattle took three dealer visits to fix. Disappointing for this price. Should have been right first time."),
    (1, "Ongoing reliability nightmare",
     "Fourteen months in and my {year} {car} has spent more time at the dealer than my driveway. Turbo failed at 8,000 miles, infotainment blank at 11,000, persistent vibration no one can locate. First and last experience with this brand."),
    (1, "Worst car purchase I've ever made",
     "Cannot recommend. Transmission issue, electrical fault that stranded me, engine light the dealer cannot diagnose. Every visit takes a week. I had high expectations. Avoid."),
]

WEIGHTS = {5: 35, 4: 30, 3: 15, 2: 10, 1: 10}
_BY_RATING = {r: [rv for rv in REVIEW_POOL if rv[0] == r] for r in range(1, 6)}


def _pick_review(car_name, year):
    rating = random.choices(list(WEIGHTS), weights=list(WEIGHTS.values()), k=1)[0]
    candidates = _BY_RATING.get(rating) or REVIEW_POOL
    t = random.choice(candidates)
    return t[0], t[1], t[2].replace('{car}', car_name).replace('{year}', str(year))


def get_wiki_image(title, width=600):
    try:
        r = requests.get('https://en.wikipedia.org/w/api.php', params={
            'action': 'query', 'titles': title, 'prop': 'pageimages',
            'pithumbsize': width, 'format': 'json',
        }, timeout=12, headers={'User-Agent': 'Mozilla/5.0'})
        pages = r.json()['query']['pages']
        page = next(iter(pages.values()))
        return page.get('thumbnail', {}).get('source')
    except Exception:
        return None


def download(url, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    for _ in range(3):
        try:
            r = requests.get(url, timeout=20, headers={'User-Agent': 'Mozilla/5.0'})
            if r.status_code == 200:
                open(dest, 'wb').write(r.content)
                return True
            elif r.status_code == 429:
                time.sleep(15)
        except Exception:
            time.sleep(2)
    return False


def main():
    app = create_app('development')
    with app.app_context():
        cat = Category.query.filter_by(slug='cars').first()
        if not cat:
            print('Cars category not found — run add_cars.py first')
            return

        total_subjects = 0
        total_reviews = 0

        for brand in BRANDS:
            sc = SubCategory.query.filter_by(category_id=cat.id, slug=brand['slug']).first()
            if not sc:
                sc = SubCategory(category_id=cat.id, name=brand['name'], slug=brand['slug'])
                db.session.add(sc)
                db.session.flush()
                print(f'  Created: {brand["name"]}')
            else:
                print(f'  Existing: {brand["name"]}')

            # Brand image
            brand_dest = os.path.join(STATIC_DIR, 'images', 'uploads', 'subcategories', f'cars-{brand["slug"]}.jpg')
            if not sc.image_path or not os.path.exists(os.path.join(STATIC_DIR, sc.image_path or '')):
                url = get_wiki_image(brand['wiki'])
                if url and download(url, brand_dest):
                    sc.image_path = f'images/uploads/subcategories/cars-{brand["slug"]}.jpg'
                    print(f'    brand image saved')
                else:
                    print(f'    brand image failed')
            time.sleep(0.5)

            for m_name, m_slug, m_wiki, m_desc, m_start in brand['models']:
                # Model image (shared across years)
                model_img_rel = f'images/uploads/subjects/cars-{m_slug}.jpg'
                model_img_dest = os.path.join(STATIC_DIR, model_img_rel)
                model_img_ok = os.path.exists(model_img_dest)
                if not model_img_ok:
                    url = get_wiki_image(m_wiki)
                    if url and download(url, model_img_dest):
                        model_img_ok = True
                        print(f'      img: {m_name}')
                    else:
                        print(f'      no img: {m_name}')
                    time.sleep(0.5)

                full_name = f'{brand["name"]} {m_name}'

                for year in YEARS:
                    if year < m_start:
                        continue
                    subj_slug = f'{m_slug}-{year}'
                    subj = Subject.query.filter_by(subcategory_id=sc.id, slug=subj_slug).first()
                    if not subj:
                        subj = Subject(
                            subcategory_id=sc.id,
                            name=f'{m_name} {year}',
                            slug=subj_slug,
                            description=f'The {year} {full_name}. {m_desc}',
                            image_path=model_img_rel if model_img_ok else None,
                        )
                        db.session.add(subj)
                        db.session.flush()
                        total_subjects += 1

                    existing = Review.query.filter_by(subject_id=subj.id).count()
                    target = random.randint(12, 40)
                    base_date = datetime.utcnow() - timedelta(days=random.randint(30, 730))
                    used_titles = set()
                    for i in range(max(0, target - existing)):
                        for _ in range(5):
                            rating, title, body = _pick_review(full_name, year)
                            if title not in used_titles:
                                used_titles.add(title)
                                break
                        db.session.add(Review(
                            subject_id=subj.id, title=title, body=body, rating=rating,
                            author_name=_rname(), source_site='sample',
                            original_date=base_date - timedelta(days=i * random.randint(2, 20)),
                            is_published=True,
                        ))
                        total_reviews += 1

            db.session.commit()
            print(f'    committed {brand["name"]}')

        # Update stats
        print('Updating stats...')
        for sc in SubCategory.query.filter_by(category_id=cat.id).all():
            for subj in sc.subjects.all():
                subj.update_stats()
        db.session.commit()

        print(f'\nDone. {total_subjects} new subjects, {total_reviews} new reviews.')


if __name__ == '__main__':
    main()
