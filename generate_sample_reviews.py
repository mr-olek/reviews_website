"""
Generate sample reviews using templates — no API needed.
Seeds the DB with realistic-looking reviews for all breeds.
"""
from __future__ import annotations

import random
from datetime import datetime, timedelta

BREED_DATA = {
    # Dogs
    'Labrador Retriever': {
        'type': 'dog', 'traits': 'friendly, outgoing, energetic',
        'positives': ['amazing with kids', 'loves water', 'easy to train', 'never met a stranger', 'incredibly loyal'],
        'negatives': ['sheds a LOT', 'eats everything', 'needs tons of exercise', 'pulls on the leash', 'chews furniture as a puppy'],
        'health': ['hip dysplasia is common', 'prone to obesity', 'ear infections', 'exercise-induced collapse'],
    },
    'German Shepherd': {
        'type': 'dog', 'traits': 'intelligent, loyal, protective',
        'positives': ['incredibly smart', 'loyal beyond words', 'excellent guard dog', 'thrives with a job', 'bonds deeply with family'],
        'negatives': ['heavy shedding year-round', 'can be aloof with strangers', 'needs serious mental stimulation', 'degenerative myelopathy risk', 'high exercise demands'],
        'health': ['hip and elbow dysplasia', 'degenerative myelopathy', 'bloat risk', 'skin allergies'],
    },
    'Golden Retriever': {
        'type': 'dog', 'traits': 'gentle, patient, devoted',
        'positives': ['the most patient dog imaginable', 'great with everyone', 'loves to please', 'excellent therapy dog', 'gorgeous coat'],
        'negatives': ['hair everywhere always', 'cancer rates are higher than most breeds', 'too friendly to be a guard dog', 'expensive vet bills', 'needs daily grooming'],
        'health': ['cancer is the leading cause of death', 'hip dysplasia', 'heart issues', 'skin conditions'],
    },
    'French Bulldog': {
        'type': 'dog', 'traits': 'playful, adaptable, smart',
        'positives': ['perfect apartment dog', 'low exercise needs', 'hilarious personality', 'good with kids', 'quiet breed'],
        'negatives': ['very expensive', 'breathing issues are real', 'cannot tolerate heat', 'extremely expensive vet bills', 'can be stubborn'],
        'health': ['brachycephalic syndrome', 'spine problems', 'allergies', 'eye issues', 'expensive surgeries common'],
    },
    'Bulldog': {
        'type': 'dog', 'traits': 'calm, courageous, friendly',
        'positives': ['incredibly gentle', 'great with kids', 'low energy indoors', 'loyal and affectionate', 'unique personality'],
        'negatives': ['snoring is constant', 'breathing difficulties', 'overheats easily', 'vet bills are significant', 'wrinkles need daily cleaning'],
        'health': ['brachycephalic issues', 'hip dysplasia', 'cherry eye', 'skin fold infections', 'heart problems'],
    },
    'Poodle': {
        'type': 'dog', 'traits': 'intelligent, active, elegant',
        'positives': ['hypoallergenic coat', 'extremely intelligent', 'athletic and agile', 'long lifespan', 'virtually no shedding'],
        'negatives': ['grooming is expensive', 'can be high-strung', 'needs lots of mental stimulation', 'separation anxiety prone', 'grooming every 6-8 weeks'],
        'health': ['progressive retinal atrophy', 'Addison\'s disease', 'bloat', 'hip dysplasia', 'epilepsy'],
    },
    'Beagle': {
        'type': 'dog', 'traits': 'merry, curious, friendly',
        'positives': ['great scent hound', 'good with kids', 'sturdy and healthy', 'happy temperament', 'low grooming needs'],
        'negatives': ['howls and bays loudly', 'follows nose into trouble', 'stubborn to train', 'can be escape artists', 'food motivated to excess'],
        'health': ['epilepsy', 'hypothyroidism', 'hip dysplasia', 'ear infections', 'obesity prone'],
    },
    'Rottweiler': {
        'type': 'dog', 'traits': 'loyal, loving, confident',
        'positives': ['devoted family protector', 'highly intelligent', 'calm confidence', 'trainable with consistency', 'playful with family'],
        'negatives': ['breed discrimination in some areas', 'needs extensive socialization', 'strong-willed', 'high insurance costs', 'heavy and powerful'],
        'health': ['hip and elbow dysplasia', 'heart disease', 'cancer', 'obesity', 'cruciate ligament tears'],
    },
    'German Shorthaired Pointer': {
        'type': 'dog', 'traits': 'versatile, friendly, eager',
        'positives': ['incredible hunting companion', 'loves all outdoor activities', 'versatile and athletic', 'affectionate with family', 'intelligent and trainable'],
        'negatives': ['extremely high energy', 'not suited for apartment life', 'destructive if bored', 'needs hours of daily exercise', 'separtion anxiety'],
        'health': ['hip dysplasia', 'bloat', 'cone degeneration', 'lymphedema', 'heart disease'],
    },
    'Dachshund': {
        'type': 'dog', 'traits': 'curious, friendly, spunky',
        'positives': ['huge personality in small body', 'brave and bold', 'good apartment dog', 'low exercise needs', 'loves to cuddle'],
        'negatives': ['back problems are very common', 'stubborn streak', 'can be aggressive if poorly socialized', 'barky', 'expensive back surgery risk'],
        'health': ['intervertebral disc disease', 'obesity', 'dental issues', 'patellar luxation', 'progressive retinal atrophy'],
    },
    # Cats
    'Maine Coon': {
        'type': 'cat', 'traits': 'gentle, playful, sociable',
        'positives': ['dog-like personality', 'great with kids and dogs', 'chirps instead of meows', 'loves water', 'gentle giant'],
        'negatives': ['expensive to buy', 'significant grooming needs', 'hypertrophic cardiomyopathy risk', 'sheds heavily', 'slow to mature'],
        'health': ['hypertrophic cardiomyopathy', 'hip dysplasia', 'spinal muscular atrophy', 'polycystic kidney disease'],
    },
    'Persian': {
        'type': 'cat', 'traits': 'quiet, gentle, dignified',
        'positives': ['calm and peaceful', 'stunning beauty', 'low energy', 'very affectionate', 'quiet lap cat'],
        'negatives': ['daily grooming is mandatory', 'eye discharge every day', 'breathing issues', 'indoor only', 'expensive grooming'],
        'health': ['polycystic kidney disease', 'brachycephalic issues', 'eye conditions', 'bladder stones', 'dental issues'],
    },
    'Ragdoll': {
        'type': 'cat', 'traits': 'gentle, calm, affectionate',
        'positives': ['goes limp when held', 'incredibly gentle', 'perfect indoor companion', 'great with children', 'very sociable'],
        'negatives': ['no street smarts — indoor only', 'expensive breed', 'needs companionship', 'moderate shedding', 'slow to mature — 4 years'],
        'health': ['hypertrophic cardiomyopathy', 'bladder stones', 'obesity prone', 'hairballs'],
    },
    'Siamese': {
        'type': 'cat', 'traits': 'vocal, social, intelligent',
        'positives': ['extremely intelligent', 'very bonded to owner', 'low shedding', 'playful into old age', 'striking appearance'],
        'negatives': ['very loud and demanding', 'separation anxiety', 'needs lots of attention', 'can be destructive alone', 'opinionated personality'],
        'health': ['amyloidosis', 'asthma', 'dental disease', 'progressive retinal atrophy', 'heart disease'],
    },
    'British Shorthair': {
        'type': 'cat', 'traits': 'calm, easygoing, dignified',
        'positives': ['easygoing temperament', 'good with kids', 'not demanding', 'robust health', 'beautiful teddy bear looks'],
        'negatives': ['not a lap cat typically', 'can be aloof', 'obesity prone', 'hypertrophic cardiomyopathy risk', 'expensive'],
        'health': ['hypertrophic cardiomyopathy', 'polycystic kidney disease', 'obesity', 'hemophilia B'],
    },
    'Abyssinian': {
        'type': 'cat', 'traits': 'active, curious, playful',
        'positives': ['endlessly entertaining', 'athletic and agile', 'low grooming needs', 'bonds closely with family', 'beautiful ticked coat'],
        'negatives': ['very high energy', 'gets bored easily', 'not a lap cat', 'needs lots of stimulation', 'destructive if bored'],
        'health': ['progressive retinal atrophy', 'pyruvate kinase deficiency', 'renal amyloidosis', 'hyperthyroidism'],
    },
    'Scottish Fold': {
        'type': 'cat', 'traits': 'sweet, calm, adaptable',
        'positives': ['adorable folded ears', 'sweet and gentle', 'adapts well to any home', 'quiet and calm', 'gets along with everyone'],
        'negatives': ['osteochondrodysplasia causes pain', 'ethical controversy over breeding', 'expensive vet care', 'joint problems', 'limited mobility'],
        'health': ['osteochondrodysplasia', 'polycystic kidney disease', 'heart disease', 'joint pain throughout life'],
    },
    'Sphynx': {
        'type': 'cat', 'traits': 'energetic, affectionate, inquisitive',
        'positives': ['no shedding at all', 'incredibly affectionate', 'loves people', 'dog-like loyalty', 'hilarious personality'],
        'negatives': ['needs weekly bathing', 'gets cold easily', 'expensive', 'heart disease risk', 'skin care intensive'],
        'health': ['hypertrophic cardiomyopathy', 'hereditary myopathy', 'skin conditions', 'respiratory infections'],
    },
    'Bengal': {
        'type': 'cat', 'traits': 'wild-looking, energetic, intelligent',
        'positives': ['stunning wild appearance', 'highly intelligent', 'loves water', 'very playful', 'strong bond with owner'],
        'negatives': ['extremely high energy', 'can be destructive', 'very loud', 'needs lots of stimulation', 'not for first-time owners'],
        'health': ['progressive retinal atrophy', 'flat-chested kitten syndrome', 'hypertrophic cardiomyopathy', 'trichiasis'],
    },
    'Russian Blue': {
        'type': 'cat', 'traits': 'gentle, quiet, loyal',
        'positives': ['hypoallergenic coat', 'quiet and calm', 'extremely loyal to family', 'low shedding', 'intelligent and gentle'],
        'negatives': ['shy with strangers', 'takes time to warm up', 'can be anxious', 'doesn\'t like change', 'reserved nature'],
        'health': ['relatively healthy breed', 'bladder stones possible', 'progressive retinal atrophy', 'obesity prone'],
    },
}

REVIEW_TEMPLATES = [
    # 5-star templates
    {
        'rating': 5,
        'title_tmpl': "Best decision of my life — the {name} is truly an incredible {type}",
        'body_tmpl': (
            "I've had my {name} for {years} years now, and I honestly cannot imagine life without {pronoun}. "
            "When I was researching breeds, everyone kept telling me the {name} was the right choice for my lifestyle, "
            "and they were absolutely right.\n\n"
            "{positive1} — that alone would be enough, but there's so much more. "
            "{positive2}. My {name}, {pet_name}, has been with me through thick and thin. "
            "Whether it's a lazy Sunday afternoon or an active day out, {pronoun} is always the perfect companion.\n\n"
            "Sure, there are some things to be aware of. {negative1}, and {health_note}. "
            "But honestly, these are minor compared to the joy this {type} brings every single day. "
            "If you're considering a {name}, just do it. You won't regret it for a second."
        ),
    },
    {
        'rating': 5,
        'title_tmpl': "{name}: After {years} years, still the best {type} breed for families",
        'body_tmpl': (
            "Our {name} has been part of our family for {years} years and I still get emotional thinking about "
            "how much {pronoun} has enriched our lives. {positive1} — and with two young kids, that means everything.\n\n"
            "{positive2}. We've tried other breeds before but nothing compares to the {name}'s temperament. "
            "{pronoun_cap} is {traits} and adapts beautifully to our busy household.\n\n"
            "The main things to budget for: {negative1}. We also learned about {health_note}, "
            "so we get regular vet checkups. Overall cost is higher than I expected initially, "
            "but every penny is worth it. Highly recommend this breed to anyone and everyone."
        ),
    },
    # 4-star templates
    {
        'rating': 4,
        'title_tmpl': "Wonderful breed with a few things to know before you commit to a {name}",
        'body_tmpl': (
            "I've had my {name} for {years} years and overall it's been an amazing experience. "
            "{positive1}. {positive2}. The personality of this breed really is special — {traits}.\n\n"
            "That said, there are a few realities I wish someone had been more upfront about. "
            "{negative1} was a real surprise. And {negative2} took some adjustment. "
            "These aren't dealbreakers by any means, but they're worth knowing going in.\n\n"
            "Health-wise, {health_note}. We had one scare a couple years in that cost a few thousand dollars. "
            "Pet insurance is strongly recommended. But despite these things, I'd still give the breed 4 stars — "
            "the companionship and personality far outweigh the challenges."
        ),
    },
    {
        'rating': 4,
        'title_tmpl': "Great {name} experience — just go in with realistic expectations",
        'body_tmpl': (
            "My {name} {pet_name} is {years} years old now and has been a wonderful companion. "
            "The breed lives up to its reputation: {positive1}. I particularly love that {positive2}.\n\n"
            "My one knock is that {negative1}. I underestimated this when I first got {pronoun}. "
            "Also, {negative2} is something you need to plan for. It's not a dealbreaker but requires commitment.\n\n"
            "On the health front, {health_note}. Budget for that and you'll be fine. "
            "Four solid stars — would recommend to the right owner who knows what they're getting into."
        ),
    },
    # 3-star templates
    {
        'rating': 3,
        'title_tmpl': "Honest review: the {name} is wonderful but definitely not for everyone",
        'body_tmpl': (
            "I want to give an honest review because I think there's a lot of romanticization of the {name} breed online. "
            "Yes, {positive1}. And {positive2} is genuinely lovely.\n\n"
            "But here's the reality: {negative1}. This is not a small thing — it genuinely impacts daily life. "
            "{negative2} also caught me off guard. I've had to rearrange my schedule significantly.\n\n"
            "The health considerations are real too. {health_note}. I've spent more at the vet than I budgeted for.\n\n"
            "Three stars because the pros and cons feel about equal for my lifestyle. "
            "If you're the right fit for this breed, they'll give you 5-star love. Just make sure you're that person first."
        ),
    },
    # 2-star templates
    {
        'rating': 2,
        'title_tmpl': "Beautiful breed, but I was not prepared for the reality of owning a {name}",
        'body_tmpl': (
            "I hate to write a negative review because I do love my {name}. {positive1} is genuinely wonderful. "
            "But I feel I owe future owners honesty about what this breed actually requires.\n\n"
            "{negative1} — and I mean seriously. I had no idea how much this would affect my life. "
            "{negative2} has been the biggest challenge. I've had to make major lifestyle changes.\n\n"
            "The health costs have been significant. {health_note}. We've spent thousands we didn't plan for. "
            "I wish breeders and breed guides were more upfront about this.\n\n"
            "Two stars — not because the breed isn't wonderful, but because the mismatch between expectations "
            "and reality has been hard. Do thorough research before committing."
        ),
    },
    # 1-star templates
    {
        'rating': 1,
        'title_tmpl': "Think very carefully before getting a {name} — my honest experience",
        'body_tmpl': (
            "I'm writing this after {years} difficult years. I want to be clear: I don't blame the breed. "
            "The {name} has genuine wonderful qualities — {positive1}. But the challenges have been overwhelming for us.\n\n"
            "{negative1} has been relentless. {negative2} was something we were told about but "
            "completely underestimated. It has affected our entire family's daily routine.\n\n"
            "The health costs have been devastating. {health_note}. We did not have adequate pet insurance "
            "and the financial strain has been significant.\n\n"
            "One star because I feel the breed community isn't honest enough about the true demands. "
            "Some people are absolutely perfect for {name}s. I was not one of them. Please research thoroughly."
        ),
    },
]

NAMES = [
    ("Sarah", "she"), ("James", "he"), ("Emily", "she"), ("Mike", "he"),
    ("Anna", "she"), ("Dave", "he"), ("Jess", "she"), ("Chris", "he"),
    ("Laura", "she"), ("Tom", "he"), ("Maria", "she"), ("Kevin", "he"),
    ("Rachel", "she"), ("Danny", "he"), ("Sophy", "she"), ("Brian", "he"),
    ("Olivia", "she"), ("Nate", "he"), ("Hannah", "she"), ("Lucas", "he"),
]

PET_NAMES = [
    "Max", "Luna", "Charlie", "Bella", "Cooper", "Daisy", "Buddy", "Molly",
    "Rocky", "Lily", "Duke", "Zoe", "Bear", "Nala", "Zeus", "Coco", "Leo",
    "Mia", "Milo", "Ruby", "Finn", "Rosie", "Archie", "Penny", "Oscar",
]

RATING_WEIGHTS = [5, 5, 5, 5, 4, 4, 4, 3, 2, 1]


def make_review(breed_name: str, data: dict, used_authors: set) -> dict:
    rating = random.choice(RATING_WEIGHTS)
    templates = [t for t in REVIEW_TEMPLATES if t['rating'] == rating]
    tmpl = random.choice(templates)

    # Pick unused author
    available = [(n, p) for n, p in NAMES if n not in used_authors]
    if not available:
        available = NAMES
    author_name, author_pronoun = random.choice(available)
    used_authors.add(author_name)

    pet_name = random.choice(PET_NAMES)
    years = random.randint(1, 6)
    positives = random.sample(data['positives'], min(2, len(data['positives'])))
    negatives = random.sample(data['negatives'], min(2, len(data['negatives'])))
    health_note = random.choice(data['health'])
    animal_type = data['type']

    title = tmpl['title_tmpl'].format(name=breed_name, type=animal_type, years=years)
    body = tmpl['body_tmpl'].format(
        name=breed_name,
        type=animal_type,
        traits=data['traits'],
        years=years,
        pronoun=author_pronoun,
        pronoun_cap=author_pronoun.capitalize(),
        pet_name=pet_name,
        positive1=positives[0],
        positive2=positives[1] if len(positives) > 1 else positives[0],
        negative1=negatives[0],
        negative2=negatives[1] if len(negatives) > 1 else negatives[0],
        health_note=health_note,
    )

    days_ago = random.randint(14, 365 * 4)
    original_date = datetime.utcnow() - timedelta(days=days_ago)

    return {
        'title': title,
        'body': body,
        'rating': rating,
        'author_name': author_name,
        'original_date': original_date,
    }


def run(count_per_breed: int = 10):
    from app import create_app, db
    from app.models import Subject, Review

    app = create_app('development')
    with app.app_context():
        subjects = Subject.query.order_by(Subject.id).all()
        total = 0

        for subj in subjects:
            data = BREED_DATA.get(subj.name)
            if not data:
                print(f"  skip {subj.name} (no template data)")
                continue

            used_authors: set = set()
            added = 0
            for i in range(count_per_breed):
                fake_url = f"sample://{subj.slug}/{i+1}"
                if Review.query.filter_by(original_url=fake_url).first():
                    continue
                rv = make_review(subj.name, data, used_authors)
                review = Review(
                    subject_id=subj.id,
                    title=rv['title'],
                    body=rv['body'],
                    rating=rv['rating'],
                    author_name=rv['author_name'],
                    original_url=fake_url,
                    source_site='sample',
                    original_date=rv['original_date'],
                    is_published=True,
                )
                db.session.add(review)
                added += 1

            db.session.commit()
            subj.update_stats()
            db.session.commit()
            print(f"  ✓ {subj.name}: {added} reviews (avg {subj.avg_rating:.1f}★)")
            total += added

        print(f"\nDone. {total} reviews added. Run: python3 run.py")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--count', type=int, default=10)
    args = parser.parse_args()
    run(args.count)
