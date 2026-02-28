"""
Seed script: creates initial categories, subcategories, and subjects.
Optionally triggers first scrape and AI processing.

Usage:
  python seed.py              # seed only (no scraping)
  python seed.py --scrape     # seed + scrape
  python seed.py --scrape --process  # seed + scrape + AI processing
  python seed.py --scrape --process --images  # full pipeline
"""
import argparse
import logging
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)


DOGS = [
    ('Labrador Retriever', 'labrador-retriever', 'Friendly, outgoing, and active companion.'),
    ('German Shepherd', 'german-shepherd', 'Confident, courageous, and smart working dog.'),
    ('Golden Retriever', 'golden-retriever', 'Intelligent, friendly, and devoted family dog.'),
    ('French Bulldog', 'french-bulldog', 'Adaptable, playful, and completely irresistible bat-eared companion.'),
    ('Bulldog', 'bulldog', 'Calm, courageous, and friendly with a distinctive wrinkled face.'),
    ('Poodle', 'poodle', 'Exceptionally smart, active, and excels in obedience training.'),
    ('Beagle', 'beagle', 'Merry, friendly, and curious small to medium-sized hound.'),
    ('Rottweiler', 'rottweiler', 'Robust and powerful guard dog with a loyal and loving personality.'),
    ('German Shorthaired Pointer', 'german-shorthaired-pointer', 'Versatile, friendly hunting and sporting dog.'),
    ('Dachshund', 'dachshund', 'Clever, lively, and courageous small breed with a big personality.'),
]

CATS = [
    ('Maine Coon', 'maine-coon', 'Gentle giant of the cat world, known for dog-like personality.'),
    ('Persian', 'persian', 'Quiet, gentle, and dignified with a luxurious long coat.'),
    ('Ragdoll', 'ragdoll', 'Laid-back, affectionate, and goes limp when held.'),
    ('Siamese', 'siamese', 'Vocal, social, and one of the oldest recognized breeds.'),
    ('British Shorthair', 'british-shorthair', 'Calm, easygoing, and famously round-faced.'),
    ('Abyssinian', 'abyssinian', 'Active, playful, and endlessly curious.'),
    ('Scottish Fold', 'scottish-fold', 'Distinctive folded ears, sweet-tempered and adaptable.'),
    ('Sphynx', 'sphynx', 'Hairless, wrinkled, and surprisingly warm to the touch.'),
    ('Bengal', 'bengal', 'Wildly beautiful with an energetic and playful nature.'),
    ('Russian Blue', 'russian-blue', 'Reserved with strangers but devoted to family.'),
]


def seed_db(app, db):
    from app.models import Category, SubCategory, Subject

    with app.app_context():
        # Category: Animals
        cat = Category.query.filter_by(slug='animals').first()
        if not cat:
            cat = Category(
                name='Animals',
                slug='animals',
                description='Reviews of cat and dog breeds from real pet owners.',
                icon='🐾',
            )
            db.session.add(cat)
            db.session.flush()
            logger.info("Created category: Animals")

        # SubCategory: Dogs
        dogs_sub = SubCategory.query.filter_by(category_id=cat.id, slug='dogs').first()
        if not dogs_sub:
            dogs_sub = SubCategory(category_id=cat.id, name='Dogs', slug='dogs')
            db.session.add(dogs_sub)
            db.session.flush()
            logger.info("Created subcategory: Dogs")

        # SubCategory: Cats
        cats_sub = SubCategory.query.filter_by(category_id=cat.id, slug='cats').first()
        if not cats_sub:
            cats_sub = SubCategory(category_id=cat.id, name='Cats', slug='cats')
            db.session.add(cats_sub)
            db.session.flush()
            logger.info("Created subcategory: Cats")

        # Seed dog breeds
        for name, slug, desc in DOGS:
            if not Subject.query.filter_by(subcategory_id=dogs_sub.id, slug=slug).first():
                subj = Subject(subcategory_id=dogs_sub.id, name=name, slug=slug, description=desc)
                db.session.add(subj)
                logger.info(f"  + Dog: {name}")

        # Seed cat breeds
        for name, slug, desc in CATS:
            if not Subject.query.filter_by(subcategory_id=cats_sub.id, slug=slug).first():
                subj = Subject(subcategory_id=cats_sub.id, name=name, slug=slug, description=desc)
                db.session.add(subj)
                logger.info(f"  + Cat: {name}")

        db.session.commit()
        logger.info("Seed complete.")
        return cat


def scrape_all(app, db):
    from app.models import Subject
    from app.scrapers import run_scraper

    with app.app_context():
        subjects = Subject.query.all()
        for subj in subjects:
            logger.info(f"Scraping: {subj.name}")
            try:
                new = run_scraper(subj, db)
                logger.info(f"  → {new} new reviews")
            except Exception as e:
                logger.error(f"  ✗ {e}")


def process_all(app, db):
    import anthropic
    from app.models import Review, Subject
    from app.processor import process_review

    with app.app_context():
        client = anthropic.Anthropic(api_key=app.config['ANTHROPIC_API_KEY'])
        model = app.config['CLAUDE_MODEL']

        reviews = Review.query.filter_by(is_published=False).all()
        logger.info(f"Processing {len(reviews)} unpublished reviews via Claude…")
        for i, rev in enumerate(reviews):
            raw = {'title': rev.title, 'body': rev.body, 'rating': rev.rating}
            result = process_review(raw, client, model)
            if result:
                rev.title = result['title']
                rev.body = result['body']
                rev.is_published = True
                logger.info(f"  [{i+1}/{len(reviews)}] processed: {rev.title[:60]}")
            else:
                logger.warning(f"  [{i+1}/{len(reviews)}] skipped (no result)")

        db.session.commit()

        # Update stats
        for subj in Subject.query.all():
            subj.update_stats()
        db.session.commit()
        logger.info("AI processing complete.")


def generate_images(app, db):
    logger.info("Image generation not supported with Claude. Skipping.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Seed the PetReviews database.')
    parser.add_argument('--scrape', action='store_true', help='Run scrapers after seeding')
    parser.add_argument('--process', action='store_true', help='Run AI processing after scraping')
    parser.add_argument('--images', action='store_true', help='Generate DALL-E images')
    args = parser.parse_args()

    from app import create_app, db as _db
    _app = create_app('development')

    seed_db(_app, _db)

    if args.scrape:
        scrape_all(_app, _db)

    if args.process:
        if not _app.config.get('OPENAI_API_KEY'):
            logger.error("OPENAI_API_KEY not set. Set it in .env to use AI processing.")
            sys.exit(1)
        process_all(_app, _db)

    if args.images:
        if not _app.config.get('OPENAI_API_KEY'):
            logger.error("OPENAI_API_KEY not set.")
            sys.exit(1)
        generate_images(_app, _db)

    logger.info("Done. Run: python run.py")
