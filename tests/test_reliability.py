import os
import unittest
from unittest.mock import patch

os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
os.environ['ANTHROPIC_API_KEY'] = ''

from app import create_app, db, cache
from app.models import Category, SubCategory, Subject, Review
from sqlalchemy.exc import OperationalError


class ReliabilityTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app('production')
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        with self.app.app_context():
            db.session.add(Category(id=1, name='Animals', slug='animals'))
            db.session.add(SubCategory(id=1, category_id=1, name='Dogs', slug='dogs'))
            db.session.add(Subject(id=1, subcategory_id=1, name='Retriever', slug='retriever'))
            db.session.commit()
            cache.clear()

    def test_tracking_failure_does_not_break_browsing(self):
        with patch.object(db.session, 'commit', side_effect=OperationalError('commit', {}, Exception('database is locked'))):
            response = self.client.get('/animals/dogs/', headers={'User-Agent': 'Mozilla/5.0'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Retriever', response.data)
        with self.app.app_context():
            self.assertEqual(Subject.query.count(), 1)

    def test_review_and_reply_workflow(self):
        path = '/animals/dogs/retriever/'
        self.assertEqual(self.client.post(path + 'submit/', data={'body': 'short'}).status_code, 200)
        response = self.client.post(path + 'submit/', data={'title': 'Good dog', 'body': 'A wonderful friendly family companion.', 'rating': '5', 'author_name': 'Tester'})
        self.assertEqual(response.status_code, 302)
        review_path = response.headers['Location']
        self.assertEqual(self.client.get(review_path).status_code, 200)
        self.assertEqual(self.client.post(review_path + 'reply/', data={'author_name': 'Reader', 'body': 'Thank you!'}).status_code, 302)
        self.assertIn(b'Thank you!', self.client.get(review_path).data)
        with self.app.app_context():
            self.assertEqual(Review.query.count(), 1)
            self.assertEqual(db.session.get(Subject, 1).review_count, 1)

    def test_language_switching_and_unknown_pages(self):
        for language in ('en', 'uk', 'de', 'fr', 'es'):
            self.assertEqual(self.client.get('/lang/' + language).status_code, 302)
            self.assertEqual(self.client.get('/animals/dogs/').status_code, 200)
        self.assertEqual(self.client.get('/unknown/').status_code, 404)


if __name__ == '__main__':
    unittest.main()
