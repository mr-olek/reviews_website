"""
Generate 10 sample reviews for each breed that has fewer than 10 sample reviews.
Usage: python generate_breed_reviews.py
"""
import json
import logging
import random
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

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

def _random_username():
    return f"{random.choice(_ADJECTIVES)}{random.choice(_ANIMALS)}{random.randint(1, 999)}"


PROMPT_TEMPLATE = """Generate exactly 10 realistic, varied pet owner reviews for the breed: {breed_name} ({breed_type}).

Each review must:
- Be written from a genuine owner's first-person perspective
- Vary in rating (mix of 3, 4, and 5 stars — include at least one 3-star honest critique)
- Cover different aspects: temperament, training, grooming, health, suitability for families/apartments, energy level, etc.
- Be 80–200 words long
- Sound natural, not like marketing copy
- Include specific, realistic details about living with this breed

Return a JSON array of exactly 10 objects, each with:
  "title": short review headline (max 15 words)
  "body": the review text
  "rating": integer 3–5

Return ONLY valid JSON, no markdown or commentary."""


def generate_reviews_for_breed(client, model, breed_name, breed_type):
    prompt = PROMPT_TEMPLATE.format(breed_name=breed_name, breed_type=breed_type)
    try:
        message = client.messages.create(
            model=model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        )
        text = message.content[0].text.strip()
        # Strip markdown code fences if present
        if text.startswith('```'):
            text = text.split('\n', 1)[1]
            text = text.rsplit('```', 1)[0]
        reviews = json.loads(text)
        if isinstance(reviews, list):
            return reviews
    except Exception as e:
        logger.error(f"Failed to generate reviews for {breed_name}: {e}")
    return []


def main():
    import anthropic
    from app import create_app, db
    from app.models import Review, Subject

    app = create_app('development')

    with app.app_context():
        api_key = app.config.get('ANTHROPIC_API_KEY')
        model = app.config.get('CLAUDE_MODEL', 'claude-sonnet-4-6')
        client = anthropic.Anthropic(api_key=api_key)

        subjects = Subject.query.all()
        total_added = 0

        for subj in subjects:
            sample_count = Review.query.filter_by(
                subject_id=subj.id, source_site='sample'
            ).count()

            if sample_count >= 10:
                logger.info(f"Skipping {subj.name} — already has {sample_count} sample reviews")
                continue

            needed = 10 - sample_count
            breed_type = subj.subcategory.name if subj.subcategory else 'Pet'
            logger.info(f"Generating {needed} reviews for {subj.name} ({breed_type})…")

            reviews = generate_reviews_for_breed(client, model, subj.name, breed_type)
            if not reviews:
                logger.warning(f"  No reviews returned for {subj.name}")
                continue

            added = 0
            for raw in reviews[:needed]:
                title = str(raw.get('title', '')).strip()
                body = str(raw.get('body', '')).strip()
                try:
                    rating = max(1, min(5, int(raw.get('rating', 4))))
                except (ValueError, TypeError):
                    rating = 4

                if not title or not body:
                    continue

                review = Review(
                    subject_id=subj.id,
                    title=title,
                    body=body,
                    rating=rating,
                    author_name=_random_username(),
                    source_site='sample',
                    is_published=True,
                )
                db.session.add(review)
                added += 1

            db.session.commit()
            subj.update_stats()
            db.session.commit()

            logger.info(f"  + Added {added} reviews for {subj.name}")
            total_added += added
            time.sleep(0.5)  # gentle rate limiting

        logger.info(f"\nDone. Total new reviews added: {total_added}")


if __name__ == '__main__':
    main()
