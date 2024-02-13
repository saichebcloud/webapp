from base64 import b64encode
import json
import pytest
from main import app, database, User

@pytest.fixture
def test_client():

    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root:saisid123@localhost:3306/TEST'
    client = app.test_client()

    with app.app_context():
        database.create_all()

    yield client

    with app.app_context():
        database.drop_all()

def test_create_update_get_user(test_client):

    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "username": "john_doe@gmail.com",
        "password": "password123"
    }
    
    print(f"\nCreating User... with the following details {user_data}")

    postResponse = test_client.post('/v1/user', json=user_data)

    assert postResponse.status_code == 201

    print("\nUser Created.")

    auth_token = f"{user_data['username']}:{user_data['password']}".encode('utf-8')
    base64_auth_token = b64encode(auth_token).decode('utf-8')

    headers = {'Authorization': f'Basic {base64_auth_token}'}

    print("\nMaking GET request to verify user details..")

    getResponse = test_client.get('/v1/user/self', headers=headers)
    assert getResponse.status_code == 200

    print(f"\nResponse Received...{getResponse.json}")

    responseJsonData = getResponse.json

    assert responseJsonData['first_name'] == user_data['first_name']
    assert responseJsonData['last_name'] == user_data['last_name']
    assert responseJsonData['username'] == user_data['username']

    print("\nModifying user details - changing name to Sam")

    modified_data = {
        "first_name" : "Sam"
    }

    putResponse = test_client.put('/v1/user/self', headers=headers, json=modified_data)

    assert putResponse.status_code == 204

    print("\nMaking GET request to verify user details..")

    getResponse = test_client.get('/v1/user/self', headers=headers)
    assert getResponse.status_code == 200

    print(f"\nResponse Received...{getResponse.json}")

    responseJsonData = getResponse.json

    assert responseJsonData['first_name'] == modified_data['first_name']
    assert responseJsonData['last_name'] == user_data['last_name']
    assert responseJsonData['username'] == user_data['username']

    print("\n Finished Testing")