from __future__ import annotations

import logging
import os
import random
import re
import time

import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Random author name generation
# ---------------------------------------------------------------------------

_ADJECTIVES = [
    'Happy', 'Curious', 'Bubbly', 'Calm', 'Eager', 'Friendly', 'Gentle',
    'Lively', 'Mellow', 'Peppy', 'Quirky', 'Radiant', 'Serene', 'Vivid',
    'Zesty', 'Bouncy', 'Chipper', 'Dazzling', 'Jolly', 'Nimble',
]

_ANIMALS = [
    'Otter', 'Panda', 'Koala', 'Penguin', 'Dolphin', 'Turtle', 'Parrot',
    'Rabbit', 'Hedgehog', 'Ferret', 'Lemur', 'Capybara', 'Axolotl',
    'Narwhal', 'Quokka', 'Manatee', 'Flamingo', 'Chameleon', 'Wombat',
    'Meerkat',
]


def _rnd_name(rng: random.Random) -> str:
    return rng.choice(_ADJECTIVES) + rng.choice(_ANIMALS)


# ---------------------------------------------------------------------------
# HTTP session
# ---------------------------------------------------------------------------

SESSION = requests.Session()
SESSION.headers.update({
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/124.0.0.0 Safari/537.36'
    )
})

# ---------------------------------------------------------------------------
# Fish data
# ---------------------------------------------------------------------------

FISH_DATA: dict[str, dict] = {
    'Goldfish': {
        'slug': 'goldfish',
        'wiki_title': 'Goldfish',
        'description': (
            'Goldfish are one of the earliest fish to be domesticated, with a history '
            'spanning over a thousand years in China. Despite their reputation as low-effort '
            'pets, they are surprisingly long-lived — often reaching 10–15 years — and '
            'require a proper filtered aquarium rather than the small bowls they are '
            'commonly kept in. Given adequate space and clean water, goldfish develop '
            'distinct personalities and can recognise their owners.'
        ),
        'pros': [
            'Hardy and tolerant of a wide temperature range',
            'Long lifespan of 10–15 years with proper care',
            'Wide variety of beautiful fancy breeds available',
            'Can recognise their owners and respond at feeding time',
            'Relatively peaceful and suitable for community tanks',
        ],
        'cons': [
            'Produce a very high bioload, requiring strong filtration',
            'Need far more space than the bowls they are stereotypically kept in',
            'Can uproot plants and stir up substrate, making planted tanks difficult',
            'Prone to swim-bladder issues if fed the wrong diet',
        ],
        'reviews': [
            (5, 'My goldfish lived 14 years!',
             "I got my first goldfish when I was twelve and he lived until I was in college. "
             "People always act surprised when I tell them that, but the secret was simple: a "
             "proper 20-gallon tank with a good filter and weekly water changes. He recognised "
             "the sound of the food container and would swim to the front of the tank every "
             "single time. Absolutely fantastic fish and a great introduction to the hobby."),
            (4, 'Great starter fish — skip the bowl',
             "Goldfish are wonderful, but please don't buy the tiny bowl the pet shop tries to "
             "sell you. I made that mistake with my first fish and he lasted only a few months. "
             "Once I upgraded to a 30-gallon with a canister filter, my current two fancy "
             "goldfish have been thriving for four years. They eat out of my hand now. Four "
             "stars because the ammonia levels can spike fast if you're not vigilant."),
            (5, 'Underrated pets',
             "Most people dismiss goldfish as disposable pets, but mine have real character. "
             "My ryukin, Dumpling, follows my finger along the glass and does a little wiggle "
             "dance at feeding time. He's been with me for seven years. The filtration costs "
             "are a bit higher than for tropical fish, but the joy they bring absolutely makes "
             "it worthwhile. I'd recommend goldfish to anyone willing to do a little research first."),
            (3, 'Beautiful but messy',
             "I love my three goldfish, but I had no idea how much waste they produce. My "
             "canister filter needs cleaning every two weeks and I do 30% water changes twice "
             "a week to keep nitrates in check. They are gorgeous — especially the oranda with "
             "his big red and white wen — but the maintenance commitment caught me off guard. "
             "Do your research before buying. Not a set-and-forget pet at all."),
            (5, 'Perfect for a large tank',
             "I have a 75-gallon goldfish display tank in my living room and it is the centrepiece "
             "of the room. Six fancy goldfish in a well-planted, heavily filtered setup. Guests "
             "always stop and stare. The fish are interactive, calm, and beautiful. Once you nail "
             "the water parameters, goldfish are actually not that hard to keep. I cannot recommend "
             "them enough for someone wanting an impressive display aquarium."),
            (4, 'Long-lived and rewarding',
             "My comet goldfish is going on eleven years old. He started in a 10-gallon as a "
             "feeder fish I rescued and now lives in a 55-gallon with a pond-grade filter. "
             "Watching him grow over the years has been genuinely rewarding. Minus one star "
             "because they do eat most soft-leaved plants, so my tank stays fairly bare. Still "
             "a brilliant fish if you give them the space they deserve."),
            (3, 'Nice fish, huge commitment',
             "I had three fantail goldfish for about two years before I had to rehome them when "
             "I moved abroad. They were lovely — very responsive and fun to watch — but the "
             "maintenance was relentless. Three fish in a 40-gallon required water changes "
             "three times a week to keep nitrates acceptable. If you have the time and space, "
             "go for it. Just know what you're signing up for."),
            (5, 'Surprisingly interactive',
             "I always thought fish were boring pets until I got goldfish. Mine swim to greet "
             "me every morning and get visibly excited when I approach the tank. My black moor "
             "even has a favourite corner where he likes to hang out. They have been with me "
             "for six years and show no signs of slowing down. Proper tank size and a good "
             "filter really do make all the difference."),
            (4, 'Great for kids who are ready',
             "We got two fancy goldfish for our nine-year-old daughter. She has learned so much "
             "about nitrogen cycles, water chemistry, and responsible pet ownership. The fish "
             "themselves are healthy, active, and beautiful. I help with the bigger water changes, "
             "but she handles feeding and basic checks. Minus one star because they do need "
             "more care than the pet shop implied — budget for a proper setup from the start."),
        ],
    },

    'Betta Fish': {
        'slug': 'betta-fish',
        'wiki_title': 'Betta splendens',
        'description': (
            'Betta fish, also known as Siamese fighting fish, are celebrated for their stunning, '
            'flowing fins and jewel-bright colouration. They possess a labyrinth organ that allows '
            'them to breathe air directly, making them more tolerant of lower oxygen levels than '
            'most fish. Males are highly territorial and must be kept alone or with carefully '
            'chosen tank mates; a single male in a well-planted 10-gallon tank with a gentle '
            'filter and heater provides an ideal home.'
        ),
        'pros': [
            'Breathtaking colours and fin varieties available',
            'Can be kept alone in a relatively small tank',
            'Labyrinth organ makes them more resilient than most fish',
            'Highly interactive and often recognise their owners',
            'Low cost to purchase and maintain',
        ],
        'cons': [
            'Males are aggressive toward other bettas and fin-nippers',
            'Require a heater — cold water shortens their lifespan significantly',
            'Prone to fin rot if water quality is poor',
            'Do not tolerate strong currents from powerful filters',
        ],
        'reviews': [
            (5, 'Most personality of any fish I have owned',
             "My betta, Poseidon, is the most interactive fish I have ever kept. He flares at "
             "his reflection, does flap-dances when I approach, and has learned that tapping "
             "the glass once means feeding time. He has been thriving in his 10-gallon planted "
             "tank for three years now. The colours are absolutely unreal — deep royal blue with "
             "red edges on every fin. I tell everyone who asks about fish to start with a betta."),
            (5, 'Perfect solo fish',
             "Living in a small flat, I didn't have room for a large aquarium. A 10-gallon "
             "betta tank fits perfectly on my desk and makes the room feel alive. My halfmoon "
             "betta, Gatsby, is endlessly entertaining. He investigates every new decoration "
             "I add, hunts bloodworms with ferocious energy, and sleeps curled up in a giant "
             "leaf hammock. Maintenance is just a 20% water change weekly and feeding twice a day."),
            (4, 'Beautiful but needs a proper setup',
             "Please do not keep bettas in tiny cups or vases. I see this all the time and it "
             "makes me sad. Mine is in a heated, filtered 10-gallon with live plants and he is "
             "an entirely different fish from the limp, faded bettas I see in pet shops. Vibrant, "
             "active, and curious. Lost a star only because fin rot can sneak up fast if you skip "
             "a water change — vigilance is required."),
            (5, 'My favourite pet I have ever owned',
             "I have had dogs, cats, hamsters, and rabbits. My betta is genuinely my favourite "
             "pet I have ever owned. He comes to the front of the tank when I sit at my desk, "
             "stares at me while I work, and has the most expressive face of any animal I know. "
             "He's two and a half years old and still as vibrant as the day I got him. A planted "
             "tank with a sponge filter changed my whole experience with bettas."),
            (3, 'Great fish, tricky tank mates',
             "I made the mistake of putting my betta with some neon tetras. He was fine at first "
             "but eventually shredded a couple of their tails. Some bettas coexist peacefully "
             "with other fish, but mine clearly prefers to be alone. Once I moved him to his own "
             "tank, he became much calmer and more active. Three stars for the tank mate challenges "
             "— do your research before adding any companions."),
            (4, 'Great for beginners if you do it right',
             "Bettas get a bad reputation because people keep them in tiny, unheated bowls. In "
             "a proper setup they are hardy, beautiful, and easy to care for. My female betta "
             "has been healthy for two years in a 10-gallon community tank. She is far less "
             "aggressive than males and gets along with my corydoras and snails. Highly recommend "
             "for anyone wanting a low-maintenance but visually stunning fish."),
            (5, 'The king of the fishbowl desk',
             "My betta sits on my home office desk and honestly makes working from home so much "
             "better. He reacts to what I do — if I play music, he swims around more actively. "
             "He knows my face distinctly from other people who come into the room. After three "
             "years he is still bright crimson with perfect fins. Bettas absolutely repay the "
             "effort of a proper cycled tank."),
            (3, 'Lovely fish but fragile health',
             "My first betta was healthy for a year and then developed velvet disease seemingly "
             "out of nowhere. Treating the tank was stressful and expensive. My second betta has "
             "been fine for eighteen months, so maybe I just had bad luck. They are stunning fish "
             "and I still recommend them, but be prepared for occasional health issues and have "
             "a small fish medicine kit ready."),
            (4, 'Surprisingly smart',
             "I taught my betta to swim through a small hoop for a food reward in about a week. "
             "He genuinely recognises me versus strangers and behaves differently around each. "
             "The care is simple once you have the tank cycled and the heater dialled in. The "
             "only reason I am not giving five stars is that the short lifespan — usually two to "
             "four years — makes every goodbye inevitable and hard."),
        ],
    },

    'Guppy': {
        'slug': 'guppy',
        'wiki_title': 'Guppy',
        'description': (
            'Guppies are one of the most popular freshwater aquarium fish in the world, prized '
            'for their vivid colouration, hardiness, and ease of breeding. Males display an '
            'astonishing variety of tail shapes and colour patterns, while females are larger '
            'and more plainly coloured. They are livebearers that breed prolifically, making '
            'them a fascinating choice for hobbyists interested in selective breeding and an '
            'excellent first fish for beginners.'
        ),
        'pros': [
            'Very hardy and forgiving of beginner mistakes',
            'Colourful males available in dozens of varieties',
            'Inexpensive to buy and to feed',
            'Active and entertaining schooling behaviour',
            'Excellent first breeding project for new hobbyists',
        ],
        'cons': [
            'Breed so prolifically that overpopulation can become a problem',
            'Females can be harassed by males if the ratio is wrong',
            'Fancy long-finned males can be targeted by fin-nipping species',
            'Water quality still matters — hard, alkaline water suits them best',
        ],
        'reviews': [
            (5, 'Perfect beginner fish',
             "Guppies were the first fish I ever kept and they are the reason I am still in the "
             "hobby fifteen years later. Hardy, colourful, active, and cheap — everything a "
             "beginner could want. My 20-gallon community tank holds a dozen guppies alongside "
             "corydoras and a couple of bristlenose plecos. They get along with everyone. The "
             "males are stunning little creatures with their flowing tails."),
            (5, 'Exploding population',
             "Fair warning: guppies breed constantly. I started with four and now have about "
             "forty. I had to set up a second tank just for the fry. That said, watching the "
             "babies grow and develop their colours is one of the most rewarding things in the "
             "hobby. I give batches away to the local fish club. If you want a breeding project, "
             "guppies are the perfect starting point."),
            (4, 'Beautiful and easy',
             "My guppy tank is a 30-gallon heavily planted setup and it looks absolutely stunning. "
             "The males dart through the plants showing off their colours while the females lumber "
             "along looking perfectly content. They eat almost anything and rarely get sick if the "
             "water is clean. I keep the male-to-female ratio at 1:3 to prevent harassment, which "
             "I'd recommend to anyone."),
            (3, 'Great fish, tricky gender balance',
             "My first guppy tank was all males for the first year and it was peaceful. Then I "
             "added females and the males went absolutely wild chasing them. Three females were "
             "too few for eight males and they got stressed and died. I researched the proper "
             "ratio and added more females — problem solved. Lovely fish once you get the balance "
             "right, but that part tripped me up early on."),
            (5, 'Vibrant and full of personality',
             "There is something magical about a well-stocked guppy tank. The males are constantly "
             "flaring their tails and competing for attention from the females. My blue moscow "
             "guppies are the most beautiful fish I have ever kept. They are cheap, cheerful, "
             "and nearly impossible to kill in good water. Perfect fish for any community tank."),
            (4, 'Brilliant for kids',
             "We started our daughter's fish-keeping journey with guppies and it has been wonderful. "
             "She loves watching the fry appear and tracking which ones survive. The fish are "
             "forgiving enough that the odd missed water change does not spell disaster. The "
             "colours are gorgeous and the activity level keeps her engaged. Great starter fish "
             "for children."),
            (5, 'Fifteen years in the hobby, still love guppies',
             "I have kept cichlids, discus, marines, and everything in between. But I always "
             "have a guppy tank running somewhere. There is a simplicity and beauty to a "
             "well-planted guppy setup that no other fish matches at the same price point. My "
             "current endler guppies are tiny jewels. Highly recommended at any experience level."),
            (3, 'Watch your filtration',
             "Guppies are hardy but not invincible. I lost half my colony when my filter failed "
             "during a heatwave. The bioload from a large group adds up fast. I now run two "
             "sponge filters in my guppy tank as a backup. Once I sorted the filtration they "
             "have been healthy for over a year. Not difficult fish, but they do need clean water."),
        ],
    },

    'Clownfish': {
        'slug': 'clownfish',
        'wiki_title': 'Clownfish',
        'description': (
            'Clownfish are among the most recognisable fish in the world, thanks to their '
            'vivid orange and white banding and their fascinating symbiotic relationship with '
            'sea anemones. As saltwater fish, they require a marine aquarium with stable '
            'salinity, temperature, and water chemistry — a more demanding setup than freshwater. '
            'However, a pair of clownfish in a well-maintained reef tank, hosting in an anemone, '
            'is one of the most rewarding sights in the aquarium hobby.'
        ),
        'pros': [
            'Iconic, instantly recognisable colouration',
            'Hardy saltwater fish suitable for beginners to marines',
            'Fascinating anemone-hosting behaviour to observe',
            'Captive-bred specimens widely available and more disease-resistant',
            'Active, entertaining, and relatively peaceful',
        ],
        'cons': [
            'Require a saltwater aquarium — significantly higher setup cost',
            'Water parameters must be kept stable: any spike can be fatal',
            'Hosting anemones add complexity and require strong lighting',
            'Marine tanks require more equipment and ongoing expense than freshwater',
        ],
        'reviews': [
            (5, 'Worth every penny of the setup cost',
             "I spent six months and a significant amount of money setting up my 75-gallon reef "
             "tank before adding my pair of ocellaris clownfish. Watching them host in their "
             "bubble tip anemone every single day makes every water change and equipment purchase "
             "completely worthwhile. They have names — Nemo and Coral — and they recognise "
             "feeding time immediately. The most beautiful thing I have ever kept."),
            (4, 'Great starter saltwater fish',
             "If you want to get into marine aquariums, clownfish are the perfect entry point. "
             "They are much more tolerant of parameter swings than many saltwater fish and eat "
             "readily. My pair have been in my 40-gallon breeder for two years now, healthy and "
             "active. The setup cost and maintenance are high compared to freshwater, but if you "
             "can budget for it, it is absolutely worth it."),
            (5, '"Finding Nemo" is real in my living room',
             "My kids begged for clownfish after watching Finding Nemo and I am so glad I gave "
             "in. Setting up a proper marine tank was a learning curve, but now it runs "
             "smoothly. The fish host in a torch coral since I haven't added an anemone yet, "
             "and watching them is endlessly entertaining. My daughter can identify each fish's "
             "personality. Absolutely magical."),
            (3, 'Beautiful fish, brutal setup',
             "I want to love my clownfish setup but the maintenance is genuinely challenging. "
             "A spike in salinity killed my first anemone. My protein skimmer broke twice in "
             "the first year. The fish themselves are robust and beautiful, but the saltwater "
             "system demands constant attention. Three stars not because of the fish, but because "
             "the infrastructure required is a significant commitment."),
            (5, 'My pair spawned!',
             "My female clownfish laid eggs on a flat rock near their anemone last month and I "
             "am absolutely over the moon. Watching the male fan and guard the clutch for days "
             "was one of the most extraordinary things I have witnessed in my years of fish "
             "keeping. Clownfish in a mature reef tank are on a completely different level from "
             "any other pet fish experience. Cannot recommend them highly enough."),
            (4, 'Perfect centrepiece fish',
             "A pair of clownfish with an anemone is the ultimate centrepiece for a reef tank. "
             "Mine are black and white ocellaris with brilliant personalities. They greet me "
             "every morning and follow my hand along the glass. The marine tank takes time to "
             "establish — you need to cycle it properly for six to eight weeks — but once "
             "stable it is not especially difficult to maintain."),
            (3, 'Amazing fish, expensive hobby',
             "Clownfish themselves are not expensive. My pair cost twenty pounds each. But the "
             "tank, light, skimmer, rock, salt, test kits, and all the rest adds up very fast. "
             "My starter reef setup cost me around six hundred pounds before I added a single "
             "fish. If you are prepared for the financial investment, they are stunning. Just "
             "go in with open eyes about what marine fishkeeping costs."),
            (5, 'Changed how I think about pets',
             "I never considered a fish a proper pet until I got my pair of clownfish. They have "
             "individual personalities — the female is bold and investigates everything, the male "
             "is shy and stays near the anemone. They respond to me in a way I find genuinely "
             "moving. Four years in, healthy and bright as ever. The reef tank is the best thing "
             "I have ever invested in."),
        ],
    },

    'Angelfish': {
        'slug': 'angelfish',
        'wiki_title': 'Freshwater angelfish',
        'description': (
            'Freshwater angelfish are graceful cichlids native to the Amazon basin, prized for '
            'their distinctive tall, triangular profile and sweeping finnage. They make a '
            'stunning display fish for aquariums of 30 gallons or more, but their semi-aggressive '
            'cichlid temperament means they may eat very small tank mates such as neon tetras '
            'as they grow. They thrive in warm, soft, slightly acidic water with plenty of '
            'vertical space and tall plants.'
        ),
        'pros': [
            'Elegant, dramatic silhouette unlike any other freshwater fish',
            'Available in many beautiful colour varieties',
            'Intelligent and interactive for a cichlid',
            'Form strong pair bonds and make attentive parents when breeding',
            'Peaceful toward similarly-sized fish',
        ],
        'cons': [
            'Will eat small fish like neon tetras once fully grown',
            'Can be aggressive toward their own kind, especially when pairing',
            'Require taller tanks due to their vertical body shape',
            'Sensitive to sudden temperature drops and poor water quality',
        ],
        'reviews': [
            (5, 'The most elegant freshwater fish',
             "I have kept freshwater fish for twenty years and angelfish remain my absolute "
             "favourite. The way they glide through a planted tank — tall, slow, and utterly "
             "graceful — is unlike anything else in the freshwater hobby. My pair of marbles "
             "have been together for four years, spawned three times, and are still the centrepiece "
             "of my 55-gallon. They recognise me and come to the front of the tank every time."),
            (4, 'Stunning but watch the tank mates',
             "My angelfish are beautiful but I made the rookie mistake of putting them with "
             "neon tetras. Within a month the tetras had all disappeared. Angelfish grow large "
             "and their mouths can fit more than you expect. Once I moved them to a tank with "
             "similarly-sized fish — corydoras, a pearl gourami, and a bristlenose pleco — "
             "everyone has been fine. Gorgeous fish, just plan your community carefully."),
            (5, 'My pair are raising fry right now',
             "My angelfish pair spawned for the first time last week and I am absolutely thrilled. "
             "They cleaned a broad leaf, laid eggs in a neat line, and are now fanning and "
             "guarding them ferociously. The parental behaviour is extraordinary to watch — "
             "they herd the wriggling fry together and will charge at me if I get too close. "
             "Angelfish breeding is one of the most rewarding experiences in fish keeping."),
            (3, 'Beautiful but temperamental',
             "My three angelfish have a constant power struggle going on. The dominant one "
             "chases the other two whenever he feels like it. I have added more plants and "
             "visual breaks to reduce the aggression, which helps. They are undeniably beautiful "
             "and I love them, but the social dynamics require management. A bigger tank would "
             "probably solve most of the issues."),
            (5, 'Regal and intelligent',
             "There is a regal quality to angelfish that I find endlessly appealing. Mine follow "
             "my finger along the glass, come to the surface for hand feeding, and have clear "
             "individual temperaments. My oldest is five years old now and still looks magnificent. "
             "They are not the easiest community fish, but in the right setup they are absolutely "
             "spectacular."),
            (4, 'Perfect for a tall planted tank',
             "Angelfish and a tall Amazonian planted tank are a match made in aquarium heaven. "
             "My 48-inch tall tank with vallisneria and amazon swords is the perfect backdrop "
             "for my two koi angelfish. They drift between the plants like ghosts. The only "
             "downside is that finding a tall enough tank can be difficult and expensive. Totally "
             "worth it if you can manage it though."),
            (3, 'Sensitive to water changes',
             "My angelfish are far more sensitive to water changes than my other fish. A large "
             "water change with water even a couple of degrees cooler will send them into stress "
             "and occasionally trigger ich. I have learned to match water temperature precisely "
             "and change no more than 20% at a time. Once I got the routine right they have "
             "been healthy. Still worth the extra care."),
            (4, 'Excellent display fish',
             "If you want a centrepiece fish for a medium to large freshwater tank, angelfish "
             "are hard to beat. The variety of colours — gold, marble, koi, zebra, black lace — "
             "means there is something for every taste. They are not aggressive toward larger "
             "tank mates and are peaceful enough for most community setups. Just keep them away "
             "from anything small enough to eat."),
        ],
    },

    'Oscar Fish': {
        'slug': 'oscar-fish',
        'wiki_title': 'Oscar (fish)',
        'description': (
            'Oscar fish are large, intelligent South American cichlids often described as the '
            '"dogs of the aquarium world" for their remarkable ability to recognise their owners '
            'and interact with them directly. They require a minimum 55-gallon tank for a single '
            'specimen and produce a significant amount of waste, demanding excellent filtration. '
            'In return they offer a level of personality and engagement that few other fish can match.'
        ),
        'pros': [
            'Remarkable intelligence and ability to recognise their owners',
            'Interactive — will eat from the hand and respond to the owner',
            'Striking appearance with bold orange and black patterning',
            'Long-lived, often reaching 10–15 years',
            'Available in several beautiful colour morphs',
        ],
        'cons': [
            'Require a very large aquarium — at least 55 gallons for one fish',
            'Extremely high bioload; powerful filtration is essential',
            'Will eat any fish small enough to fit in their mouth',
            'Can be aggressive, especially during breeding season',
        ],
        'reviews': [
            (5, 'More personality than my dog',
             "I am not exaggerating when I say my Oscar has more personality than my dog. He "
             "splashes at me when he wants food, rearranges the decorations in his tank whenever "
             "he feels like a change, and pouts visibly when I go on holiday. He is eight years "
             "old, the size of a dinner plate, and the single most entertaining animal I have "
             "ever owned. If you have a big tank and good filtration, get an Oscar."),
            (5, 'The puppy of fish',
             "Everyone warned me Oscars were aggressive and messy. They were not wrong about "
             "the mess — I run two massive canister filters on my 75-gallon and still do big "
             "weekly water changes. But the aggression has been overstated in my experience. "
             "My tiger Oscar ignores my jack dempsey completely. And the personality! He begs, "
             "he sulks, he plays. Absolutely extraordinary fish."),
            (4, 'Plan your tank around them',
             "Oscars will destroy any aquascape you create. Rocks get moved, plants get uprooted, "
             "decorations get rearranged. I eventually went bare-bottom with some large, heavy "
             "stones and he has been happy ever since. They are magnificent fish but you need "
             "to accept that they — not you — decide what the tank looks like. Love mine dearly."),
            (3, 'Amazing fish but brutal on equipment',
             "My Oscar has broken a heater guard, cracked a thermometer, and managed to "
             "relocate a 5kg piece of slate to the other side of the tank. He is also "
             "extraordinarily messy — nitrates climb visibly within days. The maintenance "
             "on this fish is serious. He is worth it, but go in knowing you will be spending "
             "real time and money on water changes and filter maintenance."),
            (5, 'Best fish I have ever kept, full stop',
             "I have kept marine fish, discus, and all manner of cichlids over twenty years. "
             "My Oscar is the best fish I have ever kept. He greets me every morning with a "
             "vigorous splash, eats pellets from my fingers, and responds to his name. He is "
             "twelve years old and still going strong. The maintenance is real but it is a "
             "small price to pay for this level of connection with a fish."),
            (4, 'Not for small tanks',
             "Please, please research Oscars before buying one. The baby in the shop is cute "
             "and about 2 inches long. Within a year it will be 10 inches and need a 55-gallon "
             "minimum. Mine is in a 90-gallon and it is barely enough. He is stunning, interactive, "
             "and full of character — but only if you can provide the space and filtration he needs."),
            (5, 'He knows when I am sad',
             "This sounds strange but my Oscar genuinely seems to pick up on my mood. On difficult "
             "days he is calmer and will sit near the glass while I talk to him. On good days he "
             "splashes around and shows off. Eleven years with this fish and he is still as "
             "vibrant and engaged as ever. No other fish has ever given me this kind of connection."),
            (3, 'Watch the water quality closely',
             "My Oscar got HITH disease in his second year because I was not on top of water "
             "changes. The holes in his head were distressing to see. With improved husbandry — "
             "more frequent changes, activated carbon, better diet — he recovered fully. Oscars "
             "are tough fish but they are very susceptible to HITH if nitrates climb. Do not "
             "skip water changes with this species."),
        ],
    },

    'Neon Tetra': {
        'slug': 'neon-tetra',
        'wiki_title': 'Neon tetra',
        'description': (
            'Neon tetras are small schooling fish from South America, famous for the vivid '
            'electric-blue stripe and red tail that run the length of their tiny bodies. '
            'They are best kept in groups of ten or more, where their coordinated shoaling '
            'behaviour creates a dazzling, shimmering effect in a planted aquarium. While '
            'fragile as juveniles and susceptible to "neon tetra disease", established adults '
            'in a stable, mature tank are hardy and straightforward to keep.'
        ),
        'pros': [
            'Stunning iridescent blue and red colouration',
            'Peaceful and safe with almost all community fish',
            'Schooling behaviour is mesmerising in a planted aquarium',
            'Inexpensive and widely available',
            'Small size suits a variety of tank sizes',
        ],
        'cons': [
            'Fragile when newly purchased; mortality can be high in uncycled tanks',
            'Susceptible to neon tetra disease, which is incurable',
            'Require a cycled, established tank — not suitable for new setups',
            'Predated by any fish large enough to eat them',
        ],
        'reviews': [
            (5, 'A hundred neon tetras is a religious experience',
             "I have 120 neon tetras in a 120-gallon planted tank and the effect is genuinely "
             "breathtaking. They move as one shimmering mass through the plants, flashing blue "
             "and red in the light. Guests stop talking when they see it. Individual fish are "
             "cheap and easy to care for once the tank is established. As a group they are "
             "one of the most spectacular sights in the freshwater hobby."),
            (4, 'Classic for good reason',
             "Neon tetras became popular for a reason. They are peaceful, beautiful, and bring "
             "life to any planted aquarium. My school of thirty lives with corydoras, ottocinclus, "
             "and a pearl gourami in perfect harmony. Minus one star only because the juveniles "
             "from the fish shop are often stressed and weak — I always quarantine new fish for "
             "two weeks before adding them to the main tank."),
            (3, 'Beautiful but fragile when young',
             "I have lost several batches of neon tetras in my early fishkeeping days because "
             "I added them to tanks that were not properly cycled. They are sensitive to ammonia "
             "and nitrite spikes. Once the tank is mature and stable, they are fine. But if you "
             "are new to the hobby, cycle your tank fully before adding these fish. They reward "
             "patience with years of beauty."),
            (5, 'The perfect planted tank fish',
             "Neon tetras and a lush planted tank are the perfect combination. The contrast of "
             "bright green plants against the electric-blue and red of a tight school is stunning. "
             "Mine have been healthy for three years in a 40-gallon with lots of live plants and "
             "a gentle sponge filter. They are easy to feed — they accept flake, micro-pellets, "
             "and frozen daphnia. Highly recommend for any planted aquarium."),
            (4, 'Peaceful community fish',
             "I have kept neon tetras in my community tank for five years and they are always "
             "a highlight. Zero aggression, get along with everyone, and look spectacular under "
             "good lighting. The schooling behaviour when they sense a perceived threat is "
             "incredible to watch — they synchronise perfectly. Good filtration and stable "
             "parameters are the keys to keeping them healthy long-term."),
            (5, 'Best value fish in the hobby',
             "You can buy a dozen neon tetras for the price of a single fancy cichlid, and the "
             "visual impact of a school of thirty is arguably greater. They are peaceful, easy "
             "to feed, and do not bother any other fish. My oldest are going on four years and "
             "still schooling tightly. For bang-for-buck beauty, nothing beats neon tetras."),
            (3, 'Neon tetra disease is devastating',
             "Lost my entire school of twenty fish to neon tetra disease last year. There is no "
             "cure and the disease spreads through the group rapidly. It is heartbreaking to watch "
             "healthy-looking fish deteriorate one by one. I have since restarted with new fish "
             "from a reputable source and they are doing well. Just be aware the disease exists "
             "and quarantine any fish showing unusual white patches or colour loss immediately."),
            (4, 'Great starter schooling fish',
             "If you want your first experience with schooling fish, neon tetras are the obvious "
             "choice. They are affordable, peaceful, and visually striking. I started with ten "
             "in a 20-gallon planted tank and have since grown my school to twenty-five. The "
             "difference in schooling behaviour between ten and twenty-five fish is remarkable. "
             "Always buy more than you think you need."),
        ],
    },

    'Discus': {
        'slug': 'discus-fish',
        'wiki_title': 'Discus (fish)',
        'description': (
            'Discus are widely regarded as the "king of the aquarium" — large, spectacularly '
            'coloured cichlids from the Amazon river system that command respect and dedication '
            'from their keepers. Their requirement for very soft, warm, acidic water and '
            'immaculate water quality places them firmly in the expert category, but those who '
            'master their care are rewarded with fish of extraordinary beauty, intelligence, '
            'and personality. They are among the most expensive fish in the freshwater hobby.'
        ),
        'pros': [
            'Arguably the most beautiful freshwater fish available',
            'Intelligent and interactive — recognise owners and beg for food',
            'Spectacular variety of colours and patterns available',
            'Form pair bonds and exhibit fascinating parental behaviour',
            'The ultimate challenge and achievement in freshwater fish keeping',
        ],
        'cons': [
            'Require very precise, soft, warm, acidic water parameters',
            'Extremely sensitive to water quality — small deviations cause stress',
            'Very expensive to purchase; quality specimens cost £50–£200 each',
            'Require frequent, large water changes to thrive',
            'Difficult to keep with other fish that do not share their water requirements',
        ],
        'reviews': [
            (5, 'The pinnacle of freshwater fishkeeping',
             "After fifteen years in the hobby I finally took the plunge with discus. Six months "
             "in and I cannot imagine keeping anything else. The colours are indescribable in "
             "photographs — a well-lit discus tank looks like someone hung stained glass in your "
             "living room. Yes, they are demanding. Yes, they are expensive. But they are worth "
             "every penny and every water change. The king of the aquarium absolutely deserves "
             "its title."),
            (4, 'Challenging but incredibly rewarding',
             "Discus are not for beginners and anyone who tells you otherwise is setting you up "
             "for expensive failure. I spent six months researching before buying my first four "
             "fish. My 75-gallon bare-bottom tank with daily 30% water changes has kept them "
             "healthy for two years. They are now the size of side plates, coloured like "
             "sunsets, and they come to my hand for food. Nothing in the hobby compares."),
            (5, 'My pair spawned',
             "My discus pair spawned on a broad leaf three weeks ago. Watching them care for "
             "the eggs, fan them constantly, and then have the fry feed off the slime coat on "
             "their flanks is one of the most extraordinary things I have ever witnessed in "
             "nature. I have been keeping fish for twenty years and discus are without question "
             "the most rewarding species I have ever kept."),
            (3, 'Beautiful but unforgiving',
             "Lost three discus in my first year because I did not fully understand their water "
             "requirements. My tap water was too hard and I did not have an RO unit. Once I "
             "invested in reverse osmosis and started mixing my own water, the survivors "
             "blossomed. The fish are magnificent but they demand expertise. Do not buy discus "
             "unless you are genuinely prepared to put in the work."),
            (5, 'Nothing else comes close',
             "I have kept marines, African cichlids, and every popular tropical fish going. "
             "Discus are the best fish I have ever kept. Full stop. The intelligence, the "
             "colouration, the personality — they interact with you in a way that feels "
             "almost mammalian. My oldest is seven years old and still glows like a jewel. "
             "Expensive, demanding, worth it."),
            (4, 'Worth the investment for experienced keepers',
             "If you have been in the hobby for several years and want the ultimate challenge, "
             "discus are the answer. The daily water changes become meditative rather than a "
             "chore. The fish respond to your presence and learn your routine. Mine swim to "
             "the front of the tank when I enter the room. The financial outlay is significant "
             "but spread over the ten-plus year lifespan of a healthy discus, it is very "
             "reasonable."),
            (3, 'Not for the casual keeper',
             "I love my discus but I will be honest: they consume a lot of my free time. Daily "
             "water changes, careful temperature monitoring, premium food preparation — it is "
             "closer to having a demanding pet than a casual aquarium. Two of my six fish have "
             "had health issues requiring medication. They are beautiful and I would not give "
             "them up, but if you want low-maintenance fish, look elsewhere."),
            (5, 'The most beautiful animals I have ever owned',
             "My discus display tank is genuinely the most beautiful thing in my home. Eight "
             "fish in full colour under warm LED lighting, floating through a Amazonian "
             "biotope with driftwood and giant val. People come to visit specifically to see "
             "the tank. The effort required is real but it has taught me more about water "
             "chemistry, fish husbandry, and patience than anything else in twenty years of "
             "the hobby. Discus changed fishkeeping for me forever."),
            (4, 'Phenomenal fish for the dedicated keeper',
             "Three years with discus and I can confidently say they are the most rewarding "
             "fish I have ever kept. The colouration changes with their mood — bright and "
             "vivid when happy, dark and barred when stressed — giving you constant feedback "
             "on how the tank is performing. Once you learn to read their behaviour, "
             "maintaining ideal conditions becomes intuitive. Spectacular animals."),
        ],
    },
}

# ---------------------------------------------------------------------------
# Image helpers
# ---------------------------------------------------------------------------


def get_wiki_image(title: str, size: int = 500) -> str | None:
    """Fetch the main image URL for a Wikipedia article via the pageimages API."""
    url = 'https://en.wikipedia.org/w/api.php'
    params = {
        'action': 'query',
        'titles': title,
        'prop': 'pageimages',
        'pithumbsize': size,
        'format': 'json',
    }
    try:
        resp = SESSION.get(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        pages = data.get('query', {}).get('pages', {})
        for page in pages.values():
            thumb = page.get('thumbnail', {})
            src = thumb.get('source', '')
            if src:
                # Ensure the requested size is reflected in the URL
                src = re.sub(r'\d+px-', f'{size}px-', src)
                return src
    except Exception as exc:
        logger.warning('get_wiki_image(%s) failed: %s', title, exc)
    return None


def try_commons_image(query: str, size: int = 500) -> str | None:
    """Search Wikimedia Commons for a file matching *query* and return a thumb URL."""
    url = 'https://commons.wikimedia.org/w/api.php'
    params = {
        'action': 'query',
        'list': 'search',
        'srsearch': query,
        'srnamespace': 6,  # File: namespace
        'srlimit': 5,
        'format': 'json',
    }
    try:
        resp = SESSION.get(url, params=params, timeout=15)
        resp.raise_for_status()
        results = resp.json().get('query', {}).get('search', [])
        for result in results:
            page_title = result.get('title', '')
            if not page_title:
                continue
            # Fetch image info for this file
            info_params = {
                'action': 'query',
                'titles': page_title,
                'prop': 'imageinfo',
                'iiprop': 'url|thumburl',
                'iiurlwidth': size,
                'format': 'json',
            }
            info_resp = SESSION.get(
                'https://commons.wikimedia.org/w/api.php',
                params=info_params,
                timeout=15,
            )
            info_resp.raise_for_status()
            pages = info_resp.json().get('query', {}).get('pages', {})
            for page in pages.values():
                infos = page.get('imageinfo', [])
                if infos:
                    thumb = infos[0].get('thumburl') or infos[0].get('url')
                    if thumb:
                        return thumb
    except Exception as exc:
        logger.warning('try_commons_image(%s) failed: %s', query, exc)
    return None


def download_image(url: str, dest_path: str) -> bool:
    """Download *url* to *dest_path*. Returns True on success."""
    try:
        resp = SESSION.get(url, timeout=30, stream=True)
        if resp.status_code == 429:
            logger.warning('Rate-limited; sleeping 5s then retrying %s', url)
            time.sleep(5)
            resp = SESSION.get(url, timeout=30, stream=True)
        resp.raise_for_status()
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        with open(dest_path, 'wb') as fh:
            for chunk in resp.iter_content(chunk_size=8192):
                fh.write(chunk)
        logger.info('Downloaded image → %s', dest_path)
        return True
    except Exception as exc:
        logger.warning('download_image(%s) failed: %s', url, exc)
        return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    from app import create_app, db
    from app.models import Category, SubCategory, Subject, Review

    app = create_app('development')
    base_dir = os.path.dirname(os.path.abspath(__file__))

    with app.app_context():
        # ------------------------------------------------------------------ #
        # 1. Find the Animals category
        # ------------------------------------------------------------------ #
        animals_cat = Category.query.filter_by(slug='animals').first()
        if animals_cat is None:
            logger.error('Animals category not found. Run seed.py first.')
            return

        # ------------------------------------------------------------------ #
        # 2. Create Fish subcategory
        # ------------------------------------------------------------------ #
        fish_sub = SubCategory.query.filter_by(
            category_id=animals_cat.id, slug='fish'
        ).first()
        if fish_sub is None:
            fish_sub = SubCategory(
                category_id=animals_cat.id,
                name='Fish',
                slug='fish',
            )
            db.session.add(fish_sub)
            db.session.flush()
            logger.info('Created subcategory: Fish')
        else:
            logger.info('SubCategory Fish already exists (id=%d)', fish_sub.id)

        # ------------------------------------------------------------------ #
        # 3. Process each fish species
        # ------------------------------------------------------------------ #
        subjects_added = 0
        reviews_added = 0

        for fish_name, data in FISH_DATA.items():
            slug = data['slug']
            pros_text = '\n'.join(data['pros'])
            cons_text = '\n'.join(data['cons'])

            # Create or retrieve subject
            subject = Subject.query.filter_by(
                subcategory_id=fish_sub.id, slug=slug
            ).first()
            if subject is None:
                subject = Subject(
                    subcategory_id=fish_sub.id,
                    name=fish_name,
                    slug=slug,
                    description=data['description'],
                    pros=pros_text,
                    cons=cons_text,
                )
                db.session.add(subject)
                db.session.flush()
                subjects_added += 1
                logger.info('  + Subject: %s', fish_name)
            else:
                # Update description and pros/cons on existing subjects
                subject.description = data['description']
                subject.pros = pros_text
                subject.cons = cons_text
                logger.info('  ~ Updated: %s', fish_name)

            # Seed reviews
            rng = random.Random(hash(fish_name) % 100_000)
            all_reviews = data['reviews']
            pick_count = rng.randint(5, 10)
            selected = rng.sample(all_reviews, min(pick_count, len(all_reviews)))

            for i, (rating, title, body) in enumerate(selected, start=1):
                original_url = f'sample-{slug}-{i}'
                if Review.query.filter_by(original_url=original_url).first():
                    continue  # skip duplicate
                author = _rnd_name(rng)
                review = Review(
                    subject_id=subject.id,
                    title=title,
                    body=body,
                    rating=rating,
                    author_name=author,
                    source_site='sample',
                    is_published=True,
                    original_url=original_url,
                )
                db.session.add(review)
                reviews_added += 1

            subject.update_stats()

        # ------------------------------------------------------------------ #
        # 4. Download subject images
        # ------------------------------------------------------------------ #
        for fish_name, data in FISH_DATA.items():
            slug = data['slug']
            subject = Subject.query.filter_by(
                subcategory_id=fish_sub.id, slug=slug
            ).first()
            if subject is None:
                continue

            # Determine file extension by trying to probe content-type later;
            # default to .jpg
            dest_jpg = os.path.join(
                base_dir, 'static', 'images', 'uploads', 'subjects', f'{slug}.jpg'
            )
            dest_png = os.path.join(
                base_dir, 'static', 'images', 'uploads', 'subjects', f'{slug}.png'
            )

            # Skip if already downloaded
            if os.path.exists(dest_jpg):
                subject.image_path = f'images/uploads/subjects/{slug}.jpg'
                logger.info('  Image already exists for %s', fish_name)
                time.sleep(0)
                continue
            if os.path.exists(dest_png):
                subject.image_path = f'images/uploads/subjects/{slug}.png'
                logger.info('  Image already exists for %s', fish_name)
                time.sleep(0)
                continue

            logger.info('  Fetching image for %s …', fish_name)
            img_url = get_wiki_image(data['wiki_title'])
            if not img_url:
                logger.info('    Wikipedia miss; trying Commons …')
                img_url = try_commons_image(fish_name + ' fish aquarium')

            if img_url:
                # Choose extension based on URL
                ext = '.jpg'
                lower = img_url.lower()
                if '.png' in lower:
                    ext = '.png'
                elif '.gif' in lower:
                    ext = '.gif'
                dest = os.path.join(
                    base_dir, 'static', 'images', 'uploads', 'subjects', f'{slug}{ext}'
                )
                ok = download_image(img_url, dest)
                if ok:
                    subject.image_path = f'images/uploads/subjects/{slug}{ext}'
            else:
                logger.warning('  No image found for %s', fish_name)

            time.sleep(2)

        # ------------------------------------------------------------------ #
        # 5. Download subcategory image
        # ------------------------------------------------------------------ #
        defaults_dir = os.path.join(base_dir, 'static', 'images', 'defaults')
        fish_default = os.path.join(defaults_dir, 'fish.jpg')

        if not os.path.exists(fish_default):
            logger.info('Fetching subcategory image for Fish …')
            img_url = get_wiki_image('Aquarium fish')
            if not img_url:
                logger.info('  Wikipedia miss; trying Commons …')
                img_url = try_commons_image('tropical fish aquarium')
            if img_url:
                download_image(img_url, fish_default)
                time.sleep(2)
            else:
                logger.warning('Could not find a subcategory image for Fish')

        if os.path.exists(fish_default):
            fish_sub.image_path = 'images/defaults/fish.jpg'
        else:
            logger.warning('fish.jpg not present; subcategory image_path not set')

        # ------------------------------------------------------------------ #
        # 6. Single commit
        # ------------------------------------------------------------------ #
        db.session.commit()
        logger.info(
            'Done. Subjects added: %d, Reviews added: %d',
            subjects_added,
            reviews_added,
        )


if __name__ == '__main__':
    main()
