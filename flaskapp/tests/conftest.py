import pytest
from flaskapp import app

@pytest.fixture(scope='module')
def test_client(request):
    app.config['TESTING']=True
    
    app_client = app.test_client()
    
    ctx = app.app_context()
    ctx.push()

    yield app_client

    ctx.pop()