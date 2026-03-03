#!/bin/bash

# Ensure persistent uploads directory exists on /home
mkdir -p /home/uploads/reviews
mkdir -p /home/uploads/subjects
mkdir -p /home/uploads/subcategories
mkdir -p /home/uploads/categories

# Symlink static/images/uploads to persistent storage
rm -rf /home/site/wwwroot/static/images/uploads
ln -sfn /home/uploads /home/site/wwwroot/static/images/uploads

# Seed DB if it doesn't exist yet
if [ ! -f /home/reviews.db ]; then
    echo "First deploy — seeding database..."
    cd /home/site/wwwroot && python3 seed.py
fi

# Symlink DB to persistent storage
ln -sfn /home/reviews.db /home/site/wwwroot/reviews.db

# Start gunicorn
cd /home/site/wwwroot
gunicorn --bind=0.0.0.0:8000 --timeout=120 --workers=2 run:app
