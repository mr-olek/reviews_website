#!/bin/bash
set -euo pipefail

# Run in the deployed application directory, including Oryx extracted builds.
cd "$(dirname "$0")"
mkdir -p /home/uploads/{reviews,subjects,subcategories,categories}
# Seed uploads once without replacing files changed by site users.
if [ -d static/images/uploads ] && [ ! -L static/images/uploads ]; then
    cp -Rn static/images/uploads/. /home/uploads/
fi
# Config uses /home/uploads, while Flask serves it through the static symlink.
if [ ! -L static/images/uploads ]; then
    mv static/images/uploads static/images/uploads-seed
fi
ln -sfn /home/uploads static/images/uploads

if [ ! -f /home/reviews.db ]; then
    cp instance/reviews.db /home/reviews.db
fi
exec gunicorn --bind=0.0.0.0:8000 --timeout=120 --workers=3 'app:create_app("production")'
