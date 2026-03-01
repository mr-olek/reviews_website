from __future__ import annotations

import logging
import os
import random
import re
import time

import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "Mozilla/5.0 (compatible; PetReviewsBot/1.0)"})

_ADJECTIVES = [
    "Happy", "Clever", "Bright", "Jolly", "Merry", "Sunny", "Brave", "Swift",
    "Wild", "Proud", "Bold", "Calm", "Keen", "Wise", "Zany", "Fancy", "Lucky",
    "Peppy", "Snappy", "Cheery", "Vivid", "Lively", "Eager", "Nimble", "Quirky",
]

_ANIMALS = [
    "Parrot", "Macaw", "Cockatoo", "Budgie", "Conure", "Lory", "Finch", "Canary",
    "Toucan", "Lorikeet", "Cockatiel", "Ibis", "Robin", "Wren", "Dove", "Raven",
    "Falcon", "Kestrel", "Sparrow", "Swallow", "Eagle", "Hawk", "Owl", "Crane",
]


def _rnd_name(rng: random.Random) -> str:
    adj = rng.choice(_ADJECTIVES)
    animal = rng.choice(_ANIMALS)
    number = rng.randint(10, 99)
    return f"{adj}{animal}{number}"


PARROT_DATA: dict[str, dict] = {
    "African Grey Parrot": {
        "slug": "african-grey-parrot",
        "description": (
            "The African Grey Parrot is widely regarded as the most intelligent parrot species, "
            "capable of learning hundreds of words and understanding context. Native to the rainforests "
            "of West and Central Africa, they can live 50 to 70 years in captivity and form deep bonds "
            "with their owners. Their emotional sensitivity means they thrive on routine, mental stimulation, "
            "and consistent companionship."
        ),
        "pros": [
            "Exceptional talking and mimicry ability",
            "Highly intelligent and can learn complex tasks",
            "Forms a deep, lasting bond with primary caregiver",
            "Long lifespan means a lifetime companion",
            "Fascinating and rewarding to interact with daily",
        ],
        "cons": [
            "Very sensitive to stress and changes in routine",
            "Requires several hours of daily interaction and enrichment",
            "Can develop feather-plucking if bored or neglected",
            "Expensive to purchase and maintain properly",
        ],
        "wiki_title": "African grey parrot",
        "reviews": [
            (
                5,
                "Fifteen years and still learning new words",
                "I have had my African Grey, Einstein, for fifteen years now and he still surprises me. "
                "Last week he called my wife by name when she walked through the door. His vocabulary is "
                "well over three hundred words and he uses many of them in context. Yes, he demands "
                "attention and gets grumpy if ignored, but the bond we share is like nothing I have ever "
                "experienced with any animal. Absolutely worth the commitment for the right owner.",
            ),
            (
                5,
                "Smartest creature I have ever shared a home with",
                "Owning an African Grey is less like having a pet and more like having a small, feathered "
                "housemate who critiques your cooking and remembers every promise you break. My bird, Pepper, "
                "learned to say 'step up' before she would allow herself to be handled — she figured out the "
                "command on her own terms. The intelligence is staggering. If you are ready for that level "
                "of commitment, this species is extraordinary.",
            ),
            (
                4,
                "Wonderful companion but demands consistency",
                "My grey is nine years old and honestly my best friend at this point. He talks constantly, "
                "asks for food by name, and even says 'I love you' when I leave the room. The downside is "
                "he really does not tolerate changes. When I redecorated the living room he feather-plucked "
                "for a month. Once things settled he was fine, but it scared me. Highly recommend for "
                "experienced bird owners who can provide a stable environment.",
            ),
            (
                4,
                "Worth every penny and every minute",
                "African Greys are not cheap, and they are not low-maintenance. But after six years with "
                "my bird I cannot imagine life without him. He talks, he problem-solves, he even seems to "
                "read my mood. On bad days he will say 'it is okay' softly and lean against my hand. "
                "I do wish I had known more about their emotional needs before getting him — they are "
                "genuinely fragile creatures emotionally, and that took me by surprise.",
            ),
            (
                3,
                "Amazing bird but not for everyone",
                "I adore my African Grey but I want to be honest with potential owners. She screams when "
                "bored, she has bitten me hard enough to leave bruises, and she went through a feather-plucking "
                "phase that cost me hundreds in vet bills. On the positive side she is breathtakingly clever "
                "and her talking ability is jaw-dropping. But please research thoroughly before buying one. "
                "These birds need far more than most people can realistically provide.",
            ),
            (
                5,
                "A conversation partner for life",
                "People ask me if my African Grey really understands what he says, and after eleven years "
                "my honest answer is sometimes, yes. He uses phrases appropriately, distinguishes between "
                "family members by name, and once told a plumber 'excuse me' when the man accidentally "
                "stepped near his cage. I have had dogs, cats, rabbits, and nothing compares to the "
                "relationship I have with this bird. Incredible species.",
            ),
            (
                3,
                "High reward but very high demand",
                "My grey is clever beyond anything I expected. She has memorised the sounds of my keys "
                "and announces my arrival before I open the door. However, she also throws screaming "
                "tantrums if I skip her morning interaction even once. Taking a holiday requires careful "
                "planning because she notices any change in caregivers. I love her dearly but I would "
                "only recommend African Greys to someone with a genuinely flexible lifestyle.",
            ),
            (
                5,
                "Twenty years and counting — no regrets",
                "I got my African Grey when I was thirty-two years old and he has been with me through "
                "marriages, house moves, and the loss of family members. He outlived my cat and my dog. "
                "At twenty years old he is still learning new words and still shouts my name when I am "
                "late coming home. If you are looking for a companion that will be with you for decades, "
                "the African Grey is unmatched. Plan accordingly.",
            ),
            (
                4,
                "Intelligent to a degree that is almost unsettling",
                "There are days when I forget this bird is a bird. She watches television and comments "
                "on it. She knows the word 'no' and understands its meaning because she uses it back "
                "at me when I try to return her to her cage. She is simultaneously the most rewarding "
                "and most demanding pet I have ever owned. I recommend her species wholeheartedly to "
                "patient, experienced bird people.",
            ),
            (
                4,
                "The parrot world is divided into Greys and everything else",
                "I owned budgies and a cockatiel before getting my African Grey and the difference in "
                "intellectual engagement is enormous. My grey plays puzzle toys, learns new words weekly, "
                "and holds what feel like genuine conversations. He is also expensive, loud when unhappy, "
                "and absolutely requires daily socialisation. Know what you are signing up for and you "
                "will be rewarded with one of the most remarkable animals on the planet.",
            ),
        ],
    },
    "Blue-and-Gold Macaw": {
        "slug": "blue-and-gold-macaw",
        "description": (
            "The Blue-and-Gold Macaw is one of the most recognisable parrots in the world, "
            "famous for its vivid cobalt-blue and golden-yellow plumage. Native to South America, "
            "these large, social birds can live more than 60 years and demand significant space, "
            "time, and interaction. Their powerful beaks and bold personalities make them best "
            "suited to experienced bird owners with large homes."
        ),
        "pros": [
            "Stunning, vibrant plumage that turns heads everywhere",
            "Highly social and bonds deeply with family members",
            "Can learn to talk and mimic with impressive clarity",
            "Playful and entertaining to watch and interact with",
            "Intelligent enough to learn tricks and structured play",
        ],
        "cons": [
            "Extremely loud — screaming can be heard streets away",
            "Requires a very large cage and daily free-flight time",
            "Powerful beak can cause serious injury if trust is broken",
            "Expensive to purchase, house, and maintain",
        ],
        "wiki_title": "Blue-and-yellow macaw",
        "reviews": [
            (
                5,
                "The most spectacular bird I have ever seen in person",
                "I have wanted a Blue-and-Gold Macaw since I was eight years old and finally got one "
                "at forty. Rio is three years old, weighs nearly a kilogram, and is the most visually "
                "stunning creature I have ever shared a home with. He sits on my shoulder at the garden "
                "and neighbours stop to stare. He talks clearly, loves shoulder rides, and screams like "
                "a foghorn when he is bored — which is often. Worth every sacrifice.",
            ),
            (
                4,
                "Beautiful bird, brutal noise level",
                "My macaw is gorgeous, affectionate, and screamingly loud. I want to be upfront about "
                "that last point because no amount of reading prepares you for a contact call at 7am. "
                "She has settled down as she has matured but she still vocalises loudly several times "
                "a day. On the positive side she stepped up on my hand within two weeks, says ten words "
                "clearly, and gives the best bird hugs imaginable. Apartment living is not recommended.",
            ),
            (
                5,
                "Sixty years of companionship in one purchase",
                "My Blue-and-Gold is twelve years old and has grown up with my children. He is gentle "
                "with the kids, plays fetch with plastic bottle caps, and has a vocabulary of about "
                "forty phrases. The size of the bird still amazes visitors — he is genuinely enormous "
                "by parrot standards. You need space, time, money, and patience. In return you get a "
                "companion that could outlive you. I consider that a privilege.",
            ),
            (
                3,
                "Not prepared for the scale of commitment",
                "I had cockatiels before so I thought I understood parrots. A macaw is a completely "
                "different category of commitment. My bird needs at least four hours out of his cage "
                "daily, destroys anything wooden in reach, and screams loud enough to upset my neighbours. "
                "He is also breathtakingly beautiful and when he nuzzles my neck I forgive everything. "
                "Be honest with yourself about whether your lifestyle can genuinely accommodate one.",
            ),
            (
                5,
                "He runs our household now",
                "Twelve months in and I can confirm the macaw is now the boss of our house. He "
                "greets everyone by name, demands breakfast at exactly the same time each morning, and "
                "lets me know when he feels my attention has lapsed for too long. He has a huge flight "
                "aviary in the garden and lives his best life in it. His colours in sunlight are "
                "genuinely otherworldly. An absolute privilege to live with.",
            ),
            (
                4,
                "Talking ability exceeded my expectations",
                "People focus on the size and noise of macaws and forget to mention how well they can "
                "talk. My Blue-and-Gold has over fifty words and uses several in context. He says "
                "good morning when I uncover his cage and calls my dog by name. His intelligence is "
                "obvious every day. The noise is real and the space requirement is real, but so is "
                "the joy this bird brings. Research carefully and then commit fully.",
            ),
            (
                3,
                "Stunning but our house is too small",
                "I am giving three stars not because my macaw is a bad bird but because I made a "
                "poor decision for my living situation. A medium terraced house with thin walls is "
                "not the right home for a bird this loud. My neighbours have complained twice. He "
                "is now living with my brother who has a large detached property and apparently he "
                "is thriving. The bird is wonderful. I was simply not the right owner for him.",
            ),
            (
                5,
                "Worth the cost, worth the effort",
                "Blue-and-Gold Macaws are expensive to acquire and expensive to keep properly. Mine "
                "has a custom stainless steel cage that cost more than my sofa. She eats fresh fruit "
                "and vegetables daily alongside her pellet diet. She sees an avian vet twice a year. "
                "And she is worth every penny. She dances to music, wolf-whistles at visitors, and "
                "screams with delight when she sees me come home. She is irreplaceable.",
            ),
            (
                4,
                "The gentlest giant imaginable when properly socialised",
                "People fear large parrots because of their beaks and that fear is not entirely wrong. "
                "But a well-socialised, hand-raised Blue-and-Gold is extraordinarily gentle. Mine "
                "allows my six-year-old niece to stroke her head feathers. She has never bitten hard "
                "in three years. The key is consistent positive interaction from a young age. These "
                "are magnificent birds that simply require respect and understanding.",
            ),
        ],
    },
    "Cockatiel": {
        "slug": "cockatiel",
        "description": (
            "The Cockatiel is the most popular pet parrot in the world after the budgerigar, "
            "beloved for its gentle temperament, ease of care, and remarkable whistling ability. "
            "Native to Australia, these small to medium parrots are affectionate, social, and "
            "well-suited to first-time bird owners. They bond closely with their families and "
            "are far less demanding than larger parrot species."
        ),
        "pros": [
            "Gentle, affectionate nature ideal for beginners",
            "Talented whistlers that can learn complex tunes",
            "Relatively quiet compared to larger parrots",
            "Lower cost to purchase and maintain",
            "Manageable size suits apartments and smaller homes",
        ],
        "cons": [
            "Produces fine feather dust that can affect allergy sufferers",
            "Needs several hours of out-of-cage time daily",
            "Males can whistle repetitively for hours",
            "Requires a companion bird or significant human attention to thrive",
        ],
        "wiki_title": "Cockatiel",
        "reviews": [
            (
                5,
                "The perfect first bird and then some",
                "I got my cockatiel Sunny two years ago as my first ever bird and he has exceeded "
                "every expectation. He whistles the Andy Griffith theme, climbs onto my glasses "
                "to steal kisses, and cheeps softly when I am working late. He is gentle with my "
                "seven-year-old daughter and never bites. I cannot recommend this species highly "
                "enough for anyone considering a companion bird for the first time.",
            ),
            (
                5,
                "Two decades of whistle-filled mornings",
                "My cockatiel Pebbles turned nineteen this year and is still going strong. She "
                "has whistled the same four songs for fifteen years and shows no sign of stopping. "
                "She naps on my shoulder every evening and demands head scratches with an insistent "
                "little foot tap. Cockatiels are the perfect combination of easy to care for and "
                "deeply rewarding to live with. Genuinely one of the best decisions of my life.",
            ),
            (
                4,
                "Affectionate little character with a big personality",
                "Cockatiels really do have enormous personalities for their size. My bird, Archie, "
                "greets me at his cage door every morning, wolf-whistles at the cat, and sulks "
                "visibly if I skip his daily out-of-cage time. He has not learned to talk but his "
                "whistling repertoire is impressive. The feather dust is the only real downside — "
                "I dust more than I used to. A wonderful species for almost any household.",
            ),
            (
                5,
                "Ideal apartment companion",
                "Living in a flat makes large parrots impossible and dogs impractical. My cockatiel "
                "is the perfect solution. He is small, relatively quiet, and endlessly entertaining. "
                "He dances to pop music, wolf-whistles at my phone screen, and snuggles under my "
                "chin when he is sleepy. My neighbours have never once complained. For anyone in "
                "smaller accommodation wanting a bird companion, the cockatiel is unbeatable.",
            ),
            (
                4,
                "Whistling talent is genuinely impressive",
                "I bought my cockatiel specifically because I read they were good whistlers. The "
                "reality surpassed my expectations. Within six months he had learned six distinct "
                "tunes including a passable rendition of Beethoven's Ode to Joy. He whistles "
                "for hours when content and the sound is actually pleasant rather than shrill. "
                "He is also gentle, easy to handle, and costs very little to keep well. Brilliant bird.",
            ),
            (
                3,
                "Lovely bird but the dust is a real issue",
                "I want to mention the feather dust problem because I was not properly warned. My "
                "cockatiel is a sweet, gentle, wonderful bird who I adore. But he produces an "
                "enormous amount of white feather dust that coats every surface in my home. I have "
                "developed mild respiratory irritation and now run an air purifier constantly. If "
                "you or anyone in your home has allergies or asthma, research this carefully before "
                "getting a cockatiel.",
            ),
            (
                5,
                "My children's first pet and the best choice we made",
                "We got a cockatiel for our children aged nine and eleven and it has been a wonderful "
                "family pet. He tolerates gentle handling beautifully, has learned his name and "
                "several whistling patterns, and seems genuinely fond of the whole family. He has "
                "taught the children responsibility and empathy. At three years old he is thriving "
                "and has become an irreplaceable part of our family.",
            ),
            (
                4,
                "Easy to keep, hard to stop loving",
                "I was sceptical about birds before getting my cockatiel. That was eighteen months "
                "ago and now I cannot imagine my home without him. He eats well on a simple pellet "
                "and seed mix with fresh vegetables, his cage is manageable to clean, and his vet "
                "bills have been minimal. He asks for very little and gives enormous amounts of "
                "affection in return. Genuinely underrated as a companion animal.",
            ),
            (
                3,
                "Great bird but needs more time than expected",
                "Cockatiels are often marketed as low-maintenance birds and I think that is slightly "
                "misleading. My bird needs at least two hours out of his cage daily and gets stressed "
                "and screamy if confined too long. He is not a bird you can leave all week and visit "
                "on weekends. That said, when I give him the time he needs he is absolutely delightful "
                "and well worth the effort. Just go in with realistic expectations.",
            ),
            (
                5,
                "Eighteen years of morning whistles",
                "My cockatiel is eighteen years old and still my morning alarm clock. He starts "
                "whistling the moment light comes through the window and does not stop until I "
                "come to uncover him. He has grey feathers where yellow ones used to be and moves "
                "a little slower, but his personality is unchanged. Cockatiels are genuinely "
                "long-lived birds and the bond that forms over nearly two decades is profound. "
                "Wonderful, wonderful species.",
            ),
        ],
    },
    "Cockatoo": {
        "slug": "cockatoo",
        "description": (
            "Cockatoos are among the most emotionally intense and affectionate of all parrots, "
            "often earning the nickname 'velcro bird' for their need to be constantly near their owners. "
            "Native to Australia and nearby islands, these medium to large parrots are famous for their "
            "dramatic crests, loud screaming, and extraordinary feather dust production. They are best "
            "suited to highly experienced owners who can meet their exceptional social needs."
        ),
        "pros": [
            "Extraordinarily affectionate and cuddly",
            "Highly intelligent and capable of learning complex behaviours",
            "Dramatic crest displays are visually impressive",
            "Forms an incredibly close bond with chosen person",
            "Long lifespan of 40-70 years",
        ],
        "cons": [
            "Screaming can reach ear-splitting volumes",
            "Produces extreme amounts of white feather dust",
            "Severe separation anxiety if not properly managed",
            "Prone to feather destructive behaviour when needs are unmet",
        ],
        "wiki_title": "Cockatoo",
        "reviews": [
            (
                5,
                "The most loving bird I have ever met",
                "My Moluccan Cockatoo came to me as a rescue at age twelve and within three months "
                "she had decided I was her person. She screams if I leave the room, demands cuddles "
                "for hours each day, and raises her crest in pure joy when I come home. The noise "
                "is intense and the dust is everywhere, but the love this bird gives is unlike "
                "anything I have experienced from any animal. Remarkable, demanding, irreplaceable.",
            ),
            (
                4,
                "The velcro bird description is completely accurate",
                "Before I got my Umbrella Cockatoo I thought the 'velcro bird' label was an "
                "exaggeration. It is not. My bird would physically fuse himself to my body if he "
                "could. He rides on my shoulder through every household task, screams when I close "
                "the bathroom door, and preens my eyebrows every morning with intense dedication. "
                "It is simultaneously the most touching and most exhausting thing. Brilliant for "
                "the right person. Disaster for the wrong one.",
            ),
            (
                3,
                "Beautiful bird but the screaming is serious",
                "I want to be honest because I see too many cockatoos in rescue. The screaming "
                "is not occasional. My bird has contact calls that last twenty minutes and can "
                "be heard across the street with all windows closed. My partner now wears "
                "ear protection during peak scream periods. She is also loving, clever, and "
                "comical. But please, please research the noise reality before committing "
                "to a cockatoo. Rescues are full of birds whose owners were not prepared.",
            ),
            (
                5,
                "Worth every dusty surface in my home",
                "People warn you about cockatoo dust but nothing prepares you for the reality. "
                "Every dark surface in my home has a fine white coating within a day of cleaning. "
                "My air purifiers run continuously. And I would not change a single thing because "
                "my Goffin's Cockatoo is the funniest, most affectionate, most entertaining "
                "creature I have ever encountered. She makes me laugh every single day. "
                "Extraordinary birds.",
            ),
            (
                4,
                "Long commitment but incredible reward",
                "My Rose-Breasted Cockatoo is thirty-one years old and likely to outlive me. "
                "He has been with me through divorces, house moves, and bereavements. He screams "
                "when I am sad and dances when I am happy. The feather dust is manageable with "
                "good filtration. The screaming requires patient neighbours. The love is "
                "completely unmanageable in the best possible way.",
            ),
            (
                3,
                "Rehomed reluctantly due to living situation",
                "My Sulphur-Crested Cockatoo was the most intelligent and affectionate pet I "
                "have ever owned. She was also incompatible with my new apartment building. "
                "I tried everything to manage the noise but after three complaints I had to "
                "find her a new home with a retired couple in a rural property. She is thriving "
                "there. The bird was perfect. My situation was not right for her. Know your "
                "living situation before committing to a cockatoo.",
            ),
            (
                5,
                "A feathered soulmate",
                "Fifteen years ago I took in a cockatoo whose owner had passed away. She was "
                "depressed and feather-plucked and the vets gave a guarded prognosis for her "
                "recovery. Today she is fully feathered, screams with enthusiasm every morning, "
                "and has her crest up more often than down. Watching a cockatoo heal and flourish "
                "is one of the most moving experiences of my life. These birds are deeply "
                "emotional animals and deserve owners who understand that.",
            ),
            (
                4,
                "Comical and clever in equal measure",
                "No one warned me how funny cockatoos are. Mine spins dramatically in circles "
                "when excited, plays peekaboo with a towel, and does an impression of my mobile "
                "phone ringtone that fools me every time. He is also loud, dusty, and entirely "
                "too clever for his own good. He has learned to open his cage from the inside "
                "and now I cannot keep him contained. Both endearing and alarming.",
            ),
            (
                5,
                "Twenty years of unconditional love",
                "My Cockatoo is twenty years old and has been with me since she was eight weeks. "
                "She knows every member of my family by name, comes when called, and has never "
                "once bitten in twenty years of daily interaction. Her screaming is real but "
                "manageable with patience and routine. The feather dust requires a cleaning "
                "routine. The love she gives requires no management at all — it is simply "
                "overwhelming and constant.",
            ),
        ],
    },
    "Amazon Parrot": {
        "slug": "amazon-parrot",
        "description": (
            "Amazon Parrots are bold, entertaining, and among the best talkers in the parrot world, "
            "with several species capable of impressive vocabulary and even singing. Native to Central "
            "and South America, these medium to large parrots are known for their confident personalities "
            "and strong opinions. They go through hormonal phases that can make them challenging, "
            "and are best suited to experienced owners who enjoy a bird with a strong character."
        ),
        "pros": [
            "Outstanding talking ability across many species",
            "Bold, confident, and genuinely entertaining personality",
            "Many species can learn to sing full songs",
            "Less dusty than cockatoos or cockatiels",
            "Highly intelligent with impressive problem-solving ability",
        ],
        "cons": [
            "Hormonal phases can cause aggression even in tame birds",
            "Loud and opinionated — will argue back",
            "Requires consistent training and clear boundaries",
            "Can become territorial and nippy without proper socialisation",
        ],
        "wiki_title": "Amazon parrot",
        "reviews": [
            (
                5,
                "The most talkative bird I have ever owned",
                "My Yellow-Naped Amazon has a vocabulary of over two hundred words and sings "
                "three complete songs including Happy Birthday in tune. He was talking within "
                "eight weeks of coming home. He is loud, opinionated, and occasionally nippy "
                "during spring hormonal periods, but his talking ability is genuinely astonishing. "
                "He holds conversations, asks for food by name, and says goodbye when I leave "
                "for work. Extraordinary species.",
            ),
            (
                4,
                "Bold personality needs confident handling",
                "Amazon Parrots are not for timid owners. My Double Yellow-Head has a huge "
                "personality and a very clear sense of what she wants. She will argue, stomp, "
                "and flash her eye-pinning pupils when displeased. She also talks beautifully, "
                "dances to salsa music, and is openly affectionate when she decides to be. "
                "The key is consistent, confident interaction. She respects owners who set "
                "clear boundaries. Wonderful bird for the right person.",
            ),
            (
                5,
                "She sings opera and I am not joking",
                "My Blue-Fronted Amazon has learned to mimic several opera arias from listening "
                "to my music collection. She gets the melody right and fills in words where she "
                "knows them. Visitors are absolutely floored. She is thirteen years old, fully "
                "tame, and one of the most entertaining creatures I have ever encountered. "
                "Amazon Parrots are underrated in the talking department — they are extraordinary.",
            ),
            (
                3,
                "Hormonal phases are genuinely challenging",
                "Nobody warned me adequately about Amazon hormonal seasons. My normally gentle "
                "bird spent three months last spring behaving like a completely different animal. "
                "He bit me hard twice and displayed constantly. I learned to read his signals "
                "and managed it better this year. Outside of hormonal periods he is hilarious, "
                "affectionate, and a brilliant talker. Just be prepared for that seasonal "
                "challenge and know how to handle it safely.",
            ),
            (
                4,
                "Singing at breakfast every morning",
                "My Amazon sings a specific song every morning when I uncover his cage. Every "
                "single morning for nine years without fail. He has also learned to imitate "
                "my laugh, my sneeze, and my coffee machine. His vocabulary is enormous and "
                "his confidence is boundless. He tells the dog off for barking. He instructs "
                "delivery drivers to 'come in' through the window. I love him more than I "
                "can reasonably explain.",
            ),
            (
                4,
                "Intelligent and opinionated in the best way",
                "Amazon Parrots have genuine opinions and they will share them whether you want "
                "them to or not. My Lilac-Crowned Amazon disagrees with me daily and makes "
                "his disagreement very clear. He is also capable of melting my heart completely "
                "by whistling softly and leaning his head against my face. He talks constantly "
                "and clearly. He is challenging and wonderful in roughly equal measure.",
            ),
            (
                3,
                "Wonderful bird that requires serious research first",
                "I came from a cockatiel background and assumed an Amazon would be a natural "
                "upgrade. The hormonal aggression caught me completely off guard and I made "
                "mistakes early on that took two years of patient training to undo. Now that "
                "I understand the species better we have a great relationship. But I urge "
                "anyone considering an Amazon to deeply research their hormonal behaviour "
                "before committing. These are powerful birds with complex emotional lives.",
            ),
            (
                5,
                "Forty years of talking and he shows no sign of stopping",
                "My Orange-Winged Amazon is forty-two years old and still learning new phrases. "
                "He has lived through my marriage, the birth of my children, and my grandchildren "
                "learning to walk. He greets everyone by name and has a specific insult he reserves "
                "exclusively for my neighbour who he has never liked. His longevity means this "
                "species is truly a lifetime commitment — plan for that and embrace it.",
            ),
            (
                5,
                "Best talker in any parrot species I have owned",
                "I have owned African Greys, Cockatiels, and Budgies over the years. For pure "
                "talking clarity and volume, my Mealy Amazon beats them all. She speaks in "
                "full sentences with a clarity that fools people into thinking there is a "
                "person in the next room. Her personality is enormous and her boldness is "
                "refreshing after more sensitive species. Amazon Parrots are fantastic for "
                "owners who enjoy a confident, chatty companion.",
            ),
        ],
    },
    "Budgerigar": {
        "slug": "budgerigar",
        "description": (
            "The Budgerigar, commonly known as the budgie or parakeet, is the world's most popular "
            "pet bird and an ideal choice for first-time bird owners. Native to Australia, these small "
            "parrots are inexpensive, cheerful, and relatively easy to care for while still offering "
            "genuine interaction and occasional talking ability. They thrive in pairs and bring "
            "enormous joy with minimal space and cost requirements."
        ),
        "pros": [
            "Very affordable to purchase and maintain",
            "Small size suits any home including small apartments",
            "Cheerful, active, and entertaining to watch",
            "Some individuals learn to talk with surprising clarity",
            "Ideal starter bird for children and adults",
        ],
        "cons": [
            "Short lifespan of 7-12 years compared to larger parrots",
            "Fine feather dust can bother allergy sufferers",
            "Taming requires patience and consistent daily handling",
            "Very small and fragile — accidental injuries can occur",
        ],
        "wiki_title": "Budgerigar",
        "reviews": [
            (
                5,
                "The most affordable joy in pet ownership",
                "I paid twenty pounds for my budgie Chip three years ago. He has cost very little "
                "to keep, lives happily in a modest cage, and chatters constantly in what I am "
                "convinced is his own private language. He has learned his name, a wolf-whistle, "
                "and about fifteen words. For someone wanting bird companionship on a budget, "
                "absolutely nothing beats a well-cared-for budgerigar.",
            ),
            (
                5,
                "My children have learned so much from our pair",
                "We bought two budgies for our children aged eight and ten as first pets. Two years "
                "later the kids feed them before breakfast without being reminded, understand that "
                "animals have feelings and needs, and can identify their birds' different vocalisations. "
                "The budgies themselves are tame, cheerful, and chat to each other all day. Wonderful "
                "choice for a family first bird.",
            ),
            (
                4,
                "Small bird with a huge personality",
                "People underestimate budgies because they are small and cheap. My budgie Bobby "
                "has a personality that fills the room. He sings to the radio, argues with his "
                "reflection, and demands to participate in every household activity by flying "
                "to the nearest person and climbing onto whatever they are doing. For their size "
                "they give enormous amounts of entertainment. Brilliant value in every sense.",
            ),
            (
                4,
                "Surprisingly good talker with patience",
                "Male budgies in particular can be excellent talkers if you work with them daily "
                "from a young age. My bird learned around forty words and short phrases over two "
                "years of consistent training. He says his name, several greetings, and a few "
                "choice phrases he picked up from the television. Not every budgie will talk "
                "but many will, and the ones that do are genuinely impressive little birds.",
            ),
            (
                5,
                "Ten years and counting",
                "My budgie turned ten this year which his vet considers exceptional for the species. "
                "He has been with me through three house moves and two jobs. He still whistles his "
                "morning greeting, still demands millet treats by rattling his food cup, and still "
                "flies to my hand when called. Small pets can leave enormous gaps when they go. "
                "I am grateful for every year I have had with him.",
            ),
            (
                3,
                "Taming is slower than I expected",
                "I got my budgie expecting to be hand-taming him within weeks. It took four months "
                "of patient daily work before he would step onto my finger reliably. Some budgies "
                "tame easily, others are more cautious by nature. Once he was tame he became a "
                "lovely little companion. But set realistic expectations for the training process, "
                "especially with older birds or those not hand-raised from the breeder.",
            ),
            (
                4,
                "Perfect for apartment living",
                "A budgie is the ideal companion for small-space living. My flat has one bedroom "
                "and a tiny living room and my pair of budgies are perfectly happy in it. They "
                "are quiet enough not to bother neighbours, eat very little, and fill my home "
                "with cheerful chatter all day. Coming home to their excited greeting after work "
                "genuinely improves my mood. Recommend without reservation for city dwellers.",
            ),
            (
                5,
                "My elderly mother's best companion",
                "My seventy-eight-year-old mother has been lonely since my father passed. A budgie "
                "seemed like a manageable solution. Two years on, she talks to him constantly, "
                "he talks back, and she says he gives her a reason to get up every morning. The "
                "bird is easy for her to care for, is not boisterous or loud, and fills her quiet "
                "house with gentle sound. For elderly people living alone, budgies are a perfect "
                "companion animal.",
            ),
            (
                3,
                "Short lifespan is the hardest part",
                "I want to prepare potential owners for the emotional reality. Budgies live "
                "seven to twelve years, sometimes less. My first budgie died at six after a "
                "rapid illness despite good vet care. The grief was real and it caught me "
                "off guard. I now have a new bird and I love him just as much. But anyone "
                "getting a budgie for a child should have an honest conversation about "
                "lifespan before the bird comes home.",
            ),
            (
                5,
                "My gateway bird into the parrot world",
                "I started with a budgie ten years ago to see if bird ownership was for me. It "
                "was. I now have a cockatiel and am researching African Greys. But my original "
                "budgie is still here, still chattering, and still the bird I reach for when I "
                "need uncomplicated, cheerful company. He is the foundation of my entire avian "
                "hobby and I owe him a great deal.",
            ),
        ],
    },
    "Sun Conure": {
        "slug": "sun-conure",
        "description": (
            "The Sun Conure is one of the most visually striking parrots available as a pet, "
            "with vivid orange, yellow, and green plumage that earns instant admiration. Native "
            "to northeastern South America, these small to medium parrots are playful, "
            "affectionate, and endlessly entertaining. However, they produce one of the loudest "
            "calls of any small parrot and require patient, experienced ownership to manage "
            "their vocal nature."
        ),
        "pros": [
            "Stunning, vibrant plumage in orange, yellow, and green",
            "Playful, energetic, and deeply entertaining",
            "Bonds closely and affectionately with owners",
            "Smaller size than macaws with similar personality energy",
            "Highly acrobatic and fun to watch at play",
        ],
        "cons": [
            "Extremely loud screaming that can carry long distances",
            "Not suitable for apartments or noise-sensitive environments",
            "Requires significant daily interaction and enrichment",
            "Can become nippy without consistent training",
        ],
        "wiki_title": "Sun parakeet",
        "reviews": [
            (
                5,
                "A tiny sun living in my living room",
                "My Sun Conure is named Mango and the name fits perfectly. He is the colour of "
                "a ripe mango and radiates warmth and energy to match. He flies to my shoulder "
                "the moment I open his cage, hangs upside down from my fingers for fun, and "
                "screams with pure joy when he sees me first thing in the morning. The scream "
                "is loud. Very loud. But so is the happiness he brings.",
            ),
            (
                4,
                "The loudest small parrot I have encountered",
                "Sun Conures have been described as loud and that is technically accurate but "
                "wildly understated. My bird's contact call could wake the dead. He is also "
                "funny, athletic, and completely in love with me. He sleeps inside my shirt "
                "collar during television evenings and wakes me with screaming at sunrise. "
                "I adore him. My neighbours require careful management. Worth it for the right "
                "living situation.",
            ),
            (
                5,
                "Most photogenic pet I have ever owned",
                "People stop me in the street when I take Mango out for socialisation walks on "
                "his harness. His colours photograph brilliantly and he poses naturally. Beyond "
                "the beauty he is clever, mischievous, and absolutely devoted. He learned to "
                "play fetch with small paper balls, ring a bell to ask for treats, and imitate "
                "three words clearly. For sheer visual impact combined with personality, the "
                "Sun Conure is unmatched among small parrots.",
            ),
            (
                3,
                "Forced to rehome — heart-breaking decision",
                "My Sun Conure was everything I wanted in a parrot except manageable in my flat. "
                "My neighbours complained within a week and the building management contacted me "
                "within a month. I tried every noise management strategy I could find. Nothing "
                "worked sufficiently. I rehomed him to a friend with a detached house where he "
                "is now thriving. The bird is spectacular. Please only get a Sun Conure if your "
                "living situation can genuinely absorb the noise.",
            ),
            (
                5,
                "The clown of the parrot world",
                "If you want a parrot that makes you laugh every single day, get a Sun Conure. "
                "Mine rolls around in his food dish pretending to bath in seeds. He plays dead "
                "on command. He hangs from the curtain rail by one foot and screams until "
                "someone notices. He is ridiculous and I love him completely. The noise is very "
                "real but for someone with the right home environment the personality payoff is "
                "extraordinary.",
            ),
            (
                4,
                "Vibrant colours that never get old",
                "Four years with my Sun Conure and I still stop and stare at his colours every "
                "morning. Full sunlight on his plumage is genuinely breathtaking. He is also "
                "clever, affectionate, and has the energy of a creature twice his size. He "
                "needs at least three hours out of his cage daily and will let me know loudly "
                "if he does not get it. Well worth the commitment for the right owner.",
            ),
            (
                4,
                "Playful and affectionate beyond all expectation",
                "I researched Sun Conures extensively before getting one and felt prepared. "
                "What I was not prepared for was how deeply affectionate they are. My bird "
                "crawls inside my jumper for warmth, sleeps on my pillow, and screams with "
                "what I can only describe as delight whenever I come home. He is not a pet "
                "that sits in a cage looking pretty. He is a full participant in daily life "
                "and I would have it no other way.",
            ),
            (
                3,
                "Brilliant bird needing honest noise warning",
                "Three stars purely to draw attention to the noise issue because it is consistently "
                "under-communicated by sellers. My Sun Conure produces contact calls at a volume "
                "that causes pain without ear protection at close range. He does this multiple "
                "times per day. He is also loving, entertaining, strikingly beautiful, and a joy "
                "to live with when I am managing the noise context properly. But the noise is "
                "not negotiable and owners must plan for it seriously.",
            ),
            (
                5,
                "Best decision I made for my mental health",
                "I adopted my Sun Conure during a very difficult period personally and he "
                "genuinely helped my recovery. His daily routine gave me structure. His "
                "undiscriminating affection gave me connection. His antics made me laugh "
                "when nothing else could. He is noisy, demanding, and utterly wonderful. "
                "Two years later I am in a much better place and he deserves a significant "
                "part of the credit.",
            ),
        ],
    },
}


def get_wiki_image(title: str, size: int = 500) -> str | None:
    params = {
        "action": "query",
        "titles": title,
        "prop": "pageimages",
        "pithumbsize": size,
        "format": "json",
    }
    try:
        r = SESSION.get("https://en.wikipedia.org/w/api.php", params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        pages = data.get("query", {}).get("pages", {})
        for page in pages.values():
            thumb = page.get("thumbnail", {})
            url = thumb.get("source")
            if url:
                url = re.sub(r"/\d+px-", f"/{size}px-", url)
                return url
    except Exception as exc:
        logger.warning("Wikipedia API error for %r: %s", title, exc)
    return None


def download_image(url: str, dest_path: str) -> bool:
    try:
        r = SESSION.get(url, timeout=15, stream=True)
        r.raise_for_status()
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        with open(dest_path, "wb") as fh:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    fh.write(chunk)
        logger.info("Downloaded image to %s", dest_path)
        return True
    except Exception as exc:
        logger.warning("Failed to download %s: %s", url, exc)
        return False


def main() -> None:
    from app import create_app, db
    from app.models import Category, Review, SubCategory, Subject

    app = create_app("development")

    with app.app_context():
        # Locate Animals category
        animals_cat = Category.query.filter_by(slug="animals").first()
        if not animals_cat:
            logger.error("Animals category not found. Run seed.py first.")
            return

        # Create Parrots subcategory if absent
        parrots_sub = SubCategory.query.filter_by(
            category_id=animals_cat.id, slug="parrots"
        ).first()
        if not parrots_sub:
            parrots_sub = SubCategory(
                category_id=animals_cat.id,
                name="Parrots",
                slug="parrots",
            )
            db.session.add(parrots_sub)
            db.session.flush()
            logger.info("Created subcategory: Parrots")
        else:
            logger.info("Subcategory Parrots already exists — skipping creation.")

        subjects_created = 0
        reviews_created = 0

        uploads_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "static",
            "images",
            "uploads",
            "subjects",
        )
        os.makedirs(uploads_dir, exist_ok=True)

        for name, data in PARROT_DATA.items():
            slug = data["slug"]

            # Create subject if absent
            subject = Subject.query.filter_by(
                subcategory_id=parrots_sub.id, slug=slug
            ).first()
            if not subject:
                subject = Subject(
                    subcategory_id=parrots_sub.id,
                    name=name,
                    slug=slug,
                )
                db.session.add(subject)
                db.session.flush()
                subjects_created += 1
                logger.info("Created subject: %s", name)
            else:
                logger.info("Subject %s already exists — updating metadata.", name)

            subject.description = data["description"]
            subject.pros = "\n".join(data["pros"])
            subject.cons = "\n".join(data["cons"])

            # Seed reviews
            rng = random.Random(hash(name) % 100000)
            all_reviews = data["reviews"]
            count = rng.randint(5, 10)
            selected = rng.sample(all_reviews, min(count, len(all_reviews)))

            author_rng = random.Random(hash(name + "authors") % 100000)
            for i, (rating, title, body) in enumerate(selected):
                original_url = f"sample-{slug}-{i}"
                existing = Review.query.filter_by(original_url=original_url).first()
                if existing:
                    continue
                review = Review(
                    subject_id=subject.id,
                    rating=rating,
                    title=title,
                    body=body,
                    author_name=_rnd_name(author_rng),
                    source_site="sample",
                    is_published=True,
                    original_url=original_url,
                )
                db.session.add(review)
                reviews_created += 1

            db.session.flush()
            subject.update_stats()

            # Download Wikipedia image
            img_url = get_wiki_image(data["wiki_title"])
            if img_url:
                ext = "jpg"
                if img_url.lower().endswith(".png"):
                    ext = "png"
                dest = os.path.join(uploads_dir, f"{slug}.{ext}")
                if download_image(img_url, dest):
                    subject.image_path = f"images/uploads/subjects/{slug}.{ext}"
                    logger.info("Set image_path for %s", name)
                time.sleep(2)
            else:
                logger.warning("No Wikipedia image found for %s (title: %s)", name, data["wiki_title"])

        db.session.commit()
        logger.info(
            "Done. Subjects created: %d, Reviews created: %d",
            subjects_created,
            reviews_created,
        )


if __name__ == "__main__":
    main()
