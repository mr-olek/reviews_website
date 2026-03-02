from __future__ import annotations

import os
import random
import uuid

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
    Blueprint, current_app, redirect,
    render_template, request, url_for,
)
from werkzeug.utils import secure_filename

from . import db
from .models import Category, Review, ReviewReply, Subject, SubCategory

main = Blueprint('main', __name__)


@main.before_request
def track_visit():
    from .models import PageView
    db.session.add(PageView(
        path=request.path,
        ip_address=request.remote_addr,
    ))
    db.session.commit()


# ---------------------------------------------------------------------------
# Public routes
# ---------------------------------------------------------------------------

@main.route('/')
def index():
    from .models import Subject
    categories = Category.query.order_by(Category.name).all()
    cat_review_counts = {}
    for cat in categories:
        subjects = Subject.query.join(SubCategory).filter(SubCategory.category_id == cat.id).all()
        cat_review_counts[cat.id] = sum(s.review_count or 0 for s in subjects)
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


def _allowed_file(filename: str) -> bool:
    allowed = current_app.config.get('ALLOWED_EXTENSIONS', {'jpg', 'jpeg', 'png', 'gif', 'webp'})
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed


def _save_upload(file, subfolder: str) -> str | None:
    """Save an uploaded file, return relative path like 'images/uploads/reviews/abc.jpg'."""
    if not file or not file.filename:
        return None
    if not _allowed_file(file.filename):
        return None
    ext = secure_filename(file.filename).rsplit('.', 1)[-1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    upload_dir = os.path.join(current_app.config['UPLOADS_DIR'], subfolder)
    os.makedirs(upload_dir, exist_ok=True)
    file.save(os.path.join(upload_dir, filename))
    return f"images/uploads/{subfolder}/{filename}"


@main.route('/<category_slug>/<subcategory_slug>/')
def subcategory(category_slug, subcategory_slug):
    cat = Category.query.filter_by(slug=category_slug).first_or_404()
    subcat = SubCategory.query.filter_by(category_id=cat.id, slug=subcategory_slug).first_or_404()
    subjects = subcat.subjects.order_by('name').all()
    return render_template('subcategory.html', category=cat, subcategory=subcat, subjects=subjects)


@main.route('/<category_slug>/<subcategory_slug>/<subject_slug>/')
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

    image_path = _save_upload(request.files.get('image'), 'reviews')

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

    return redirect(url_for('main.review', category_slug=category_slug,
                            subcategory_slug=subcategory_slug,
                            subject_slug=subject_slug, review_id=review.id))


@main.route('/<category_slug>/<subcategory_slug>/<subject_slug>/<int:review_id>/')
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
        reply = ReviewReply(
            review_id=rev.id,
            parent_id=parent_id or None,
            author_name=author,
            body=body,
        )
        db.session.add(reply)
        db.session.commit()

    return redirect(url_for('main.review', category_slug=category_slug,
                            subcategory_slug=subcategory_slug,
                            subject_slug=subject_slug, review_id=review_id) + '#replies')
