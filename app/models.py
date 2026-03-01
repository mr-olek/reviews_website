from datetime import datetime
from . import db


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))  # emoji or icon class
    image_path = db.Column(db.String(500))

    subcategories = db.relationship('SubCategory', backref='category', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Category {self.name}>'


class SubCategory(db.Model):
    __tablename__ = 'subcategories'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), nullable=False)
    image_path = db.Column(db.String(500))

    subjects = db.relationship('Subject', backref='subcategory', lazy='dynamic', cascade='all, delete-orphan')

    __table_args__ = (db.UniqueConstraint('category_id', 'slug'),)

    def __repr__(self):
        return f'<SubCategory {self.name}>'


class Subject(db.Model):
    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategories.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    pros = db.Column(db.Text)   # newline-separated bullet points
    cons = db.Column(db.Text)   # newline-separated bullet points
    image_path = db.Column(db.String(500))
    avg_rating = db.Column(db.Float, default=0.0)
    review_count = db.Column(db.Integer, default=0)

    reviews = db.relationship('Review', backref='subject', lazy='dynamic', cascade='all, delete-orphan')
    scraper_jobs = db.relationship('ScraperJob', backref='subject', lazy='dynamic', cascade='all, delete-orphan')

    __table_args__ = (db.UniqueConstraint('subcategory_id', 'slug'),)

    def update_stats(self):
        published = self.reviews.filter_by(is_published=True).all()
        self.review_count = len(published)
        if published:
            self.avg_rating = sum(r.rating for r in published) / len(published)
        else:
            self.avg_rating = 0.0

    def __repr__(self):
        return f'<Subject {self.name}>'


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    title = db.Column(db.String(500), nullable=False)
    body = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    author_name = db.Column(db.String(200))
    original_url = db.Column(db.String(1000), unique=True)
    source_site = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    original_date = db.Column(db.DateTime)
    is_published = db.Column(db.Boolean, default=False)
    image_path = db.Column(db.String(500))

    all_replies = db.relationship('ReviewReply', backref='review', lazy='dynamic',
                                  cascade='all, delete-orphan',
                                  foreign_keys='ReviewReply.review_id',
                                  order_by='ReviewReply.created_at')

    def __repr__(self):
        return f'<Review {self.id}: {self.title[:50]}>'


class ReviewReply(db.Model):
    __tablename__ = 'review_replies'

    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey('reviews.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('review_replies.id'), nullable=True)
    author_name = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    children = db.relationship('ReviewReply', backref=db.backref('parent', remote_side='ReviewReply.id'),
                               lazy='dynamic', order_by='ReviewReply.created_at')

    def __repr__(self):
        return f'<ReviewReply {self.id} on review {self.review_id}>'


class PageView(db.Model):
    __tablename__ = 'page_views'

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(500), nullable=False)
    ip_address = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f'<PageView {self.path}>'


class ScraperJob(db.Model):
    __tablename__ = 'scraper_jobs'

    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    source_site = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='pending')  # pending, running, done, error
    last_run = db.Column(db.DateTime)
    reviews_found = db.Column(db.Integer, default=0)
    error_message = db.Column(db.Text)

    def __repr__(self):
        return f'<ScraperJob {self.source_site} for subject {self.subject_id}>'
