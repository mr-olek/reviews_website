from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()


def create_app(config_name='default'):
    app = Flask(__name__, template_folder='templates', static_folder='../static')
    app.config.from_object(config[config_name])

    db.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    from .admin import admin_bp
    app.register_blueprint(admin_bp)

    from .i18n import load_translations, t, t_cat, t_subcat, get_lang, get_trans, LANGUAGES
    load_translations(app)

    @app.context_processor
    def inject_globals():
        from .models import Category
        return {
            'nav_categories': Category.query.order_by(Category.name).all(),
            't': t,
            't_cat': t_cat,
            't_subcat': t_subcat,
            'get_trans': get_trans,
            'current_lang': get_lang(),
            'LANGUAGES': LANGUAGES,
        }

    with app.app_context():
        db.create_all()
        _migrate(db)
        _start_scheduler(app)

    return app


def _migrate(db):
    """Add any missing columns to existing tables (SQLite-safe)."""
    from sqlalchemy import text
    migrations = [
        "ALTER TABLE categories ADD COLUMN image_path VARCHAR(500)",
        "ALTER TABLE subcategories ADD COLUMN image_path VARCHAR(500)",
        "ALTER TABLE subcategories ADD COLUMN description TEXT",
        "ALTER TABLE subcategories ADD COLUMN pros TEXT",
        "ALTER TABLE subcategories ADD COLUMN cons TEXT",
        "ALTER TABLE subjects ADD COLUMN pros TEXT",
        "ALTER TABLE subjects ADD COLUMN cons TEXT",
        """CREATE TABLE IF NOT EXISTS review_replies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            review_id INTEGER NOT NULL REFERENCES reviews(id),
            parent_id INTEGER REFERENCES review_replies(id),
            author_name VARCHAR(200) NOT NULL,
            body TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )""",
        "ALTER TABLE reviews ADD COLUMN translations TEXT",
        "ALTER TABLE subjects ADD COLUMN translations TEXT",
        "ALTER TABLE subcategories ADD COLUMN translations TEXT",
        "ALTER TABLE categories ADD COLUMN translations TEXT",
        "CREATE INDEX IF NOT EXISTS ix_reviews_subject_id ON reviews (subject_id)",
        "CREATE INDEX IF NOT EXISTS ix_reviews_is_published ON reviews (is_published)",
        "CREATE INDEX IF NOT EXISTS ix_reviews_created_at ON reviews (created_at)",
    ]
    with db.engine.connect() as conn:
        for sql in migrations:
            try:
                conn.execute(text(sql))
                conn.commit()
            except Exception:
                pass  # column already exists


def _start_scheduler(app):
    try:
        from apscheduler.schedulers.background import BackgroundScheduler
        from apscheduler.triggers.cron import CronTrigger

        scheduler = BackgroundScheduler()

        def daily_scrape():
            with app.app_context():
                from .models import Subject
                from .scrapers import run_scraper
                subjects = Subject.query.all()
                for subject in subjects:
                    try:
                        run_scraper(subject, db)
                    except Exception as e:
                        app.logger.error(f"Scheduler scrape error for {subject.name}: {e}")

        scheduler.add_job(daily_scrape, CronTrigger(hour=2, minute=0))
        scheduler.start()
        app.logger.info("APScheduler started (daily scrape at 2am)")
    except Exception as e:
        app.logger.warning(f"Could not start scheduler: {e}")
