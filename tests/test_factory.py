from src import create_app

def test_config():
    """Test create_app without passing test config."""
    assert not create_app().testing
