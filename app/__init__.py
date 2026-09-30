from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from config import config
from werkzeug.middleware.proxy_fix import ProxyFix

db = SQLAlchemy()
cache = Cache()


def create_app(config_name='default'):
    app = Flask(__name__, template_folder='templates', static_folder='../static')
    app.config.from_object(config[config_name])
    # Azure terminates TLS before forwarding requests to Gunicorn.
    if app.config.get('TRUST_PROXY_HEADERS'):
        app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1)

    db.init_app(app)
    cache.init_app(app)

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

    _ensure_persistent_db(app)

    with app.app_context():
        db.create_all()
        _migrate(db)
        _start_scheduler(app)

    return app


def _ensure_persistent_db(app):
    """On Azure App Service, copy seed DB to /home/ on first deploy."""
    import os, shutil
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
    if not db_uri.startswith('sqlite:////'):
        return  # Not an absolute path (local dev), skip
    db_path = db_uri[len('sqlite:///'):]  # e.g. /home/reviews.db
    if os.path.exists(db_path):
        return  # Already exists, nothing to do
    seed = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'instance', 'reviews.db'))
    if os.path.exists(seed):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        shutil.copy2(seed, db_path)
        app.logger.info(f'First deploy: copied seed database to {db_path}')


def _migrate(db):
    """Add legacy columns only when missing; support SQLite and PostgreSQL."""
    from sqlalchemy import inspect, text
    columns = {
        'categories': {'image_path': 'VARCHAR(500)', 'translations': 'TEXT'},
        'subcategories': {'image_path': 'VARCHAR(500)', 'description': 'TEXT',
                          'pros': 'TEXT', 'cons': 'TEXT', 'translations': 'TEXT'},
        'subjects': {'pros': 'TEXT', 'cons': 'TEXT', 'translations': 'TEXT'},
        'reviews': {'translations': 'TEXT'},
        'page_views': {'country': 'VARCHAR(2)', 'device_type': 'VARCHAR(10)'},
    }
    with db.engine.begin() as conn:
        inspector = inspect(conn)
        for table, additions in columns.items():
            existing = {column['name'] for column in inspector.get_columns(table)}
            for column, sql_type in additions.items():
                if column not in existing:
                    conn.execute(text(f'ALTER TABLE {table} ADD COLUMN {column} {sql_type}'))
        for column in ('subject_id', 'is_published', 'created_at'):
            conn.execute(text(f'CREATE INDEX IF NOT EXISTS ix_reviews_{column} ON reviews ({column})'))


def _start_scheduler(app):
    pass  # Scraper disabled
