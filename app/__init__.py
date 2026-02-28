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

    with app.app_context():
        db.create_all()
        _start_scheduler(app)

    return app


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
