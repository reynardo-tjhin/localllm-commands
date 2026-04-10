from src.db import get_db

def test_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()
    