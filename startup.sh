#!/bin/bash

# Ensure persistent uploads directories exist on /home
mkdir -p /home/uploads/reviews
mkdir -p /home/uploads/subjects
mkdir -p /home/uploads/subcategories
mkdir -p /home/uploads/categories

# Symlink static/images/uploads to persistent storage
rm -rf /home/site/wwwroot/static/images/uploads
ln -sfn /home/uploads /home/site/wwwroot/static/images/uploads

# On first deploy, copy seed DB from repo to persistent storage
if [ ! -f /home/reviews.db ]; then
    echo "First deploy — copying seed database to persistent storage..."
    cp /home/site/wwwroot/instance/reviews.db /home/reviews.db
fi

# Start gunicorn (DATABASE_URL points to /home/reviews.db via env var)
cd /home/site/wwwroot
gunicorn --bind=0.0.0.0:8000 --timeout=120 --workers=2 run:app
