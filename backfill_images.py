"""
Backfill review images for already-scraped reviews that have no image.
Run when irecommend.ru is accessible (VPN if needed).

Usage:
  python3 backfill_images.py
  python3 backfill_images.py --limit 50   # process at most 50 reviews
"""
import argparse
import logging
import os
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)


def main(limit: int = 0):
    from app import create_app, db
    from app.models import Review
    from app.scrapers.irecommend import IRecommendScraper

    app = create_app('development')
    with app.app_context():
        upload_dir = os.path.join(app.config['UPLOADS_DIR'], 'reviews')

        query = Review.query.filter(
            Review.source_site == 'irecommend',
            Review.image_path.is_(None),
            Review.original_url.isnot(None),
        )
        if limit:
            query = query.limit(limit)
        reviews = query.all()

        logger.info(f"Found {len(reviews)} irecommend reviews without images")

        scraper = IRecommendScraper(delay=1.0, max_reviews=1)
        updated = 0
        failed = 0

        for i, rev in enumerate(reviews):
            try:
                full = scraper._fetch_full_review(rev.original_url)
                if full and full.get('image_url'):
                    path = scraper.download_image(full['image_url'], upload_dir)
                    if path:
                        rev.image_path = path
                        db.session.commit()
                        updated += 1
                        logger.info(f"  [{i+1}/{len(reviews)}] ✓ {rev.id}: {path}")
                    else:
                        failed += 1
                        logger.debug(f"  [{i+1}/{len(reviews)}] download failed: {rev.original_url}")
                else:
                    logger.debug(f"  [{i+1}/{len(reviews)}] no image: {rev.original_url}")
                time.sleep(0.5)
            except Exception as e:
                logger.warning(f"  [{i+1}/{len(reviews)}] error: {e}")
                failed += 1

        logger.info(f"Done. Updated: {updated}, failed/no image: {failed}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, default=0, help='Max reviews to process (0 = all)')
    args = parser.parse_args()
    main(limit=args.limit)
