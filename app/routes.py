from __future__ import annotations

import json
import random

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

def _random_username() -> str:
    return f"{random.choice(_ADJECTIVES)}{random.choice(_ANIMALS)}{random.randint(1, 999)}"

from flask import (
    Blueprint, current_app, make_response, redirect, session,
    render_template, request, url_for,
)
from . import db, cache
from .models import Category, Review, ReviewReply, Subject, SubCategory
from .utils import save_upload

main = Blueprint('main', __name__)


def _ensure_translations(objects, lang: str, fields: list[str]) -> None:
    """
    For any object missing a translation for `lang`, batch-translate `fields`
    via Claude and persist results to the `translations` JSON column.
    Silently skips if no API key is configured or if translation fails.
    """
    if lang == 'en':
        return
    api_key = current_app.config.get('ANTHROPIC_API_KEY', '')
    if not api_key:
        return

    missing = []
    for obj in objects:
        try:
            trans = json.loads(obj.translations or '{}')
        except Exception:
            trans = {}
        if not trans.get(lang):
            missing.append(obj)

    if not missing:
        return

    from .processor import translate_texts_batch, translate_with_google
    items = [
        {'id': obj.id, **{f: getattr(obj, f, '') or '' for f in fields}}
        for obj in missing
    ]

    results = {}
    # Try Claude first (if credits are available)
    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=api_key)
        results = translate_texts_batch(items, lang, fields, client)
    except Exception as e:
        current_app.logger.warning(f"Claude translation failed ({lang}): {e}")

    # Fall back to Google Translate (free, no key needed)
    if not results:
        try:
            results = translate_with_google(items, lang, fields)
        except Exception as e:
            current_app.logger.warning(f"Google translation also failed ({lang}): {e}")

    if results:
        for obj in missing:
            if obj.id in results:
                try:
                    trans = json.loads(obj.translations or '{}')
                except Exception:
                    trans = {}
                trans[lang] = results[obj.id]
                obj.translations = json.dumps(trans, ensure_ascii=False)
        try:
            db.session.commit()
        except Exception as e:
            current_app.logger.warning(f"Failed to save translations: {e}")


@main.route('/lang/<code>')
def set_lang(code):
    from .i18n import LANGUAGES
    if code in LANGUAGES:
        session['lang'] = code
    return redirect(request.referrer or url_for('main.index'))


def _page_cache_key():
    lang = session.get('lang', 'en')
    qs = request.query_string.decode('utf-8', errors='replace')
    return f'page:{request.path}:{qs}:{lang}'


def _detect_device(ua: str) -> str:
    ua = ua.lower()
    if 'ipad' in ua or 'tablet' in ua or ('android' in ua and 'mobile' not in ua):
        return 'tablet'
    if 'mobile' in ua or 'iphone' in ua or 'android' in ua or 'ipod' in ua:
        return 'mobile'
    return 'desktop'


@main.before_request
def track_visit():
    # Skip static files, admin, and bots to avoid unnecessary DB writes
    if (request.path.startswith('/static/')
            or request.path.startswith('/admin/')
            or request.path in ('/favicon.ico', '/robots.txt', '/sitemap.xml', '/llms.txt')):
        return
    from .models import PageView
    ua = request.headers.get('User-Agent', '')
    db.session.add(PageView(
        path=request.path,
        ip_address=request.remote_addr,
        device_type=_detect_device(ua),
    ))
    db.session.commit()


# ---------------------------------------------------------------------------
# Public routes
# ---------------------------------------------------------------------------

@main.route('/')
@cache.cached(timeout=300, key_prefix=_page_cache_key)
def index():
    from sqlalchemy import func
    categories = Category.query.order_by(Category.name).all()
    counts = (
        db.session.query(SubCategory.category_id, func.sum(Subject.review_count))
        .join(Subject, Subject.subcategory_id == SubCategory.id)
        .group_by(SubCategory.category_id)
        .all()
    )
    cat_review_counts = {cat_id: int(count or 0) for cat_id, count in counts}
    total_reviews = sum(cat_review_counts.values())
    total_subjects = Subject.query.count()
    return render_template('index.html', categories=categories, cat_review_counts=cat_review_counts,
                           total_reviews=total_reviews, total_subjects=total_subjects)


_SUBCAT_ORDER = [
    'dogs', 'cats', 'rabbits', 'fish', 'small-animals', 'parrots',
    'horses', 'chickens', 'reptiles', 'ferrets', 'turtles-tortoises',
]

# Food cuisines: Ukrainian first, then by global popularity
_FOOD_ORDER = [
    'ukrainian', 'italian', 'japanese', 'chinese', 'mexican', 'indian',
    'french', 'american', 'thai', 'greek', 'spanish', 'turkish', 'lebanese',
    'korean', 'vietnamese', 'moroccan', 'ethiopian', 'brazilian', 'peruvian',
    'german', 'british', 'russian', 'indonesian', 'malaysian', 'filipino',
    'portuguese', 'argentinian', 'swedish', 'polish', 'hungarian', 'georgian',
    'iranian', 'israeli', 'egyptian', 'nigerian', 'south-african', 'pakistani',
    'sri-lankan', 'cambodian', 'singaporean', 'taiwanese', 'australian',
    'canadian', 'jamaican', 'cuban', 'colombian', 'bangladeshi', 'nepalese',
    'afghan', 'uzbek', 'armenian', 'azerbaijani', 'burmese', 'norwegian',
    'danish', 'czech', 'tunisian', 'ghanaian', 'venezuelan', 'chilean',
    'ecuadorian', 'bolivian',
]

@main.route('/<category_slug>/')
@cache.cached(timeout=300, key_prefix=_page_cache_key)
def category(category_slug):
    from .models import Subject
    cat = Category.query.filter_by(slug=category_slug).first_or_404()
    subcats = SubCategory.query.filter_by(category_id=cat.id).order_by(db.func.lower(SubCategory.name)).all()
    order = _FOOD_ORDER if cat.slug == 'food' else _SUBCAT_ORDER
    subcats.sort(key=lambda s: order.index(s.slug) if s.slug in order else 999)

    # Aggregate review count and avg rating per subcategory
    subcat_stats = {}
    for sc in subcats:
        subjects = Subject.query.filter_by(subcategory_id=sc.id).all()
        total_reviews = sum(s.review_count or 0 for s in subjects)
        rated = [s for s in subjects if s.avg_rating and s.review_count]
        avg = (sum(s.avg_rating * s.review_count for s in rated) / sum(s.review_count for s in rated)) if rated else 0
        subcat_stats[sc.id] = {'review_count': total_reviews, 'avg_rating': round(avg, 1)}

    return render_template('category.html', category=cat, subcategories=subcats, subcat_stats=subcat_stats)




@main.route('/<category_slug>/<subcategory_slug>/')
@cache.cached(timeout=300, key_prefix=_page_cache_key)
def subcategory(category_slug, subcategory_slug):
    cat = Category.query.filter_by(slug=category_slug).first_or_404()
    subcat = SubCategory.query.filter_by(category_id=cat.id, slug=subcategory_slug).first_or_404()
    subjects = subcat.subjects.order_by('name').all()
    return render_template('subcategory.html', category=cat, subcategory=subcat, subjects=subjects)


@main.route('/<category_slug>/<subcategory_slug>/<subject_slug>/')
@cache.cached(timeout=120, key_prefix=_page_cache_key)
def subject(category_slug, subcategory_slug, subject_slug):
    cat = Category.query.filter_by(slug=category_slug).first_or_404()
    subcat = SubCategory.query.filter_by(category_id=cat.id, slug=subcategory_slug).first_or_404()
    subj = Subject.query.filter_by(subcategory_id=subcat.id, slug=subject_slug).first_or_404()

    page = request.args.get('page', 1, type=int)
    pagination = (
        Review.query
        .filter_by(subject_id=subj.id, is_published=True)
        .order_by(Review.created_at.desc())
        .paginate(page=page, per_page=10, error_out=False)
    )
    return render_template('subject.html', category=cat, subcategory=subcat, subject=subj, pagination=pagination)


@main.route('/<category_slug>/<subcategory_slug>/<subject_slug>/submit/', methods=['POST'])
def submit_review(category_slug, subcategory_slug, subject_slug):
    from datetime import datetime
    cat = Category.query.filter_by(slug=category_slug).first_or_404()
    subcat = SubCategory.query.filter_by(category_id=cat.id, slug=subcategory_slug).first_or_404()
    subj = Subject.query.filter_by(subcategory_id=subcat.id, slug=subject_slug).first_or_404()

    title = request.form.get('title', '').strip()
    body = request.form.get('body', '').strip()
    author = request.form.get('author_name', '').strip() or _random_username()
    try:
        rating = max(1, min(5, int(request.form.get('rating', 3))))
    except ValueError:
        rating = 3

    errors = []
    if not title:
        errors.append('Title is required.')
    if not body or len(body) < 20:
        errors.append('Review must be at least 20 characters.')

    if errors:
        page = request.args.get('page', 1, type=int)
        pagination = (
            Review.query
            .filter_by(subject_id=subj.id, is_published=True)
            .order_by(Review.created_at.desc())
            .paginate(page=page, per_page=10, error_out=False)
        )
        return render_template('subject.html', category=cat, subcategory=subcat, subject=subj,
                               pagination=pagination, form_errors=errors,
                               form_data=request.form)

    image_path = save_upload(request.files.get('image'), 'reviews')

    review = Review(
        subject_id=subj.id,
        title=title,
        body=body,
        rating=rating,
        author_name=author,
        source_site='user',
        original_date=datetime.utcnow(),
        is_published=True,
        image_path=image_path,
    )
    db.session.add(review)
    db.session.commit()
    subj.update_stats()
    db.session.commit()
    cache.clear()

    return redirect(url_for('main.review', category_slug=category_slug,
                            subcategory_slug=subcategory_slug,
                            subject_slug=subject_slug, review_id=review.id))


@main.route('/<category_slug>/<subcategory_slug>/<subject_slug>/<int:review_id>/')
@cache.cached(timeout=300, key_prefix=_page_cache_key)
def review(category_slug, subcategory_slug, subject_slug, review_id):
    cat = Category.query.filter_by(slug=category_slug).first_or_404()
    subcat = SubCategory.query.filter_by(category_id=cat.id, slug=subcategory_slug).first_or_404()
    subj = Subject.query.filter_by(subcategory_id=subcat.id, slug=subject_slug).first_or_404()

    rev = Review.query.filter_by(id=review_id, subject_id=subj.id, is_published=True).first_or_404()
    top_replies = rev.all_replies.filter_by(parent_id=None).all()
    return render_template('review.html', category=cat, subcategory=subcat, subject=subj,
                           review=rev, top_replies=top_replies)


@main.route('/<category_slug>/<subcategory_slug>/<subject_slug>/<int:review_id>/reply/', methods=['POST'])
def post_reply(category_slug, subcategory_slug, subject_slug, review_id):
    cat = Category.query.filter_by(slug=category_slug).first_or_404()
    subcat = SubCategory.query.filter_by(category_id=cat.id, slug=subcategory_slug).first_or_404()
    subj = Subject.query.filter_by(subcategory_id=subcat.id, slug=subject_slug).first_or_404()
    rev = Review.query.filter_by(id=review_id, subject_id=subj.id, is_published=True).first_or_404()

    author = request.form.get('author_name', '').strip()
    body = request.form.get('body', '').strip()
    parent_id = request.form.get('parent_id', type=int)

    if author and body:
        # Cap nesting at 2 levels: flatten deeper replies to the top-level parent
        if parent_id:
            parent = ReviewReply.query.get(parent_id)
            if parent and parent.parent_id is not None:
                parent_id = parent.parent_id
        reply = ReviewReply(
            review_id=rev.id,
            parent_id=parent_id or None,
            author_name=author,
            body=body,
        )
        db.session.add(reply)
        db.session.commit()
        cache.clear()

    return redirect(url_for('main.review', category_slug=category_slug,
                            subcategory_slug=subcategory_slug,
                            subject_slug=subject_slug, review_id=review_id) + '#replies')


# ---------------------------------------------------------------------------
# SEO / discoverability routes
# ---------------------------------------------------------------------------

@main.route('/go/youtube')
def youtube_redirect():
    return redirect('https://www.youtube.com/@Carpe_Diem_Travels/videos')


@main.route('/sitemap.xml')
def sitemap():
    base = request.host_url.rstrip('/')
    pages = [{'loc': base + '/', 'changefreq': 'daily', 'priority': '1.0', 'lastmod': None}]

    categories = Category.query.all()
    cat_dict = {c.id: c for c in categories}
    subcats = SubCategory.query.all()
    subcat_dict = {s.id: s for s in subcats}

    for cat in categories:
        pages.append({'loc': base + url_for('main.category', category_slug=cat.slug),
                      'changefreq': 'weekly', 'priority': '0.9', 'lastmod': None})

    for sc in subcats:
        cat = cat_dict.get(sc.category_id)
        if not cat:
            continue
        pages.append({'loc': base + url_for('main.subcategory', category_slug=cat.slug, subcategory_slug=sc.slug),
                      'changefreq': 'weekly', 'priority': '0.8', 'lastmod': None})

    subjects = Subject.query.all()
    subj_dict = {s.id: s for s in subjects}
    for subj in subjects:
        sc = subcat_dict.get(subj.subcategory_id)
        cat = cat_dict.get(sc.category_id) if sc else None
        if not sc or not cat:
            continue
        pages.append({'loc': base + url_for('main.subject', category_slug=cat.slug,
                                            subcategory_slug=sc.slug, subject_slug=subj.slug),
                      'changefreq': 'daily', 'priority': '0.7', 'lastmod': None})

    rows = (db.session.query(Review.id, Review.subject_id, Review.created_at)
            .filter_by(is_published=True).all())
    for row in rows:
        subj = subj_dict.get(row.subject_id)
        sc = subcat_dict.get(subj.subcategory_id) if subj else None
        cat = cat_dict.get(sc.category_id) if sc else None
        if not subj or not sc or not cat:
            continue
        pages.append({'loc': base + url_for('main.review', category_slug=cat.slug,
                                            subcategory_slug=sc.slug, subject_slug=subj.slug,
                                            review_id=row.id),
                      'changefreq': 'monthly', 'priority': '0.5',
                      'lastmod': row.created_at.strftime('%Y-%m-%d') if row.created_at else None})

    resp = make_response(render_template('sitemap.xml', pages=pages))
    resp.headers['Content-Type'] = 'application/xml; charset=utf-8'
    return resp


@main.route('/robots.txt')
def robots():
    base = request.host_url.rstrip('/')
    resp = make_response(render_template('robots.txt', base_url=base))
    resp.headers['Content-Type'] = 'text/plain; charset=utf-8'
    return resp


@main.route('/llms.txt')
def llms():
    base = request.host_url.rstrip('/')
    categories = Category.query.order_by(Category.name).all()
    resp = make_response(render_template('llms.txt', categories=categories, base_url=base))
    resp.headers['Content-Type'] = 'text/plain; charset=utf-8'
    return resp
