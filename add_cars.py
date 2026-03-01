#!/usr/bin/env python3
"""Adds Cars & Vehicles category with car brands as subcategories
and model+year as subjects, with sample reviews and Wikipedia images.

Usage: python add_cars.py
"""
import os, sys, time, random, requests
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Category, SubCategory, Subject, Review

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

_ADJECTIVES = [
    'Big', 'Tiny', 'Blue', 'Red', 'Happy', 'Grumpy', 'Sneaky', 'Fluffy',
    'Brave', 'Lazy', 'Spicy', 'Chilly', 'Wild', 'Calm', 'Swift', 'Clumsy',
    'Bouncy', 'Fuzzy', 'Mighty', 'Sleepy', 'Dizzy', 'Funky', 'Shiny', 'Dusty',
]
_ANIMALS = [
    'Baboon', 'Penguin', 'Panda', 'Narwhal', 'Capybara', 'Quokka', 'Axolotl',
    'Platypus', 'Wombat', 'Toucan', 'Lemur', 'Meerkat', 'Tapir', 'Okapi',
    'Alpaca', 'Manatee', 'Blobfish', 'Gecko', 'Flamingo', 'Armadillo',
]

def _rname():
    return f"{random.choice(_ADJECTIVES)}{random.choice(_ANIMALS)}{random.randint(1, 999)}"


YEARS = [2021, 2022, 2023, 2024, 2025]

# (model_name, slug, wiki_title, description, start_year)
BRANDS = [
    {
        'name': 'Toyota', 'slug': 'toyota', 'wiki': 'Toyota',
        'models': [
            ('Camry', 'camry', 'Toyota Camry', 'Mid-size sedan renowned for exceptional reliability, a smooth ride, and low running costs.', 2021),
            ('Corolla', 'corolla', 'Toyota Corolla', "The world's best-selling compact car — dependable, economical, and consistently refined.", 2021),
            ('RAV4', 'rav4', 'Toyota RAV4', "America's top-selling SUV, combining everyday practicality with capable standard or optional AWD.", 2021),
            ('Highlander', 'highlander', 'Toyota Highlander', 'Three-row family SUV delivering generous space, comfort, and proven long-term reliability.', 2021),
            ('Tacoma', 'tacoma', 'Toyota Tacoma', 'The mid-size pickup that dominates its segment with off-road chops and outstanding resale value.', 2021),
            ('Prius', 'prius', 'Toyota Prius', 'The hybrid that started it all — exceptional fuel economy in a modern, increasingly stylish package.', 2021),
        ],
    },
    {
        'name': 'Ford', 'slug': 'ford', 'wiki': 'Ford Motor Company',
        'models': [
            ('F-150', 'f-150', 'Ford F-150', "America's best-selling vehicle for decades — powerful, configurable, and available with every powertrain imaginable.", 2021),
            ('Mustang', 'mustang', 'Ford Mustang', 'The iconic American muscle car, blending performance heritage with modern tech since 1964.', 2021),
            ('Explorer', 'explorer', 'Ford Explorer', 'A full-size three-row SUV with a long legacy as the go-to family adventure vehicle.', 2021),
            ('Escape', 'escape', 'Ford Escape', 'A compact SUV offering efficiency, technology, and an available plug-in hybrid powertrain.', 2021),
            ('Bronco', 'bronco', 'Ford Bronco (sixth generation)', "Ford's legendary 4x4 reborn — rugged, capable, and dripping with retro off-road style.", 2021),
            ('Ranger', 'ranger', 'Ford Ranger', 'A versatile mid-size pickup balancing genuine work capability with everyday drivability.', 2021),
        ],
    },
    {
        'name': 'BMW', 'slug': 'bmw', 'wiki': 'BMW',
        'models': [
            ('3 Series', '3-series', 'BMW 3 Series', 'The benchmark sports sedan — precise handling, premium quality, and real driver engagement.', 2021),
            ('5 Series', '5-series', 'BMW 5 Series', 'Executive luxury sedan combining sharp dynamics with true long-distance comfort.', 2021),
            ('X3', 'x3', 'BMW X3', 'A compact luxury SUV that refuses to compromise on driving dynamics or interior quality.', 2021),
            ('X5', 'x5', 'BMW X5', "BMW's most popular SUV — spacious, powerful, and supremely refined on any road.", 2021),
            ('M3', 'm3', 'BMW M3', 'The ultimate sports sedan — track-ready performance wrapped in practical daily-driver packaging.', 2021),
        ],
    },
    {
        'name': 'Honda', 'slug': 'honda', 'wiki': 'Honda',
        'models': [
            ('Civic', 'civic', 'Honda Civic', 'The perennial compact benchmark — sharp styling, engaging drive, and legendary Honda build quality.', 2021),
            ('Accord', 'accord', 'Honda Accord', 'A mid-size sedan that consistently sets the standard for space, refinement, and value.', 2021),
            ('CR-V', 'cr-v', 'Honda CR-V', "One of America's favourite compact SUVs — practical, fuel-efficient, and genuinely family-friendly.", 2021),
            ('Pilot', 'pilot', 'Honda Pilot', 'A three-row family SUV with a strong reputation for reliability and a spacious cabin.', 2021),
            ('Odyssey', 'odyssey', 'Honda Odyssey', 'The minivan that refuses to be boring — clever storage, a potent engine, and Honda reliability.', 2021),
        ],
    },
    {
        'name': 'Chevrolet', 'slug': 'chevrolet', 'wiki': 'Chevrolet',
        'models': [
            ('Silverado 1500', 'silverado-1500', 'Chevrolet Silverado', "America's perennial pickup choice — tough, configurable, and available with every engine you could want.", 2021),
            ('Equinox', 'equinox', 'Chevrolet Equinox', 'A compact SUV delivering practicality and user-friendly technology at an accessible price.', 2021),
            ('Traverse', 'traverse', 'Chevrolet Traverse', 'A spacious three-row SUV with genuinely comfortable seating and a generous boot.', 2021),
            ('Blazer', 'blazer', 'Chevrolet Blazer', 'A sporty mid-size SUV with head-turning looks and a well-equipped interior.', 2021),
            ('Colorado', 'colorado', 'Chevrolet Colorado', 'A mid-size pickup offering the right balance between hauling capability and everyday comfort.', 2021),
        ],
    },
    {
        'name': 'Mercedes-Benz', 'slug': 'mercedes-benz', 'wiki': 'Mercedes-Benz',
        'models': [
            ('C-Class', 'c-class', 'Mercedes-Benz C-Class', "Mercedes' most popular model worldwide — elegant, tech-loaded, and supremely well built.", 2021),
            ('E-Class', 'e-class', 'Mercedes-Benz E-Class', 'The definitive executive sedan — benchmark luxury, advanced safety tech, and effortless cruising.', 2021),
            ('GLE', 'gle', 'Mercedes-Benz GLE', 'A flagship luxury SUV delivering opulence, cutting-edge technology, and genuine off-road ability.', 2021),
            ('GLC', 'glc', 'Mercedes-Benz GLC', 'A compact luxury SUV combining everyday practicality with understated Mercedes-Benz prestige.', 2021),
            ('S-Class', 's-class', 'Mercedes-Benz S-Class', 'The flagship that sets the global standard for automotive luxury and technological leadership.', 2021),
        ],
    },
    {
        'name': 'Audi', 'slug': 'audi', 'wiki': 'Audi',
        'models': [
            ('A4', 'a4', 'Audi A4', 'A compact executive saloon with impeccable build quality and available quattro all-wheel drive.', 2021),
            ('A6', 'a6', 'Audi A6', 'A mid-size luxury saloon that effortlessly blends class-leading technology with refined, quiet driving.', 2021),
            ('Q5', 'q5', 'Audi Q5', "The world's best-selling Audi — a premium compact SUV with quattro sure-footedness.", 2021),
            ('Q7', 'q7', 'Audi Q7', 'A three-row luxury SUV offering understated elegance and genuine long-distance comfort.', 2021),
            ('e-tron', 'e-tron', 'Audi e-tron', "Audi's fully electric SUV — luxurious, refined, and all-wheel drive as standard.", 2021),
        ],
    },
    {
        'name': 'Volkswagen', 'slug': 'volkswagen', 'wiki': 'Volkswagen',
        'models': [
            ('Golf', 'golf', 'Volkswagen Golf', 'The quintessential hatchback — class-leading build quality and driving dynamics in a practical package.', 2021),
            ('Jetta', 'jetta', 'Volkswagen Jetta', 'A refined compact sedan delivering European driving feel at a very sensible price.', 2021),
            ('Tiguan', 'tiguan', 'Volkswagen Tiguan', 'A premium compact SUV with a sophisticated interior and optional third-row seating.', 2021),
            ('Atlas', 'atlas', 'Volkswagen Atlas', "VW's boldest SUV — genuinely spacious three-row seating in a refined, well-equipped package.", 2021),
            ('ID.4', 'id4', 'Volkswagen ID.4', 'An all-electric crossover that makes the transition to EV feel completely natural and stress-free.', 2021),
        ],
    },
    {
        'name': 'Hyundai', 'slug': 'hyundai', 'wiki': 'Hyundai',
        'models': [
            ('Elantra', 'elantra', 'Hyundai Elantra', 'A compact sedan with genuinely striking design and a feature-packed interior at a competitive price.', 2021),
            ('Tucson', 'tucson', 'Hyundai Tucson', 'A compact SUV that punches well above its weight in design, technology, and interior refinement.', 2021),
            ('Santa Fe', 'santa-fe', 'Hyundai Santa Fe', 'A mid-size SUV offering a premium-feel interior, standard safety tech, and an industry-leading warranty.', 2021),
            ('Ioniq 5', 'ioniq-5', 'Hyundai Ioniq 5', 'A revolutionary EV with ultra-fast charging, a spacious interior, and stunning retro-futurist design.', 2022),
            ('Palisade', 'palisade', 'Hyundai Palisade', 'A three-row SUV with a genuinely premium interior that rivals vehicles costing significantly more.', 2021),
        ],
    },
    {
        'name': 'Kia', 'slug': 'kia', 'wiki': 'Kia',
        'models': [
            ('Forte', 'forte', 'Kia Forte', "Kia's sporty compact sedan — sharp styling, a generous feature list, and a class-leading warranty.", 2021),
            ('K5', 'k5', 'Kia K5', 'A mid-size sedan with striking looks, driver-focused dynamics, and strong value for money.', 2021),
            ('Sportage', 'sportage', 'Kia Sportage', 'A compact SUV balancing bold design, a practical interior, and impressive standard safety tech.', 2021),
            ('Telluride', 'telluride', 'Kia Telluride', 'The award-winning three-row SUV that redefined what the Kia brand can achieve.', 2021),
            ('EV6', 'ev6', 'Kia EV6', "Kia's breakthrough electric vehicle — sporty, ultra-fast-charging, and design-forward.", 2022),
        ],
    },
    {
        'name': 'Nissan', 'slug': 'nissan', 'wiki': 'Nissan',
        'models': [
            ('Altima', 'altima', 'Nissan Altima', 'A mid-size sedan offering available AWD, a smooth ride, and competitive fuel economy.', 2021),
            ('Rogue', 'rogue', 'Nissan Rogue', 'A compact SUV known for a comfortable ride and clever ProPilot Assist driver technology.', 2021),
            ('Pathfinder', 'pathfinder', 'Nissan Pathfinder', 'A three-row SUV with genuine off-road heritage and comfortable family-friendly accommodations.', 2021),
            ('Sentra', 'sentra', 'Nissan Sentra', 'An affordable compact sedan with surprisingly upscale styling and standard safety features.', 2021),
            ('Frontier', 'frontier', 'Nissan Frontier', 'A refreshed mid-size pickup with a proven powertrain and capable standard and off-road specs.', 2021),
        ],
    },
    {
        'name': 'Subaru', 'slug': 'subaru', 'wiki': 'Subaru',
        'models': [
            ('Outback', 'outback', 'Subaru Outback', 'The adventure-ready wagon-SUV crossover with standard AWD, EyeSight safety, and generous ground clearance.', 2021),
            ('Forester', 'forester', 'Subaru Forester', 'A compact SUV prioritising exceptional visibility, all-weather confidence, and practical packaging.', 2021),
            ('Crosstrek', 'crosstrek', 'Subaru Crosstrek', 'A compact crossover with an adventurous spirit, high ground clearance, and available hybrid powertrain.', 2021),
            ('WRX', 'wrx', 'Subaru WRX', 'The rally-bred performance sedan with turbocharged grunt and iconic all-weather symmetrical AWD.', 2021),
            ('BRZ', 'brz', 'Subaru BRZ', 'A pure, lightweight sports coupe focused entirely on driving engagement over outright horsepower.', 2021),
        ],
    },
    {
        'name': 'Mazda', 'slug': 'mazda', 'wiki': 'Mazda',
        'models': [
            ('Mazda3', 'mazda3', 'Mazda3', 'A compact car that genuinely feels premium — refined, stylish, and driver-focused above its class.', 2021),
            ('CX-5', 'cx-5', 'Mazda CX-5', 'The benchmark compact SUV for ride quality and driving dynamics in its segment.', 2021),
            ('CX-50', 'cx-50', 'Mazda CX-50', "Mazda's rugged outdoor-capable crossover with standard AWD and a genuinely upscale interior.", 2022),
            ('MX-5 Miata', 'mx-5-miata', 'Mazda MX-5', "The world's best-selling roadster — pure, lightweight, and joyously fun to drive.", 2021),
        ],
    },
    {
        'name': 'Jeep', 'slug': 'jeep', 'wiki': 'Jeep',
        'models': [
            ('Wrangler', 'wrangler', 'Jeep Wrangler', 'The ultimate off-road icon — removable doors and roof, open-air freedom, and go-anywhere capability.', 2021),
            ('Grand Cherokee', 'grand-cherokee', 'Jeep Grand Cherokee', "Jeep's flagship SUV balancing genuine luxury with Quadra-Trac off-road ability.", 2021),
            ('Compass', 'compass', 'Jeep Compass', 'A compact SUV bringing Jeep ruggedness, available 4x4, and distinctive style to everyday commuting.', 2021),
            ('Gladiator', 'gladiator', 'Jeep Gladiator', "The world's most capable mid-size pickup — a Wrangler with a bed.", 2021),
        ],
    },
    {
        'name': 'Tesla', 'slug': 'tesla', 'wiki': 'Tesla, Inc.',
        'models': [
            ('Model 3', 'model-3', 'Tesla Model 3', 'The electric sedan that made EVs genuinely desirable — long range, rapid Supercharging, and Autopilot.', 2021),
            ('Model Y', 'model-y', 'Tesla Model Y', "Tesla's best-selling SUV and one of the world's best-selling vehicles overall.", 2021),
            ('Model S', 'model-s', 'Tesla Model S', 'The flagship electric sedan — extraordinary performance, exceptional range, and over-the-air updates.', 2021),
            ('Model X', 'model-x', 'Tesla Model X', 'A flagship electric SUV with iconic falcon-wing doors and breathtaking acceleration.', 2021),
            ('Cybertruck', 'cybertruck', 'Tesla Cybertruck', "Tesla's angular stainless-steel pickup — polarising design, massive capability, and tri-motor power.", 2024),
        ],
    },
    {
        'name': 'Porsche', 'slug': 'porsche', 'wiki': 'Porsche',
        'models': [
            ('911', '911', 'Porsche 911', "The world's most iconic sports car — continuously evolved over 60 years yet unmistakably itself.", 2021),
            ('Cayenne', 'cayenne', 'Porsche Cayenne', 'A luxury SUV that drives like a sports car — extraordinary performance with genuine daily practicality.', 2021),
            ('Macan', 'macan', 'Porsche Macan', 'The compact SUV that proved Porsche dynamics can coexist beautifully with everyday usability.', 2021),
            ('Taycan', 'taycan', 'Porsche Taycan', "Porsche's electric revolution — stunning performance, beautiful design, and genuine 911 DNA.", 2021),
        ],
    },
    {
        'name': 'Dodge', 'slug': 'dodge', 'wiki': 'Dodge',
        'models': [
            ('Charger', 'charger', 'Dodge Charger', 'A muscle car that serves as a practical four-door — thunderous V8 performance meets daily usability.', 2021),
            ('Challenger', 'challenger', 'Dodge Challenger', 'The last of the old-school muscle cars — brutish, retro, and utterly characterful.', 2021),
            ('Durango', 'durango', 'Dodge Durango', 'A three-row SUV available with HEMI V8 power — the muscle car of the family hauler world.', 2021),
        ],
    },
    {
        'name': 'RAM', 'slug': 'ram', 'wiki': 'Ram Trucks',
        'models': [
            ('1500', 'ram-1500', 'Ram 1500', "America's most award-winning pickup — coil-spring rear suspension delivers a genuinely car-like ride.", 2021),
            ('2500', 'ram-2500', 'Ram 2500', 'A heavy-duty pickup with class-leading towing capacity and surprising luxury-vehicle refinement.', 2021),
            ('TRX', 'ram-trx', 'Ram 1500 TRX', 'The supercharged 702-hp monster truck that laughs in the face of any terrain.', 2021),
        ],
    },
    {
        'name': 'GMC', 'slug': 'gmc', 'wiki': 'GMC (automobile)',
        'models': [
            ('Sierra 1500', 'sierra-1500', 'GMC Sierra 1500', 'A premium pickup with professional-grade capability and a more upscale character than its Silverado sibling.', 2021),
            ('Yukon', 'yukon', 'GMC Yukon', 'A full-size three-row SUV offering genuine luxury, massive towing, and commanding road presence.', 2021),
            ('Terrain', 'terrain', 'GMC Terrain', 'A compact SUV with a refined interior, punchy turbo engine options, and standard safety tech.', 2021),
            ('Canyon', 'canyon', 'GMC Canyon', "GMC's mid-size pickup — smart, capable, and available with the brilliant AT4 off-road package.", 2021),
        ],
    },
    {
        'name': 'Lexus', 'slug': 'lexus', 'wiki': 'Lexus',
        'models': [
            ('RX', 'rx', 'Lexus RX', "The original luxury SUV — Lexus's best-seller for decades, refined and remarkably reliable.", 2021),
            ('ES', 'es', 'Lexus ES', 'A front-wheel-drive luxury sedan delivering silky ride quality and impeccable long-term reliability.', 2021),
            ('IS', 'is', 'Lexus IS', 'A sporty compact luxury sedan with sharp looks and available turbo or naturally aspirated power.', 2021),
            ('NX', 'nx', 'Lexus NX', 'A compact luxury SUV that blends premium quality with efficient hybrid powertrains.', 2021),
        ],
    },
    {
        'name': 'Volvo', 'slug': 'volvo', 'wiki': 'Volvo Cars',
        'models': [
            ('XC60', 'xc60', 'Volvo XC60', 'The Scandinavian compact SUV setting industry standards for safety, interior quality, and refinement.', 2021),
            ('XC90', 'xc90', 'Volvo XC90', "Volvo's flagship three-row SUV — minimalist luxury, advanced safety, and mild-hybrid efficiency.", 2021),
            ('S60', 's60', 'Volvo S60', "A sporty executive compact sedan with Volvo's safety pedigree and Scandinavian cool.", 2021),
        ],
    },
    {
        'name': 'Land Rover', 'slug': 'land-rover', 'wiki': 'Land Rover',
        'models': [
            ('Range Rover', 'range-rover', 'Range Rover', 'The definitive luxury SUV — equal parts opulent boardroom and seriously capable off-roader.', 2021),
            ('Defender', 'defender', 'Land Rover Defender', "An icon reborn — modern engineering wrapped in the Defender's legendary go-anywhere identity.", 2021),
            ('Discovery', 'discovery', 'Land Rover Discovery', 'A genuinely capable family SUV with seven seats and Terrain Response technology.', 2021),
        ],
    },
    {
        'name': 'Genesis', 'slug': 'genesis', 'wiki': 'Genesis (automobile)',
        'models': [
            ('G70', 'g70', 'Genesis G70', "Korea's answer to the BMW 3 Series — dynamic, beautifully designed, and startlingly good value.", 2021),
            ('G80', 'g80', 'Genesis G80', 'A luxury executive sedan with world-class interior quality and a comprehensive standard feature list.', 2021),
            ('GV70', 'gv70', 'Genesis GV70', 'An award-winning compact luxury SUV that regularly outscores European rivals in quality surveys.', 2021),
            ('GV80', 'gv80', 'Genesis GV80', "Genesis's flagship SUV — dramatic styling, a sumptuous interior, and genuine luxury credentials.", 2021),
        ],
    },
    {
        'name': 'MINI', 'slug': 'mini', 'wiki': 'Mini (marque)',
        'models': [
            ('Cooper', 'cooper', 'Mini Cooper', 'A go-kart for the road — iconic styling, premium fit and finish, and genuine driver engagement.', 2021),
            ('Countryman', 'countryman', 'Mini Countryman', "The Mini grown up — a practical compact SUV that retains the brand's characterful personality.", 2021),
            ('Clubman', 'clubman', 'Mini Clubman', "Mini's most practical model — a compact estate with clever barn doors and a surprisingly spacious boot.", 2021),
        ],
    },
    {
        'name': 'Cadillac', 'slug': 'cadillac', 'wiki': 'Cadillac',
        'models': [
            ('Escalade', 'escalade', 'Cadillac Escalade', "America's most prestigious full-size SUV — a curved OLED screen, cavernous space, and commanding presence.", 2021),
            ('CT5', 'ct5', 'Cadillac CT5', 'An American luxury sedan fighting back with bold design, Magnetic Ride Control, and optional V-Series power.', 2021),
            ('XT5', 'xt5', 'Cadillac XT5', "Cadillac's best-selling model — a polished luxury crossover with a genuinely premium interior.", 2021),
        ],
    },
]

REVIEW_POOL = [
    {
        'title': "Absolutely love it — couldn't be happier",
        'body': "Picked up my {year} {car} six months ago and I have zero complaints. The build quality is exceptional, the technology is intuitive, and the driving experience genuinely puts a smile on my face every single commute. Did a lot of research before buying and glad I went with this one. Fuel economy is actually better than EPA estimates in real-world conditions. Highly recommend to anyone on the fence.",
        'rating': 5,
    },
    {
        'title': 'Best car I\'ve ever owned',
        'body': "I've owned quite a few cars over the years and the {year} {car} is comfortably the best. The interior quality feels genuinely premium, the ride is smooth without feeling disconnected, and the infotainment system actually works without frustrating you. My only minor gripe is wind noise at motorway speeds, but it's a small thing on an otherwise outstanding vehicle.",
        'rating': 5,
    },
    {
        'title': 'Exceeded every expectation',
        'body': "I was nervous buying a {year} {car} without test-driving more alternatives, but after 18 months I can confirm it was the right call. Reliability has been perfect — not a single unplanned trip to the shop. The safety features have already intervened twice on the motorway and I believe they prevented accidents. Comfortable on long journeys, easy to park in town. Everything you could want.",
        'rating': 5,
    },
    {
        'title': 'Worth every penny',
        'body': "Yes, I spent more than my budget initially allowed, but the {year} {car} has more than justified the extra outlay. The refinement difference is immediately noticeable coming from my old car. Cruising at motorway speeds is serene, the seats are supportive over long distances, and the tech suite is genuinely useful rather than gimmicky. Running costs are lower than expected too.",
        'rating': 5,
    },
    {
        'title': 'Three years in — still no complaints',
        'body': "Bought my {year} {car} new and just crossed 45,000 miles with not a single mechanical issue. Tyres wearing evenly, everything works as it did on day one, and it still gets compliments in car parks. Resale value is holding up brilliantly. For anyone looking for a reliable long-term ownership proposition, this should be top of your list.",
        'rating': 5,
    },
    {
        'title': 'My favourite commuter ever',
        'body': "Forty miles each way, five days a week. The {year} {car} makes what should be a miserable commute genuinely enjoyable. The seats stay comfortable across the full journey, the adaptive cruise control works brilliantly on the motorway, and the fuel costs are very reasonable. After 25,000 miles I've had nothing go wrong. Cannot fault it.",
        'rating': 5,
    },
    {
        'title': 'Family road trip approved',
        'body': "Just returned from a 1,200-mile round trip in our {year} {car} with two children and a labrador. Couldn't have asked for a better companion. Boot swallowed everything we packed, rear passenger space was comfortable even for a ten-hour day, and the fuel stops were infrequent. Kids slept most of the way — I'll take that as the ultimate endorsement.",
        'rating': 5,
    },
    {
        'title': 'Resale value is remarkable',
        'body': "Three years into owning my {year} {car} and I just had it valued for part-exchange — I was genuinely shocked how much it's retained. Depreciation has been far lower than I budgeted for. The car itself has been completely trouble-free. If you're thinking long-term, this is a smart buy.",
        'rating': 5,
    },
    {
        'title': 'Surprisingly fun to drive',
        'body': "I bought the {year} {car} primarily for practicality and expected it to be dull. I was wrong. The chassis is genuinely sorted — accurate steering, good body control, and an engine that's eager rather than just adequate. Great seats, solid visibility, and enough tech to feel modern. Makes you look forward to driving rather than dreading it.",
        'rating': 4,
    },
    {
        'title': 'Really good — a few niggles but nothing major',
        'body': "The {year} {car} is a genuinely excellent car and I'm happy with my purchase. Strong points are the ride quality, interior space, and standard safety tech. Weak points are a slightly fiddly touchscreen that requires too many taps for simple tasks, and a blind spot from the thick rear quarter pillar. Neither is a dealbreaker. Overall I'd buy it again.",
        'rating': 4,
    },
    {
        'title': 'Great daily driver, small gripes',
        'body': "Been driving my {year} {car} for eight months now. The positives are numerous — fuel efficiency, comfort, and the way it handles city traffic are all impressive. My gripes are that rear legroom is slightly tight for taller adults and the automatic transmission occasionally hesitates in slow-speed traffic. Minor things. The overall package is excellent and I regularly achieve 30+ mpg.",
        'rating': 4,
    },
    {
        'title': 'Solid choice — does most things very well',
        'body': "The {year} {car} hits a sweet spot for me. Refined enough for the motorway, economical enough for commuting, and practical enough for family duties. I'd have rated it five stars but the infotainment system has a frustrating habit of not connecting to my phone immediately on start-up. Software update might sort it. Otherwise, excellent — build quality is noticeably better than my previous vehicle.",
        'rating': 4,
    },
    {
        'title': 'Excellent value at the spec I chose',
        'body': "I opted for the mid-spec {year} {car} and hit the sweet spot. All the features I actually use are included without the premium of the top trim. Standard kit is generous — heated seats, wireless Apple CarPlay, blind-spot monitoring, and rear cross-traffic alert all came as standard. Build quality feels honest and durable. Exactly what I needed.",
        'rating': 4,
    },
    {
        'title': 'Impressed after 12 months of ownership',
        'body': "I was sceptical about the {year} {car} when I ordered it — felt like I was playing it safe rather than exciting myself — but a year in I'm genuinely impressed. Far more refined than I expected, the seats are comfortable over long distances, and not one unexpected thing has gone wrong. Knocked a star because dealer experience was poor, but the car itself is excellent.",
        'rating': 4,
    },
    {
        'title': 'Decent, but not outstanding',
        'body': "The {year} {car} is a solid car that does its job competently without really exciting me. The ride is comfortable, easy to drive, and the safety features work well. However, the interior materials feel a step below what the price suggests, and the engine is noticeably noisy when pushed. Expected more polish for the money. Reliable for daily duties but I wouldn't call it class-leading.",
        'rating': 3,
    },
    {
        'title': 'Mixed feelings after six months',
        'body': "I was very excited about my {year} {car} purchase but reality has been more subdued. The positives: generous space, good fuel economy, and a perfect driving position. The negatives: the touchscreen regularly freezes requiring a reboot, the rear wiper smears in light rain, and lane-keeping assist is overly aggressive. Not bad overall but needs some software polish.",
        'rating': 3,
    },
    {
        'title': 'Good but expected more',
        'body': "There's nothing wrong with the {year} {car} per se — it's competent, reliable, and comfortable. But 'competent' isn't what you want when you've spent this much. The interior has a couple of hard plastic panels that feel out of place for the price, and the engine note isn't particularly pleasant. Rivals offer more character. It'll do the job but test-drive the competition before committing.",
        'rating': 3,
    },
    {
        'title': 'Average experience — wouldn\'t buy again',
        'body': "The {year} {car} has been perfectly functional but underwhelming. The ride is fine, fuel economy is acceptable, and it's reliable enough. But every time I get in I feel like I settled. The infotainment lag is annoying, the interior feels plasticky in places, and I've seen better driving dynamics at this price point. Looking at the competition for my next car.",
        'rating': 3,
    },
    {
        'title': 'Disappointed — expected better reliability',
        'body': "I bought my {year} {car} based on strong reviews and brand reputation, but I've had ongoing electronic issues. The infotainment system has crashed twice requiring dealer visits to reset. The automatic emergency braking has triggered unexpectedly three times, which was frightening. Dealer has been slow to acknowledge these as known issues. Driving experience is fine but reliability has soured the whole ownership experience.",
        'rating': 2,
    },
    {
        'title': 'Quality control issues from day one',
        'body': "My {year} {car} came with several fit-and-finish issues straight from the factory — a door seal that whistles at speed, a dashboard rattle that took three dealer visits to fix, and a paint imperfection on the boot lid. The underlying car may be good but mine had a bad build day. Disappointing for this price point. The dealer has been helpful but the car should have been right first time.",
        'rating': 2,
    },
    {
        'title': 'Ongoing reliability nightmare',
        'body': "I've owned my {year} {car} for fourteen months and it has spent more time at the dealer than on my driveway. The turbo failed at 8,000 miles, the infotainment screen went blank at 11,000 miles, and there's a persistent vibration the dealer cannot locate. This is my first experience with this brand and it will be my last. Pay the extra and buy something with a proven track record.",
        'rating': 1,
    },
    {
        'title': 'Worst car purchase I\'ve ever made',
        'body': "I cannot recommend the {year} {car} based on my experience. Within the first year I've had a transmission issue, an electrical fault that left me stranded, and a persistent engine warning light that the dealer cannot diagnose. Every visit takes the car off the road for a week. I had high expectations based on the brand's reputation but this year clearly had quality control problems. Avoid.",
        'rating': 1,
    },
]

# Review rating weights: mostly positive, some neutral, few negative
RATING_WEIGHTS = {5: 35, 4: 30, 3: 15, 2: 10, 1: 10}
REVIEWS_BY_RATING = {r: [rv for rv in REVIEW_POOL if rv['rating'] == r] for r in range(1, 6)}


def _random_review(car_name, year):
    pool = list(range(1, 6))
    weights = [RATING_WEIGHTS[r] for r in pool]
    rating = random.choices(pool, weights=weights, k=1)[0]
    candidates = REVIEWS_BY_RATING.get(rating) or REVIEW_POOL
    tmpl = random.choice(candidates)
    return {
        'title': tmpl['title'],
        'body': tmpl['body'].replace('{car}', car_name).replace('{year}', str(year)),
        'rating': rating,
    }


def get_wiki_image(title, width=500):
    try:
        r = requests.get('https://en.wikipedia.org/w/api.php', params={
            'action': 'query', 'titles': title, 'prop': 'pageimages',
            'pithumbsize': width, 'format': 'json',
        }, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        pages = r.json()['query']['pages']
        page = next(iter(pages.values()))
        return page.get('thumbnail', {}).get('source')
    except Exception:
        return None


def download_image(url, dest_path):
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    for attempt in range(3):
        try:
            r = requests.get(url, timeout=20, headers={'User-Agent': 'Mozilla/5.0'})
            if r.status_code == 200:
                with open(dest_path, 'wb') as f:
                    f.write(r.content)
                return True
            elif r.status_code == 429:
                print('    rate limited, waiting 15s...')
                time.sleep(15)
        except Exception as e:
            print(f'    download error: {e}')
            time.sleep(2)
    return False


def fetch_image(wiki_title, dest_path):
    if os.path.exists(dest_path):
        return True
    url = get_wiki_image(wiki_title)
    if url:
        if download_image(url, dest_path):
            return True
    return False


def main():
    app = create_app('development')
    with app.app_context():
        # --- Category ---
        cat = Category.query.filter_by(slug='cars').first()
        if not cat:
            cat = Category(
                name='Cars & Vehicles',
                slug='cars',
                description='Real owner reviews of car brands and models, year by year.',
                icon='🚗',
            )
            db.session.add(cat)
            db.session.flush()
            print('Created category: Cars & Vehicles')

        # Fetch category image
        cat_img_path = os.path.join(STATIC_DIR, 'images', 'uploads', 'subcategories', 'cars-category.jpg')
        if fetch_image('Automobile', cat_img_path):
            cat.image_path = 'images/uploads/subcategories/cars-category.jpg'

        total_subjects = 0
        total_reviews = 0

        for brand in BRANDS:
            # --- SubCategory (brand) ---
            sc = SubCategory.query.filter_by(category_id=cat.id, slug=brand['slug']).first()
            if not sc:
                sc = SubCategory(
                    category_id=cat.id,
                    name=brand['name'],
                    slug=brand['slug'],
                )
                db.session.add(sc)
                db.session.flush()
                print(f'  Created brand: {brand["name"]}')
            else:
                print(f'  Existing brand: {brand["name"]}')

            # Brand image
            brand_img_dest = os.path.join(STATIC_DIR, 'images', 'uploads', 'subcategories', f'cars-{brand["slug"]}.jpg')
            if not sc.image_path and fetch_image(brand['wiki'], brand_img_dest):
                sc.image_path = f'images/uploads/subcategories/cars-{brand["slug"]}.jpg'
                print(f'    image saved')
            elif not sc.image_path:
                print(f'    no image found')
            time.sleep(0.5)

            for model_data in brand['models']:
                m_name, m_slug, m_wiki, m_desc, m_start_year = model_data

                # Download one image per model, reuse across years
                model_img_rel = f'images/uploads/subjects/cars-{m_slug}.jpg'
                model_img_dest = os.path.join(STATIC_DIR, model_img_rel)
                model_img_ok = False
                if os.path.exists(model_img_dest):
                    model_img_ok = True
                else:
                    if fetch_image(m_wiki, model_img_dest):
                        model_img_ok = True
                        print(f'      image: {m_name}')
                    else:
                        print(f'      no image: {m_name}')
                    time.sleep(0.5)

                for year in YEARS:
                    if year < m_start_year:
                        continue

                    subj_slug = f'{m_slug}-{year}'
                    subj_name = f'{m_name} {year}'
                    full_name = f'{brand["name"]} {m_name}'

                    subj = Subject.query.filter_by(subcategory_id=sc.id, slug=subj_slug).first()
                    if not subj:
                        subj = Subject(
                            subcategory_id=sc.id,
                            name=subj_name,
                            slug=subj_slug,
                            description=f'The {year} {full_name}. {m_desc}',
                            image_path=model_img_rel if model_img_ok else None,
                        )
                        db.session.add(subj)
                        db.session.flush()
                        total_subjects += 1

                    # Add reviews if fewer than 5
                    existing = Review.query.filter_by(subject_id=subj.id, is_published=True).count()
                    needed = max(0, 5 - existing)
                    base_date = datetime.utcnow() - timedelta(days=random.randint(30, 730))
                    for i in range(needed):
                        rv = _random_review(full_name, year)
                        db.session.add(Review(
                            subject_id=subj.id,
                            title=rv['title'],
                            body=rv['body'],
                            rating=rv['rating'],
                            author_name=_rname(),
                            source_site='sample',
                            original_date=base_date - timedelta(days=i * random.randint(3, 30)),
                            is_published=True,
                        ))
                        total_reviews += 1

            db.session.commit()
            print(f'    committed {brand["name"]}')

        # Update stats for all new subjects
        print('Updating stats...')
        for sc_brand in SubCategory.query.filter_by(category_id=cat.id).all():
            for subj in sc_brand.subjects.all():
                subj.update_stats()
        db.session.commit()

        print(f'\nDone. {total_subjects} subjects, {total_reviews} reviews added.')


if __name__ == '__main__':
    main()
