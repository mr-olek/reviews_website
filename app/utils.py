"""Shared upload helpers used by both routes.py and admin.py."""
from __future__ import annotations

import os
import uuid

from flask import current_app
from werkzeug.utils import secure_filename


def allowed_file(filename: str) -> bool:
    allowed = current_app.config.get('ALLOWED_EXTENSIONS', {'jpg', 'jpeg', 'png', 'gif', 'webp'})
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed


def save_upload(file, subfolder: str) -> str | None:
    """Save an uploaded file and return its relative path, or None on failure."""
    if not file or not file.filename or not allowed_file(file.filename):
        return None
    ext = secure_filename(file.filename).rsplit('.', 1)[-1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    upload_dir = os.path.join(current_app.config['UPLOADS_DIR'], subfolder)
    os.makedirs(upload_dir, exist_ok=True)
    file.save(os.path.join(upload_dir, filename))
    return f"images/uploads/{subfolder}/{filename}"
