"""
Generate realistic pet breed reviews using Claude (Anthropic).

Usage:
  python3 generate_reviews.py               # generate for all subjects
  python3 generate_reviews.py --subject 1   # specific subject id
  python3 generate_reviews.py --count 5     # reviews per subject (default 8)
"""
from __future__ import annotations

import argparse
import json
import logging
import random
import re
import sys
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

PERSONAS = [
    "Sarah", "James", "Emily", "Mike", "Anna",
    "Dave", "Jess", "Chris", "Laura", "Tom",
    "Maria", "Kevin", "Rachel", "Danny", "Sophy",
    "Brian", "Olivia", "Nate", "Hannah", "Lucas",
]

RATING_WEIGHTS = {5: 40, 4: 30, 3: 15, 2: 10, 1: 5}


def weighted_rating() -> int:
    pool = []
    for r, w in RATING_WEIGHTS.items():
        pool.extend([r] * w)
    return random.choice(pool)


def _extract_json(text: str) -> list:
    """Extract JSON array from Claude's response."""
    # Strip markdown fences
    text = re.sub(r'^```(?:json)?\s*', '', text.strip(), flags=re.MULTILINE)
    text = re.sub(r'\s*```$', '', text.strip(), flags=re.MULTILINE)
    parsed = json.loads(text.strip())
    if isinstance(parsed, list):
        return parsed
    # Sometimes Claude wraps in {"reviews": [...]}
    for v in parsed.values():
        if isinstance(v, list):
            return v
    raise ValueError(f"No JSON array found in response")


def generate_reviews_for_subject(
    subject_name: str,
    subcategory_name: str,
    count: int,
    client,
    model: str = 'claude-sonnet-4-6',
) -> list[dict]:
    ratings = [weighted_rating() for _ in range(count)]
    personas = random.sample(PERSONAS, min(count, len(PERSONAS)))

    animal_type = subcategory_name.rstrip('s')  # "Dogs" → "Dog", "Cats" → "Cat"

    prompt = f"""Generate exactly {count} distinct, realistic owner reviews for the {subject_name} {animal_type} breed.

Each review must feel genuine — include specific personal experiences, anecdotes, pros/cons that real owners mention.
Vary writing style, length (150-400 words body), and sentiment to match the rating.

Ratings to use in order: {ratings}
Author names to use in order: {personas[:count]}

Rating guide:
- 5★: enthusiastic, loves the breed, specific positive traits, personal story
- 4★: mostly positive, one or two minor complaints
- 3★: balanced, honest pros and cons
- 2★: disappointed, specific problems experienced
- 1★: serious issues — health problems, behavior, unexpected costs

Include breed-specific details: temperament, grooming needs, health issues, training difficulty, cost, compatibility with kids/other pets.

Return a JSON array of {count} objects, each with:
- "title": compelling review title (10-15 words)
- "body": full review text with paragraphs separated by \\n\\n
- "rating": integer 1-5
- "author_name": string (use the names provided above in order)

Return ONLY the JSON array, no markdown, no explanation."""

    try:
        message = client.messages.create(
            model=model,
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}],
        )
        content = message.content[0].text
        reviews = _extract_json(content)

        # Enforce ratings and clamp
        for i, rev in enumerate(reviews):
            rev['rating'] = max(1, min(5, int(ratings[i] if i < len(ratings) else 3)))

        return reviews[:count]
    except Exception as e:
        logger.error(f"Claude generation failed for {subject_name}: {e}")
        return []


def run(args):
    import anthropic
    from app import create_app, db
    from app.models import Subject, Review

    app = create_app('development')
    client = anthropic.Anthropic(api_key=app.config['ANTHROPIC_API_KEY'])
    model = app.config['CLAUDE_MODEL']

    with app.app_context():
        if args.subject:
            subjects = [Subject.query.get(args.subject)]
            if not subjects[0]:
                logger.error(f"Subject {args.subject} not found")
                sys.exit(1)
        else:
            subjects = Subject.query.order_by(Subject.id).all()

        logger.info(f"Generating {args.count} reviews each for {len(subjects)} subjects using {model}…")

        for subj in subjects:
            subcat_name = subj.subcategory.name if subj.subcategory else 'Pets'
            logger.info(f"→ {subj.name} ({subcat_name})")

            reviews_data = generate_reviews_for_subject(
                subj.name, subcat_name, args.count, client, model
            )

            if not reviews_data:
                logger.warning(f"  No reviews generated for {subj.name}")
                continue

            from datetime import datetime, timedelta
            added = 0
            for i, rd in enumerate(reviews_data):
                days_ago = random.randint(30, 365 * 4)
                fake_date = datetime.utcnow() - timedelta(days=days_ago)
                fake_url = f"generated://{subj.slug}/{i+1}"

                if Review.query.filter_by(original_url=fake_url).first():
                    continue

                review = Review(
                    subject_id=subj.id,
                    title=rd.get('title', f'{subj.name} Review'),
                    body=rd.get('body', ''),
                    rating=rd.get('rating', 3),
                    author_name=rd.get('author_name', 'Anonymous'),
                    original_url=fake_url,
                    source_site='generated',
                    original_date=fake_date,
                    is_published=True,
                )
                db.session.add(review)
                added += 1

            db.session.commit()
            subj.update_stats()
            db.session.commit()

            logger.info(f"  ✓ {added} reviews added (avg rating: {subj.avg_rating:.1f})")
            time.sleep(0.5)

        logger.info("Done. Run: python3 run.py")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--subject', type=int, help='Subject ID (default: all)')
    parser.add_argument('--count', type=int, default=8, help='Reviews per subject (default: 8)')
    args = parser.parse_args()
    run(args)
