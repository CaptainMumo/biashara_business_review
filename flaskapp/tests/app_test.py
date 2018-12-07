def test_app(test_client):
    #response = test_client.get("/")
    #assert response.status_code == 200
    response = test_client.get('/')
    
    assert response.status_code == 200