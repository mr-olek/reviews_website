#!/usr/bin/env python3
"""Add movie subcategories: Top Shows, Top Cartoons, Top Anime, Top Marvel, Top DC."""
import os, sys, random, time, requests
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Category, SubCategory, Subject, Review

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
SESSION = requests.Session()
SESSION.headers['User-Agent'] = 'Mozilla/5.0 (compatible; VerdictlyBot/1.0)'

# ===========================================================================
# TOP SHOWS  (name, slug, wiki_article, year)
# ===========================================================================
SHOWS = [
    ('Breaking Bad',                'breaking-bad',         'Breaking Bad',                         2008),
    ('The Wire',                    'the-wire',             'The Wire',                             2002),
    ('The Sopranos',                'the-sopranos',         'The Sopranos',                         1999),
    ('Game of Thrones',             'game-of-thrones',      'Game of Thrones',                      2011),
    ('Chernobyl',                   'chernobyl-hbo',        'Chernobyl (miniseries)',               2019),
    ('Band of Brothers',            'band-of-brothers',     'Band of Brothers (miniseries)',        2001),
    ('True Detective',              'true-detective',       'True Detective',                       2014),
    ('Westworld',                   'westworld-show',       'Westworld (TV series)',                2016),
    ('The Office',                  'the-office-us',        'The Office (American TV series)',      2005),
    ('Stranger Things',             'stranger-things',      'Stranger Things',                      2016),
    ('Sherlock',                    'sherlock-bbc',         'Sherlock (TV series)',                 2010),
    ('Peaky Blinders',              'peaky-blinders',       'Peaky Blinders',                      2013),
    ('The Crown',                   'the-crown',            'The Crown (TV series)',                2016),
    ('Mindhunter',                  'mindhunter',           'Mindhunter (TV series)',               2017),
    ('Better Call Saul',            'better-call-saul',     'Better Call Saul',                    2015),
    ('Succession',                  'succession-show',      'Succession (TV series)',               2018),
    ('The Boys',                    'the-boys-tv',          'The Boys (TV series)',                 2019),
    ('Black Mirror',                'black-mirror',         'Black Mirror',                         2011),
    ('Ozark',                       'ozark',                'Ozark (TV series)',                    2017),
    ('House of Cards',              'house-of-cards-us',    'House of Cards (American TV series)', 2013),
]

SHOW_DATA = {
    'breaking-bad': {
        'creator': 'Vince Gilligan',
        'characters': ['Walter White', 'Jesse Pinkman', 'Hank Schrader', 'Skyler White'],
        'themes': ['moral decay', 'pride and ego', 'consequences of choice', 'the making of a monster'],
        'episodes': ['Ozymandias', 'Felina', 'Face Off', 'Dead Freight'],
        'highlights': ["Bryan Cranston's transformation from chemistry teacher to villain",
                       'the slow methodical build of tension across five seasons',
                       'the consistency of the writing from start to finish'],
    },
    'the-wire': {
        'creator': 'David Simon',
        'characters': ['Jimmy McNulty', 'Omar Little', 'Avon Barksdale', 'Stringer Bell'],
        'themes': ['institutional failure', 'the drug trade as ecosystem', 'systemic inequality', 'the war on drugs'],
        'episodes': ['Middle Ground', '-30-', 'The Wire', 'Cleaning Up'],
        'highlights': ['the naturalistic dialogue',
                       'the ensemble depth across every season',
                       'the season-long story arcs that build quietly'],
    },
    'the-sopranos': {
        'creator': 'David Chase',
        'characters': ['Tony Soprano', 'Carmela Soprano', 'Dr. Melfi', 'Christopher Moltisanti'],
        'themes': ['family dysfunction', 'the American Dream and crime', 'therapy and self-awareness', 'violence and guilt'],
        'episodes': ['Pine Barrens', 'Long Term Parking', 'Made in America', 'College'],
        'highlights': ["James Gandolfini's nuanced performance",
                       'the therapy sessions as a window into Tony\'s psychology',
                       'the legendary ambiguous series finale'],
    },
    'game-of-thrones': {
        'creator': 'David Benioff and D.B. Weiss',
        'characters': ['Jon Snow', 'Daenerys Targaryen', 'Tyrion Lannister', 'Cersei Lannister'],
        'themes': ['power and its costs', 'betrayal', 'the futility of war', 'the nature of leadership'],
        'episodes': ['Battle of the Bastards', 'Hardhome', 'The Rains of Castamere', 'Baelor'],
        'highlights': ['the spectacular production scale',
                       'the political intrigue of the early seasons',
                       'the unpredictable willingness to kill major characters'],
    },
    'chernobyl-hbo': {
        'creator': 'Craig Mazin',
        'characters': ['Valery Legasov', 'Lyudmila Ignatenko', 'Boris Shcherbina'],
        'themes': ['the cost of lies', 'Soviet bureaucracy and denial', 'human sacrifice and duty'],
        'episodes': ['1:23:45', 'The Happiness of All Mankind', 'Vichnaya Pamyat', 'Open Wide, O Earth'],
        'highlights': ['the meticulous historical accuracy',
                       'Jared Harris and Stellan Skarsgård\'s performances',
                       'the terrifying recreation of the disaster itself'],
    },
    'band-of-brothers': {
        'creator': 'Steven Spielberg and Tom Hanks',
        'characters': ['Dick Winters', 'Lewis Nixon', 'Carwood Lipton', 'Ronald Speirs'],
        'themes': ['brotherhood under fire', 'the horrors and absurdity of war', 'leadership and sacrifice'],
        'episodes': ['Why We Fight', 'The Breaking Point', 'Day of Days', 'Bastogne'],
        'highlights': ['the extraordinary ensemble cast',
                       'the authenticity of the battle sequences',
                       'the real veterans speaking to camera in the final episode'],
    },
    'true-detective': {
        'creator': 'Nic Pizzolatto',
        'characters': ['Rust Cohle', 'Marty Hart', 'Ani Bezzerides'],
        'themes': ['nihilism vs hope', 'the dark side of the American South', 'memory and obsession'],
        'episodes': ["After You've Gone", 'Who Goes There', 'The Secret Fate of All Life'],
        'highlights': ["Matthew McConaughey's existential monologues",
                       'the long tracking shot through the housing projects',
                       'the philosophical depth of Season 1'],
    },
    'westworld-show': {
        'creator': 'Jonathan Nolan and Lisa Joy',
        'characters': ['Dolores', 'The Man in Black', 'Maeve', 'Bernard'],
        'themes': ['consciousness and free will', 'the ethics of artificial intelligence', 'cyclical suffering'],
        'episodes': ['The Bicameral Mind', 'Trace Decay', 'The Well-Tempered Clavier'],
        'highlights': ['the mystery-box storytelling of Season 1',
                       'the incredible production design',
                       'Evan Rachel Wood and Thandiwe Newton\'s performances'],
    },
    'the-office-us': {
        'creator': 'Greg Daniels',
        'characters': ['Michael Scott', 'Jim Halpert', 'Dwight Schrute', 'Pam Beesly'],
        'themes': ['workplace relationships', 'the mundane and the meaningful', 'cringe comedy'],
        'episodes': ['Goodbye Michael', 'Casino Night', 'Dinner Party', 'The Injury'],
        'highlights': ['Steve Carell\'s comedic genius as Michael Scott',
                       'the Jim and Pam relationship arc',
                       'the perfect use of the mockumentary format'],
    },
    'stranger-things': {
        'creator': 'The Duffer Brothers',
        'characters': ['Eleven', 'Mike Wheeler', 'Hopper', 'Dustin Henderson'],
        'themes': ['childhood friendship and loss', 'Cold War paranoia', 'the supernatural as metaphor'],
        'episodes': ['Chapter Seven: The Bathtub', 'Dear Billy', 'The Piggyback'],
        'highlights': ['the 80s nostalgia done right',
                       'the ensemble cast chemistry',
                       "Millie Bobby Brown's remarkable performance"],
    },
    'sherlock-bbc': {
        'creator': 'Steven Moffat and Mark Gatiss',
        'characters': ['Sherlock Holmes', 'John Watson', 'Moriarty', 'Irene Adler'],
        'themes': ['genius and loneliness', 'friendship as an anchor', 'the battle of wits'],
        'episodes': ['A Study in Pink', 'The Reichenbach Fall', 'His Last Vow'],
        'highlights': ["Benedict Cumberbatch's charismatic reinvention of the character",
                       'the modern London setting',
                       'the kinetic fast-paced editing and direction'],
    },
    'peaky-blinders': {
        'creator': 'Steven Knight',
        'characters': ['Tommy Shelby', 'Arthur Shelby', 'Polly Gray', 'Alfie Solomons'],
        'themes': ['post-war trauma and ambition', 'power and family loyalty', 'the working class rise'],
        'episodes': ['Season 4 Finale', 'Season 5 Finale', 'Dangerous'],
        'highlights': ["Cillian Murphy's magnetic intensity",
                       'the Nick Cave soundtrack choices',
                       'the atmospheric cinematography'],
    },
    'the-crown': {
        'creator': 'Peter Morgan',
        'characters': ['Queen Elizabeth II', 'Prince Philip', 'Princess Margaret', 'Margaret Thatcher'],
        'themes': ['duty vs personal desire', 'the weight of the Crown', 'Britain\'s post-war decline'],
        'episodes': ['Aberfan', 'Fairytale', 'Tywysog Cymru'],
        'highlights': ['the stunning production values',
                       'Claire Foy and Olivia Colman\'s respective portrayals',
                       'the historical drama quality'],
    },
    'mindhunter': {
        'creator': 'Joe Penhall',
        'characters': ['Holden Ford', 'Bill Tench', 'Wendy Carr', 'Ed Kemper'],
        'themes': ['the birth of criminal profiling', 'understanding evil', 'bureaucratic obstruction'],
        'episodes': ['Episode 2 Season 1', 'Episode 9 Season 1', 'Episode 5 Season 2'],
        'highlights': ['the dynamic between Jonathan Groff and Holt McCallany',
                       'Cameron Britton\'s chilling Ed Kemper',
                       'David Fincher\'s cold clinical direction'],
    },
    'better-call-saul': {
        'creator': 'Vince Gilligan and Peter Gould',
        'characters': ['Jimmy McGill', 'Mike Ehrmantraut', 'Kim Wexler', 'Gus Fring'],
        'themes': ['identity and self-deception', 'the slow corruption of integrity', 'legal and moral grey zones'],
        'episodes': ['Plan and Execution', 'Saul Gone', 'Magic Man'],
        'highlights': ["Rhea Seehorn's Emmy-worthy performance as Kim Wexler",
                       'the black-and-white Gene Takavic timeline',
                       'many argue it surpasses Breaking Bad'],
    },
    'succession-show': {
        'creator': 'Jesse Armstrong',
        'characters': ['Logan Roy', 'Kendall Roy', 'Siobhan Roy', 'Roman Roy'],
        'themes': ['toxic wealth and family', 'ambition and self-worth', 'the dysfunction of power'],
        'episodes': ["Connor's Wedding", 'All the Bells Say', 'This Is Not for Tears'],
        'highlights': ["Brian Cox's commanding presence as Logan",
                       'the sharp satirical writing',
                       'the perfect balance of comedy and tragedy'],
    },
    'the-boys-tv': {
        'creator': 'Eric Kripke',
        'characters': ['Billy Butcher', 'Hughie Campbell', 'Homelander', 'Starlight'],
        'themes': ['superhero deconstruction', 'corporate power and complicity', 'toxic masculinity unchecked'],
        'episodes': ['What I Know', 'Herogasm', 'The Instant White-Hot Wild'],
        'highlights': ['Antony Starr\'s terrifying Homelander',
                       'the satirical corporate villainy',
                       'the genre-defying violence with purpose'],
    },
    'black-mirror': {
        'creator': 'Charlie Brooker',
        'characters': ['various characters per episode'],
        'themes': ['technology and its dark side', 'social media addiction', 'surveillance and control'],
        'episodes': ['San Junipero', 'White Bear', 'USS Callister', 'Nosedive'],
        'highlights': ['the standalone anthology format',
                       'the prescient technology warnings',
                       'the emotional gut-punches in the best episodes'],
    },
    'ozark': {
        'creator': 'Bill Dubuque and Mark Williams',
        'characters': ['Marty Byrde', 'Wendy Byrde', 'Ruth Langmore', 'Darlene Snell'],
        'themes': ['family survival over morality', 'money laundering and its costs', 'rural crime dynamics'],
        'episodes': ['Tonight We Improvise', 'All In', 'Rethinking Mortality'],
        'highlights': ["Jason Bateman's dramatic range",
                       "Julia Garner's scene-stealing Ruth Langmore",
                       'the Missouri Ozarks atmosphere'],
    },
    'house-of-cards-us': {
        'creator': 'Beau Willimon',
        'characters': ['Frank Underwood', 'Claire Underwood', 'Doug Stamper'],
        'themes': ['political ambition without conscience', 'manipulation and power', 'the Washington machine'],
        'episodes': ['Chapter 1', 'Chapter 14', 'Chapter 52'],
        'highlights': ["Kevin Spacey's fourth-wall breaks",
                       'the Machiavellian plot threading',
                       "Robin Wright's increasingly central role"],
    },
}

# ===========================================================================
# TOP CARTOONS
# ===========================================================================
CARTOONS = [
    ('The Simpsons',                    'the-simpsons',             'The Simpsons',                     1989),
    ('Family Guy',                      'family-guy',               'Family Guy',                       1999),
    ('South Park',                      'south-park',               'South Park',                       1997),
    ('Avatar: The Last Airbender',      'avatar-tla',               'Avatar: The Last Airbender',       2005),
    ('Batman: The Animated Series',     'batman-animated-series',   'Batman: The Animated Series',      1992),
    ('Futurama',                        'futurama',                 'Futurama',                         1999),
    ('Rick and Morty',                  'rick-and-morty',           'Rick and Morty',                   2013),
    ('Gravity Falls',                   'gravity-falls',            'Gravity Falls',                    2012),
    ('Adventure Time',                  'adventure-time',           'Adventure Time',                   2010),
    ('Regular Show',                    'regular-show',             'Regular Show',                     2010),
    ('Steven Universe',                 'steven-universe',          'Steven Universe',                  2013),
    ('Teen Titans',                     'teen-titans-cartoon',      'Teen Titans (TV series)',           2003),
    ('Archer',                          'archer-fx',                'Archer (TV series)',                2009),
    ("Bob's Burgers",                   'bobs-burgers',             "Bob's Burgers",                    2011),
    ('BoJack Horseman',                 'bojack-horseman',          'BoJack Horseman',                  2014),
]

CARTOON_DATA = {
    'the-simpsons': {
        'creator': 'Matt Groening',
        'characters': ['Homer Simpson', 'Bart Simpson', 'Lisa Simpson', 'Marge Simpson'],
        'themes': ['suburban life satire', 'the dysfunctional but loving family', 'American culture critique'],
        'episodes': ['Cape Feare', 'Marge vs. the Monorail', 'Homer at the Bat', 'Last Exit to Springfield'],
        'highlights': ['the Golden Age seasons three through eight',
                       'the celebrity guest formula',
                       'the layered adult humour beneath the cartoonish surface'],
    },
    'family-guy': {
        'creator': 'Seth MacFarlane',
        'characters': ['Peter Griffin', 'Stewie Griffin', 'Brian Griffin', 'Quagmire'],
        'themes': ['absurdist pop culture satire', 'family dysfunction', 'cutaway comedy'],
        'episodes': ['Road to the Multiverse', 'And Then There Were Fewer', 'PTV'],
        'highlights': ['the Stewie and Brian road trip episodes',
                       'the rapid-fire pop culture cutaways',
                       'Seth MacFarlane\'s impressive voice work'],
    },
    'south-park': {
        'creator': 'Trey Parker and Matt Stone',
        'characters': ['Cartman', 'Stan Marsh', 'Kyle Broflovski', 'Kenny McCormick'],
        'themes': ['political satire', 'social hypocrisy', 'offensive comedy with a genuine point'],
        'episodes': ['Scott Tenorman Must Die', 'Make Love Not Warcraft', 'Imaginationland'],
        'highlights': ['the incredibly fast production turnaround',
                       'the fearless political commentary',
                       "Cartman's cartoonish villainy"],
    },
    'avatar-tla': {
        'creator': 'Michael DiMartino and Bryan Konietzko',
        'characters': ['Aang', 'Zuko', 'Katara', 'Toph'],
        'themes': ['balance and responsibility', 'redemption', 'found family'],
        'episodes': ["Zuko Alone", "The Ember Island Players", "Sozin's Comet"],
        'highlights': ["Zuko's full redemption arc",
                       'the world-building depth',
                       'the mature themes for a children\'s show'],
    },
    'batman-animated-series': {
        'creator': 'Bruce Timm and Paul Dini',
        'characters': ['Batman', 'The Joker', 'Harley Quinn', 'Mr. Freeze'],
        'themes': ['justice vs revenge', 'the tragedy behind the villains', 'Gotham as a noir city'],
        'episodes': ['Heart of Ice', "Almost Got 'Im", 'Mad Love'],
        'highlights': ['the Art Deco visual style',
                       "Paul Dini's empathetic villain writing",
                       'Kevin Conroy as the definitive Batman'],
    },
    'futurama': {
        'creator': 'Matt Groening and David X. Cohen',
        'characters': ['Fry', 'Leela', 'Bender', 'Professor Farnsworth'],
        'themes': ['sci-fi satire', 'love and longing across time', 'identity and belonging'],
        'episodes': ['Jurassic Bark', 'The Luck of the Fryrish', 'The Late Philip J. Fry'],
        'highlights': ['the science-based humour',
                       'the emotional gut-punches disguised as comedy',
                       "Bender's comic anarchy"],
    },
    'rick-and-morty': {
        'creator': 'Justin Roiland and Dan Harmon',
        'characters': ['Rick Sanchez', 'Morty Smith', 'Beth Smith', 'Summer Smith'],
        'themes': ['nihilism and existential dread', 'family dysfunction', 'sci-fi deconstruction'],
        'episodes': ['Pickle Rick', 'Total Rickall', 'A Rickle in Time'],
        'highlights': ["Rick's paradoxical emotional depth",
                       'the science fiction concept creativity',
                       'the dark humour with genuine philosophical ambition'],
    },
    'gravity-falls': {
        'creator': 'Alex Hirsch',
        'characters': ['Dipper Pines', 'Mabel Pines', 'Grunkle Stan', 'Bill Cipher'],
        'themes': ['mystery and the supernatural', 'growing up', 'trust and family secrets'],
        'episodes': ['Weirdmageddon', 'Not What He Seems', 'Dipper and Mabel vs. the Future'],
        'highlights': ['the mystery-box storytelling done right',
                       'the sibling relationship at the heart of the show',
                       'the callbacks and Easter eggs rewarding careful viewers'],
    },
    'adventure-time': {
        'creator': 'Pendleton Ward',
        'characters': ['Finn the Human', 'Jake the Dog', 'Princess Bubblegum', 'Marceline'],
        'themes': ['post-apocalyptic whimsy', 'growing up and identity', 'love and friendship'],
        'episodes': ['I Remember You', 'Simon and Marcy', 'Come Along with Me'],
        'highlights': ['the surreal world-building',
                       'the emotional depth beneath the weirdness',
                       'the music episodes'],
    },
    'regular-show': {
        'creator': 'J.G. Quintel',
        'characters': ['Mordecai', 'Rigby', 'Benson', 'Pops'],
        'themes': ['slacker life and responsibility', 'friendship', 'the absurd escalation of everyday problems'],
        'episodes': ['Exit 9B', 'Limousine Lunchtime', 'The Last Laserdisc Player'],
        'highlights': ['the 80s and 90s nostalgia',
                       'the absurdist escalation formula',
                       'the surprisingly emotional series finale'],
    },
    'steven-universe': {
        'creator': 'Rebecca Sugar',
        'characters': ['Steven Universe', 'Garnet', 'Amethyst', 'Pearl', 'Lapis Lazuli'],
        'themes': ['identity and self-acceptance', 'grief and recovery', 'love as strength'],
        'episodes': ['Jail Break', 'Mr. Greg', 'A Single Pale Rose'],
        'highlights': ['the LGBTQ+ representation',
                       'the character-driven storytelling',
                       "Rebecca Sugar's original musical numbers"],
    },
    'teen-titans-cartoon': {
        'creator': 'Glen Murakami',
        'characters': ['Robin', 'Raven', 'Starfire', 'Cyborg', 'Beast Boy'],
        'themes': ['identity and belonging', 'the burden of heroism', 'friendship'],
        'episodes': ['Apprentice', 'Haunted', 'The End'],
        'highlights': ["Raven's dark emotional arc",
                       'the anime-influenced action sequences',
                       'the emotionally resonant finale'],
    },
    'archer-fx': {
        'creator': 'Adam Reed',
        'characters': ['Sterling Archer', 'Lana Kane', 'Malory Archer', 'Pam Poovey'],
        'themes': ['spy parody', 'narcissism and family dysfunction', 'workplace comedy'],
        'episodes': ['The Archer Sanction', 'Heart of Archness', 'Placebo Effect'],
        'highlights': ['the rapid-fire wordplay',
                       "H. Jon Benjamin's perfect deadpan delivery",
                       'the ensemble cast chemistry'],
    },
    'bobs-burgers': {
        'creator': 'Loren Bouchard',
        'characters': ['Bob Belcher', 'Linda Belcher', 'Tina Belcher', 'Gene Belcher'],
        'themes': ['family warmth', 'working-class struggle', 'everyday weirdness'],
        'episodes': ['The Belchies', 'Mutiny on the Windbreaker', 'Flu-ouise'],
        'highlights': ['the genuinely loving family dynamics',
                       "Tina's dry delivery",
                       'the restaurant-of-the-day chalkboard gag'],
    },
    'bojack-horseman': {
        'creator': 'Raphael Bob-Waksberg',
        'characters': ['BoJack Horseman', 'Diane Nguyen', 'Todd Chavez', 'Princess Carolyn'],
        'themes': ['depression and self-destruction', 'the entertainment industry', 'accountability'],
        'episodes': ["Time's Arrow", 'Free Churro', 'The View from Halfway Down'],
        'highlights': ['the unflinching portrayal of addiction',
                       "Will Arnett's performance",
                       'the genre-defying emotional depth for an animated show'],
    },
}

# ===========================================================================
# TOP ANIME
# ===========================================================================
ANIME = [
    ('Attack on Titan',                         'attack-on-titan',              'Attack on Titan',                          2013),
    ('Death Note',                              'death-note',                   'Death Note',                               2006),
    ('Fullmetal Alchemist: Brotherhood',        'fma-brotherhood',              'Fullmetal Alchemist: Brotherhood',         2009),
    ('Naruto',                                  'naruto',                       'Naruto',                                   2002),
    ('Dragon Ball Z',                           'dragon-ball-z',                'Dragon Ball Z',                            1989),
    ('Demon Slayer',                            'demon-slayer',                 'Demon Slayer: Kimetsu no Yaiba',           2019),
    ('My Hero Academia',                        'my-hero-academia',             'My Hero Academia',                         2016),
    ('Hunter × Hunter',                         'hunter-x-hunter',              'Hunter × Hunter (2011 TV series)',         2011),
    ('Steins;Gate',                             'steins-gate',                  'Steins;Gate (TV series)',                  2011),
    ('Neon Genesis Evangelion',                 'neon-genesis-evangelion',      'Neon Genesis Evangelion',                  1995),
    ('Cowboy Bebop',                            'cowboy-bebop',                 'Cowboy Bebop',                             1998),
    ('Your Lie in April',                       'your-lie-in-april',            'Your Lie in April',                        2014),
    ('Sword Art Online',                        'sword-art-online',             'Sword Art Online',                         2012),
    ('Tokyo Ghoul',                             'tokyo-ghoul',                  'Tokyo Ghoul',                              2014),
    ('One-Punch Man',                           'one-punch-man',                'One-Punch Man',                            2015),
]

ANIME_DATA = {
    'attack-on-titan': {
        'creator': 'Hajime Isayama',
        'characters': ['Eren Yeager', 'Mikasa Ackerman', 'Armin Arlert', 'Levi Ackerman'],
        'themes': ['freedom and the cycle of violence', 'moral grey areas in war', 'the cost of vengeance'],
        'episodes': ['The Door of Hope', 'Hero', 'The Rumbling'],
        'highlights': ['the jaw-dropping animation in later seasons',
                       "Levi's character depth",
                       'the subversion of genre expectations'],
    },
    'death-note': {
        'creator': 'Tsugumi Ohba and Takeshi Obata',
        'characters': ['Light Yagami', 'L', 'Near', 'Ryuk'],
        'themes': ['justice vs self-righteousness', 'the corrupting nature of absolute power', 'cat-and-mouse psychology'],
        'episodes': ['Confrontation', 'Silence', 'New World'],
        'highlights': ['the intellectual battle between Light and L',
                       'the tension in every single scene',
                       'the moral ambiguity that challenges you throughout'],
    },
    'fma-brotherhood': {
        'creator': 'Hiromu Arakawa',
        'characters': ['Edward Elric', 'Alphonse Elric', 'Roy Mustang', 'Winry Rockbell'],
        'themes': ['equivalent exchange', 'the consequences of hubris', 'brotherhood and sacrifice'],
        'episodes': ['The Ishvalan War of Extermination', "Journey's End", 'Eye of Heaven, Gateway of Earth'],
        'highlights': ['the extraordinary world-building depth',
                       'the emotional weight of every sacrifice',
                       'the satisfying and earned ending'],
    },
    'naruto': {
        'creator': 'Masashi Kishimoto',
        'characters': ['Naruto Uzumaki', 'Sasuke Uchiha', 'Sakura Haruno', 'Kakashi Hatake'],
        'themes': ['perseverance and self-belief', 'the pain of loneliness', 'the cycle of hatred'],
        'episodes': ['Chunin Exams arc', "Pain's Assault arc", 'Sasuke Retrieval arc'],
        'highlights': ["Naruto vs Pain",
                       'the emotional backstories of Gaara and Itachi',
                       'the ninja world-building'],
    },
    'dragon-ball-z': {
        'creator': 'Akira Toriyama',
        'characters': ['Goku', 'Vegeta', 'Gohan', 'Piccolo'],
        'themes': ['pushing beyond limits', 'redemption and rivalry', 'the Saiyan warrior spirit'],
        'episodes': ['Frieza saga', 'Cell Games', 'Majin Vegeta vs Goku'],
        'highlights': ["Vegeta's arc from villain to antihero",
                       'the iconic Super Saiyan transformations',
                       'Gohan vs Cell'],
    },
    'demon-slayer': {
        'creator': 'Koyoharu Gotouge',
        'characters': ['Tanjiro Kamado', 'Nezuko Kamado', 'Zenitsu Agatsuma', 'Inosuke Hashibira'],
        'themes': ['family and protection', 'humanity within monsters', 'the cost of being a demon slayer'],
        'episodes': ['Hinokami', 'Entertainment District Arc finale', 'Mugen Train'],
        'highlights': ["ufotable's jaw-dropping animation",
                       'the emotional sibling bond',
                       'the unexpected sympathy for villains'],
    },
    'my-hero-academia': {
        'creator': 'Kōhei Horikoshi',
        'characters': ['Izuku Midoriya', 'Katsuki Bakugo', 'All Might', 'Shoto Todoroki'],
        'themes': ['what it means to be a hero', 'overcoming limitations', 'the burden of power'],
        'episodes': ['United States of Smash', 'My Hero', 'Katsuki Bakugo: Rising'],
        'highlights': ['All Might vs All For One',
                       "Bakugo's character growth across the series",
                       'the sports festival arc'],
    },
    'hunter-x-hunter': {
        'creator': 'Yoshihiro Togashi',
        'characters': ['Gon Freecss', 'Killua Zoldyck', 'Hisoka', 'Kurapika'],
        'themes': ['the darkness within people', 'friendship and its limits', 'the cost of obsession'],
        'episodes': ['Chimera Ant Arc', "Heaven's Arena Arc", 'Yorknew City Arc'],
        'highlights': ['the Chimera Ant arc as one of anime\'s greatest achievements',
                       "Killua's emotional journey",
                       "Gon's heartbreaking transformation"],
    },
    'steins-gate': {
        'creator': 'Naotaka Hayashi',
        'characters': ['Rintaro Okabe', 'Kurisu Makise', 'Mayuri Shiina', 'Daru'],
        'themes': ['time travel and consequence', 'grief and acceptance', 'the cost of changing fate'],
        'episodes': ['Dogma in Event Horizon', 'Being Meltdown', 'Achievement Point'],
        'highlights': ['the slow-burn payoff that rewards patient viewers',
                       'Okabe and Kurisu\'s relationship',
                       'the internally consistent time travel logic'],
    },
    'neon-genesis-evangelion': {
        'creator': 'Hideaki Anno',
        'characters': ['Shinji Ikari', 'Rei Ayanami', 'Asuka Langley Soryu', 'Misato Katsuragi'],
        'themes': ['depression and self-worth', 'the fear of human connection', 'apocalypse as psychological metaphor'],
        'episodes': ['Splitting of the Breast', 'The Beginning and the End', 'The End of Evangelion'],
        'highlights': ['the psychological depth',
                       'the deconstruction of the mecha genre',
                       'its lasting and enormous cultural impact'],
    },
    'cowboy-bebop': {
        'creator': 'Shinichirō Watanabe',
        'characters': ['Spike Spiegel', 'Jet Black', 'Faye Valentine', 'Edward'],
        'themes': ['living in the past vs the present', 'loneliness and found family', 'the jazz of existence'],
        'episodes': ['Ballad of Fallen Angels', 'Hard Luck Woman', 'The Real Folk Blues'],
        'highlights': ["Yoko Kanno's legendary soundtrack",
                       "Spike's tragic arc",
                       'the genre-blending episode format'],
    },
    'your-lie-in-april': {
        'creator': 'Naoshi Arakawa',
        'characters': ['Kousei Arima', 'Kaori Miyazono', 'Tsubaki Sawabe', 'Ryota Watari'],
        'themes': ['grief and healing', 'music as emotional expression', 'living fully in the present'],
        'episodes': ['Reverberations', 'Heart of a Stalagmite', 'A Prepared Lie'],
        'highlights': ['the stunning classical music integration',
                       "Kaori's emotional impact on viewers",
                       'the devastating and beautiful ending'],
    },
    'sword-art-online': {
        'creator': 'Reki Kawahara',
        'characters': ['Kirito', 'Asuna', 'Sinon', 'Alice'],
        'themes': ['virtual identity vs real identity', 'survival and love', 'the ethics of virtual reality'],
        'episodes': ['The Gleam Eyes', 'Calibur', 'Alicization arc'],
        'highlights': ['the first arc\'s trapped-in-a-game tension',
                       'Kirito and Asuna\'s relationship',
                       'pioneer status for the isekai genre'],
    },
    'tokyo-ghoul': {
        'creator': 'Sui Ishida',
        'characters': ['Ken Kaneki', 'Touka Kirishima', 'Rize Kamishiro', 'Hide Nagachika'],
        'themes': ['identity between two worlds', 'the cost of survival', 'what makes us human'],
        'episodes': ['Ghoul', 'Episode 12', 'Root A arc'],
        'highlights': ["Kaneki's transformation",
                       'the body horror imagery',
                       'the existential questions it raises'],
    },
    'one-punch-man': {
        'creator': 'ONE',
        'characters': ['Saitama', 'Genos', 'Mumen Rider', 'Speed-o-Sound Sonic'],
        'themes': ['the existential boredom of absolute power', 'heroism without recognition', 'strength and purpose'],
        'episodes': ['The Strongest Hero', 'The Ultimate Master', 'The Deep Sea King'],
        'highlights': ["Saitama's comedic invincibility",
                       "Genos's earnest devotion",
                       "Season 1's stunning animation quality"],
    },
}

# ===========================================================================
# TOP MARVEL
# ===========================================================================
MARVEL_FILMS = [
    ('Avengers: Endgame',                           'avengers-endgame',             'Avengers: Endgame',                        2019),
    ('Iron Man',                                    'iron-man-2008',                'Iron Man (2008 film)',                      2008),
    ('The Avengers',                                'the-avengers-2012',            'The Avengers (2012 film)',                  2012),
    ('Captain America: Civil War',                  'captain-america-civil-war',    'Captain America: Civil War',               2016),
    ('Black Panther',                               'black-panther-mcu',            'Black Panther (film)',                      2018),
    ('Thor: Ragnarok',                              'thor-ragnarok',                'Thor: Ragnarok',                           2017),
    ('Guardians of the Galaxy',                     'guardians-of-the-galaxy',      'Guardians of the Galaxy (film)',           2014),
    ('Spider-Man: Homecoming',                      'spider-man-homecoming',        'Spider-Man: Homecoming',                   2017),
    ('Doctor Strange',                              'doctor-strange-mcu',           'Doctor Strange (film)',                    2016),
    ('Captain America: The Winter Soldier',         'captain-america-winter-soldier','Captain America: The Winter Soldier',      2014),
    ('Ant-Man',                                     'ant-man-mcu',                  'Ant-Man (film)',                           2015),
    ('Thor',                                        'thor-2011',                    'Thor (film)',                              2011),
    ('Captain Marvel',                              'captain-marvel-mcu',           'Captain Marvel (film)',                    2019),
    ('Black Widow',                                 'black-widow-2021',             'Black Widow (2021 film)',                  2021),
    ('Shang-Chi',                                   'shang-chi',                    'Shang-Chi and the Legend of the Ten Rings',2021),
    ('Spider-Man: No Way Home',                     'spider-man-no-way-home',       'Spider-Man: No Way Home',                  2021),
    ('Doctor Strange in the Multiverse of Madness', 'doctor-strange-multiverse',    'Doctor Strange in the Multiverse of Madness',2022),
    ('Eternals',                                    'eternals-mcu',                 'Eternals (film)',                          2021),
]

MARVEL_DATA = {
    'avengers-endgame': {
        'director': 'Anthony and Joe Russo',
        'characters': ['Iron Man', 'Captain America', 'Thor', 'Black Widow', 'Hulk'],
        'themes': ['sacrifice and legacy', 'time and regret', 'doing whatever it takes'],
        'scenes': ['the time heist', '"I am Iron Man"', 'Portals scene', 'Cap wielding Mjolnir'],
        'highlights': ['the culmination of 22 films',
                       "Tony Stark's sacrifice",
                       'the emotional weight of the ending'],
    },
    'iron-man-2008': {
        'director': 'Jon Favreau',
        'characters': ['Tony Stark', 'Pepper Potts', 'Obadiah Stane', 'Rhodey'],
        'themes': ['responsibility', 'ego and redemption', 'the cost of weapons manufacturing'],
        'scenes': ['the cave escape', '"I am Iron Man" press conference', 'first suit test flight'],
        'highlights': ['Robert Downey Jr. defining the MCU',
                       'the practical suit design',
                       'the perfect origin story tone'],
    },
    'the-avengers-2012': {
        'director': 'Joss Whedon',
        'characters': ['Iron Man', 'Captain America', 'Thor', 'Hulk', 'Black Widow', 'Loki'],
        'themes': ['teamwork despite ego', "earth's defence", 'what makes a hero'],
        'scenes': ['Hulk smashing Loki', 'the single-take battle shot', 'the shawarma scene'],
        'highlights': ['the genre-defining ensemble assembly',
                       'Loki as the perfect villain',
                       "the Hulk's comedic timing"],
    },
    'captain-america-civil-war': {
        'director': 'Anthony and Joe Russo',
        'characters': ['Captain America', 'Iron Man', 'Black Panther', 'Spider-Man', 'Bucky'],
        'themes': ['freedom vs accountability', 'loyalty and friendship', 'political oversight of superheroes'],
        'scenes': ['the airport battle', 'the Siberia confrontation', "Spider-Man's debut"],
        'highlights': ['the moral complexity where both sides are right',
                       "Black Panther's introduction",
                       'arguably the best film in the MCU'],
    },
    'black-panther-mcu': {
        'director': 'Ryan Coogler',
        'characters': ["T'Challa", 'Killmonger', 'Shuri', 'Okoye', 'Nakia'],
        'themes': ['isolationism vs global responsibility', 'colonialism and identity', "a king's duty to his people"],
        'scenes': ['the waterfall challenge', 'the Korean casino chase', 'the vibranium train fight'],
        'highlights': ["Michael B. Jordan's compelling Killmonger",
                       'the Afrofuturism design',
                       'the cultural significance'],
    },
    'thor-ragnarok': {
        'director': 'Taika Waititi',
        'characters': ['Thor', 'Hulk', 'Loki', 'Valkyrie', 'Hela'],
        'themes': ['home is not a place', "the truth about Asgard's history", 'reinvention'],
        'scenes': ['Thor vs Hulk gladiator fight', 'Led Zeppelin entrance', '"He\'s a friend from work"'],
        'highlights': ["Taika Waititi's comedic reinvention of Thor",
                       'the neon-lit visual palette',
                       'Cate Blanchett as Hela'],
    },
    'guardians-of-the-galaxy': {
        'director': 'James Gunn',
        'characters': ['Star-Lord', 'Gamora', 'Drax', 'Rocket', 'Groot'],
        'themes': ['found family', 'being a hero on your own terms', 'grief and belonging'],
        'scenes': ['the jail break', '"We are Groot"', 'the Awesome Mix Vol. 1 opening'],
        'highlights': ['the unexpected surprise hit of the MCU',
                       'the perfect needle-drop soundtrack',
                       "Bradley Cooper's Rocket"],
    },
    'spider-man-homecoming': {
        'director': 'Jon Watts',
        'characters': ['Peter Parker', 'Tony Stark', 'The Vulture', 'Ned Leeds'],
        'themes': ['growing up and earning responsibility', 'the everyman hero', 'academic pressure and heroism'],
        'scenes': ['the ferry rescue', 'the Vulture reveal', '"If you\'re nothing without the suit..."'],
        'highlights': ["Tom Holland's perfect Peter Parker",
                       "Michael Keaton's relatable villain",
                       'the high school tone'],
    },
    'doctor-strange-mcu': {
        'director': 'Scott Derrickson',
        'characters': ['Stephen Strange', 'The Ancient One', 'Mordo', 'Wong'],
        'themes': ['ego and humility', 'the multiverse of possibility', 'the sacrifice of the ego'],
        'scenes': ['the kaleidoscope NYC sequence', 'the Dark Dimension time loop', 'the car crash opening'],
        'highlights': ['the visual effects as genuine art',
                       "Tilda Swinton's mystical presence",
                       "Benedict Cumberbatch's charm"],
    },
    'captain-america-winter-soldier': {
        'director': 'Anthony and Joe Russo',
        'characters': ['Steve Rogers', 'Bucky Barnes', 'Natasha Romanoff', 'Nick Fury'],
        'themes': ['surveillance vs freedom', 'loyalty to a friend vs loyalty to a cause', 'the past haunting the present'],
        'scenes': ['the elevator fight', 'the highway fight', 'the SHIELD reveal'],
        'highlights': ['the political thriller tone',
                       'the best action choreography in the MCU',
                       "Robert Redford's casting"],
    },
    'ant-man-mcu': {
        'director': 'Peyton Reed',
        'characters': ['Scott Lang', 'Hank Pym', 'Hope van Dyne', 'Darren Cross'],
        'themes': ['second chances', 'fatherhood', 'scaling down as strength'],
        'scenes': ['the bathtub sequence', 'the Thomas the Tank Engine fight', 'the training montage'],
        'highlights': ["Paul Rudd's likability",
                       'the heist movie structure',
                       'the clever scale-shift comedy'],
    },
    'thor-2011': {
        'director': 'Kenneth Branagh',
        'characters': ['Thor', 'Loki', 'Jane Foster', 'Odin'],
        'themes': ['humility and worthiness', 'sibling jealousy', 'the bridge between worlds'],
        'scenes': ["Thor's banishment", 'the Frost Giant battle', 'the rainbow bridge finale'],
        'highlights': ["Loki's origin tragedy",
                       "Kenneth Branagh's Shakespearean direction",
                       'the fish-out-of-water comedy'],
    },
    'captain-marvel-mcu': {
        'director': 'Anna Boden and Ryan Fleck',
        'characters': ['Carol Danvers', 'Nick Fury', 'Talos', 'Yon-Rogg'],
        'themes': ['identity and memory', 'female power', 'questioning authority'],
        'scenes': ['the train fight', 'the 90s nostalgia montage', 'Captain Marvel going supernova'],
        'highlights': ["Brie Larson's confident performance",
                       'young Nick Fury',
                       'Goose the Flerken'],
    },
    'black-widow-2021': {
        'director': 'Cate Shortland',
        'characters': ['Natasha Romanoff', 'Yelena Belova', 'Red Guardian', 'Taskmaster'],
        'themes': ['confronting a past of manipulation', 'chosen family', 'breaking free from programming'],
        'scenes': ['the Red Room assault', 'the Budapest flashback reveal', 'the highway chase'],
        'highlights': ['Florence Pugh stealing the film as Yelena',
                       'the spy thriller aesthetic',
                       'the family dynamic humour'],
    },
    'shang-chi': {
        'director': 'Destin Daniel Cretton',
        'characters': ['Shang-Chi', 'Xu Wenwu', 'Katy', 'Xialing'],
        'themes': ['living up to a legacy vs forging your own path', 'family and sacrifice', 'eastern mythology in the MCU'],
        'scenes': ['the bamboo scaffolding fight', 'the bus fight opener', 'the Ten Rings vs the Great Protector'],
        'highlights': ['Tony Leung\'s devastating Xu Wenwu',
                       'the martial arts choreography',
                       'fresh MCU mythology'],
    },
    'spider-man-no-way-home': {
        'director': 'Jon Watts',
        'characters': ['Peter Parker', 'Doctor Strange', 'MJ', 'Green Goblin', 'Doctor Octopus'],
        'themes': ['the cost of being known', 'identity and sacrifice', 'learning from past mistakes'],
        'scenes': ['the statue of liberty battle', 'the three Spider-Men together', 'the "with great power" moment'],
        'highlights': ['the nostalgia done right',
                       "Willem Dafoe's terrifying return",
                       "Tom Holland's emotional arc"],
    },
    'doctor-strange-multiverse': {
        'director': 'Sam Raimi',
        'characters': ['Doctor Strange', 'America Chavez', 'Scarlet Witch', 'Christine Palmer'],
        'themes': ['obsession and loss', 'the multiverse of consequences', 'what makes us heroes'],
        'scenes': ['the Illuminati massacre', 'the musical note battle', 'Strange dreaming walking'],
        'highlights': ["Sam Raimi's horror-inflected direction",
                       "Elizabeth Olsen's terrifying Wanda",
                       'the multiversal imagination'],
    },
    'eternals-mcu': {
        'director': 'Chloé Zhao',
        'characters': ['Sersi', 'Ikaris', 'Thena', 'Gilgamesh', 'Druig'],
        'themes': ['the ethics of intervention', 'creation vs destruction on a cosmic scale', 'love as motivation'],
        'scenes': ['the Deviant attack in Babylon', 'Ikaris vs the Eternals', 'the Emergence reveal'],
        'highlights': ["Chloé Zhao's naturalistic cinematography",
                       'the diverse and compelling ensemble',
                       'the cosmic MCU ambition'],
    },
}

# ===========================================================================
# TOP DC
# ===========================================================================
DC_FILMS = [
    ('Batman Begins',                           'batman-begins',            'Batman Begins',                        2005),
    ('The Dark Knight Rises',                   'the-dark-knight-rises',    'The Dark Knight Rises',               2012),
    ('Man of Steel',                            'man-of-steel',             'Man of Steel (film)',                  2013),
    ('Wonder Woman',                            'wonder-woman-2017',        'Wonder Woman (2017 film)',             2017),
    ('Aquaman',                                 'aquaman-2018',             'Aquaman (film)',                       2018),
    ('Shazam!',                                 'shazam-2019',              'Shazam! (film)',                       2019),
    ('The Suicide Squad',                       'the-suicide-squad',        'The Suicide Squad',                   2021),
    ("Zack Snyder's Justice League",            'zack-snyders-justice-league',"Zack Snyder's Justice League",      2021),
    ('Superman',                                'superman-1978',            'Superman (1978 film)',                 1978),
    ('Batman',                                  'batman-1989',              'Batman (1989 film)',                   1989),
    ('Batman Returns',                          'batman-returns',           'Batman Returns',                      1992),
    ('Batman v Superman: Dawn of Justice',      'batman-v-superman',        'Batman v Superman: Dawn of Justice',  2016),
    ('Justice League',                          'justice-league-2017',      'Justice League (film)',               2017),
    ('Black Adam',                              'black-adam',               'Black Adam (film)',                   2022),
    ('The Flash',                               'the-flash-2023',           'The Flash (film)',                    2023),
]

DC_DATA = {
    'batman-begins': {
        'director': 'Christopher Nolan',
        'characters': ["Bruce Wayne", "Ra's al Ghul", 'Rachel Dawes', 'Alfred Pennyworth'],
        'themes': ['fear as a weapon', 'the making of a hero', 'justice vs vengeance'],
        'scenes': ['the ninja training in Nepal', 'the microwave emitter climax', 'Batman\'s first appearance'],
        'highlights': ["Christian Bale's grounded Bruce Wayne",
                       'the realistic origin story',
                       'Nolan establishing the Gotham tone'],
    },
    'the-dark-knight-rises': {
        'director': 'Christopher Nolan',
        'characters': ['Bruce Wayne', 'Bane', 'Selina Kyle', 'John Blake'],
        'themes': ['rising from defeat', 'the end of a legend', 'revolution and anarchy'],
        'scenes': ['the plane hijack opening', 'the stock exchange chase', 'the final reveal'],
        'highlights': ["Tom Hardy's physical Bane",
                       'the emotional conclusion of the trilogy',
                       "Hans Zimmer's rising score"],
    },
    'man-of-steel': {
        'director': 'Zack Snyder',
        'characters': ['Clark Kent', 'Lois Lane', 'General Zod', 'Jor-El'],
        'themes': ['identity when you are different', 'the immigrant experience', 'hope vs fear'],
        'scenes': ['the Krypton opening', 'the oil rig rescue', 'the Zod fight in Metropolis'],
        'highlights': ["Hans Zimmer's emotional score",
                       "Henry Cavill's physical presence",
                       'the reimagined Kryptonian mythology'],
    },
    'wonder-woman-2017': {
        'director': 'Patty Jenkins',
        'characters': ['Diana Prince', 'Steve Trevor', 'Ares', 'Antiope'],
        'themes': ['the nature of humanity', 'love as motivation for heroism', 'war and its costs'],
        'scenes': ["the No Man's Land charge", 'Themyscira battle opening', 'the God Killer reveal'],
        'highlights': ["Gal Gadot's commanding presence",
                       'the WWI setting distinction',
                       "the inspiring No Man's Land sequence"],
    },
    'aquaman-2018': {
        'director': 'James Wan',
        'characters': ['Arthur Curry', 'Mera', 'Orm', 'Black Manta'],
        'themes': ['belonging between two worlds', 'legacy and birthright', 'protecting the ocean'],
        'scenes': ['the Trench sequence', 'the Sicily rooftop chase', 'the final arena battle'],
        'highlights': ['the wild visual imagination underwater',
                       "Jason Momoa's charisma",
                       'the rom-com tone that works'],
    },
    'shazam-2019': {
        'director': 'David F. Sandberg',
        'characters': ['Billy Batson', 'Dr. Thaddeus Sivana', 'Freddy Freeman'],
        'themes': ['chosen family', 'power without wisdom', 'growing up'],
        'scenes': ['the ATM robbery scene', 'the foster siblings becoming heroes', 'the school showdown'],
        'highlights': ["Zachary Levi's child-in-an-adult-body joy",
                       'the light-hearted tone',
                       'the heartwarming foster family arc'],
    },
    'the-suicide-squad': {
        'director': 'James Gunn',
        'characters': ['Harley Quinn', 'Bloodsport', 'Peacemaker', 'King Shark', 'Ratcatcher 2'],
        'themes': ['expendability and found purpose', 'anti-heroes doing the right thing', 'government complicity in atrocity'],
        'scenes': ['the beach landing massacre', "Harley Quinn's prison break", 'the Starro finale'],
        'highlights': ["James Gunn's subversive R-rated energy",
                       'Idris Elba and John Cena\'s chemistry',
                       'the gorilla with a jetpack'],
    },
    'zack-snyders-justice-league': {
        'director': 'Zack Snyder',
        'characters': ['Batman', 'Wonder Woman', 'Aquaman', 'Flash', 'Cyborg', 'Superman'],
        'themes': ['unity against impossible odds', 'sacrifice and resurrection', 'the Snyder vision realised'],
        'scenes': ['Flash saving Iris West', "Cyborg's father and son scene", 'Superman in the black suit'],
        'highlights': ['the vindication of the director\'s cut',
                       "Cyborg's emotional arc finally told",
                       'the IMAX aspect ratio'],
    },
    'superman-1978': {
        'director': 'Richard Donner',
        'characters': ['Clark Kent', 'Lex Luthor', 'Lois Lane', 'Jor-El'],
        'themes': ['truth justice and the American way', 'power wielded responsibly', 'alien identity on Earth'],
        'scenes': ['the flight scene', 'the reverse-time ending', 'the reveal of Superman'],
        'highlights': ["Christopher Reeve's perfect Superman",
                       "John Williams's iconic score",
                       '"You will believe a man can fly"'],
    },
    'batman-1989': {
        'director': 'Tim Burton',
        'characters': ['Bruce Wayne', 'The Joker', 'Vicki Vale', 'Alfred'],
        'themes': ['duality of good and evil', 'Gothic Gotham as psychological space', 'media and spectacle'],
        'scenes': ["Batman's first museum appearance", 'the parade sequence', 'the cathedral finale'],
        'highlights': ["Jack Nicholson's flamboyant Joker",
                       'the Tim Burton Gothic aesthetic',
                       "Prince's soundtrack"],
    },
    'batman-returns': {
        'director': 'Tim Burton',
        'characters': ['Batman', 'The Penguin', 'Catwoman', 'Max Shreck'],
        'themes': ["society's treatment of outcasts", 'identity and masks', 'Christmas darkness'],
        'scenes': ["Catwoman's transformation", "the Penguin's campaign speech", 'the rooftop confrontation'],
        'highlights': ["Michelle Pfeiffer's iconic Catwoman",
                       'the dark festive atmosphere',
                       "DeVito's grotesque Penguin"],
    },
    'batman-v-superman': {
        'director': 'Zack Snyder',
        'characters': ['Batman', 'Superman', 'Lex Luthor', 'Wonder Woman'],
        'themes': ['fear of unchecked power', 'manufactured conflict', 'the dawn of a superhero world'],
        'scenes': ['Batman vs Superman warehouse fight', "Wonder Woman's entrance", 'the Doomsday battle'],
        'highlights': ["Gal Gadot's Wonder Woman debut",
                       "Ben Affleck's physical Batman",
                       "the director's cut improvement"],
    },
    'justice-league-2017': {
        'director': 'Zack Snyder and Joss Whedon',
        'characters': ['Batman', 'Wonder Woman', 'Flash', 'Aquaman', 'Cyborg'],
        'themes': ['assembling against an existential threat', 'resurrection and return', 'hope restored'],
        'scenes': ['Flash time-reversal', "Superman's return fight", 'the Amazons vs Steppenwolf'],
        'highlights': ["the Flash's lightspeed visuals",
                       'the team chemistry glimpsed',
                       'the theatrical version vs the Snyder Cut comparison'],
    },
    'black-adam': {
        'director': 'Jaume Collet-Serra',
        'characters': ['Black Adam', 'Hawkman', 'Doctor Fate', 'Cyclone'],
        'themes': ['power without mercy vs power with justice', 'colonial oppression and liberation', 'anti-heroism'],
        'scenes': ["Black Adam's first rampage", 'Doctor Fate vs Sabbac', 'the end-credits scene'],
        'highlights': ["Dwayne Johnson's long-awaited role",
                       "Pierce Brosnan's Doctor Fate",
                       'the action spectacle'],
    },
    'the-flash-2023': {
        'director': 'Andy Muschietti',
        'characters': ['Barry Allen', 'Supergirl', 'Michael Keaton Batman'],
        'themes': ['altering the past and its consequences', 'letting go', 'the multiverse'],
        'scenes': ['the Speed Force opening', 'Batman vs the soldiers', 'the flashpoint reveal'],
        'highlights': ["Michael Keaton's beloved Batman return",
                       'Ezra Miller\'s dual performance',
                       'the emotional core of Barry and his mother'],
    },
}

# ===========================================================================
# REVIEW TEMPLATES
# ===========================================================================
# Reuse the film templates from add_movies.py for Marvel/DC
FILM_REVIEW_TEMPLATES = [
    {'title': 'One of the greatest films ever made',
     'body': "I've seen {name} multiple times now and it just keeps getting better. {highlight} is something rarely matched in cinema. If you haven't watched it yet, clear your evening.",
     'rating': 5},
    {'title': 'The ending absolutely floored me',
     'body': "{name} builds so carefully to its conclusion that when it arrives you feel genuinely moved. The {theme} thread pays off in a way that's earned rather than manipulative. Couldn't sleep afterward.",
     'rating': 5},
    {'title': 'Changed how I think about {theme}',
     'body': "I didn't expect {name} to affect me so deeply. The way {director} handles {theme} is unlike anything I'd seen before. I came out of it looking at the world differently.",
     'rating': 5},
    {'title': 'The {scene} is cinematic perfection',
     'body': "There are scenes in cinema you never forget. For me, {scene} in {name} is one of them. {director} constructs it with total precision and it lands exactly as intended. Pure craft.",
     'rating': 5},
    {'title': 'Better on second watch',
     'body': "I liked {name} when I first saw it, but the second viewing is where it clicked. Once you notice how {director} plants every detail early on, the whole film transforms. Layers everywhere.",
     'rating': 5},
    {'title': "Can't believe I waited this long to watch it",
     'body': "Everyone told me to watch {name} for years. Finally did and instantly understood why. {highlight} is immediately apparent. Now I'm recommending it just as loudly to everyone else.",
     'rating': 5},
    {'title': 'The score elevates every scene',
     'body': "The music in {name} is so deeply married to the images that you almost can't separate them. It stays in your head days later and when you hear it again the emotions return immediately.",
     'rating': 5},
    {'title': 'A career-best performance',
     'body': "Every actor brings something to {name}, but the lead performance is genuinely extraordinary. The subtlety involved, the way the character changes without announcing it — it's a masterclass.",
     'rating': 5},
    {'title': 'Hard to watch but impossible to look away',
     'body': "{name} deals with {theme} in a way that's genuinely uncomfortable at times. But that discomfort is the point. {director} never lets you look away, and the film is better for it.",
     'rating': 4},
    {'title': 'The {theme} theme resonates more as you get older',
     'body': "I first watched {name} as a teenager and thought it was fine. Rewatched at 30 and it hit completely differently. The {theme} undercurrent makes total sense now in a way it didn't before.",
     'rating': 5},
    {'title': 'Overrated but still very good',
     'body': "{name} has been praised so heavily that no film could live up completely. It's an excellent film — {highlight} is genuinely remarkable — but it's not the untouchable masterpiece some claim.",
     'rating': 4},
    {'title': 'Watched with my family — sparked an incredible conversation',
     'body': "We watched {name} together and spent an hour talking about {theme} afterward. That kind of conversation doesn't happen often. The film gives you something real to think about together.",
     'rating': 5},
    {'title': 'Not my genre but it completely won me over',
     'body': "I usually avoid this kind of film but gave {name} a chance after constant recommendations. Completely converted. {director} transcends genre entirely. It works as pure human drama first.",
     'rating': 5},
    {'title': 'The craft behind this film is astonishing',
     'body': "Every choice in {name} feels deliberate. The framing, the pacing, {scene} — {director} is operating at a level most filmmakers never reach. It's the kind of film you study rather than just watch.",
     'rating': 5},
    {'title': 'Stayed with me for weeks',
     'body': "{name} ended and I sat with it for weeks. The {theme} theme kept circling back. I'd be doing something mundane and {scene} would pop into my head. That kind of resonance is rare.",
     'rating': 5},
    {'title': 'The ending is divisive for a reason',
     'body': "{name} commits to a conclusion that not everyone will appreciate. I found it perfectly right — it refuses easy comfort. If you want tidy resolution you may be frustrated. If you want truth, it delivers.",
     'rating': 4},
    {'title': 'A film that demands your full attention',
     'body': "{name} is not background viewing. Every scene requires you. Put your phone down. {director} is doing too much to be half-watched. Give it the attention it deserves.",
     'rating': 5},
    {'title': 'Dated in some ways but still powerful',
     'body': "Some elements of {name} show their age, but the core of it — {theme}, {highlight} — hasn't diminished at all. Films this good age better than almost anything else.",
     'rating': 4},
    {'title': 'Disappointed given the reputation',
     'body': "{name} is technically accomplished and I understand its place in film history. But it left me cold. The {theme} element felt mechanical and I never connected emotionally. Maybe I'll try again.",
     'rating': 3},
    {'title': "Watched it blind and was blown away",
     'body': "I went into {name} knowing nothing — no trailer, no plot summary. I strongly recommend that approach. The {theme} hits much harder when you haven't been primed for it. Go in cold.",
     'rating': 5},
]

SHOW_REVIEW_TEMPLATES = [
    {'title': 'One of the greatest shows ever made',
     'body': "{name} is a masterclass in television storytelling. {creator}'s writing is meticulous — every episode builds towards something. The theme of {theme} runs through every storyline. A must-watch.",
     'rating': 5},
    {'title': 'Binge-watched the whole thing in a week',
     'body': "I started {name} thinking I'd watch an episode or two. Three sleepless nights later I'd finished the entire run. {highlight} is just unmatched. {character} is one of the great characters in TV history.",
     'rating': 5},
    {'title': 'Changed how I think about television drama',
     'body': "{name} showed me what television can do. The {theme} storyline is handled with more intelligence than most films. {highlight} elevates the whole thing. Required viewing for anyone who cares about storytelling.",
     'rating': 5},
    {'title': 'The writing is extraordinary',
     'body': "Every line of dialogue in {name} has purpose. {creator} and the writers\' room craft scenes where subtext carries more weight than text. The episode {episode} is one of the best hours of television I've ever seen.",
     'rating': 5},
    {'title': "Doesn't disappoint at any point",
     'body': "There are no filler episodes in {name}. Every single hour justifies its existence. {character} has one of the great character arcs in television. I've already rewatched it twice.",
     'rating': 5},
    {'title': 'A bit overhyped but still very good',
     'body': "{name} lives up to maybe 80% of the hype. {highlight} is genuinely excellent. The {theme} element is well done. My only complaint is that things drag slightly in the middle. Still four stars.",
     'rating': 4},
    {'title': 'Slow start but rewards patience',
     'body': "{name} takes a few episodes to find its feet. By the time you reach {episode}, you understand what the show is going for. {creator} has a long game in mind and it pays off beautifully.",
     'rating': 4},
    {'title': 'Absolutely gripping from start to finish',
     'body': "I haven't been this invested in characters since I was a kid. {character} is brilliantly written — you understand exactly why they make terrible decisions. {highlight} is the best part of an already excellent show.",
     'rating': 5},
    {'title': 'Excellent ensemble cast',
     'body': "What makes {name} special is how every character feels fully realised. Not just {character} — even the minor characters have depth. {creator} clearly spent years thinking about this world.",
     'rating': 5},
    {'title': 'Some dips but overall a classic',
     'body': "{name} has a few uneven episodes across its run but the high points are some of the best television ever made. {episode} alone is worth the subscription. {theme} is explored in genuinely surprising ways.",
     'rating': 4},
    {'title': 'The finale actually delivered',
     'body': "So many shows fail their endings. {name} stuck the landing. The final episode resolves {character}'s arc in a way that feels both surprising and inevitable. {creator} clearly knew where this was going from episode one.",
     'rating': 5},
    {'title': 'Perfect for bingeing',
     'body': "Every episode of {name} ends at exactly the right moment to make you immediately start the next one. {highlight} is addictive in the best possible way. I finished the whole run in four days.",
     'rating': 5},
    {"title": "One of the decade's defining shows",
     'body': "{name} will be talked about in TV history discussions for decades. The way it handles {theme} is mature, nuanced, and unflinching. {character} is one of the most complex characters ever written for television.",
     'rating': 5},
    {'title': 'Genuinely difficult to watch at times — in a good way',
     'body': "{name} doesn't let you off the hook. {highlight} is genuinely uncomfortable in ways few shows dare to be. It respects the audience's intelligence. {episode} is just astonishing television.",
     'rating': 5},
    {'title': 'The acting is what makes it',
     'body': "{character} is played with incredible subtlety. You believe every choice they make even when those choices are catastrophic. {highlight} is a big reason this show rose above its peers.",
     'rating': 5},
    {'title': 'Good but not the greatest ever',
     'body': "{name} is excellent television but I wouldn't rank it as the all-time greatest. {highlight} is legitimately fantastic but some middle episodes lose momentum. Worth watching absolutely, just with tempered expectations.",
     'rating': 4},
    {'title': 'Rewatchable from the very first episode',
     'body': "Knowing how {name} ends makes the early episodes even more rewarding. {creator} plants seeds so subtly you don't notice them until the second watch. {character}'s journey hits harder when you know where it leads.",
     'rating': 5},
    {'title': 'The world-building is unmatched',
     'body': "{name} creates a world so fully realised that every detail feels intentional. The rules are consistent, the consequences are real. {theme} gives the whole world a moral weight that most shows lack entirely.",
     'rating': 5},
]

CARTOON_REVIEW_TEMPLATES = [
    {'title': 'Far more than just a cartoon',
     'body': "{name} is one of those shows you can't believe was made for children. The themes of {theme} are handled with more depth than most adult dramas. {creator}'s vision is unmistakable.",
     'rating': 5},
    {'title': 'Grew up with this show and it holds up',
     'body': "I watched {name} as a kid and rewatched it as an adult. It's even better the second time. {highlight} is only apparent when you're older. {character} remains one of the great animated characters.",
     'rating': 5},
    {'title': 'The writing is genuinely brilliant',
     'body': "{name} works on two levels: kids get the surface entertainment and adults get the subtext. {creator}'s writing treats its audience with respect. The episode {episode} is as good as any live-action drama.",
     'rating': 5},
    {'title': 'Changed what animation could be',
     'body': "{name} pushed the boundaries of what animated storytelling could do. The exploration of {theme} was groundbreaking for its medium. I still think about {character}'s arc regularly.",
     'rating': 5},
    {'title': 'Surprisingly emotional for an animated show',
     'body': "I did not expect {name} to make me cry but here we are. {episode} hit me completely off guard. {character} is written with such care that the emotional moments land with full weight.",
     'rating': 5},
    {'title': 'Funny and smart in equal measure',
     'body': "{name} manages to be both laugh-out-loud funny and genuinely insightful. {highlight} gives the show a comedic engine that never gets old. {creator} understood that smart humour and broad comedy can coexist.",
     'rating': 5},
    {'title': 'An all-time classic of the genre',
     'body': "Ask anyone to name the best animated shows ever made and {name} will be on every list. {character} is one of animation's great characters. The {theme} theme gives it lasting relevance.",
     'rating': 5},
    {'title': 'Perfect balance of fun and substance',
     'body': "You can watch {name} for pure entertainment or for something more meaningful. Either way you win. {creator}'s ability to layer complexity into seemingly simple stories is remarkable. {highlight} is evidence of a master.",
     'rating': 5},
    {'title': 'The animation style is iconic',
     'body': "{name} has a visual identity so distinctive that you can recognise it from a single frame. {creator} worked with artists who understood that style should reflect substance. The look of the show embodies {theme}.",
     'rating': 4},
    {'title': 'Got better with every season',
     'body': "{name} started strong and only improved. By season two, {creator} had found a confidence that made the show feel inevitable. {episode} is one of the finest episodes in animated television history.",
     'rating': 5},
    {'title': 'A little dated but still charming',
     'body': "{name} shows its age in places but the core of what made it special remains. {highlight} is still funny and {character} is still endearing. Some references land flat now but the heart is intact.",
     'rating': 3},
    {'title': 'The characters carry everything',
     'body': "What makes {name} work is the characters. {character} is one of the most fully realised animated personalities ever created. {creator} gave them enough depth that their choices always feel meaningful.",
     'rating': 5},
    {'title': 'Rewatching with my kids now',
     'body': "I grew up with {name} and now I'm watching it with my own children. They love it as much as I did. {highlight} is just as effective the twentieth time. True classics work across generations.",
     'rating': 5},
    {'title': 'Not perfect but close enough',
     'body': "{name} has a few weak episodes scattered through its run but the high points more than compensate. {character}'s storyline is beautifully handled. {creator} had a rare clarity of vision for the whole series.",
     'rating': 4},
    {'title': 'Underrated gem',
     'body': "More people should watch {name}. It never got the cultural attention it deserved while it was airing. {highlight} is genuinely brilliant and the {theme} exploration is more sophisticated than most prestige live-action drama.",
     'rating': 5},
]

ANIME_REVIEW_TEMPLATES = [
    {'title': 'My gateway into anime — still the best',
     'body': "{name} was the first anime I watched and it set an impossibly high standard. The story of {character} explores {theme} with a maturity I didn't expect. I've watched dozens of anime since and this remains the peak.",
     'rating': 5},
    {'title': 'A masterpiece of the medium',
     'body': "{name} isn't just a great anime — it's a great work of fiction full stop. {creator}'s storytelling is dense, emotional, and intellectually rigorous. The theme of {theme} is handled with genuine philosophical depth.",
     'rating': 5},
    {'title': 'The animation quality is breathtaking',
     'body': "{name} raises the bar for what anime can look like. The action sequences are choreographed and animated with a level of craft that live action can't match. {highlight} is jaw-dropping every single time.",
     'rating': 5},
    {'title': 'Changed the way I think about storytelling',
     'body': "{name} took narrative risks that paid off completely. {creator}'s willingness to subvert expectations while honouring its themes makes it genuinely original. The {episode} arc is one of the great story arcs in all of fiction.",
     'rating': 5},
    {'title': 'The characters are incredibly well written',
     'body': "{character}'s development across the series is one of the most convincing character journeys I've experienced. You understand every choice even when you disagree with it. {highlight} makes the whole thing click.",
     'rating': 5},
    {'title': 'Non-anime fans should give this a chance',
     'body': "I always skipped anime. A friend made me watch {name} and now I understand the fuss. {theme} is explored in ways that make Western animation feel shallow by comparison. Just try it.",
     'rating': 5},
    {'title': 'Emotionally devastating in the best way',
     'body': "{name} has moments that hit harder than any film I've seen this year. {episode} completely wrecked me. {creator} has an understanding of grief, hope and the human condition that is genuinely exceptional.",
     'rating': 5},
    {'title': 'The world-building is extraordinary',
     'body': "{name} creates a world with its own logic, history, and rules. Everything is internally consistent. The way {theme} shapes the world's politics and relationships is incredibly thoughtful. {highlight} is the payoff to years of setup.",
     'rating': 5},
    {'title': 'Worth tolerating the filler for',
     'body': "{name} has some filler episodes that slow the pacing. Get past them. The story arcs surrounding {episode} are worth every minute of slower content. The best parts are genuinely great.",
     'rating': 4},
    {'title': 'Perfect introduction to its genre',
     'body': "If someone wants to understand what makes anime special, I recommend {name} first. It demonstrates everything: the visual storytelling, the emotional range, the commitment to character. {highlight} is the best single example.",
     'rating': 5},
    {'title': 'Surprisingly philosophical',
     'body': "{name} uses its genre conventions to explore {theme} in genuinely surprising ways. {creator}'s work rewards careful attention. There are layers here that only reveal themselves on rewatch.",
     'rating': 5},
    {'title': 'The soundtrack alone is worth the watch',
     'body': "{name} has one of the great anime soundtracks. The music elevates emotional scenes to something transcendent. {highlight} is made three times more impactful by the score. {creator} clearly understood how music and image work together.",
     'rating': 5},
    {'title': 'Brilliant from episode one',
     'body': "{name} establishes its world, characters, and stakes within the first three episodes. There's no wasted time. {character} is immediately compelling and {theme} is clearly defined. A sign of confident purposeful writing.",
     'rating': 5},
    {'title': 'The villain is unforgettable',
     'body': "Great stories need great antagonists. {name}'s villain understands that the most compelling opposition comes from someone with internally coherent logic. The conflict between {character} and the antagonist is one of the great rivalries.",
     'rating': 5},
    {'title': 'Has its flaws but transcends them',
     'body': "{name} isn't perfect. The pacing sags occasionally and some characters are underwritten. But when it fires on all cylinders — as in {episode} — it reaches heights that few shows ever achieve. The flaws are forgiven.",
     'rating': 4},
]

FIRST_NAMES = [
    'Emma', 'Liam', 'Olivia', 'Noah', 'Ava', 'Ethan', 'Sophia', 'Mason',
    'Isabella', 'James', 'Mia', 'Logan', 'Charlotte', 'Lucas', 'Amelia',
    'Jackson', 'Harper', 'Aiden', 'Evelyn', 'Sebastian', 'Abigail', 'Mateo',
    'Emily', 'Jack', 'Elizabeth', 'Owen', 'Sofia', 'Henry', 'Avery', 'Samuel',
    'Ella', 'Elijah', 'Madison', 'Daniel', 'Scarlett', 'Benjamin', 'Victoria',
    'Dylan', 'Grace', 'Michael', 'Chloe', 'Jayden', 'Penelope', 'Ryan',
    'Marcus', 'Diana', 'Derek', 'Priya', 'Kenji', 'Fatima', 'Carlos', 'Ingrid',
    'Yuki', 'Aleksei', 'Zara', 'Finn', 'Niamh', 'Rafael', 'Leila', 'Connor',
]


def random_author():
    return random.choice(FIRST_NAMES)


def make_film_review(name, slug, data_dict, tmpl):
    data = data_dict.get(slug, {})
    director = data.get('director', 'the director')
    characters = data.get('characters', ['the main character'])
    themes = data.get('themes', ['identity', 'survival', 'justice'])
    scenes = data.get('scenes', ['the opening scene', 'the climax', 'the final moment'])
    highlights = data.get('highlights', ['the performances', 'the direction', 'the script'])
    title = tmpl['title'].format(
        name=name, theme=random.choice(themes), scene=random.choice(scenes),
        director=director, highlight=random.choice(highlights),
    )
    body = tmpl['body'].format(
        name=name, director=director,
        character=random.choice(characters),
        theme=random.choice(themes),
        scene=random.choice(scenes),
        highlight=random.choice(highlights),
    )
    return title, body, tmpl['rating']


def make_show_review(name, slug, data_dict, tmpl):
    data = data_dict.get(slug, {})
    creator = data.get('creator', 'the creator')
    characters = data.get('characters', ['the main character'])
    themes = data.get('themes', ['identity', 'survival', 'justice'])
    episodes = data.get('episodes', ['the pilot', 'the midseason finale', 'the finale'])
    highlights = data.get('highlights', ['the performances', 'the direction', 'the script'])
    title = tmpl['title'].format(
        name=name, theme=random.choice(themes), episode=random.choice(episodes),
        creator=creator, highlight=random.choice(highlights), character=random.choice(characters),
    )
    body = tmpl['body'].format(
        name=name, creator=creator,
        character=random.choice(characters),
        theme=random.choice(themes),
        episode=random.choice(episodes),
        highlight=random.choice(highlights),
    )
    return title, body, tmpl['rating']


# ---------------------------------------------------------------------------
# Wikipedia helpers
# ---------------------------------------------------------------------------
def wiki_image(title, width=500):
    """Try REST summary API first, fall back to pageimages."""
    import urllib.parse
    encoded = urllib.parse.quote(title.replace(' ', '_'))
    try:
        r = SESSION.get(f'https://en.wikipedia.org/api/rest_v1/page/summary/{encoded}',
                        timeout=12)
        if r.status_code == 200:
            thumb = r.json().get('thumbnail', {}).get('source')
            if thumb:
                return thumb
    except Exception:
        pass
    # Fallback: pageimages API
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
# Core seeding function
# ---------------------------------------------------------------------------
def seed_subcat(cat, sc_name, sc_slug, subjects_list, subject_data, templates,
                make_review_fn, wiki_cat_article, pros, cons):
    from datetime import datetime, timedelta

    sc = SubCategory.query.filter_by(category_id=cat.id, slug=sc_slug).first()
    if sc:
        print(f'Subcategory exists: {sc_name}')
    else:
        sc = SubCategory(category_id=cat.id, name=sc_name, slug=sc_slug,
                         pros=pros, cons=cons)
        db.session.add(sc)
        db.session.flush()
        print(f'Created subcategory: {sc_name}')

        # Subcategory tile image
        img_url = wiki_image(wiki_cat_article)
        if img_url:
            ext = img_url.split('.')[-1].split('?')[0].lower()
            if ext not in ('jpg', 'jpeg', 'png', 'webp', 'gif'):
                ext = 'jpg'
            fname = f'{sc_slug}-subcat.{ext}'
            dest = os.path.join(STATIC_DIR, 'images', 'uploads', 'subcategories', fname)
            if download(img_url, dest):
                sc.image_path = f'images/uploads/subcategories/{fname}'
                print(f'  subcat image saved: {fname}')
        db.session.commit()

    total_subjects = 0
    total_reviews = 0

    for entry in subjects_list:
        subj_name, subj_slug, wiki_title, year = entry
        subj = Subject.query.filter_by(subcategory_id=sc.id, slug=subj_slug).first()
        if subj:
            print(f'  Skipping {subj_name} (exists)')
            continue

        display_name = f'{subj_name} ({year})'
        subj = Subject(subcategory_id=sc.id, name=display_name, slug=subj_slug)
        db.session.add(subj)
        db.session.flush()

        # Image
        img_url = wiki_image(wiki_title)
        if img_url:
            ext = img_url.split('.')[-1].split('?')[0].lower()
            if ext not in ('jpg', 'jpeg', 'png', 'webp', 'gif'):
                ext = 'jpg'
            fname = f'{sc_slug}-{subj_slug}.{ext}'
            dest = os.path.join(STATIC_DIR, 'images', 'uploads', 'subjects', fname)
            if download(img_url, dest):
                subj.image_path = f'images/uploads/subjects/{fname}'
                print(f'  img ok: {subj_name}')
            else:
                print(f'  no img: {subj_name}')
        else:
            print(f'  no img: {subj_name}')
        time.sleep(0.8)

        # Reviews
        target = random.randint(12, 25)
        used_titles = set()
        reviews_added = 0
        shuffled = templates[:]
        random.shuffle(shuffled)

        for tmpl in shuffled * 4:
            if reviews_added >= target:
                break
            try:
                title, body, base_rating = make_review_fn(subj_name, subj_slug, subject_data, tmpl)
            except KeyError:
                continue
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
        print(f'  {subj_name} ({year}): {reviews_added} reviews')

    db.session.commit()
    print(f'  → {sc_name}: {total_subjects} subjects, {total_reviews} reviews\n')


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    app = create_app()
    with app.app_context():
        cat = Category.query.filter_by(slug='movies').first()
        if not cat:
            print('ERROR: Movies category not found. Run add_movies.py first.')
            return

        print('=== Top Shows ===')
        seed_subcat(
            cat, 'Top Shows', 'top-shows',
            SHOWS, SHOW_DATA, SHOW_REVIEW_TEMPLATES, make_show_review,
            'Television show',
            'Epic\nDeep\nBingeable',
            'Long\nWait\nHype',
        )

        print('=== Top Cartoons ===')
        seed_subcat(
            cat, 'Top Cartoons', 'top-cartoons',
            CARTOONS, CARTOON_DATA, CARTOON_REVIEW_TEMPLATES, make_show_review,
            'Animation',
            'Fun\nTimeless\nCreative',
            'Repetitive\nAdult\nVaried',
        )

        print('=== Top Anime ===')
        seed_subcat(
            cat, 'Top Anime', 'top-anime',
            ANIME, ANIME_DATA, ANIME_REVIEW_TEMPLATES, make_show_review,
            'Anime',
            'Unique\nDeep\nVisual',
            'Subtitles\nFiller\nLong',
        )

        print('=== Top Marvel ===')
        seed_subcat(
            cat, 'Top Marvel', 'top-marvel',
            MARVEL_FILMS, MARVEL_DATA, FILM_REVIEW_TEMPLATES, make_film_review,
            'Marvel Cinematic Universe',
            'Action\nFun\nConnected',
            'Formula\nCGI\nFatigue',
        )

        print('=== Top DC ===')
        seed_subcat(
            cat, 'Top DC', 'top-dc',
            DC_FILMS, DC_DATA, FILM_REVIEW_TEMPLATES, make_film_review,
            'DC Extended Universe',
            'Dark\nIconic\nRich',
            'Uneven\nGrimm\nChaos',
        )

        print('All done.')


if __name__ == '__main__':
    main()
