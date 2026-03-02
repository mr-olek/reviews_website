#!/usr/bin/env python3
"""
Replace generic template reviews for Sports with specific, data-driven
reviews referencing real techniques, athletes, gear, competitions, and training concepts.

Usage:
  python3 generate_sports_reviews.py               # all sports
  python3 generate_sports_reviews.py --slug boxing # single sport
  python3 generate_sports_reviews.py --start-from crossfit  # resume
  python3 generate_sports_reviews.py --count 15    # reviews per sport (default 15)
"""
from __future__ import annotations
import argparse, os, random, sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# Sport-specific facts
# ---------------------------------------------------------------------------
SPORT_DATA = {
    'muay-thai': {
        'techniques':   ['teep push kick', 'roundhouse kick', 'elbow strikes', 'clinch work', 'knee strikes', 'switch kick'],
        'concepts':     ['eight limbs', 'reading distance', 'timing counters', 'pad work', 'shadowboxing', 'sparring rounds'],
        'gear':         ['shin guards', 'Muay Thai gloves', 'hand wraps', 'mouth guard', 'shorts', 'heavy bag'],
        'athletes':     ['Saenchai', 'Buakaw', 'Dieselnoi', 'Jongsanan', 'Lerdsila'],
        'highlights':   ['full-body conditioning', 'mental toughness under pressure', 'the clinch game opening up', 'hitting pads with a good coach'],
        'challenges':   ['shin conditioning', 'finding quality sparring partners', 'the clinch learning curve'],
    },
    'brazilian-jiu-jitsu': {
        'techniques':   ['guard passing', 'triangle choke', 'rear naked choke', 'armbar', 'kimura', 'De La Riva guard', 'X-guard sweeps'],
        'concepts':     ['positional hierarchy', 'rolling', 'tapping out', 'drilling', 'open mat', 'stripe promotions'],
        'gear':         ['gi', 'no-gi rashguard and shorts', 'mouthguard', 'ear guards', 'knee sleeves'],
        'athletes':     ['Roger Gracie', 'Gordon Ryan', 'Marcelo Garcia', 'Bernardo Faria', 'Mikey Musumeci'],
        'highlights':   ['the chess-like mental game', 'how technique genuinely beats strength', 'community at open mat', 'first competition experience'],
        'challenges':   ['ego adjustment in early rolling sessions', 'cauliflower ear risk without ear guards', 'finding a reputable Gracie lineage gym'],
    },
    'karate': {
        'techniques':   ['gyaku-zuki reverse punch', 'mawashi-geri roundhouse', 'oi-zuki lunge punch', 'gedan-barai lower block', 'shuto-uke knife-hand', 'kata Heian Shodan'],
        'concepts':     ['kihon basics', 'kata forms', 'kumite sparring', 'kime', 'zanshin awareness', 'dojo etiquette'],
        'gear':         ['gi (karategi)', 'belt', 'sparring gloves', 'foot protectors', 'mouth guard'],
        'athletes':     ['Ryutaro Araga', 'Sandra Sanchez', 'Antonio Diaz', 'Sajad Ganjzadeh', 'Damian Quintero'],
        'highlights':   ['the meditative quality of kata practice', 'how kime transforms every strike', 'the belt grading ceremony', 'kumite opening up after basics click'],
        'challenges':   ['kata memorisation', 'developing real kime under pressure', 'the split between traditional and sport karate schools'],
    },
    'boxing': {
        'techniques':   ['jab-cross combination', 'left hook', 'body shot', 'uppercut', 'slipping punches', 'footwork', 'the jab as a range finder'],
        'concepts':     ['southpaw stance', 'head movement', 'working the body', 'ring generalship', 'punch output', 'feinting'],
        'gear':         ['boxing gloves', 'hand wraps', 'headgear', 'mouthguard', 'jump rope', 'heavy bag', 'speed bag'],
        'athletes':     ['Muhammad Ali', 'Sugar Ray Leonard', 'Floyd Mayweather', 'Vasyl Lomachenko', 'Canelo Álvarez'],
        'highlights':   ['the meditative focus of bag work', 'how the jab controls a whole fight', 'sparring building real confidence', 'first amateur bout experience'],
        'challenges':   ['developing instinctive head movement', 'inconsistent gym culture', 'hand injuries from poor wrapping technique'],
    },
    'mma': {
        'techniques':   ['double-leg takedown', 'guard passing', 'ground and pound', 'Muay Thai clinch', 'guillotine choke', 'cage work'],
        'concepts':     ['grappling vs. striking balance', 'cage control', 'transitions', 'scrambles', 'wrestling base'],
        'gear':         ['MMA gloves', 'shin guards', 'mouthguard', 'groin guard', 'rashguard', 'shorts'],
        'athletes':     ['Khabib Nurmagomedov', 'Jon Jones', 'Georges St-Pierre', 'Anderson Silva', 'Demetrious Johnson'],
        'highlights':   ['how everything connects into one system', 'takedown defence becoming instinctive', 'the cage fitness level', 'first amateur fight'],
        'challenges':   ['managing multiple disciplines simultaneously', 'the higher injury rate vs. single-discipline training', 'finding a gym with quality striking and grappling coaches'],
    },
    'judo': {
        'techniques':   ['o-soto-gari', 'seoi-nage shoulder throw', 'uchi-mata', 'tai-otoshi', 'harai-goshi', 'osoto-otoshi', 'newaza ground work'],
        'concepts':     ['kuzushi off-balance', 'grip fighting', 'ippon', 'randori', 'shiai competition', 'nage-waza throwing techniques'],
        'gear':         ['judogi', 'belt', 'ear guards for groundwork sessions'],
        'athletes':     ['Teddy Riner', 'Shohei Ono', 'Daria Bilodid', 'Ilias Iliadis', 'Yasuhiro Yamashita'],
        'highlights':   ['landing a clean ippon throw', 'grip fighting becoming its own game', 'how hip positioning changes everything', 'the judo community warmth'],
        'challenges':   ['grip fighting exhaustion', 'trusting breakfalling (ukemi) instinctively', 'finding competitive clubs outside Japan or France'],
    },
    'kickboxing': {
        'techniques':   ['jab-cross-kick combination', 'switch kick', 'body kick', 'spinning back kick', 'question mark kick', 'lead leg teep'],
        'concepts':     ['punching range vs. kicking range', 'setting up kicks with punches', 'checking leg kicks', 'counter-striking'],
        'gear':         ['boxing gloves', 'shin guards', 'hand wraps', 'mouthguard', 'headgear for sparring'],
        'athletes':     ['Giorgio Petrosyan', 'Sittichai Sitsongpeenong', 'Superbon', 'Robin van Roosmalen', 'Andy Souwer'],
        'highlights':   ['how kicks extend your reach and change fight dynamics', 'the cardio from three-minute rounds', 'landing a clean body kick', 'K-1 rules learning'],
        'challenges':   ['shin conditioning', 'the counterintuitive feel of catching kicks', 'timing kicks within combinations'],
    },
    'wrestling': {
        'techniques':   ['single-leg takedown', 'double-leg', 'sprawl', 'front headlock', 'cradle pin', 'hip toss', 'stand-up from bottom'],
        'concepts':     ['level change', 'penetration step', 'mat returns', 'riding time', 'scrambles', 'chain wrestling'],
        'gear':         ['wrestling shoes', 'singlet', 'headgear', 'knee pads', 'mouth guard'],
        'athletes':     ['Aleksandr Karelin', 'John Smith', 'Cael Sanderson', 'Jordan Burroughs', 'Kyle Snyder'],
        'highlights':   ['the explosive athleticism wrestling builds', 'scrambles becoming instinctive', 'how it transfers to every other grappling art', 'live drilling intensity'],
        'challenges':   ['cauliflower ear without headgear', 'mat burn management', 'finding adult beginner classes outside the US'],
    },
    'taekwondo': {
        'techniques':   ['back kick', 'spinning heel kick', 'axe kick', 'jump spinning back kick', 'dollyo-chagi roundhouse', 'push kick'],
        'concepts':     ['point scoring system', 'hogu body protector sparring', 'poomsae forms', 'pattern memorisation', 'reaction time training'],
        'gear':         ['dobok', 'hogu chest protector', 'helmet', 'forearm guards', 'shin guards', 'groin guard'],
        'athletes':     ['Steven Lopez', 'Jade Jones', 'Dae-hoon Lee', 'Bianca Walkden', 'Milica Mandić'],
        'highlights':   ['the unique acrobatic kick repertoire', 'how poomsae develops balance and body control', 'Olympic competition format understanding', 'first sparring session'],
        'challenges':   ['underdeveloped hand techniques relative to kicks', 'adjusting to the point-scoring system', 'finding gyms that teach self-defence alongside sport'],
    },
    'weightlifting': {
        'techniques':   ['snatch', 'clean and jerk', 'overhead squat', 'power clean', 'front squat', 'jerk footwork'],
        'concepts':     ['triple extension', 'third pull under the bar', 'receiving position', 'bar path', 'cat stretch', 'percentages and programming'],
        'gear':         ['weightlifting shoes', 'belt', 'knee sleeves', 'wrist wraps', 'chalk', 'competition barbell'],
        'athletes':     ['Lasha Talakhadze', 'Pyrros Dimas', 'Naim Süleymanoğlu', 'Matthias Steiner', 'Lu Xiaojun'],
        'highlights':   ['landing a perfect snatch', 'how the sport rewards technique over brute strength', 'the full-body explosion it develops', 'the moment the third pull clicks'],
        'challenges':   ['mobility requirements for beginners', 'technique-before-loading discipline', 'finding quality coaching outside specialist gyms'],
    },
    'powerlifting': {
        'techniques':   ['low-bar squat', 'sumo deadlift', 'bench press pause', 'hip hinge', 'leg drive in bench', 'bracing and Valsalva'],
        'concepts':     ['the big three', 'total', 'wilks score', 'RPE-based programming', 'peaking for a meet', 'weight classes'],
        'gear':         ['powerlifting belt', 'knee sleeves', 'wrist wraps', 'deadlift socks', 'singlet', 'squat shoes'],
        'athletes':     ['Ed Coan', 'Cailer Woolam', 'Ray Williams', 'Stefi Cohen', 'Jessie Norris'],
        'highlights':   ['the clarity of chasing three measurable numbers', 'competition day atmosphere', 'how the big three build total-body strength', 'hitting a three-white-light total'],
        'challenges':   ['injury risk at heavy loading', 'learning to brace and Valsalva properly', 'gear costs adding up'],
    },
    'crossfit': {
        'techniques':   ['kipping pull-up', 'muscle-up', 'double-unders', 'wall balls', 'toes-to-bar', 'Olympic lifting in metcons'],
        'concepts':     ['WOD', 'AMRAP', 'EMOM', 'Fran', 'Murph', 'benchmark workouts', 'box culture'],
        'gear':         ['CrossFit shoes', 'jump rope', 'gymnastics grips', 'knee sleeves', 'belt for heavy days', 'chalk'],
        'athletes':     ['Mat Fraser', 'Tia-Clair Toomey', 'Rich Froning', 'Katrin Davidsdóttir', 'Patrick Vellner'],
        'highlights':   ['the community atmosphere in a good box', 'how varied the programming keeps you engaged', 'first muscle-up milestone', 'Open season competition'],
        'challenges':   ['kipping movements causing injury if rushed', 'cult-like culture in some boxes', 'membership costs vs. regular gyms'],
    },
    'bodybuilding': {
        'techniques':   ['mind-muscle connection', 'progressive overload', 'drop sets', 'supersets', 'peak week water manipulation', 'posing'],
        'concepts':     ['hypertrophy training', 'cutting and bulking phases', 'macros tracking', 'symmetry and proportion', 'stage presence', 'natural vs. enhanced'],
        'gear':         ['posing trunks/suit', 'tanning products', 'competition heels (women)', 'resistance bands', 'cable machines'],
        'athletes':     ['Arnold Schwarzenegger', 'Ronnie Coleman', 'Lee Haney', 'Chris Bumstead', 'Iris Kyle'],
        'highlights':   ['how posing transforms the look of your physique', 'peak week when everything comes together', 'stepping on stage for the first time', 'the discipline it builds around nutrition'],
        'challenges':   ['the physical and mental brutality of peak week', 'subjective judging criteria', 'limited prize money in natural shows'],
    },
    'rock-climbing': {
        'techniques':   ['footwork precision', 'heel hooks', 'smearing', 'dynos', 'mantling', 'crack climbing', 'route reading'],
        'concepts':     ['bouldering', 'sport climbing', 'trad climbing', 'V-grades', 'French sport grades', 'projecting a route', 'redpoint'],
        'gear':         ['climbing shoes', 'harness', 'belay device', 'chalk bag', 'quickdraws', 'crash pad for bouldering'],
        'athletes':     ['Alex Honnold', 'Adam Ondra', 'Ashima Shiraishi', 'Janja Garnbret', 'Tommy Caldwell'],
        'highlights':   ['how footwork transforms everything', 'sending a project after weeks of effort', 'the outdoor climbing community', 'how it builds problem-solving under pressure'],
        'challenges':   ['finger injury risk', 'expensive trad climbing gear', 'fear of heights even indoors at first'],
    },
    'swimming': {
        'techniques':   ['flip turns', 'bilateral breathing', 'high elbow catch', 'underwater dolphin kicks', 'open water sighting', 'butterfly timing'],
        'concepts':     ['stroke efficiency over power', 'interval sets', 'pull buoy drills', 'drafting in open water', 'pace per 100m', 'tapering'],
        'gear':         ['tech suit', 'goggles', 'pull buoy', 'fins', 'paddles', 'swim cap', 'training watch'],
        'athletes':     ['Michael Phelps', 'Katie Ledecky', 'Ian Thorpe', 'Caeleb Dressel', 'Sarah Sjöström'],
        'highlights':   ['the meditative quality of long sets', 'flip turns becoming automatic', 'the full-body fatigue after a hard set', 'open water swimming freedom'],
        'challenges':   ['technique errors entrenching without coaching', 'lane etiquette with unwritten rules', 'pool access and early morning scheduling'],
    },
    'running': {
        'techniques':   ['cadence', 'midfoot strike', 'arm swing efficiency', 'hill running form', 'negative splitting', 'tempo effort'],
        'concepts':     ['easy aerobic base', 'threshold runs', 'interval training', 'long run', 'periodisation', 'marathon fuelling strategy'],
        'gear':         ['road shoes', 'trail shoes', 'GPS watch', 'foam roller', 'compression socks', 'hydration vest'],
        'athletes':     ['Eliud Kipchoge', 'Kelvin Kiptum', 'Sifan Hassan', 'Kilian Jornet', 'Courtney Dauwalter'],
        'highlights':   ['the meditative state of long easy runs', 'race day energy at a marathon', 'negative splitting a goal race', 'trail running scenery'],
        'challenges':   ['the high injury rate', 'easy pace feeling embarrassingly slow at first', 'overtraining temptation before a goal race'],
    },
    'cycling': {
        'techniques':   ['cadence over gear', 'descending technique', 'drafting in a group', 'climbing seated vs. standing', 'cleat positioning', 'cornering'],
        'concepts':     ['FTP', 'watts per kilo', 'group ride etiquette', 'bonking and fuelling', 'periodised training blocks', 'tubeless tyres'],
        'gear':         ['road bike', 'cycling shoes and cleats', 'helmet', 'kit (bibs and jersey)', 'GPS head unit', 'power meter'],
        'athletes':     ['Tadej Pogačar', 'Jonas Vingegaard', 'Marianne Vos', 'Eddy Merckx', 'Mathieu van der Poel'],
        'highlights':   ['the freedom of long endurance rides', 'first sportive completion', 'descending a mountain pass smoothly', 'the group ride dynamic'],
        'challenges':   ['expensive initial gear investment', 'car traffic safety concerns', 'saddle soreness in the early weeks'],
    },
    'tennis': {
        'techniques':   ['topspin forehand', 'slice backhand', 'serve and volley', 'drop shot', 'kick serve', 'inside-out forehand'],
        'concepts':     ['rally depth', 'approaching the net', 'reading the opponent\'s racket face', 'serve placement patterns', 'clay vs. hard court adjustments'],
        'gear':         ['racket', 'strings and tension', 'court shoes', 'overgrips', 'dampener', 'tennis bag'],
        'athletes':     ['Roger Federer', 'Rafael Nadal', 'Novak Djokovic', 'Serena Williams', 'Carlos Alcaraz'],
        'highlights':   ['how topspin changes the game once learned', 'match play sharpening everything fast', 'the tactical cat-and-mouse of a close set', 'first club competition'],
        'challenges':   ['serve coordination taking months', 'the racket and string selection rabbit hole', 'booking court time at busy clubs'],
    },
    'basketball': {
        'techniques':   ['triple threat position', 'pick and roll', 'crossover dribble', 'pull-up jumper', 'euro step', 'post up footwork'],
        'concepts':     ['floor spacing', 'defensive rotations', 'shot clock awareness', 'pick and roll coverage', 'IQ vs. athleticism'],
        'gear':         ['basketball shoes', 'shorts and jersey', 'compression tights', 'mouthguard', 'ankle braces'],
        'athletes':     ['Michael Jordan', 'LeBron James', 'Steph Curry', 'Giannis Antetokounmpo', 'Nikola Jokić'],
        'highlights':   ['the flow state of a good shooting session', 'team chemistry in a pickup game', 'breaking down defenders with dribble moves', 'the pick and roll clicking in a real game'],
        'challenges':   ['ankle injury risk', 'height disadvantage in some positions', 'cliquey pickup game culture at busy courts'],
    },
    'yoga': {
        'techniques':   ['chaturanga', 'downward dog alignment', 'Warrior II hip positioning', 'pranayama breathwork', 'savasana', 'headstand prep'],
        'concepts':     ['vinyasa flow', 'yin yoga', 'Ashtanga primary series', 'drishti gaze point', 'bandhas', 'ahimsa', 'the eight limbs of yoga'],
        'gear':         ['yoga mat', 'blocks', 'strap', 'bolster', 'yoga towel', 'comfortable breathable clothing'],
        'athletes':     ['B.K.S. Iyengar', 'Sri K. Pattabhi Jois', 'Adriene Mishler', 'Dharma Mittra', 'Seane Corn'],
        'highlights':   ['how breathwork calms the nervous system', 'the mental stillness of a strong yin practice', 'hip opening unlocking new poses', 'the shift from physical exercise to practice'],
        'challenges':   ['wrist pain before building sufficient strength', 'hot yoga overwhelming some beginners', 'pretentious studio culture'],
    },
}

# ---------------------------------------------------------------------------
# Review templates
# ---------------------------------------------------------------------------
TEMPLATES = [
    {
        'title_tmpl': 'Six months of {name} — here is what actually changed',
        'body_tmpl': (
            "I started {name} six months ago with zero background in the sport. The first few weeks were humbling — "
            "I couldn't do {technique} properly and had no idea what {concept} even meant. My coach kept pulling me back "
            "to fundamentals, which was frustrating at the time but clearly the right call.\n\n"
            "By month three something shifted. {highlight}. That was the moment I understood why people stick with this. "
            "The {gear} investment was worthwhile — don't cheap out on that. "
            "{challenge} is real and took me longer than I expected to work through. "
            "If you're thinking about starting, just go. The learning curve is real but so are the rewards."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': '{technique} finally clicked after {n} months — and everything changed',
        'body_tmpl': (
            "I've been training {name} for {n} months and the moment {technique} finally clicked was a turning point. "
            "Before that I was going through the motions. After, the whole game opened up.\n\n"
            "My coach breaks things down well and has a good understanding of {concept}, which made the difference. "
            "The community at the gym is genuine — no ego, everyone remembers being a beginner. "
            "{highlight} was something I never expected to get from a sport like this. "
            "One honest note: {challenge}. Factor that in from day one."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Honest review: {name} is brilliant but {challenge} is real',
        'body_tmpl': (
            "{name} has been one of the best decisions I've made for my fitness and mental health. "
            "The {technique} and the deeper {concept} keep training mentally engaging in a way the gym never did.\n\n"
            "But I want to be honest: {challenge}. Nobody told me about that before I started and it caught me off guard. "
            "Invest in proper {gear} early — again, something I wished I'd done sooner. "
            "{highlight} came later than I expected but when it arrived it was worth the wait. "
            "Four stars rather than five because of that one persistent issue."
        ),
        'rating': 4,
    },
    {
        'title_tmpl': 'Competed for the first time in {name} — here is what I learned',
        'body_tmpl': (
            "After {n} months of training {name} I entered my first competition. I lost. It was the best thing that's "
            "happened to my development in the sport.\n\n"
            "Competition exposes gaps in your game that rolling or drilling never will. My {technique} fell apart under "
            "pressure. My understanding of {concept} was theoretical, not instinctive. I came home with a specific list "
            "of things to fix, which is more valuable than any win. "
            "{highlight} was what I took away from the experience beyond the tactical lessons. "
            "If your gym trains you for competition, do it. It will accelerate you."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Started {name} at 40 — no regrets whatsoever',
        'body_tmpl': (
            "I started {name} at 40 and felt completely out of my depth in the first class. Most people were twenty-something "
            "and athletic. I was neither. But the coach adapted sessions to my level and nobody made me feel unwelcome.\n\n"
            "Recovery takes longer at my age, and {challenge} hit harder than it would have at 25. But {highlight} "
            "has been more pronounced than I expected — probably because I needed it more. "
            "I now train three times a week and have no plans to stop. "
            "The {gear} setup was a surprise cost — budget for that separately."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'The mental side of {name} is what nobody warns you about',
        'body_tmpl': (
            "I came to {name} for the fitness and stayed for the mental challenge. Everyone talks about the physical "
            "side — the {technique}, the conditioning, the {gear}. Nobody mentioned what happens to your mind.\n\n"
            "Learning {concept} demands a kind of focused presence that clears everything else out. "
            "After a hard session I'm genuinely calmer and clearer. {highlight} has been the unexpected gift. "
            "The physical transformation is real too, but honestly it's secondary now. "
            "If you're dealing with stress and want something that genuinely helps, give {name} a proper chance."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Good gym, real progress — but {challenge} frustrated me',
        'body_tmpl': (
            "I've been training {name} for {n} months at a decent gym with good coaches. "
            "My {technique} has improved significantly and I've developed a real understanding of {concept}. "
            "{highlight} has been a consistent positive.\n\n"
            "The one thing that has genuinely frustrated me: {challenge}. "
            "I've read that this is common in {name} but it's still annoying when you're experiencing it. "
            "I've worked around it mostly, but it's the reason this is four stars rather than five. "
            "The sport itself is excellent — the frustration is circumstantial."
        ),
        'rating': 4,
    },
    {
        'title_tmpl': 'Watching {athlete} made me start — training made me stay',
        'body_tmpl': (
            "I got into {name} after watching {athlete} compete and thinking I wanted a piece of that. "
            "Reality check: what they make look effortless takes years of work. "
            "The {technique} I admired on screen took me {n} months just to do passably.\n\n"
            "But somewhere in that process I stopped caring about looking like {athlete} and started caring about "
            "my own progress with {concept}. That shift is when {name} really got its hooks in me. "
            "{highlight} is the part nobody sees in the highlights. {challenge} is the part nobody mentions either. "
            "Both are real. Both are worth knowing."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Dropped {name} after {n} months — honest about why',
        'body_tmpl': (
            "I trained {name} for {n} months and then stopped. I want to be honest about why, because most reviews "
            "only come from people who stuck with it.\n\n"
            "{challenge} was a bigger issue for me than I anticipated. My gym also had a culture problem — "
            "a few people had developed an ego around their {concept} knowledge that made sessions uncomfortable. "
            "The sport itself isn't the issue. The {technique} is genuinely interesting and {highlight} is real. "
            "I'm open to going back to a different gym. The sport deserves a better environment than I found."
        ),
        'rating': 2,
    },
    {
        'title_tmpl': '{name} transformed my fitness — specific results after {n} months',
        'body_tmpl': (
            "I track everything, so here are actual results after {n} months of {name}: significantly improved "
            "cardiovascular fitness, noticeable strength gains, and a flexibility improvement I didn't expect. "
            "None of that came from a gym program — it came from learning {technique} and understanding {concept}.\n\n"
            "{highlight} was the qualitative thing I didn't expect to measure but felt clearly. "
            "The {gear} cost was about what I expected. {challenge} is real — I had to adjust my schedule around it. "
            "For pure fitness return on time investment, {name} is hard to beat."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'The {name} community is unlike anything else I have trained in',
        'body_tmpl': (
            "I've done gym, running clubs, and team sports. The {name} community is different. "
            "There's something about shared struggle around {technique} and {concept} that creates a genuine bond. "
            "People at my gym remember everyone's name. Higher belts and better athletes make time for beginners.\n\n"
            "{highlight} was the thing that made me feel like I belonged. "
            "{challenge} came up early and the gym had good collective solutions for it. "
            "Even if the sport itself didn't suit me — and it does — the community alone would be worth the membership."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Three things I wish someone had told me before starting {name}',
        'body_tmpl': (
            "After {n} months of {name} I want to share what I wished I'd known at the start.\n\n"
            "First: {challenge} — it hits earlier and harder than the internet suggests. Budget for it practically and mentally. "
            "Second: the {gear} you buy first will probably be wrong — ask your coach before spending money. "
            "Third: {concept} is the foundation everything else builds on, but it looks boring from the outside. "
            "Resist the temptation to rush toward advanced {technique} before the fundamentals are solid.\n\n"
            "{highlight} is the reward for getting through all of that. It's worth it."
        ),
        'rating': 4,
    },
    {
        'title_tmpl': 'Returned to {name} after injury — the comeback experience',
        'body_tmpl': (
            "I'd been training {name} for two years when I picked up an injury that kept me out for four months. "
            "Coming back was harder mentally than physically. My {technique} had regressed and {concept} I'd taken "
            "for granted needed rebuilding.\n\n"
            "{highlight} was what brought me back to myself — about six weeks into the comeback. "
            "{challenge} was a greater factor in the comeback phase than it had been before injury. "
            "I'm now back to pre-injury level and training smarter. The sport is more rewarding now "
            "than it was before, because I know what it feels like to miss it."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Average experience — good sport, mediocre gym',
        'body_tmpl': (
            "I want to separate the sport from my specific experience. {name} as a discipline is genuinely compelling — "
            "the {technique}, the depth of {concept}, {highlight}. All of that is real and valuable.\n\n"
            "My gym, however, has been mediocre. Coaching quality varies session to session and {challenge} has been "
            "handled poorly. I've seen people get hurt because progression was rushed. "
            "If I were starting over I'd research gym culture more carefully before committing. "
            "The sport gets four stars; my current gym gets two. This review averages to three."
        ),
        'rating': 3,
    },
    {
        'title_tmpl': 'What {name} actually does to your body after {n} months',
        'body_tmpl': (
            "People describe {name} as a workout but that undersells it. After {n} months your body moves differently. "
            "The {technique} drills reshape how you use your hips, shoulders, and weight distribution in ways that carry "
            "into everything else you do. It's not just fitness — it's body literacy.\n\n"
            "Understanding {concept} added a tactical dimension that made sessions feel like problem-solving, not exercise. "
            "{highlight} was the physical change I noticed most clearly. {challenge} was the main friction — managed it "
            "eventually, but it took longer than I expected. Genuinely one of the best physical investments I've made."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Tried {name} expecting one thing, found something completely different',
        'body_tmpl': (
            "I signed up for {name} expecting a straightforward fitness class. What I found was a technical discipline "
            "that demands real skill development. The {technique} I was shown in week one is still something I'm refining "
            "now, {n} months later. {concept} gave me a framework for understanding why things work, not just what to do.\n\n"
            "{highlight} was the surprise that hooked me. {challenge} was the reality check that made me respect the sport. "
            "The {gear} is worth the investment — don't cut corners. I came for fitness and found a practice. "
            "That's a much better outcome."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Plateau at {n} months — what helped me push through',
        'body_tmpl': (
            "Around the {n}-month mark in {name} I hit a wall. My progress with {technique} wasn't improving and I felt like "
            "I was spinning wheels. It's apparently common but that didn't make it less frustrating.\n\n"
            "What helped: going back to fundamentals with my coach, spending more time drilling {concept} slowly rather "
            "than at full speed, and watching {athlete} breakdowns to understand what I was missing. "
            "{highlight} eventually returned once I let go of trying to advance too fast. "
            "{challenge} was actually the underlying cause of the plateau — once I addressed it, things moved again. "
            "If you hit that wall, stick with it. It passes."
        ),
        'rating': 4,
    },
    {
        'title_tmpl': 'The gear rabbit hole in {name} — what you actually need',
        'body_tmpl': (
            "When I started {name} I had no idea what to buy. I over-researched, bought the wrong things, and wasted money. "
            "Here's what I've learned: start with basic {gear}. Don't spend serious money until you know you're committed "
            "and until a coach has watched you move.\n\n"
            "The premium version of everything in {name} is genuinely better — but only once you've developed enough "
            "{technique} to feel the difference. Beginners can't feel it. "
            "{challenge} is where the right gear actually matters early on, so prioritise that. "
            "{highlight} has nothing to do with gear — it's purely about time and repetition with {concept}."
        ),
        'rating': 4,
    },
    {
        'title_tmpl': 'From complete beginner to first grading in {name}',
        'body_tmpl': (
            "I had zero athletic background when I started {name}. First class I was completely lost — "
            "everyone seemed to know the language of {concept} and I didn't. My {technique} was nonexistent. "
            "I nearly didn't go back.\n\n"
            "I did go back. And the first grading {n} months later was one of the proudest moments I've had in sport. "
            "{highlight} had become natural by that point, which I wouldn't have believed at week one. "
            "{challenge} is still something I work on. But it no longer feels like an obstacle — it feels like the game."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Overrated for fitness, underrated for everything else',
        'body_tmpl': (
            "Purely as a fitness tool, {name} is good but not exceptional. There are more efficient ways to get fit. "
            "Where {name} is genuinely underrated is everything else: the {technique} problem-solving, "
            "the {concept} depth, {highlight}. These aren't fitness outcomes — they're life outcomes.\n\n"
            "{challenge} is the honest downside that the fitness crowd often glosses over. "
            "If you're coming for abs and cardio, you'll get decent results but maybe not optimal ones. "
            "If you're coming for something that changes how you think and move and manage stress, "
            "{name} is exceptional value."
        ),
        'rating': 4,
    },
    {
        'title_tmpl': 'Serious competitive journey in {name} — what it really takes',
        'body_tmpl': (
            "I've been competing in {name} for three years now, training five days a week. "
            "I want to give an honest picture of what the competitive path looks like.\n\n"
            "The technical demands compound. {technique} at beginner level and at competition level are almost different skills. "
            "Understanding {concept} deeply enough to deploy it under pressure takes years, not months. "
            "Studying {athlete}'s approach changed how I think about the game entirely. "
            "{highlight} is what makes it worth the commitment. {challenge} is the tax you pay. "
            "Not everyone needs to compete — but if you have the itch, chase it. It will make you better in every direction."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Expected to hate {name}, now cannot imagine stopping',
        'body_tmpl': (
            "A friend dragged me to a {name} trial class. I went to be polite. I was terrible. "
            "I went back because I couldn't stand being terrible at something.\n\n"
            "That was {n} months ago. The {technique} I stumbled through in that first class is now something I teach "
            "to newer beginners. {concept} has become a genuine interest rather than a confusion. "
            "{highlight} happened somewhere around month three and reframed the whole thing. "
            "{challenge} is still there but it's familiar now — part of the texture of the practice. "
            "I'm glad my friend didn't take no for an answer."
        ),
        'rating': 5,
    },
]

FIRST_NAMES = [
    'Sarah', 'James', 'Olivia', 'Liam', 'Emma', 'Noah', 'Ava', 'Ethan',
    'Sophia', 'Mason', 'Isabella', 'Logan', 'Charlotte', 'Lucas', 'Amelia',
    'Jackson', 'Mia', 'Aiden', 'Harper', 'Sebastian', 'Emily', 'Jack',
    'Elizabeth', 'Owen', 'Sofia', 'Henry', 'Avery', 'Samuel', 'Ella',
    'Daniel', 'Scarlett', 'Benjamin', 'Victoria', 'Aria', 'Dylan', 'Grace',
    'Michael', 'Chloe', 'Ryan', 'Marcus', 'Diana', 'Priya', 'Kenji',
    'Fatima', 'Carlos', 'Ingrid', 'Takashi', 'Miriam', 'Stefan', 'Leila',
]

RATING_WEIGHTS = {5: 38, 4: 30, 3: 18, 2: 9, 1: 5}


def weighted_rating():
    pool = []
    for r, w in RATING_WEIGHTS.items():
        pool.extend([r] * w)
    return random.choice(pool)


def make_review(sport_name: str, slug: str, tmpl: dict) -> tuple | None:
    facts = SPORT_DATA.get(slug)
    if not facts:
        return None

    n          = random.randint(3, 18)
    technique  = random.choice(facts['techniques'])
    concept    = random.choice(facts['concepts'])
    gear       = random.choice(facts['gear'])
    athlete    = random.choice(facts['athletes'])
    highlight  = random.choice(facts['highlights'])
    challenge  = random.choice(facts['challenges'])

    title = tmpl['title_tmpl'].format(
        name=sport_name, n=n, technique=technique, concept=concept,
        gear=gear, athlete=athlete, highlight=highlight, challenge=challenge,
    )
    body = tmpl['body_tmpl'].format(
        name=sport_name, n=n, technique=technique, concept=concept,
        gear=gear, athlete=athlete, highlight=highlight, challenge=challenge,
    )
    base_rating = tmpl['rating']
    rating = max(1, min(5, base_rating + random.choice([-1, 0, 0, 0, 1])))
    if random.random() < 0.25:
        rating = weighted_rating()
    return title, body, rating


def run(args):
    from app import create_app, db
    from app.models import Subject, SubCategory, Review

    app = create_app('development')
    with app.app_context():
        sc = SubCategory.query.filter_by(slug='all-sports').first()
        if not sc:
            print('Subcategory all-sports not found')
            sys.exit(1)

        if args.slug:
            subjects = Subject.query.filter_by(subcategory_id=sc.id, slug=args.slug).all()
            if not subjects:
                print(f'Sport slug "{args.slug}" not found')
                sys.exit(1)
        else:
            subjects = Subject.query.filter_by(subcategory_id=sc.id).order_by(Subject.id).all()

        if args.start_from:
            slugs = [s.slug for s in subjects]
            if args.start_from in slugs:
                idx = slugs.index(args.start_from)
                subjects = subjects[idx:]
                print(f'Resuming from {args.start_from} ({len(subjects)} sports left)')

        print(f'Processing {len(subjects)} sports, ~{args.count} reviews each')

        for subj in subjects:
            if subj.slug not in SPORT_DATA:
                print(f'  SKIP {subj.name} — no facts data')
                continue

            deleted = Review.query.filter_by(subject_id=subj.id, source_site='sample').delete()
            deleted += Review.query.filter_by(subject_id=subj.id, source_site='generated').delete()
            db.session.commit()

            target = args.count
            used_titles: set[str] = set()
            reviews_added = 0

            shuffled = TEMPLATES[:]
            random.shuffle(shuffled)
            pool = (shuffled * ((target // len(shuffled)) + 2))[:target * 2]

            for tmpl in pool:
                if reviews_added >= target:
                    break
                result = make_review(subj.name, subj.slug, tmpl)
                if result is None:
                    continue
                title, body, rating = result
                if title in used_titles:
                    continue
                used_titles.add(title)

                days_ago = random.randint(30, 365 * 3)
                rev = Review(
                    subject_id=subj.id,
                    title=title,
                    body=body,
                    rating=rating,
                    author_name=random.choice(FIRST_NAMES),
                    source_site='generated',
                    original_date=datetime.utcnow() - timedelta(days=days_ago),
                    is_published=True,
                )
                db.session.add(rev)
                reviews_added += 1

            db.session.commit()
            subj.update_stats()
            db.session.commit()
            print(f'  {subj.name}: {reviews_added} reviews (avg {subj.avg_rating:.1f}★, deleted {deleted})')

        print('Done.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--slug', help='Single sport slug')
    parser.add_argument('--start-from', dest='start_from', help='Resume from this slug')
    parser.add_argument('--count', type=int, default=15, help='Reviews per sport (default 15)')
    args = parser.parse_args()
    run(args)
