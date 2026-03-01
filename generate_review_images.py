"""
Generate AI images for published reviews that have no image.
Uses Hugging Face Inference API (FLUX.1-schnell, free tier).

Requires HF_API_KEY in .env (get one at huggingface.co/settings/tokens).

Usage:
  python3 generate_review_images.py
  python3 generate_review_images.py --limit 20   # process at most 20 reviews
  python3 generate_review_images.py --all        # include unpublished reviews too
"""
import argparse
import logging
import os
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)


def main(limit: int = 0, include_unpublished: bool = False):
    from app import create_app, db
    from app.models import Review
    from app.image_gen import generate_review_image

    app = create_app('development')
    with app.app_context():
        api_key = app.config.get('HF_API_KEY', '')
        if not api_key:
            logger.error("HF_API_KEY is not set. Add it to your .env file.")
            logger.error("Get a free key at: https://huggingface.co/settings/tokens")
            return

        upload_dir = os.path.join(app.config['UPLOADS_DIR'], 'reviews')

        query = Review.query.filter(Review.image_path.is_(None))
        if not include_unpublished:
            query = query.filter(Review.is_published == True)
        if limit:
            query = query.limit(limit)

        reviews = query.all()
        logger.info(f"Found {len(reviews)} reviews without images")

        updated = 0
        failed = 0

        for i, rev in enumerate(reviews):
            subject_name = rev.subject.name if rev.subject else 'pet'
            try:
                path = generate_review_image(
                    subject_name=subject_name,
                    upload_dir=upload_dir,
                    api_key=api_key,
                    review_title=rev.title or '',
                    review_body=(rev.body or '')[:100],
                )
                if path:
                    rev.image_path = path
                    db.session.commit()
                    updated += 1
                    logger.info(f"  [{i+1}/{len(reviews)}] ✓ {rev.id} ({subject_name}): {path}")
                else:
                    failed += 1
                    logger.debug(f"  [{i+1}/{len(reviews)}] no image generated for review {rev.id}")

                # Free tier rate-limit: ~1 req/sec
                time.sleep(1.2)

            except Exception as e:
                logger.warning(f"  [{i+1}/{len(reviews)}] error on review {rev.id}: {e}")
                failed += 1

        logger.info(f"Done. Generated: {updated}, failed: {failed}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, default=0, help='Max reviews to process (0 = all)')
    parser.add_argument('--all', dest='include_unpublished', action='store_true',
                        help='Include unpublished reviews')
    args = parser.parse_args()
    main(limit=args.limit, include_unpublished=args.include_unpublished)
