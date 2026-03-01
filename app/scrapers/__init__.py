import logging
import os
from datetime import datetime

from flask import current_app

logger = logging.getLogger(__name__)


def run_scraper(subject, db) -> int:
    """
    Run all scrapers for a subject. Returns total new reviews saved.
    Deduplicates by original_url.
    """
    from ..models import Review, ScraperJob
    from .otzovik import OtzovikScraper
    from .irecommend import IRecommendScraper

    delay = current_app.config.get('SCRAPE_DELAY', 2.0)
    max_reviews = current_app.config.get('MAX_REVIEWS_PER_SCRAPE', 20)

    scrapers = [
        OtzovikScraper(delay=delay, max_reviews=max_reviews // 2),
        IRecommendScraper(delay=delay, max_reviews=max_reviews // 2),
    ]

    breed_type = subject.subcategory.name if subject.subcategory else ''
    total_new = 0

    for scraper in scrapers:
        job = ScraperJob.query.filter_by(
            subject_id=subject.id, source_site=scraper.site_name
        ).first()
        if not job:
            job = ScraperJob(subject_id=subject.id, source_site=scraper.site_name)
            db.session.add(job)

        job.status = 'running'
        job.last_run = datetime.utcnow()
        db.session.commit()

        try:
            raw_reviews = scraper.scrape_reviews(subject.name, breed_type)
            new_count = 0
            upload_dir = current_app.config['UPLOADS_DIR']

            for raw in raw_reviews:
                url = raw.get('original_url', '')
                if url and Review.query.filter_by(original_url=url).first():
                    continue  # deduplicate

                # Download image if scraper found one
                image_path = None
                image_url = raw.get('image_url')
                if image_url and hasattr(scraper, 'download_image'):
                    image_path = scraper.download_image(
                        image_url,
                        os.path.join(upload_dir, 'reviews'),
                    )

                review = Review(
                    subject_id=subject.id,
                    title=raw['title'],
                    body=raw['body'],
                    rating=raw['rating'],
                    author_name=raw.get('author_name', 'Anonymous'),
                    original_url=url or None,
                    source_site=raw.get('source_site', scraper.site_name),
                    original_date=raw.get('original_date'),
                    is_published=False,
                    image_path=image_path,
                )
                db.session.add(review)
                new_count += 1

            db.session.commit()
            job.status = 'done'
            job.reviews_found = new_count
            db.session.commit()

            total_new += new_count
            logger.info(f"[{scraper.site_name}] saved {new_count} new reviews for {subject.name}")

        except Exception as e:
            logger.error(f"[{scraper.site_name}] scrape failed for {subject.name}: {e}")
            job.status = 'error'
            job.error_message = str(e)
            db.session.commit()

    return total_new
