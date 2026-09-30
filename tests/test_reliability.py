import os
import unittest
from unittest.mock import patch
import re
import io
import tempfile

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

    def post_form(self, path, data=None):
        page = path.removesuffix('submit/').removesuffix('reply/')
        response = self.client.get(page)
        token = re.search(rb'name="csrf_token" value="([^"]+)"', response.data).group(1).decode()
        return self.client.post(path, data={**(data or {}), 'csrf_token': token})

    def test_tracking_failure_does_not_break_browsing(self):
        with patch.object(db.session, 'commit', side_effect=OperationalError('commit', {}, Exception('database is locked'))):
            response = self.client.get('/animals/dogs/', headers={'User-Agent': 'Mozilla/5.0'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Retriever', response.data)
        with self.app.app_context():
            self.assertEqual(Subject.query.count(), 1)

    def test_review_and_reply_workflow(self):
        path = '/animals/dogs/retriever/'
        self.assertEqual(self.post_form(path + 'submit/', data={'body': 'short'}).status_code, 200)
        response = self.post_form(path + 'submit/', data={'title': 'Good dog', 'body': 'A wonderful friendly family companion.', 'rating': '5', 'author_name': 'Tester'})
        self.assertEqual(response.status_code, 302)
        review_path = response.headers['Location']
        self.assertEqual(self.client.get(review_path).status_code, 200)
        self.assertEqual(self.post_form(review_path + 'reply/', data={'author_name': 'Reader', 'body': 'Thank you!'}).status_code, 302)
        self.assertIn(b'Thank you!', self.client.get(review_path).data)
        with self.app.app_context():
            self.assertEqual(Review.query.count(), 1)
            self.assertEqual(db.session.get(Subject, 1).review_count, 1)

    def test_forms_reject_missing_csrf_tokens(self):
        self.assertEqual(self.client.post('/animals/dogs/retriever/submit/', data={'title': 'Forged'}).status_code, 400)
        self.assertEqual(self.client.post('/admin/login', data={}).status_code, 400)

    def test_form_tokens_are_separate_for_each_visitor(self):
        path = '/animals/dogs/retriever/'
        other = self.app.test_client()
        a = self.client.get(path)
        b = other.get(path)
        pattern = rb'name="csrf_token" value="([^"]+)"'
        first = re.search(pattern, a.data).group(1).decode()
        second = re.search(pattern, b.data).group(1).decode()
        self.assertNotEqual(first, second)
        self.assertEqual(other.post(path + 'submit/', data={'csrf_token': first}).status_code, 400)
        self.assertEqual(other.post(path + 'submit/', data={'csrf_token': second}).status_code, 200)

    def test_uploads_validate_image_content(self):
        from app.utils import save_upload
        from PIL import Image
        from werkzeug.datastructures import FileStorage
        with tempfile.TemporaryDirectory() as directory, self.app.app_context():
            self.app.config['UPLOADS_DIR'] = directory
            invalid = FileStorage(stream=io.BytesIO(b'<html>Not a photo</html>'), filename='bad.jpg')
            self.assertIsNone(save_upload(invalid, 'reviews'))
            data = io.BytesIO()
            Image.new('RGB', (2, 2)).save(data, 'PNG')
            data.seek(0)
            valid = FileStorage(stream=data, filename='photo.jpg')
            self.assertTrue(save_upload(valid, 'reviews').endswith('.png'))

    def test_admin_login_rejects_external_redirects(self):
        response = self.client.get('/admin/login')
        token = re.search(rb'name="csrf_token" value="([^"]+)"', response.data).group(1).decode()
        response = self.client.post('/admin/login?next=//example.com', data={
            'csrf_token': token, 'username': self.app.config['ADMIN_USERNAME'],
            'password': self.app.config['ADMIN_PASSWORD']})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], '/admin/dashboard')

    def test_search_filtering_and_sorting(self):
        response = self.client.get('/search/?q=Retriever')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Retriever', response.data)
        for path in ['/search/?q=%25', '/search/?q=no-such-topic', '/animals/dogs/?q=Retriever&sort=rating', '/animals/dogs/?sort=invalid']:
            self.assertEqual(self.client.get(path).status_code, 200)
        self.assertNotIn(b'class="subject-card"', self.client.get('/search/?q=%25').data)

    def test_language_switching_and_unknown_pages(self):
        for language in ('en', 'uk', 'de', 'fr', 'es'):
            self.assertEqual(self.client.get('/lang/' + language).status_code, 302)
            self.assertEqual(self.client.get('/animals/dogs/').status_code, 200)
        self.assertEqual(self.client.get('/unknown/').status_code, 404)


if __name__ == '__main__':
    unittest.main()
