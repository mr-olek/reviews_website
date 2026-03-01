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
    # New dog breeds
    ('Siberian Husky', 'siberian-husky', 'Athletic, loyal sled dog with striking blue eyes and high energy.'),
    ('Border Collie', 'border-collie', 'The world\'s most intelligent dog, bred for herding with intense focus.'),
    ('Australian Shepherd', 'australian-shepherd', 'Energetic, highly trainable herding dog that loves having a job.'),
    ('Boxer', 'boxer', 'Playful, energetic, and loyal family dog with a goofy personality.'),
    ('Yorkshire Terrier', 'yorkshire-terrier', 'Tiny but feisty terrier with a gorgeous silky coat and bold attitude.'),
    ('Shih Tzu', 'shih-tzu', 'Affectionate lap dog bred for Chinese royalty, loves to be pampered.'),
    ('Doberman Pinscher', 'doberman-pinscher', 'Fearless, loyal, and highly intelligent guardian breed.'),
    ('Chihuahua', 'chihuahua', 'The world\'s smallest dog breed, with a huge personality to compensate.'),
    ('Cavalier King Charles Spaniel', 'cavalier-king-charles-spaniel', 'Gentle, affectionate, and adaptable companion with a silky coat.'),
    ('Bernese Mountain Dog', 'bernese-mountain-dog', 'Gentle giant from Switzerland, calm and devoted with a tri-colour coat.'),
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
    ('Norwegian Forest Cat', 'norwegian-forest-cat', 'Hardy, independent, and built for cold climates with a thick double coat.'),
    ('Burmese', 'burmese', 'Affectionate, playful, and thrives on human companionship.'),
    ('Devon Rex', 'devon-rex', 'Curly-coated, elfin-faced, and endlessly mischievous.'),
    ('American Shorthair', 'american-shorthair', 'Hardy, adaptable, and one of the most popular pedigree breeds in the USA.'),
    ('Exotic Shorthair', 'exotic-shorthair', 'The plush, low-maintenance version of the Persian.'),
    ('Birman', 'birman', 'Silky semi-long coat, blue eyes, and a gentle, curious nature.'),
    ('Tonkinese', 'tonkinese', 'Intelligent, social, and a natural cross between Siamese and Burmese.'),
    ('Himalayan', 'himalayan', 'Persian body with Siamese colourpoints and an ultra-calm temperament.'),
    ('Turkish Angora', 'turkish-angora', 'Elegant, athletic, and one of the oldest natural cat breeds.'),
    ('Chartreux', 'chartreux', 'Ancient French breed with a blue-grey coat and a quiet, loyal character.'),
    # New cat breeds
    ('Munchkin', 'munchkin', 'Short-legged, playful, and surprisingly agile little cat with a big personality.'),
    ('Siberian', 'siberian', 'Large, powerful Russian forest cat with a hypoallergenic-friendly coat.'),
    ('Turkish Van', 'turkish-van', 'Loves water, has a distinctive coloured tail, and is fiercely playful.'),
    ('Cornish Rex', 'cornish-rex', 'Wavy-coated, bat-eared, and endlessly energetic show-off.'),
    ('Balinese', 'balinese', 'Long-haired Siamese cousin that is equally vocal but slightly calmer.'),
    ('Somali', 'somali', 'Long-haired Abyssinian with a bushy fox-like tail and boundless curiosity.'),
    ('Egyptian Mau', 'egyptian-mau', 'The fastest domestic cat breed, naturally spotted and fiercely loyal.'),
    ('Manx', 'manx', 'Tailless or short-tailed island cat known for its round shape and playful nature.'),
    ('Selkirk Rex', 'selkirk-rex', 'Plush, curly-coated cat with a patient and loving temperament.'),
    ('Savannah', 'savannah', 'Tall, exotic-looking hybrid of domestic cat and serval with boundless energy.'),
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
                image_path='images/defaults/animals.jpg',
            )
            db.session.add(cat)
            db.session.flush()
            logger.info("Created category: Animals")
        elif not cat.image_path:
            cat.image_path = 'images/defaults/animals.jpg'

        # SubCategory: Dogs
        dogs_sub = SubCategory.query.filter_by(category_id=cat.id, slug='dogs').first()
        if not dogs_sub:
            dogs_sub = SubCategory(category_id=cat.id, name='Dogs', slug='dogs',
                                   image_path='images/defaults/dogs.jpg')
            db.session.add(dogs_sub)
            db.session.flush()
            logger.info("Created subcategory: Dogs")
        elif not dogs_sub.image_path:
            dogs_sub.image_path = 'images/defaults/dogs.jpg'

        # SubCategory: Cats
        cats_sub = SubCategory.query.filter_by(category_id=cat.id, slug='cats').first()
        if not cats_sub:
            cats_sub = SubCategory(category_id=cat.id, name='Cats', slug='cats',
                                   image_path='images/defaults/cats.jpg')
            db.session.add(cats_sub)
            db.session.flush()
            logger.info("Created subcategory: Cats")
        elif not cats_sub.image_path:
            cats_sub.image_path = 'images/defaults/cats.jpg'

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
