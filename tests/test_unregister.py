"""
Tests for the POST /activities/{activity_name}/unregister endpoint.
"""

import pytest


def test_unregister_successful(client):
    """
    Test successful unregister from an activity.
    """
    email = "michael@mergington.edu"  # Already signed up for Chess Club
    activity_name = "Chess Club"
    
    response = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]


def test_unregister_removes_participant(client):
    """
    Test that unregister actually removes the participant from the list.
    """
    email = "michael@mergington.edu"
    activity_name = "Chess Club"
    
    # Verify they're in the list before
    get_response = client.get("/activities")
    assert email in get_response.json()[activity_name]["participants"]
    
    # Unregister
    response = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Verify they're removed
    get_response = client.get("/activities")
    assert email not in get_response.json()[activity_name]["participants"]


def test_unregister_nonexistent_activity(client):
    """
    Test that unregister from non-existent activity returns 404.
    """
    response = client.post(
        "/activities/NonexistentActivity/unregister",
        params={"email": "test@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_unregister_not_signed_up(client):
    """
    Test that unregistering when not signed up fails with 400.
    """
    email = "notsignedup@mergington.edu"
    activity_name = "Chess Club"
    
    response = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "not signed up" in data["detail"].lower()


def test_unregister_then_signup_again(client):
    """
    Test that a student can unregister and then sign up again for the same activity.
    """
    email = "resignup@mergington.edu"
    activity_name = "Programming Class"
    
    # First signup
    response1 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Verify signup
    get_response = client.get("/activities")
    assert email in get_response.json()[activity_name]["participants"]
    
    # Unregister
    response2 = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    assert response2.status_code == 200
    
    # Verify unregistered
    get_response = client.get("/activities")
    assert email not in get_response.json()[activity_name]["participants"]
    
    # Sign up again
    response3 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    assert response3.status_code == 200
    
    # Verify signed up again
    get_response = client.get("/activities")
    assert email in get_response.json()[activity_name]["participants"]


def test_unregister_independent_activities(client):
    """
    Test that unregistering from one activity doesn't affect others.
    """
    email = "multitest@mergington.edu"
    
    # Sign up for two activities
    client.post("/activities/Chess Club/signup", params={"email": email})
    client.post("/activities/Programming Class/signup", params={"email": email})
    
    # Unregister from one
    response = client.post(
        "/activities/Chess Club/unregister",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Verify unregistered from Chess but still in Programming
    get_response = client.get("/activities")
    activities = get_response.json()
    assert email not in activities["Chess Club"]["participants"]
    assert email in activities["Programming Class"]["participants"]


def test_unregister_response_format(client):
    """
    Test that unregister response has correct format.
    """
    email = "daniel@mergington.edu"  # Already signed up for Chess Club
    response = client.post(
        "/activities/Chess Club/unregister",
        params={"email": email}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "message" in data
    assert isinstance(data["message"], str)


def test_unregister_various_activities(client):
    """
    Test unregister works for various different activities.
    """
    email = "versatile@mergington.edu"
    activities_to_test = [
        ("Art Studio", "grace@mergington.edu"),
        ("Music Band", "noah@mergington.edu"),
        ("Debate Club", "isabella@mergington.edu"),
        ("Science Olympiad", "tyler@mergington.edu")
    ]
    
    for activity_name, existing_email in activities_to_test:
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": existing_email}
        )
        assert response.status_code == 200, \
            f"Failed to unregister from {activity_name}"


def test_unregister_twice_fails(client):
    """
    Test that unregistering twice fails on the second attempt.
    """
    email = "michael@mergington.edu"
    activity_name = "Chess Club"
    
    # First unregister
    response1 = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Second unregister should fail
    response2 = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    assert response2.status_code == 400
    data = response2.json()
    assert "not signed up" in data["detail"].lower()


def test_unregister_participant_count_decreases(client):
    """
    Test that participant count decreases after unregister.
    """
    email = "counttest@mergington.edu"
    activity_name = "Gym Class"
    
    # Get count before signup
    get_response = client.get("/activities")
    count_before = len(get_response.json()[activity_name]["participants"])
    
    # Sign up
    client.post(f"/activities/{activity_name}/signup", params={"email": email})
    
    # Verify count increased
    get_response = client.get("/activities")
    count_after_signup = len(get_response.json()[activity_name]["participants"])
    assert count_after_signup == count_before + 1
    
    # Unregister
    client.post(f"/activities/{activity_name}/unregister", params={"email": email})
    
    # Verify count back to original
    get_response = client.get("/activities")
    count_after_unregister = len(get_response.json()[activity_name]["participants"])
    assert count_after_unregister == count_before
