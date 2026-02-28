from __future__ import annotations

import logging
import os
import uuid
from datetime import datetime

from flask import (
    Blueprint, current_app, flash, redirect, render_template,
    request, session, url_for,
)
from werkzeug.utils import secure_filename

from . import db
from .models import Category, Review, Subject, SubCategory

logger = logging.getLogger(__name__)
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


# ---------------------------------------------------------------------------
# Auth helpers
# ---------------------------------------------------------------------------

def _is_admin() -> bool:
    return session.get('admin') is True


def admin_required(f):
    import functools
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if not _is_admin():
            return redirect(url_for('admin.login', next=request.path))
        return f(*args, **kwargs)
    return wrapper


def _allowed_file(filename: str) -> bool:
    allowed = current_app.config.get('ALLOWED_EXTENSIONS', {'jpg', 'jpeg', 'png', 'gif', 'webp'})
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed


def _save_upload(file, subfolder: str) -> str | None:
    if not file or not file.filename or not _allowed_file(file.filename):
        return None
    ext = secure_filename(file.filename).rsplit('.', 1)[-1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    upload_dir = os.path.join(current_app.config['UPLOADS_DIR'], subfolder)
    os.makedirs(upload_dir, exist_ok=True)
    file.save(os.path.join(upload_dir, filename))
    return f"images/uploads/{subfolder}/{filename}"


# ---------------------------------------------------------------------------
# Login / Logout
# ---------------------------------------------------------------------------

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if _is_admin():
        return redirect(url_for('admin.dashboard'))
    error = None
    if request.method == 'POST':
        if request.form.get('password') == current_app.config.get('ADMIN_PASSWORD'):
            session['admin'] = True
            session.permanent = False
            next_url = request.args.get('next') or url_for('admin.dashboard')
            return redirect(next_url)
        error = 'Incorrect password.'
    return render_template('admin/login.html', error=error)


@admin_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('admin', None)
    return redirect(url_for('admin.login'))


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------

@admin_bp.route('/')
@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    from datetime import date, timedelta
    from .models import PageView

    stats = {
        'reviews': Review.query.count(),
        'published': Review.query.filter_by(is_published=True).count(),
        'unpublished': Review.query.filter_by(is_published=False).count(),
        'subjects': Subject.query.count(),
        'with_images': Review.query.filter(Review.image_path.isnot(None)).count(),
    }
    recent = Review.query.order_by(Review.created_at.desc()).limit(5).all()

    # Visitor stats — last 30 days per-day counts
    today = date.today()
    days = [today - timedelta(days=i) for i in range(29, -1, -1)]
    day_counts = {}
    for d in days:
        start = datetime(d.year, d.month, d.day)
        end = start + timedelta(days=1)
        count = PageView.query.filter(
            PageView.created_at >= start,
            PageView.created_at < end,
        ).count()
        day_counts[d.isoformat()] = count

    visit_stats = {
        'today': day_counts[today.isoformat()],
        'last_7': sum(list(day_counts.values())[-7:]),
        'last_30': sum(day_counts.values()),
        'chart': [{'date': k, 'count': v} for k, v in day_counts.items()],
    }

    return render_template('admin/dashboard.html', stats=stats, recent=recent, visit_stats=visit_stats)


# ---------------------------------------------------------------------------
# Reviews
# ---------------------------------------------------------------------------

@admin_bp.route('/reviews')
@admin_required
def reviews():
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', '').strip()
    source = request.args.get('source', '')
    published = request.args.get('published', '')

    query = Review.query
    if q:
        query = query.filter(Review.title.ilike(f'%{q}%') | Review.author_name.ilike(f'%{q}%'))
    if source:
        query = query.filter_by(source_site=source)
    if published == '1':
        query = query.filter_by(is_published=True)
    elif published == '0':
        query = query.filter_by(is_published=False)

    pagination = query.order_by(Review.created_at.desc()).paginate(page=page, per_page=20, error_out=False)
    sources = db.session.query(Review.source_site).distinct().all()
    sources = [s[0] for s in sources if s[0]]
    return render_template('admin/reviews.html', pagination=pagination,
                           sources=sources, q=q, source=source, published=published)


@admin_bp.route('/reviews/<int:review_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_review(review_id):
    rev = Review.query.get_or_404(review_id)
    if request.method == 'POST':
        rev.title = request.form.get('title', rev.title).strip()
        rev.body = request.form.get('body', rev.body).strip()
        try:
            rev.rating = max(1, min(5, int(request.form.get('rating', rev.rating))))
        except ValueError:
            pass
        rev.author_name = request.form.get('author_name', rev.author_name).strip()
        rev.is_published = 'is_published' in request.form

        # Replace image if new file uploaded
        new_file = request.files.get('image')
        if new_file and new_file.filename:
            path = _save_upload(new_file, 'reviews')
            if path:
                _delete_file(rev.image_path)
                rev.image_path = path

        db.session.commit()
        rev.subject.update_stats()
        db.session.commit()
        flash('Review updated.', 'success')
        return redirect(url_for('admin.reviews'))

    return render_template('admin/edit_review.html', review=rev)


@admin_bp.route('/reviews/<int:review_id>/delete', methods=['POST'])
@admin_required
def delete_review(review_id):
    rev = Review.query.get_or_404(review_id)
    subj = rev.subject
    _delete_file(rev.image_path)
    db.session.delete(rev)
    db.session.commit()
    subj.update_stats()
    db.session.commit()
    flash('Review deleted.', 'success')
    return redirect(url_for('admin.reviews'))


@admin_bp.route('/reviews/<int:review_id>/delete-image', methods=['POST'])
@admin_required
def delete_review_image(review_id):
    rev = Review.query.get_or_404(review_id)
    _delete_file(rev.image_path)
    rev.image_path = None
    db.session.commit()
    flash('Image removed.', 'success')
    return redirect(url_for('admin.edit_review', review_id=review_id))


@admin_bp.route('/reviews/<int:review_id>/toggle-published', methods=['POST'])
@admin_required
def toggle_published(review_id):
    rev = Review.query.get_or_404(review_id)
    rev.is_published = not rev.is_published
    db.session.commit()
    rev.subject.update_stats()
    db.session.commit()
    return redirect(request.referrer or url_for('admin.reviews'))


# ---------------------------------------------------------------------------
# Subjects
# ---------------------------------------------------------------------------

@admin_bp.route('/subjects')
@admin_required
def subjects():
    all_subjects = Subject.query.order_by(Subject.name).all()
    return render_template('admin/subjects.html', subjects=all_subjects)


@admin_bp.route('/subjects/<int:subject_id>/upload-image', methods=['POST'])
@admin_required
def upload_subject_image(subject_id):
    subj = Subject.query.get_or_404(subject_id)
    file = request.files.get('image')
    path = _save_upload(file, 'subjects')
    if path:
        _delete_file(subj.image_path)
        subj.image_path = path
        db.session.commit()
        flash(f'Photo updated for {subj.name}.', 'success')
    else:
        flash('Invalid file. Use jpg, png, webp, or gif.', 'error')
    return redirect(url_for('admin.subjects'))


@admin_bp.route('/subjects/<int:subject_id>/delete-image', methods=['POST'])
@admin_required
def delete_subject_image(subject_id):
    subj = Subject.query.get_or_404(subject_id)
    _delete_file(subj.image_path)
    subj.image_path = None
    db.session.commit()
    flash(f'Photo removed for {subj.name}.', 'success')
    return redirect(url_for('admin.subjects'))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _delete_file(relative_path: str | None):
    """Delete a file from static/ if it was user-uploaded."""
    if not relative_path or not relative_path.startswith('images/uploads/'):
        return
    full = os.path.join(current_app.root_path, '..', 'static', relative_path)
    try:
        if os.path.exists(full):
            os.remove(full)
    except Exception as e:
        logger.warning(f"Could not delete {full}: {e}")
