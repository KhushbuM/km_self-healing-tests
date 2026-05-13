import requests
import pytest

BASE_URL = "https://jsonplaceholder.typicode.com"

def test_get_all_users():
    """Test that we can fetch a list of users"""
    response = requests.get(f"{BASE_URL}/users")

    assert response.status_code == 200
    assert len(response.json()) > 0
    print(f"✓ Got {len(response.json())} users")

def test_get_single_user():
     """Test fetching one specific user by ID"""
     response = requests.get(f"{BASE_URL}/users/1")
     user = response.json()

     assert response.status_code == 200
     assert user["id"] == 1
     assert "name" in user
     assert "email" in user
     print(f"✓ Got user: {user['name']}")

def test_create_user():
      """Test creating a new user (POST request)"""

      new_user = {
           "name": "Test User",
            "username": "testuser",
            "email": "test@example.com"
            }
      response = requests.post(f"{BASE_URL}/users", json=new_user)
      user_details = response.json()

      assert response.status_code == 201
      assert user_details["name"] == new_user["name"]
      print(f"✓ Created user with ID: {user_details["id"]}")

def test_delete_user():
     """Test deleting a user"""
     response = requests.delete(f"{BASE_URL}/users/1")   

     assert response.status_code == 200
     print(f"✓ User deleted successfully")   
          