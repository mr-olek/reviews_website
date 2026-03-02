#!/usr/bin/env python3
"""Seed Movies category with top 100 movies and reviews."""
import os, sys, random, time, requests
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Category, SubCategory, Subject, Review

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
SESSION = requests.Session()
SESSION.headers['User-Agent'] = 'Mozilla/5.0 (compatible; VerdictlyBot/1.0)'

# ---------------------------------------------------------------------------
# (Display Name, slug, Wikipedia article for image, year)
# ---------------------------------------------------------------------------
MOVIES = [
    ('The Shawshank Redemption',                        'the-shawshank-redemption',             'The Shawshank Redemption',                     1994),
    ('The Godfather',                                   'the-godfather',                        'The Godfather',                                1972),
    ('The Dark Knight',                                 'the-dark-knight',                      'The Dark Knight (film)',                       2008),
    ('The Godfather Part II',                           'the-godfather-part-ii',                'The Godfather Part II',                        1974),
    ('12 Angry Men',                                    '12-angry-men',                         '12 Angry Men (1957 film)',                     1957),
    ("Schindler's List",                                'schindlers-list',                      "Schindler's List",                             1993),
    ('The Lord of the Rings: The Return of the King',  'lotr-return-of-the-king',              'The Lord of the Rings: The Return of the King',2003),
    ('Pulp Fiction',                                    'pulp-fiction',                         'Pulp Fiction',                                 1994),
    ('The Good, the Bad and the Ugly',                  'the-good-the-bad-and-the-ugly',        'The Good, the Bad and the Ugly',               1966),
    ('Forrest Gump',                                    'forrest-gump',                         'Forrest Gump',                                 1994),
    ('Fight Club',                                      'fight-club',                           'Fight Club (film)',                            1999),
    ('Inception',                                       'inception',                            'Inception (film)',                             2010),
    ('The Lord of the Rings: The Fellowship of the Ring','lotr-fellowship-of-the-ring',         'The Lord of the Rings: The Fellowship of the Ring',2001),
    ('The Empire Strikes Back',                         'the-empire-strikes-back',              'The Empire Strikes Back',                      1980),
    ('The Matrix',                                      'the-matrix',                           'The Matrix',                                   1999),
    ('Goodfellas',                                      'goodfellas',                           'GoodFellas',                                   1990),
    ('One Flew Over the Cuckoo\'s Nest',                'one-flew-over-the-cuckoos-nest',       "One Flew Over the Cuckoo's Nest (film)",       1975),
    ('Seven',                                           'seven',                                'Seven (1995 film)',                            1995),
    ('The Silence of the Lambs',                        'the-silence-of-the-lambs',             'The Silence of the Lambs (film)',              1991),
    ('Interstellar',                                    'interstellar',                         'Interstellar (film)',                          2014),
    ('Saving Private Ryan',                             'saving-private-ryan',                  'Saving Private Ryan',                          1998),
    ('The Usual Suspects',                              'the-usual-suspects',                   'The Usual Suspects',                           1995),
    ('American History X',                              'american-history-x',                   'American History X',                           1998),
    ('Parasite',                                        'parasite',                             'Parasite (2019 film)',                         2019),
    ('The Lion King',                                   'the-lion-king',                        'The Lion King',                                1994),
    ('Terminator 2: Judgment Day',                      'terminator-2',                         'Terminator 2: Judgment Day',                   1991),
    ('Gladiator',                                       'gladiator',                            'Gladiator (2000 film)',                        2000),
    ('Whiplash',                                        'whiplash',                             'Whiplash (2014 film)',                         2014),
    ('The Prestige',                                    'the-prestige',                         'The Prestige (film)',                          2006),
    ('Memento',                                         'memento',                              'Memento (film)',                               2000),
    ('The Departed',                                    'the-departed',                         'The Departed',                                 2006),
    ('Django Unchained',                                'django-unchained',                     'Django Unchained',                             2012),
    ('WALL-E',                                          'wall-e',                               'WALL-E',                                       2008),
    ('Toy Story',                                       'toy-story',                            'Toy Story',                                    1995),
    ('No Country for Old Men',                          'no-country-for-old-men',               'No Country for Old Men (film)',                2007),
    ('Alien',                                           'alien',                                'Alien (film)',                                 1979),
    ('Apocalypse Now',                                  'apocalypse-now',                       'Apocalypse Now',                               1979),
    ('The Shining',                                     'the-shining',                          'The Shining (film)',                           1980),
    ('Braveheart',                                      'braveheart',                           'Braveheart',                                   1995),
    ('Full Metal Jacket',                               'full-metal-jacket',                    'Full Metal Jacket',                            1987),
    ('2001: A Space Odyssey',                           '2001-a-space-odyssey',                 '2001: A Space Odyssey',                        1968),
    ('Casablanca',                                      'casablanca',                           'Casablanca (film)',                            1942),
    ('Psycho',                                          'psycho',                               'Psycho (1960 film)',                           1960),
    ('Rear Window',                                     'rear-window',                          'Rear Window',                                  1954),
    ('Blade Runner',                                    'blade-runner',                         'Blade Runner',                                 1982),
    ('Eternal Sunshine of the Spotless Mind',           'eternal-sunshine',                     'Eternal Sunshine of the Spotless Mind',        2004),
    ('Reservoir Dogs',                                  'reservoir-dogs',                       'Reservoir Dogs',                               1992),
    ('There Will Be Blood',                             'there-will-be-blood',                  'There Will Be Blood',                          2007),
    ('Oldboy',                                          'oldboy',                               'Oldboy (2003 film)',                           2003),
    ('Amelie',                                          'amelie',                               'Amélie',                                       2001),
    ('Heat',                                            'heat',                                 'Heat (1995 film)',                             1995),
    ('Taxi Driver',                                     'taxi-driver',                          'Taxi Driver',                                  1976),
    ("Pan's Labyrinth",                                 'pans-labyrinth',                       "Pan's Labyrinth",                              2006),
    ('The Truman Show',                                 'the-truman-show',                      'The Truman Show',                              1998),
    ('Die Hard',                                        'die-hard',                             'Die Hard',                                     1988),
    ('Spirited Away',                                   'spirited-away',                        'Spirited Away',                                2001),
    ('City of God',                                     'city-of-god',                          'City of God (film)',                           2002),
    ('Life Is Beautiful',                               'life-is-beautiful',                    'Life Is Beautiful',                            1997),
    ('A Beautiful Mind',                                'a-beautiful-mind',                     'A Beautiful Mind (film)',                      2001),
    ('Back to the Future',                              'back-to-the-future',                   'Back to the Future',                           1985),
    ('The Pianist',                                     'the-pianist',                          'The Pianist (film)',                           2002),
    ('Avengers: Infinity War',                          'avengers-infinity-war',                'Avengers: Infinity War',                       2018),
    ('Mad Max: Fury Road',                              'mad-max-fury-road',                    'Mad Max: Fury Road',                           2015),
    ('The Grand Budapest Hotel',                        'the-grand-budapest-hotel',             'The Grand Budapest Hotel',                     2014),
    ('La La Land',                                      'la-la-land',                           'La La Land',                                   2016),
    ('Get Out',                                         'get-out',                              'Get Out (film)',                               2017),
    ('1917',                                            '1917',                                 '1917 (film)',                                  2019),
    ('Dunkirk',                                         'dunkirk',                              'Dunkirk (2017 film)',                          2017),
    ('Arrival',                                         'arrival',                              'Arrival (film)',                               2016),
    ('The Social Network',                              'the-social-network',                   'The Social Network',                           2010),
    ('Black Swan',                                      'black-swan',                           'Black Swan (film)',                            2010),
    ('Inside Out',                                      'inside-out',                           'Inside Out (film)',                            2015),
    ('Leon: The Professional',                          'leon-the-professional',                'Léon: The Professional',                       1994),
    ('Requiem for a Dream',                             'requiem-for-a-dream',                  'Requiem for a Dream',                          2000),
    ('Monty Python and the Holy Grail',                 'monty-python-holy-grail',              'Monty Python and the Holy Grail',              1975),
    ('Into the Wild',                                   'into-the-wild',                        'Into the Wild (film)',                         2007),
    ('The Revenant',                                    'the-revenant',                         'The Revenant (film)',                          2015),
    ('Gravity',                                         'gravity',                              'Gravity (film)',                               2013),
    ('Her',                                             'her',                                  'Her (film)',                                   2013),
    ('Ex Machina',                                      'ex-machina',                           'Ex Machina (film)',                            2014),
    ('A Separation',                                    'a-separation',                         'A Separation',                                 2011),
    ('The Green Mile',                                  'the-green-mile',                       'The Green Mile (film)',                        1999),
    ('Catch Me If You Can',                             'catch-me-if-you-can',                  'Catch Me If You Can',                          2002),
    ('American Beauty',                                 'american-beauty',                      'American Beauty (film)',                       1999),
    ('Once Upon a Time in the West',                    'once-upon-a-time-in-the-west',         'Once Upon a Time in the West',                 1968),
    ('Inglourious Basterds',                            'inglourious-basterds',                 'Inglourious Basterds',                         2009),
    ('A Clockwork Orange',                              'a-clockwork-orange',                   'A Clockwork Orange (film)',                    1971),
    ('Coco',                                            'coco',                                 'Coco (2017 film)',                             2017),
    ('Joker',                                           'joker',                                'Joker (2019 film)',                            2019),
    ('Knives Out',                                      'knives-out',                           'Knives Out',                                   2019),
    ('Spider-Man: Into the Spider-Verse',               'spider-man-into-the-spider-verse',     'Spider-Man: Into the Spider-Verse',            2018),
    ('The Wolf of Wall Street',                         'the-wolf-of-wall-street',              'The Wolf of Wall Street (2013 film)',          2013),
    ('Lawrence of Arabia',                              'lawrence-of-arabia',                   'Lawrence of Arabia (film)',                    1962),
    ('Dr. Strangelove',                                 'dr-strangelove',                       'Dr. Strangelove',                              1964),
    ('Mulholland Drive',                                'mulholland-drive',                     'Mulholland Drive (film)',                      2001),
    ('It\'s a Wonderful Life',                          'its-a-wonderful-life',                 "It's a Wonderful Life",                        1946),
    ('The Sixth Sense',                                 'the-sixth-sense',                      'The Sixth Sense',                              1999),
    ('Good Will Hunting',                               'good-will-hunting',                    'Good Will Hunting',                            1997),
    ('The Big Lebowski',                                'the-big-lebowski',                     'The Big Lebowski',                             1998),
    ('Schindler\'s List',                               'schindlers-list-alt',                  "Schindler's List",                             1993),  # duplicate guard handled
]

# Remove duplicates by slug
seen_slugs = set()
MOVIES_DEDUPED = []
for m in MOVIES:
    if m[1] not in seen_slugs:
        seen_slugs.add(m[1])
        MOVIES_DEDUPED.append(m)
MOVIES = MOVIES_DEDUPED[:100]


# ---------------------------------------------------------------------------
# Per-movie facts for personalised reviews
# ---------------------------------------------------------------------------
MOVIE_DATA = {
    'the-shawshank-redemption': {
        'director': 'Frank Darabont', 'characters': ['Andy Dufresne', 'Red', 'Warden Norton'],
        'themes': ['hope', 'friendship', 'perseverance', 'freedom'],
        'scenes': ['the library scene', 'the rooftop beer scene', 'the finale on the beach'],
        'highlights': ['Morgan Freeman\'s narration', 'the emotional payoff', 'the script\'s quiet power'],
    },
    'the-godfather': {
        'director': 'Francis Ford Coppola', 'characters': ['Michael Corleone', 'Vito Corleone', 'Tom Hagen'],
        'themes': ['family loyalty', 'power and corruption', 'the American dream'],
        'scenes': ['the horse head scene', 'the baptism montage', 'the garden scene'],
        'highlights': ['Marlon Brando\'s performance', 'Nino Rota\'s score', 'Gordon Willis\'s cinematography'],
    },
    'the-dark-knight': {
        'director': 'Christopher Nolan', 'characters': ['Batman', 'The Joker', 'Harvey Dent'],
        'themes': ['chaos vs order', 'moral compromise', 'the nature of heroism'],
        'scenes': ['the interrogation scene', 'the hospital explosion', 'the magic trick'],
        'highlights': ['Heath Ledger\'s Joker', 'the practical effects', 'the escalation of stakes'],
    },
    'the-godfather-part-ii': {
        'director': 'Francis Ford Coppola', 'characters': ['Michael Corleone', 'Young Vito', 'Fredo'],
        'themes': ['the corruption of power', 'immigrant ambition', 'family betrayal'],
        'scenes': ['the parallel flashbacks', 'the Senate hearing', 'the lake house ending'],
        'highlights': ['De Niro\'s young Vito', 'the dual narrative structure', 'Al Pacino\'s cold transformation'],
    },
    '12-angry-men': {
        'director': 'Sidney Lumet', 'characters': ['Juror 8', 'Juror 3', 'Juror 4'],
        'themes': ['justice', 'prejudice', 'reasonable doubt'],
        'scenes': ['the knife demonstration', 'the rain at the window', 'the final vote'],
        'highlights': ['Henry Fonda\'s quiet determination', 'the single-room tension', 'the script\'s logic'],
    },
    'schindlers-list': {
        'director': 'Steven Spielberg', 'characters': ['Oskar Schindler', 'Amon Goeth', 'Itzhak Stern'],
        'themes': ['the Holocaust', 'moral awakening', 'the value of human life'],
        'scenes': ['the girl in the red coat', 'the list compilation', 'the final goodbye'],
        'highlights': ['Spielberg\'s black-and-white photography', 'Liam Neeson\'s arc', 'John Williams\'s score'],
    },
    'lotr-return-of-the-king': {
        'director': 'Peter Jackson', 'characters': ['Frodo', 'Sam', 'Aragorn', 'Gandalf'],
        'themes': ['friendship', 'sacrifice', 'the corruption of power'],
        'scenes': ['the lighting of the beacons', 'the Pelennor Fields battle', 'the Grey Havens'],
        'highlights': ['the emotional conclusion', 'the scale of the battles', 'Howard Shore\'s score'],
    },
    'pulp-fiction': {
        'director': 'Quentin Tarantino', 'characters': ['Vincent Vega', 'Jules', 'Mia Wallace', 'Butch'],
        'themes': ['redemption', 'chance and fate', 'pop culture and violence'],
        'scenes': ['the diner opening', 'the Ezekiel 25:17 speech', 'the Royale with Cheese conversation'],
        'highlights': ['the non-linear structure', 'John Travolta and Samuel L. Jackson\'s chemistry', 'the dialogue'],
    },
    'the-good-the-bad-and-the-ugly': {
        'director': 'Sergio Leone', 'characters': ['Blondie', 'Angel Eyes', 'Tuco'],
        'themes': ['greed', 'survival', 'the moral ambiguity of the West'],
        'scenes': ['the three-way standoff', 'the bridge explosion', 'the cemetery finale'],
        'highlights': ['Ennio Morricone\'s iconic score', 'the extreme close-ups', 'Clint Eastwood\'s stoicism'],
    },
    'forrest-gump': {
        'director': 'Robert Zemeckis', 'characters': ['Forrest Gump', 'Jenny', 'Lieutenant Dan'],
        'themes': ['innocence', 'love and loss', 'American history'],
        'scenes': ['the running sequence', 'the shrimp boat in the storm', 'the final letter scene'],
        'highlights': ['Tom Hanks\'s warm performance', 'the historical cameos', 'Alan Silvestri\'s music'],
    },
    'fight-club': {
        'director': 'David Fincher', 'characters': ['The Narrator', 'Tyler Durden', 'Marla Singer'],
        'themes': ['masculinity and identity', 'consumerism', 'self-destruction'],
        'scenes': ['the twist reveal', 'the homework assignment', 'the ending with the buildings'],
        'highlights': ['Brad Pitt\'s charisma', 'Fincher\'s dark aesthetic', 'the unreliable narrator device'],
    },
    'inception': {
        'director': 'Christopher Nolan', 'characters': ['Cobb', 'Arthur', 'Ariadne', 'Mal'],
        'themes': ['dreams and reality', 'grief', 'the nature of memory'],
        'scenes': ['the folding city', 'the zero-gravity hallway fight', 'the spinning top ending'],
        'highlights': ['Hans Zimmer\'s score', 'the layered dream structure', 'the visual effects'],
    },
    'lotr-fellowship-of-the-ring': {
        'director': 'Peter Jackson', 'characters': ['Frodo', 'Gandalf', 'Aragorn', 'Boromir'],
        'themes': ['friendship', 'the burden of power', 'courage in the face of darkness'],
        'scenes': ['the Shire opening', 'the Mines of Moria', 'the breaking of the Fellowship'],
        'highlights': ['the world-building', 'Ian McKellen as Gandalf', 'Howard Shore\'s score'],
    },
    'the-empire-strikes-back': {
        'director': 'Irvin Kershner', 'characters': ['Luke Skywalker', 'Darth Vader', 'Han Solo', 'Yoda'],
        'themes': ['failure as growth', 'father and son', 'the nature of evil'],
        'scenes': ['the "I am your father" reveal', 'the Hoth battle', 'Cloud City'],
        'highlights': ['the darker tone', 'Yoda\'s introduction', 'John Williams\'s score'],
    },
    'the-matrix': {
        'director': 'The Wachowskis', 'characters': ['Neo', 'Morpheus', 'Trinity', 'Agent Smith'],
        'themes': ['simulation and reality', 'free will', 'the chosen one'],
        'scenes': ['the red pill / blue pill scene', 'the bullet time sequence', 'the lobby shootout'],
        'highlights': ['the revolutionary visual effects', 'Keanu Reeves\'s understated performance', 'the philosophical depth'],
    },
    'goodfellas': {
        'director': 'Martin Scorsese', 'characters': ['Henry Hill', 'Jimmy Conway', 'Tommy DeVito'],
        'themes': ['the glamour and cost of crime', 'loyalty and betrayal', 'the American Dream'],
        'scenes': ['the Copacabana tracking shot', 'the "funny how?" scene', 'the final freeze frame'],
        'highlights': ['Ray Liotta\'s narration', 'Joe Pesci\'s terrifying energy', 'the soundtrack choices'],
    },
    'one-flew-over-the-cuckoos-nest': {
        'director': 'Milos Forman', 'characters': ['R.P. McMurphy', 'Nurse Ratched', 'Chief Bromden'],
        'themes': ['freedom vs control', 'institutional power', 'rebellion'],
        'scenes': ['the fishing trip', 'the World Series argument', 'the ending'],
        'highlights': ['Jack Nicholson\'s electric performance', 'Louise Fletcher\'s chilling authority', 'the ensemble cast'],
    },
    'seven': {
        'director': 'David Fincher', 'characters': ['Detective Mills', 'Detective Somerset', 'John Doe'],
        'themes': ['sin and punishment', 'cynicism vs idealism', 'the nature of evil'],
        'scenes': ['the "what\'s in the box?" scene', 'the opening credits', 'John Doe\'s confession'],
        'highlights': ['the rain-soaked atmosphere', 'Kevin Spacey\'s menace', 'the bleak ending'],
    },
    'the-silence-of-the-lambs': {
        'director': 'Jonathan Demme', 'characters': ['Clarice Starling', 'Hannibal Lecter', 'Buffalo Bill'],
        'themes': ['predator and prey', 'identity and transformation', 'the female gaze'],
        'scenes': ['the first Lecter meeting', 'the night vision chase', 'Lecter\'s escape'],
        'highlights': ['Anthony Hopkins in limited screen time', 'Jodie Foster\'s conviction', 'the tense atmosphere'],
    },
    'interstellar': {
        'director': 'Christopher Nolan', 'characters': ['Cooper', 'Murph', 'Brand', 'TARS'],
        'themes': ['love transcending time', 'sacrifice for humanity', 'relativity and time'],
        'scenes': ['the water planet sequence', 'the docking scene', 'the tesseract'],
        'highlights': ['Hans Zimmer\'s organ-driven score', 'the practical space visuals', 'the emotional father-daughter core'],
    },
    'saving-private-ryan': {
        'director': 'Steven Spielberg', 'characters': ['Captain Miller', 'Private Ryan', 'Sergeant Horvath'],
        'themes': ['the cost of war', 'duty and sacrifice', 'the value of a single life'],
        'scenes': ['the D-Day opening', 'the tower sniper sequence', 'the final bridge battle'],
        'highlights': ['the immersive handheld camera work', 'Tom Hanks\'s restrained performance', 'Janusz Kaminski\'s desaturated photography'],
    },
    'the-usual-suspects': {
        'director': 'Bryan Singer', 'characters': ['Verbal Kint', 'Keyser Soze', 'Keaton'],
        'themes': ['identity and deception', 'legend and myth', 'the unreliable narrator'],
        'scenes': ['the lineup scene', 'the Keyser Soze reveal', 'the coffee cup moment'],
        'highlights': ['Kevin Spacey\'s Oscar-winning performance', 'the rewatch value of the twist', 'the intricate plotting'],
    },
    'american-history-x': {
        'director': 'Tony Kaye', 'characters': ['Derek Vinyard', 'Danny Vinyard', 'Dr. Sweeney'],
        'themes': ['racism and redemption', 'cycles of hatred', 'education and change'],
        'scenes': ['the curb scene', 'the prison shower scene', 'the basketball game'],
        'highlights': ['Edward Norton\'s transformative performance', 'the black-and-white flashback structure', 'the devastating ending'],
    },
    'parasite': {
        'director': 'Bong Joon-ho', 'characters': ['Ki-woo Kim', 'Ki-taek Kim', 'Nathan Park'],
        'themes': ['class inequality', 'the parasitic nature of wealth', 'the smell of poverty'],
        'scenes': ['the peach allergy reveal', 'the flooding basement', 'the garden party massacre'],
        'highlights': ['the genre-shifting structure', 'Bong\'s precise social commentary', 'the production design'],
    },
    'the-lion-king': {
        'director': 'Roger Allers and Rob Minkoff', 'characters': ['Simba', 'Mufasa', 'Scar', 'Timon and Pumbaa'],
        'themes': ['responsibility', 'grief and guilt', 'the circle of life'],
        'scenes': ['the stampede', 'Mufasa\'s death', 'Simba\'s return'],
        'highlights': ['Hans Zimmer\'s score', 'Jeremy Irons as Scar', 'the emotional depth for an animated film'],
    },
    'terminator-2': {
        'director': 'James Cameron', 'characters': ['Sarah Connor', 'John Connor', 'T-800', 'T-1000'],
        'themes': ['fate vs free will', 'the nature of humanity', 'sacrifice'],
        'scenes': ['the mall chase', 'the thumbs-up descent into steel', 'the steel mill finale'],
        'highlights': ['groundbreaking CGI for its time', 'Linda Hamilton\'s physical transformation', 'the emotional reversal of the T-800'],
    },
    'gladiator': {
        'director': 'Ridley Scott', 'characters': ['Maximus', 'Commodus', 'Lucilla'],
        'themes': ['revenge and justice', 'honour and loyalty', 'the corruption of power'],
        'scenes': ['the opening battle in Germania', 'the Colosseum entrance', 'the father and son reunion ending'],
        'highlights': ['Russell Crowe\'s presence', 'Hans Zimmer and Lisa Gerrard\'s score', 'the arena spectacle'],
    },
    'whiplash': {
        'director': 'Damien Chazelle', 'characters': ['Andrew Neiman', 'Terence Fletcher'],
        'themes': ['obsession and ambition', 'the cost of greatness', 'abuse disguised as mentorship'],
        'scenes': ['the drum practice in blood', 'the finale at Carnegie Hall', 'the car accident'],
        'highlights': ['J.K. Simmons\'s terrifying Fletcher', 'Miles Teller\'s physicality', 'the jazz drumming as tension'],
    },
    'the-prestige': {
        'director': 'Christopher Nolan', 'characters': ['Robert Angier', 'Alfred Borden', 'Nikola Tesla'],
        'themes': ['obsession and sacrifice', 'the nature of illusion', 'what we sacrifice for our art'],
        'scenes': ['the opening monologue about the trick', 'Tesla\'s machine reveal', 'the final warehouse twist'],
        'highlights': ['the double twist ending', 'Bale and Jackman\'s rivalry', 'the Victorian atmosphere'],
    },
    'memento': {
        'director': 'Christopher Nolan', 'characters': ['Leonard Shelby', 'Natalie', 'Teddy'],
        'themes': ['memory and identity', 'self-deception', 'the unreliable mind'],
        'scenes': ['the reversed opening', 'the tattoo revelation', 'the Polaroid clue trail'],
        'highlights': ['the reverse chronology structure', 'Guy Pearce\'s committed performance', 'the philosophical depth about memory'],
    },
    'the-departed': {
        'director': 'Martin Scorsese', 'characters': ['Billy Costigan', 'Colin Sullivan', 'Frank Costello'],
        'themes': ['identity and loyalty', 'the cost of deception', 'institutional corruption'],
        'scenes': ['the elevator finale', 'the rat imagery', 'Jack Nicholson\'s restaurant scene'],
        'highlights': ['the all-star ensemble', 'the mirrored spy plot', 'the unpredictable violence'],
    },
    'django-unchained': {
        'director': 'Quentin Tarantino', 'characters': ['Django Freeman', 'Dr. King Schultz', 'Calvin Candie'],
        'themes': ['slavery and freedom', 'revenge', 'the mythology of the Western'],
        'scenes': ['the Candyland dinner scene', 'the final shootout', 'the Mandingo fight'],
        'highlights': ['Christoph Waltz\'s charm', 'Jamie Foxx\'s quiet intensity', 'DiCaprio as a villain'],
    },
    'wall-e': {
        'director': 'Andrew Stanton', 'characters': ['WALL-E', 'EVE', 'Auto'],
        'themes': ['environmental destruction', 'loneliness and love', 'humanity\'s dependency on technology'],
        'scenes': ['WALL-E\'s video collection', 'the space dance', 'the plant reveal'],
        'highlights': ['the nearly wordless first act', 'Thomas Newman\'s score', 'the visual world-building'],
    },
    'toy-story': {
        'director': 'John Lasseter', 'characters': ['Woody', 'Buzz Lightyear', 'Sid'],
        'themes': ['jealousy and friendship', 'identity and purpose', 'growing up'],
        'scenes': ['Buzz\'s first flight attempt', 'the gas station escape', 'the Sid nightmare'],
        'highlights': ['the groundbreaking CGI', 'Tom Hanks and Tim Allen\'s voice chemistry', 'the emotional resonance'],
    },
    'no-country-for-old-men': {
        'director': 'Joel and Ethan Coen', 'characters': ['Anton Chigurh', 'Llewelyn Moss', 'Sheriff Bell'],
        'themes': ['fate and mortality', 'evil that cannot be reasoned with', 'the changing West'],
        'scenes': ['the gas station coin toss', 'the hotel room standoff', 'the non-ending ending'],
        'highlights': ['Javier Bardem\'s terrifying Chigurh', 'Roger Deakins\'s cinematography', 'the refusal to deliver catharsis'],
    },
    'alien': {
        'director': 'Ridley Scott', 'characters': ['Ripley', 'Ash', 'Dallas'],
        'themes': ['corporate indifference to human life', 'survival', 'the body as a site of horror'],
        'scenes': ['the chestburster scene', 'the airlock finale', 'Dallas in the ventilation shaft'],
        'highlights': ['H.R. Giger\'s creature design', 'the slow-burn tension', 'Sigourney Weaver\'s iconic hero'],
    },
    'apocalypse-now': {
        'director': 'Francis Ford Coppola', 'characters': ['Captain Willard', 'Colonel Kurtz', 'Lieutenant Kilgore'],
        'themes': ['the madness of war', 'the darkness within civilisation', 'imperialism'],
        'scenes': ['the helicopter attack to Wagner', 'the surfing scene', 'Kurtz\'s compound'],
        'highlights': ['Marlon Brando\'s enigmatic Kurtz', 'the immersive sound design', 'the visceral chaos of battle'],
    },
    'the-shining': {
        'director': 'Stanley Kubrick', 'characters': ['Jack Torrance', 'Wendy Torrance', 'Danny Torrance'],
        'themes': ['domestic violence', 'isolation and madness', 'the supernatural'],
        'scenes': ['the elevator blood flood', 'Room 237', 'the hedge maze chase'],
        'highlights': ['Kubrick\'s wide-angle dread', 'Jack Nicholson\'s unhinged performance', 'the unresolved ambiguity'],
    },
    'braveheart': {
        'director': 'Mel Gibson', 'characters': ['William Wallace', 'Robert the Bruce', 'Princess Isabelle'],
        'themes': ['freedom and sacrifice', 'nationalism', 'betrayal'],
        'scenes': ['the Battle of Stirling Bridge', 'the final execution', 'the battle cry'],
        'highlights': ['the epic battle choreography', 'James Horner\'s sweeping score', 'Mel Gibson\'s directorial scope'],
    },
    'full-metal-jacket': {
        'director': 'Stanley Kubrick', 'characters': ['Private Joker', 'Gunnery Sergeant Hartman', 'Private Pyle'],
        'themes': ['the dehumanisation of soldiers', 'the split nature of man', 'Vietnam\'s moral bankruptcy'],
        'scenes': ['the boot camp opening tirade', 'Pyle\'s breakdown', 'the sniper in the ruins'],
        'highlights': ['R. Lee Ermey\'s improvised insults', 'the tonal shift between halves', 'the unsettling finale'],
    },
    '2001-a-space-odyssey': {
        'director': 'Stanley Kubrick', 'characters': ['Dave Bowman', 'HAL 9000', 'Dr. Floyd'],
        'themes': ['human evolution', 'artificial intelligence and fear', 'the unknowable universe'],
        'scenes': ['the bone-to-spacecraft cut', '"Daisy Bell" as HAL dies', 'the Star Gate sequence'],
        'highlights': ['the visionary special effects', 'Douglas Rain\'s HAL voice', 'the philosophical ambition'],
    },
    'casablanca': {
        'director': 'Michael Curtiz', 'characters': ['Rick Blaine', 'Ilsa Lund', 'Victor Laszlo', 'Captain Renault'],
        'themes': ['love and sacrifice', 'cynicism redeemed by honour', 'the fight against fascism'],
        'scenes': ['the "Play it, Sam" scene', 'the airport goodbye', 'the Marseillaise scene'],
        'highlights': ['Bogart and Bergman\'s chemistry', 'the quotable dialogue', 'the wartime moral urgency'],
    },
    'psycho': {
        'director': 'Alfred Hitchcock', 'characters': ['Norman Bates', 'Marion Crane', 'Lila Crane'],
        'themes': ['duality and repression', 'voyeurism', 'the nature of evil'],
        'scenes': ['the shower scene', 'Norman\'s final monologue', 'the taxidermy reveal'],
        'highlights': ['Bernard Herrmann\'s strings', 'Anthony Perkins\'s quiet menace', 'the audacity of killing the lead early'],
    },
    'rear-window': {
        'director': 'Alfred Hitchcock', 'characters': ['L.B. Jefferies', 'Lisa Fremont', 'Lars Thorwald'],
        'themes': ['voyeurism and complicity', 'marriage and isolation', 'the act of watching'],
        'scenes': ['Miss Lonelyhearts at dinner', 'the dog murder', 'Thorwald\'s confrontation'],
        'highlights': ['the single-set formal constraint', 'Grace Kelly\'s elegance', 'the film\'s meditation on cinema itself'],
    },
    'blade-runner': {
        'director': 'Ridley Scott', 'characters': ['Rick Deckard', 'Roy Batty', 'Rachael'],
        'themes': ['what makes us human', 'mortality and memory', 'corporate dystopia'],
        'scenes': ['Roy\'s "tears in rain" monologue', 'the eye-opener opening', 'the dove release'],
        'highlights': ['Vangelis\'s synth score', 'the noir atmosphere in a sci-fi setting', 'Rutger Hauer\'s haunting villain'],
    },
    'eternal-sunshine': {
        'director': 'Michel Gondry', 'characters': ['Joel Barish', 'Clementine Kruczynski', 'Dr. Mierzwiak'],
        'themes': ['love and memory', 'the pain we choose to keep', 'imperfect relationships'],
        'scenes': ['the memory erasure sequence', 'hiding Clementine in childhood memories', 'the beach house ending'],
        'highlights': ['Jim Carrey\'s quiet vulnerability', 'Jon Brion\'s score', 'the inventive non-linear structure'],
    },
    'reservoir-dogs': {
        'director': 'Quentin Tarantino', 'characters': ['Mr. White', 'Mr. Orange', 'Mr. Blonde', 'Joe Cabot'],
        'themes': ['loyalty and betrayal', 'professionalism among criminals', 'the aftermath of violence'],
        'scenes': ['the ear torture scene', 'the opening diner conversation', 'the Mexican standoff'],
        'highlights': ['the debut confidence', 'Steve Buscemi\'s Mr. Pink', 'the non-linear reveal structure'],
    },
    'there-will-be-blood': {
        'director': 'Paul Thomas Anderson', 'characters': ['Daniel Plainview', 'Eli Sunday', 'H.W. Plainview'],
        'themes': ['capitalism and greed', 'religion as power', 'the American hunger'],
        'scenes': ['the oil derrick fire', 'the I drink your milkshake scene', 'the bowling alley finale'],
        'highlights': ['Daniel Day-Lewis\'s volcanic performance', 'Jonny Greenwood\'s discordant score', 'the epic sweep'],
    },
    'oldboy': {
        'director': 'Park Chan-wook', 'characters': ['Oh Dae-su', 'Lee Woo-jin', 'Mi-do'],
        'themes': ['revenge and its futility', 'imprisonment', 'the horror of truth'],
        'scenes': ['the corridor fight', 'the octopus eating', 'the reveal at the hypnotherapist'],
        'highlights': ['the one-take hallway fight', 'the narrative ruthlessness', 'Choi Min-sik\'s physical commitment'],
    },
    'amelie': {
        'director': 'Jean-Pierre Jeunet', 'characters': ['Amelie Poulain', 'Nino Quincampoix', 'Raymond Dufayel'],
        'themes': ['finding joy in small things', 'loneliness and connection', 'the magic of observation'],
        'scenes': ['the crème brûlée moment', 'the gnome photographs', 'the photo booth mystery'],
        'highlights': ['Audrey Tautou\'s infectious charm', 'Bruno Delbonnel\'s warm cinematography', 'Yann Tiersen\'s score'],
    },
    'heat': {
        'director': 'Michael Mann', 'characters': ['Neil McCauley', 'Vincent Hanna', 'Chris Shiherlis'],
        'themes': ['obsession and professionalism', 'crime as mirror of law', 'isolation as strength'],
        'scenes': ['the diner meeting between De Niro and Pacino', 'the downtown LA bank heist shootout', 'the airport finale'],
        'highlights': ['the first on-screen pairing of Pacino and De Niro', 'the realistic tactical gunfight', 'Mann\'s cold night aesthetic'],
    },
    'taxi-driver': {
        'director': 'Martin Scorsese', 'characters': ['Travis Bickle', 'Iris', 'Betsy'],
        'themes': ['urban alienation', 'masculine violence as salvation', 'vigilantism'],
        'scenes': ['the "You talkin\' to me?" mirror scene', 'the rescue massacre', 'the overhead shot aftermath'],
        'highlights': ['Robert De Niro\'s complete immersion', 'Bernard Herrmann\'s final score', 'Scorsese\'s nighttime New York'],
    },
    'pans-labyrinth': {
        'director': 'Guillermo del Toro', 'characters': ['Ofelia', 'Captain Vidal', 'The Faun', 'Mercedes'],
        'themes': ['fantasy as escape from fascism', 'childhood innocence vs adult brutality', 'disobedience and courage'],
        'scenes': ['the Pale Man banquet', 'the chalk door escape', 'the final choice'],
        'highlights': ['Doug Jones\'s creature performance', 'del Toro\'s practical creature design', 'the bittersweet ending'],
    },
    'the-truman-show': {
        'director': 'Peter Weir', 'characters': ['Truman Burbank', 'Christof', 'Sylvia'],
        'themes': ['the simulated reality', 'surveillance and control', 'authentic vs manufactured life'],
        'scenes': ['Truman\'s first confrontation with the set', 'the boat storm', 'the exit door'],
        'highlights': ['Jim Carrey\'s dramatic range', 'Ed Harris as the manipulative creator', 'the prescient satire of reality TV'],
    },
    'die-hard': {
        'director': 'John McTiernan', 'characters': ['John McClane', 'Hans Gruber', 'Sergeant Powell'],
        'themes': ['the reluctant everyman hero', 'Christmas in a hostile world', 'wits vs force'],
        'scenes': ['the ventilation shaft crawl', 'the barefoot glass walk', 'the rooftop explosion'],
        'highlights': ['Alan Rickman\'s suave villain', 'Bruce Willis\'s vulnerability', 'the tight building-set pacing'],
    },
    'spirited-away': {
        'director': 'Hayao Miyazaki', 'characters': ['Chihiro', 'Haku', 'Yubaba', 'No-Face'],
        'themes': ['growing up and responsibility', 'greed and transformation', 'the spirit world'],
        'scenes': ['the train over water', 'No-Face\'s rampage', 'the parents turned into pigs'],
        'highlights': ['Miyazaki\'s imagination', 'the hand-drawn animation', 'the emotional depth for all ages'],
    },
    'city-of-god': {
        'director': 'Fernando Meirelles and Katia Lund', 'characters': ['Rocket', 'Li\'l Ze', 'Benny'],
        'themes': ['cycles of violence', 'poverty and crime', 'the observer vs participant'],
        'scenes': ['the opening chicken chase', 'the apartment children\'s shoot', 'the final war'],
        'highlights': ['the kinetic handheld direction', 'the non-professional cast', 'the humanity within the brutality'],
    },
    'life-is-beautiful': {
        'director': 'Roberto Benigni', 'characters': ['Guido Orefice', 'Joshua', 'Dora'],
        'themes': ['love as protection', 'imagination vs reality', 'parental sacrifice'],
        'scenes': ['the game rules speech in the barracks', 'the loudspeaker serenade', 'the morning after'],
        'highlights': ['Benigni\'s simultaneous comedy and tragedy', 'Nicola Piovani\'s music', 'the child\'s perspective'],
    },
    'a-beautiful-mind': {
        'director': 'Ron Howard', 'characters': ['John Nash', 'Alicia Nash', 'Charles'],
        'themes': ['genius and mental illness', 'love as anchor to reality', 'the gift and burden of an exceptional mind'],
        'scenes': ['the revelation of the hallucinations', 'the pen ceremony', 'Nash\'s Nobel Prize speech'],
        'highlights': ['Russell Crowe\'s internal performance', 'the twist on the audience\'s perception', 'Jennifer Connelly\'s support'],
    },
    'back-to-the-future': {
        'director': 'Robert Zemeckis', 'characters': ['Marty McFly', 'Doc Brown', 'Biff Tannen'],
        'themes': ['family and identity', 'the consequences of change', 'the friendship between generations'],
        'scenes': ['the clocktower lightning sequence', 'the first DeLorean drive', 'the Johnny B. Goode performance'],
        'highlights': ['Michael J. Fox\'s boundless energy', 'Christopher Lloyd\'s eccentricity', 'Alan Silvestri\'s theme'],
    },
    'the-pianist': {
        'director': 'Roman Polanski', 'characters': ['Wladyslaw Szpilman', 'Captain Wilm Hosenfeld'],
        'themes': ['survival and human dignity', 'art as resistance', 'the Holocaust'],
        'scenes': ['the German officer hearing the piano', 'the ghetto uprising', 'the roof hiding'],
        'highlights': ['Adrien Brody\'s physical transformation', 'the restrained direction', 'the real survival story'],
    },
    'avengers-infinity-war': {
        'director': 'Anthony and Joe Russo', 'characters': ['Thanos', 'Iron Man', 'Thor', 'Spider-Man'],
        'themes': ['the weight of sacrifice', 'utilitarian morality', 'the villain with a mission'],
        'scenes': ['the snap', 'Titan battle', 'Thor\'s arrival in Wakanda'],
        'highlights': ['Josh Brolin\'s Thanos as a rounded antagonist', 'the sheer scale of characters', 'the gutpunch ending'],
    },
    'mad-max-fury-road': {
        'director': 'George Miller', 'characters': ['Max Rockatansky', 'Furiosa', 'Immortan Joe'],
        'themes': ['female liberation', 'the resource wars of the future', 'hope in a wasteland'],
        'scenes': ['the flamethrower guitar chase', 'the wives\' introduction', 'the canyon crash'],
        'highlights': ['Charlize Theron\'s Furiosa', 'the practical stunt work', 'the relentless kinetic energy'],
    },
    'the-grand-budapest-hotel': {
        'director': 'Wes Anderson', 'characters': ['M. Gustave H.', 'Zero Moustafa', 'Madame D.'],
        'themes': ['nostalgia and loss', 'the old Europe', 'loyalty between mentor and student'],
        'scenes': ['the ski chase', 'the prison break', 'the lobby confession'],
        'highlights': ['Ralph Fiennes\'s comedic precision', 'the symmetrical visual style', 'Alexandre Desplat\'s score'],
    },
    'la-la-land': {
        'director': 'Damien Chazelle', 'characters': ['Mia', 'Sebastian', 'Keith'],
        'themes': ['dreams vs love', 'the cost of ambition', 'nostalgia for classic Hollywood'],
        'scenes': ['the Griffith Observatory dance', 'the epilogue what-if sequence', 'the opening highway number'],
        'highlights': ['Ryan Gosling and Emma Stone\'s chemistry', 'Linus Sandgren\'s widescreen photography', 'Justin Hurwitz\'s score'],
    },
    'get-out': {
        'director': 'Jordan Peele', 'characters': ['Chris Washington', 'Rose Armitage', 'Rod Williams'],
        'themes': ['racism disguised as liberalism', 'the sunken place as Black erasure', 'the horror of assimilation'],
        'scenes': ['the hypnotherapy scene', 'the Bingo party', 'the tea cup'],
        'highlights': ['Daniel Kaluuya\'s expressive eyes', 'the precise social commentary', 'the tonal balance of comedy and dread'],
    },
    '1917': {
        'director': 'Sam Mendes', 'characters': ['Schofield', 'Blake', 'General Erinmore'],
        'themes': ['sacrifice and duty', 'the impossible mission', 'survival under fire'],
        'scenes': ['the ruined town at night', 'crossing no man\'s land', 'the river sequence'],
        'highlights': ['Roger Deakins\'s single-take illusion', 'the real-time tension', 'the emotional stakes of the letter'],
    },
    'dunkirk': {
        'director': 'Christopher Nolan', 'characters': ['Tommy', 'Farrier', 'Mr. Dawson'],
        'themes': ['survival over heroism', 'the collective over the individual', 'the fog of war'],
        'scenes': ['the Spitfire gliding silent', 'the mole under fire', 'the burning sea'],
        'highlights': ['Hans Zimmer\'s ticking score', 'the three interwoven timelines', 'the immersive sound design'],
    },
    'arrival': {
        'director': 'Denis Villeneuve', 'characters': ['Louise Banks', 'Ian Donnelly', 'Colonel Weber'],
        'themes': ['language shapes perception', 'grief and time', 'the cost of knowing the future'],
        'scenes': ['first contact in the shell', 'the non-linear memory reveal', 'the heptapod communication'],
        'highlights': ['Amy Adams\'s understated brilliance', 'Jóhann Jóhannsson\'s alien score', 'the emotional science fiction'],
    },
    'the-social-network': {
        'director': 'David Fincher', 'characters': ['Mark Zuckerberg', 'Eduardo Saverin', 'Sean Parker'],
        'themes': ['ambition and betrayal', 'the loneliness of success', 'ownership in the digital age'],
        'scenes': ['the opening breakup', 'the deposition cross-cuts', 'the final reload of the friend request'],
        'highlights': ['Aaron Sorkin\'s lightning dialogue', 'Jesse Eisenberg\'s contemptible charisma', 'Trent Reznor\'s score'],
    },
    'black-swan': {
        'director': 'Darren Aronofsky', 'characters': ['Nina Sayers', 'Thomas Leroy', 'Lily'],
        'themes': ['perfectionism and self-destruction', 'the dual nature of art', 'psychological disintegration'],
        'scenes': ['the mirror doppelganger', 'the transformation into the black swan', 'the final performance'],
        'highlights': ['Natalie Portman\'s physically demanding performance', 'the blurring of reality and fantasy', 'the ballet world detail'],
    },
    'inside-out': {
        'director': 'Pete Docter', 'characters': ['Joy', 'Sadness', 'Bing Bong', 'Riley'],
        'themes': ['the necessity of sadness', 'growing up and loss', 'emotional complexity'],
        'scenes': ['Bing Bong\'s sacrifice', 'the core memories shattering', 'Joy finally understanding Sadness'],
        'highlights': ['the conceptual originality', 'the emotional intelligence for children and adults', 'Michael Giacchino\'s score'],
    },
    'leon-the-professional': {
        'director': 'Luc Besson', 'characters': ['Leon', 'Mathilda', 'Norman Stansfield'],
        'themes': ['found family', 'the assassin with a soul', 'innocence in a violent world'],
        'scenes': ['the apartment siege finale', 'the milk-drinking hitman', 'the rooftop training'],
        'highlights': ['Jean Reno\'s gentle giant', 'Gary Oldman\'s deranged villain', 'the unlikely bond at the film\'s core'],
    },
    'requiem-for-a-dream': {
        'director': 'Darren Aronofsky', 'characters': ['Sara Goldfarb', 'Harry Goldfarb', 'Marion Silver'],
        'themes': ['addiction and the American Dream', 'loneliness and longing', 'the destruction of the self'],
        'scenes': ['the split-screen drug montage', 'Sara\'s refrigerator hallucination', 'the four-way ending'],
        'highlights': ['Ellen Burstyn\'s devastatingly truthful performance', 'Clint Mansell\'s score', 'the formal assault on the viewer'],
    },
    'monty-python-holy-grail': {
        'director': 'Terry Gilliam and Terry Jones', 'characters': ['King Arthur', 'Sir Lancelot', 'The Black Knight'],
        'themes': ['the absurdity of authority', 'the British class system', 'anti-war satire'],
        'scenes': ['the Black Knight fight', 'the swallow debate', 'the Trojan Rabbit'],
        'highlights': ['the anarchic improvised energy', 'the timeless quotability', 'the low budget used as a joke'],
    },
    'into-the-wild': {
        'director': 'Sean Penn', 'characters': ['Christopher McCandless', 'Ron Franz', 'Jan Burres'],
        'themes': ['the romance and danger of solitude', 'rejection of materialism', 'what makes a life meaningful'],
        'scenes': ['the Magic Bus arrival', 'the final pages of the journal', 'the wheat field'],
        'highlights': ['Emile Hirsch\'s physical dedication', 'Eddie Vedder\'s acoustic score', 'the breathtaking Alaska landscapes'],
    },
    'the-revenant': {
        'director': 'Alejandro G. Iñárritu', 'characters': ['Hugh Glass', 'John Fitzgerald', 'Hawk'],
        'themes': ['survival and vengeance', 'man vs wilderness', 'the destruction of indigenous peoples'],
        'scenes': ['the bear attack', 'the horse cliff jump', 'the final river confrontation'],
        'highlights': ['DiCaprio\'s punishing physical performance', 'Emmanuel Lubezki\'s natural light photography', 'the overwhelming landscape'],
    },
    'gravity': {
        'director': 'Alfonso Cuarón', 'characters': ['Ryan Stone', 'Matt Kowalski'],
        'themes': ['rebirth and survival', 'isolation in the void', 'letting go of grief'],
        'scenes': ['the opening 13-minute single shot', 'the ISS fire', 'the return to Earth'],
        'highlights': ['the immersive sound design', 'Sandra Bullock\'s physical performance', 'the technical filmmaking achievement'],
    },
    'her': {
        'director': 'Spike Jonze', 'characters': ['Theodore Twombly', 'Samantha', 'Amy Adams'],
        'themes': ['intimacy in the digital age', 'love without a body', 'loneliness and connection'],
        'scenes': ['the walk through the crowds of people talking to their AIs', 'Samantha\'s goodbye', 'the rooftop ending'],
        'highlights': ['Scarlett Johansson\'s voice performance', 'the warm Pastel future aesthetic', 'Arcade Fire\'s score'],
    },
    'ex-machina': {
        'director': 'Alex Garland', 'characters': ['Caleb', 'Ava', 'Nathan'],
        'themes': ['artificial consciousness', 'manipulation and power', 'the Turing Test as theatre'],
        'scenes': ['Ava\'s drawing of Caleb', 'the power cut conversations', 'the forest ending'],
        'highlights': ['Alicia Vikander\'s uncanny performance', 'the claustrophobic single-location dread', 'the ambiguous morality'],
    },
    'a-separation': {
        'director': 'Asghar Farhadi', 'characters': ['Nader', 'Simin', 'Razieh'],
        'themes': ['moral ambiguity', 'the impossibility of truth', 'class and gender in Iran'],
        'scenes': ['the stairwell confrontation', 'the courtroom sequence', 'the final choice between parents'],
        'highlights': ['the Kafkaesque justice system', 'the ensemble\'s naturalistic performances', 'the refusal to assign blame'],
    },
    'the-green-mile': {
        'director': 'Frank Darabont', 'characters': ['Paul Edgecomb', 'John Coffey', 'Percy Wetmore'],
        'themes': ['innocence and injustice', 'the supernatural and mercy', 'guilt and memory'],
        'scenes': ['John healing Mr. Jingles', 'the execution', 'Paul\'s confession at the end'],
        'highlights': ['Michael Clarke Duncan\'s gentle giant', 'Tom Hanks\'s compassion', 'the emotional devastation of the finale'],
    },
    'catch-me-if-you-can': {
        'director': 'Steven Spielberg', 'characters': ['Frank Abagnale Jr.', 'Carl Hanratty', 'Frank Sr.'],
        'themes': ['identity and reinvention', 'the father-son longing', 'the chase as a dance'],
        'scenes': ['the Pan Am stewardess walk', 'the Christmas phone call', 'the Paris capture'],
        'highlights': ['DiCaprio\'s charm and lightness', 'Tom Hanks\'s dogged determination', 'John Williams\'s playful score'],
    },
    'american-beauty': {
        'director': 'Sam Mendes', 'characters': ['Lester Burnham', 'Carolyn Burnham', 'Ricky Fitts'],
        'themes': ['suburban emptiness', 'beauty in the mundane', 'repression and release'],
        'scenes': ['the plastic bag in the wind', 'the cheerleader fantasy', 'the final monologue'],
        'highlights': ['Kevin Spacey\'s mid-life awakening', 'Thomas Newman\'s score', 'Conrad Hall\'s saturated cinematography'],
    },
    'once-upon-a-time-in-the-west': {
        'director': 'Sergio Leone', 'characters': ['Harmonica', 'Frank', 'Cheyenne', 'Jill McBain'],
        'themes': ['the dying of the Old West', 'revenge as identity', 'the railroad bringing modernity'],
        'scenes': ['the opening three-minute standoff', 'the harmonica flashback reveal', 'the railroad gang assembly'],
        'highlights': ['Henry Fonda against type as the villain', 'Ennio Morricone\'s character-specific themes', 'the operatic scope'],
    },
    'inglourious-basterds': {
        'director': 'Quentin Tarantino', 'characters': ['Hans Landa', 'Lt. Aldo Raine', 'Shosanna'],
        'themes': ['revenge fantasy vs historical reality', 'language as power', 'cinema as propaganda'],
        'scenes': ['the basement bar standoff', 'the opening dairy farm interrogation', 'the cinema fire'],
        'highlights': ['Christoph Waltz\'s Hans Landa', 'the chapter-by-chapter structure', 'the audacity of rewriting history'],
    },
    'a-clockwork-orange': {
        'director': 'Stanley Kubrick', 'characters': ['Alex DeLarge', 'F. Alexander', 'The Minister of the Interior'],
        'themes': ['free will vs state control', 'violence and art', 'the limits of rehabilitation'],
        'scenes': ['the "Singin\' in the Rain" attack', 'the Ludovico treatment', 'the final milk bar'],
        'highlights': ['Malcolm McDowell\'s provocative performance', 'Kubrick\'s formal precision amid chaos', 'Wendy Carlos\'s electronic score'],
    },
    'coco': {
        'director': 'Lee Unkrich', 'characters': ['Miguel', 'Hector', 'Mama Imelda', 'Ernesto de la Cruz'],
        'themes': ['family and memory', 'the fear of being forgotten', 'following your passion'],
        'scenes': ['Remember Me to Mama Coco', 'the Land of the Dead reveal', 'the final family reunion'],
        'highlights': ['the visual splendour of the Land of the Dead', 'the emotional gut-punch finale', 'Michael Giacchino\'s score'],
    },
    'joker': {
        'director': 'Todd Phillips', 'characters': ['Arthur Fleck', 'Thomas Wayne', 'Sophie Dumond'],
        'themes': ['mental illness and social failure', 'the making of a monster', 'class resentment'],
        'scenes': ['the subway murder', 'the talk show confrontation', 'the dancing on the stairs'],
        'highlights': ['Joaquin Phoenix\'s total physical transformation', 'the ambiguous unreliable narrator', 'Hildur Guðnadóttir\'s score'],
    },
    'knives-out': {
        'director': 'Rian Johnson', 'characters': ['Benoit Blanc', 'Marta Cabrera', 'Harlan Thrombey'],
        'highlights': ['Daniel Craig\'s delightful Southern detective', 'the subverted whodunnit structure', 'the ensemble Thrombey family'],
        'themes': ['immigration and inheritance', 'the entitled elite', 'truth and lies'],
        'scenes': ['the will reading', 'Marta\'s vomiting lie detector', 'Blanc\'s donut metaphor'],
    },
    'spider-man-into-the-spider-verse': {
        'director': 'Bob Persichetti, Peter Ramsey, Rodney Rothman', 'characters': ['Miles Morales', 'Peter B. Parker', 'Gwen Stacy'],
        'themes': ['anyone can be a hero', 'legacy and identity', 'grief and responsibility'],
        'scenes': ['the leap of faith', 'the falling upward sequence', 'the first web swing'],
        'highlights': ['the revolutionary comic-book animation style', 'the hip-hop score by Daniel Pemberton', 'Miles Morales as the definitive Spider-Man'],
    },
    'the-wolf-of-wall-street': {
        'director': 'Martin Scorsese', 'characters': ['Jordan Belfort', 'Donnie Azoff', 'Agent Denham'],
        'themes': ['greed without limits', 'the seduction of excess', 'complicity of the viewer'],
        'scenes': ['the Lemmon-Quaalude car scene', 'the chest-beating speech', 'the Stratton Oakmont sales floor'],
        'highlights': ['DiCaprio\'s most explosive performance', 'the three-hour comedy of excess', 'Scorsese\'s non-judgmental lens'],
    },
    'lawrence-of-arabia': {
        'director': 'David Lean', 'characters': ['T.E. Lawrence', 'Sherif Ali', 'Prince Feisal'],
        'themes': ['the colonial project', 'self-mythology', 'identity and belonging'],
        'scenes': ['the desert horizon appearance of Omar Sharif', 'the Aqaba charge', 'the match cut candle-to-sunrise'],
        'highlights': ['Peter O\'Toole\'s magnetic presence', 'Freddie Young\'s 70mm desert cinematography', 'Maurice Jarre\'s score'],
    },
    'dr-strangelove': {
        'director': 'Stanley Kubrick', 'characters': ['General Ripper', 'President Muffley', 'Dr. Strangelove', 'Major Kong'],
        'themes': ['the absurdity of nuclear deterrence', 'military madness', 'the failure of institutions'],
        'scenes': ['Strangelove\'s arm', 'riding the bomb', 'the War Room negotiation'],
        'highlights': ['Peter Sellers in three roles', 'Kubrick\'s black comedy precision', 'the satirical target that never ages'],
    },
    'mulholland-drive': {
        'director': 'David Lynch', 'characters': ['Betty / Diane', 'Rita / Camilla', 'Adam Kesher'],
        'themes': ['the dark side of Hollywood dreams', 'identity and illusion', 'guilt and desire'],
        'scenes': ['the Club Silencio scene', 'the diner Winkie\'s monster', 'the blue box opening'],
        'highlights': ['Naomi Watts\'s layered dual performance', 'Angelo Badalamenti\'s score', 'the hypnotic dreamlike structure'],
    },
    'its-a-wonderful-life': {
        'director': 'Frank Capra', 'characters': ['George Bailey', 'Clarence', 'Mary', 'Potter'],
        'themes': ['the value of an ordinary life', 'community over ambition', 'gratitude'],
        'scenes': ['the alternate Bedford Falls', 'the bridge jump', 'the Christmas ending'],
        'highlights': ['James Stewart\'s emotional depth', 'the warmth of Frank Capra\'s vision', 'the enduring resonance at Christmas'],
    },
    'the-sixth-sense': {
        'director': 'M. Night Shyamalan', 'characters': ['Cole Sear', 'Malcolm Crowe', 'Lynn Sear'],
        'themes': ['the inability to let go', 'childhood isolation', 'communication across the divide'],
        'scenes': ['the tent scene with ghosts', 'the "I see dead people" reveal', 'the wedding video clue'],
        'highlights': ['Haley Joel Osment\'s fearless child performance', 'the rewatch-rewiring twist', 'Bruce Willis\'s understated sadness'],
    },
    'good-will-hunting': {
        'director': 'Gus Van Sant', 'characters': ['Will Hunting', 'Sean Maguire', 'Chuckie Sullivan', 'Skylar'],
        'themes': ['the fear of being seen', 'working-class genius', 'healing through vulnerability'],
        'scenes': ['the park bench "It\'s not your fault" scene', 'the math problem solution', 'the final gone-to-see-about-a-girl'],
        'highlights': ['Robin Williams and Matt Damon\'s chemistry', 'the Damon-Affleck screenplay', 'Elliott Smith\'s soundtrack'],
    },
    'the-big-lebowski': {
        'director': 'Joel and Ethan Coen', 'characters': ['The Dude', 'Walter Sobchak', 'Maude Lebowski', 'Donny'],
        'themes': ['the slacker as hero', 'the absurdity of Los Angeles', 'bowling as philosophy'],
        'scenes': ['the dream sequence', 'Walter scattering Donny\'s ashes', 'the opener in the grocery store'],
        'highlights': ['Jeff Bridges\'s iconic laziness', 'the bowling dream sequences', 'the cult following the film earned'],
    },
}


# ---------------------------------------------------------------------------
# Review templates
# ---------------------------------------------------------------------------
REVIEW_TEMPLATES = [
    {
        'title': 'One of the greatest films ever made',
        'body': "I've seen {name} multiple times now and it just keeps getting better. {highlight} is something rarely matched in cinema. If you haven't watched it yet, clear your evening.",
        'rating': 5,
    },
    {
        'title': 'The ending absolutely floored me',
        'body': "{name} builds so carefully to its conclusion that when it arrives you feel genuinely moved. The {theme} thread pays off in a way that's earned rather than manipulative. Couldn't sleep afterward.",
        'rating': 5,
    },
    {
        'title': 'Changed how I think about {theme}',
        'body': "I didn't expect {name} to affect me so deeply. The way {director} handles {theme} is unlike anything I'd seen before. I came out of it looking at the world differently.",
        'rating': 5,
    },
    {
        'title': 'The {scene} is cinematic perfection',
        'body': "There are scenes in cinema you never forget. For me, {scene} in {name} is one of them. {director} constructs it with total precision and it lands exactly as intended. Pure craft.",
        'rating': 5,
    },
    {
        'title': 'Better on second watch',
        'body': "I liked {name} when I first saw it, but the second viewing is where it clicked. Once you notice how {director} plants every detail early on, the whole film transforms. Layers everywhere.",
        'rating': 5,
    },
    {
        'title': "Can't believe I waited this long to watch it",
        'body': "Everyone told me to watch {name} for years. Finally did and instantly understood why. {highlight} is immediately apparent. Now I'm recommending it just as loudly to everyone else.",
        'rating': 5,
    },
    {
        'title': 'The score elevates every scene',
        'body': "The music in {name} is so deeply married to the images that you almost can't separate them. It stays in your head days later and when you hear it again the emotions return immediately.",
        'rating': 5,
    },
    {
        'title': 'A career-best performance',
        'body': "Every actor brings something to {name}, but the lead performance is genuinely extraordinary. The subtlety involved, the way the character changes without announcing it — it's a masterclass.",
        'rating': 5,
    },
    {
        'title': 'Hard to watch but impossible to look away',
        'body': "{name} deals with {theme} in a way that's genuinely uncomfortable at times. But that discomfort is the point. {director} never lets you look away, and the film is better for it.",
        'rating': 4,
    },
    {
        'title': 'The {theme} theme resonates more as you get older',
        'body': "I first watched {name} as a teenager and thought it was fine. Rewatched at 30 and it hit completely differently. The {theme} undercurrent makes total sense now in a way it didn't before.",
        'rating': 5,
    },
    {
        'title': 'Overrated but still very good',
        'body': "{name} has been praised so heavily that no film could live up to the hype completely. It's an excellent film — {highlight} is genuinely remarkable — but it's not the untouchable masterpiece some claim.",
        'rating': 4,
    },
    {
        'title': 'Watched with my family — sparked an incredible conversation',
        'body': "We watched {name} together and spent an hour talking about {theme} afterward. That kind of conversation doesn't happen often. The film gives you something real to think about together.",
        'rating': 5,
    },
    {
        'title': 'Not my genre but it completely won me over',
        'body': "I usually avoid this kind of film but gave {name} a chance after constant recommendations. Completely converted. {director} transcends genre entirely. It works as pure human drama first and everything else second.",
        'rating': 5,
    },
    {
        'title': 'The craft behind this film is astonishing',
        'body': "Every choice in {name} feels deliberate. The framing, the pacing, {scene} — {director} is operating at a level most filmmakers never reach. It's the kind of film you study rather than just watch.",
        'rating': 5,
    },
    {
        'title': 'Stayed with me for weeks',
        'body': "{name} ended and I sat with it for weeks. The {theme} theme kept circling back. I'd be doing something mundane and {scene} would pop into my head. That kind of resonance is rare.",
        'rating': 5,
    },
    {
        'title': 'The ending is divisive for a reason',
        'body': "{name} commits to a conclusion that not everyone will appreciate. I found it perfectly right — it refuses easy comfort. If you want tidy resolution you may be frustrated. If you want truth, it delivers.",
        'rating': 4,
    },
    {
        'title': 'A film that demands your full attention',
        'body': "{name} is not background viewing. Every scene requires you. Put your phone down, dim the lights. {director} is doing too much to be half-watched. Give it the attention it deserves.",
        'rating': 5,
    },
    {
        'title': 'Dated in some ways but still powerful',
        'body': "Some elements of {name} show their age, but the core of it — {theme}, {highlight} — hasn't diminished at all. Films this good age better than almost anything else.",
        'rating': 4,
    },
    {
        'title': 'The supporting cast deserves more credit',
        'body': "Everyone focuses on the lead in {name} but the supporting cast is extraordinary. Every scene partner brings something real. It makes the world feel fully inhabited rather than staged.",
        'rating': 5,
    },
    {
        'title': 'Disappointed given the reputation',
        'body': "{name} is technically accomplished and I understand its place in film history. But it left me cold. The {theme} element felt mechanical and I never connected emotionally. Maybe I'll try again someday.",
        'rating': 3,
    },
    {
        'title': 'The cinematography alone is worth it',
        'body': "Whatever you think of the story, {name} is one of the most visually extraordinary films ever shot. There are frames here that belong in a gallery. Worth seeing on the biggest screen possible.",
        'rating': 5,
    },
    {
        'title': "Watched it blind and was blown away",
        'body': "I went into {name} knowing nothing — no trailer, no plot summary. I strongly recommend that approach. The {theme} hits much harder when you haven't been primed for it. Go in cold.",
        'rating': 5,
    },
]

FIRST_NAMES = [
    'Emma', 'Liam', 'Olivia', 'Noah', 'Ava', 'Ethan', 'Sophia', 'Mason',
    'Isabella', 'James', 'Mia', 'Logan', 'Charlotte', 'Lucas', 'Amelia',
    'Jackson', 'Harper', 'Aiden', 'Evelyn', 'Sebastian', 'Abigail', 'Mateo',
    'Emily', 'Jack', 'Elizabeth', 'Owen', 'Sofia', 'Henry', 'Avery', 'Samuel',
    'Ella', 'Elijah', 'Madison', 'Daniel', 'Scarlett', 'Benjamin', 'Victoria',
    'Dylan', 'Grace', 'Michael', 'Chloe', 'Jayden', 'Penelope', 'Ryan',
    'Marcus', 'Diana', 'Derek', 'Priya', 'Kenji', 'Fatima', 'Carlos', 'Ingrid',
]


def random_author():
    return random.choice(FIRST_NAMES)


def make_review(movie_name, slug, tmpl):
    data = MOVIE_DATA.get(slug, {})
    director = data.get('director', 'the director')
    characters = data.get('characters', ['the main character'])
    themes = data.get('themes', ['identity', 'survival', 'justice'])
    scenes = data.get('scenes', ['the opening scene', 'the climax', 'the final moment'])
    highlights = data.get('highlights', ['the performances', 'the direction', 'the script'])

    title = tmpl['title'].format(
        name=movie_name, theme=random.choice(themes), scene=random.choice(scenes),
        director=director, highlight=random.choice(highlights),
    )
    body = tmpl['body'].format(
        name=movie_name, director=director,
        character=random.choice(characters),
        theme=random.choice(themes),
        scene=random.choice(scenes),
        highlight=random.choice(highlights),
    )
    return title, body, tmpl['rating']


# ---------------------------------------------------------------------------
# Wikipedia image helpers
# ---------------------------------------------------------------------------
def wiki_image(title, width=500):
    try:
        r = SESSION.get('https://en.wikipedia.org/w/api.php', params={
            'action': 'query', 'titles': title, 'prop': 'pageimages',
            'pithumbsize': width, 'format': 'json',
        }, timeout=12)
        pages = r.json()['query']['pages']
        page = next(iter(pages.values()))
        return page.get('thumbnail', {}).get('source')
    except Exception:
        return None


def download(url, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    for attempt in range(3):
        try:
            r = SESSION.get(url, timeout=20)
            if r.status_code == 200:
                with open(dest, 'wb') as f:
                    f.write(r.content)
                return True
            elif r.status_code == 429:
                print('    rate limited, sleeping 30s...')
                time.sleep(30)
        except Exception as e:
            print(f'    download error: {e}')
            time.sleep(3)
    return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    app = create_app()
    with app.app_context():
        # Category
        cat = Category.query.filter_by(slug='movies').first()
        if not cat:
            cat = Category(name='Movies', slug='movies', icon='🎬',
                           description='Reviews of the greatest films of all time.')
            db.session.add(cat)
            db.session.flush()
            print(f'Created category: {cat.name}')

            img_url = wiki_image('Film')
            if img_url:
                ext = img_url.split('.')[-1].split('?')[0].lower()
                if ext not in ('jpg', 'jpeg', 'png', 'webp', 'gif'):
                    ext = 'jpg'
                fname = f'movies-category.{ext}'
                dest = os.path.join(STATIC_DIR, 'images', 'uploads', 'categories', fname)
                if download(img_url, dest):
                    cat.image_path = f'images/uploads/categories/{fname}'
                    print('  category image saved')
            db.session.commit()
        else:
            print(f'Category exists: {cat.name}')

        # Subcategory
        sc = SubCategory.query.filter_by(category_id=cat.id, slug='top-100').first()
        if not sc:
            sc = SubCategory(category_id=cat.id, name='Top 100', slug='top-100')
            db.session.add(sc)
            db.session.commit()
            print('Created subcategory: Top 100')
        else:
            print('Subcategory exists: Top 100')

        total_subjects = 0
        total_reviews = 0

        for movie_name, movie_slug, wiki_title, year in MOVIES:
            subj = Subject.query.filter_by(subcategory_id=sc.id, slug=movie_slug).first()
            if subj:
                print(f'  Skipping {movie_name} (exists)')
                continue

            subj = Subject(subcategory_id=sc.id, name=f'{movie_name} ({year})', slug=movie_slug)
            db.session.add(subj)
            db.session.flush()

            # Image
            img_url = wiki_image(wiki_title)
            if img_url:
                ext = img_url.split('.')[-1].split('?')[0].lower()
                if ext not in ('jpg', 'jpeg', 'png', 'webp', 'gif'):
                    ext = 'jpg'
                fname = f'movies-{movie_slug}.{ext}'
                dest = os.path.join(STATIC_DIR, 'images', 'uploads', 'subjects', fname)
                if download(img_url, dest):
                    subj.image_path = f'images/uploads/subjects/{fname}'
                    print(f'  img ok: {movie_name}')
                else:
                    print(f'  no img: {movie_name}')
            else:
                print(f'  no img: {movie_name}')
            time.sleep(0.8)

            # Reviews
            from datetime import datetime, timedelta
            target = random.randint(12, 25)
            used_titles = set()
            reviews_added = 0
            shuffled = REVIEW_TEMPLATES[:]
            random.shuffle(shuffled)

            for tmpl in shuffled * 3:
                if reviews_added >= target:
                    break
                title, body, base_rating = make_review(movie_name, movie_slug, tmpl)
                if title in used_titles:
                    continue
                used_titles.add(title)
                rating = max(1, min(5, base_rating + random.choice([-1, 0, 0, 0, 1])))
                days_ago = random.randint(1, 730)
                rev = Review(
                    subject_id=subj.id,
                    title=title,
                    body=body,
                    rating=rating,
                    author_name=random_author(),
                    source_site='sample',
                    original_date=datetime.utcnow() - timedelta(days=days_ago),
                    is_published=True,
                )
                db.session.add(rev)
                reviews_added += 1

            subj.update_stats()
            total_subjects += 1
            total_reviews += reviews_added
            print(f'  {movie_name} ({year}): {reviews_added} reviews')

        db.session.commit()
        print(f'\nDone. {total_subjects} movies, {total_reviews} reviews.')


if __name__ == '__main__':
    main()
