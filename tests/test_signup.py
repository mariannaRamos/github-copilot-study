"""
Tests for the POST /activities/{activity_name}/signup endpoint.
"""

import pytest


def test_signup_successful(client):
    """
    Test successful signup for an activity.
    """
    email = "newstudent@mergington.edu"
    activity_name = "Chess Club"
    
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]


def test_signup_adds_participant_to_list(client):
    """
    Test that signup actually adds the participant to the activity's participants list.
    """
    email = "newstudent@mergington.edu"
    activity_name = "Programming Class"
    
    # Sign up
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Verify participant was added
    activities_response = client.get("/activities")
    assert activities_response.status_code == 200
    activities = activities_response.json()
    assert email in activities[activity_name]["participants"]


def test_signup_nonexistent_activity(client):
    """
    Test that signup for non-existent activity returns 404.
    """
    response = client.post(
        "/activities/NonexistentActivity/signup",
        params={"email": "test@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_signup_duplicate_fails(client):
    """
    Test that signing up for the same activity twice fails with 400.
    """
    email = "michael@mergington.edu"  # Already signed up for Chess Club
    activity_name = "Chess Club"
    
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already" in data["detail"].lower()


def test_signup_different_activities_allowed(client):
    """
    Test that a student can sign up for multiple different activities.
    """
    email = "multistudent@mergington.edu"
    
    # Sign up for first activity
    response1 = client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Sign up for different activity
    response2 = client.post(
        "/activities/Programming Class/signup",
        params={"email": email}
    )
    assert response2.status_code == 200
    
    # Verify in both activities
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities["Chess Club"]["participants"]
    assert email in activities["Programming Class"]["participants"]


def test_signup_near_max_capacity(client):
    """
    Test signup when activity is near max capacity.
    """
    # Tennis Club has max 16 participants, currently has 1
    email = "testcapacity@mergington.edu"
    activity_name = "Tennis Club"
    
    # Get current state
    get_response = client.get("/activities")
    tennis_club = get_response.json()["Tennis Club"]
    participants_before = len(tennis_club["participants"])
    
    # Sign up
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 200
    
    # Verify capacity is still within limit
    get_response = client.get("/activities")
    tennis_club = get_response.json()["Tennis Club"]
    participants_after = len(tennis_club["participants"])
    
    assert participants_after == participants_before + 1
    assert participants_after <= tennis_club["max_participants"]


def test_signup_response_format(client):
    """
    Test that signup response has correct format.
    """
    email = "formattest@mergington.edu"
    response = client.post(
        "/activities/Art Studio/signup",
        params={"email": email}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "message" in data
    assert isinstance(data["message"], str)


def test_signup_various_activities(client):
    """
    Test signup works for various different activities.
    """
    email = "versatile@mergington.edu"
    activities_to_test = [
        "Chess Club",
        "Debate Club",
        "Science Olympiad",
        "Music Band"
    ]
    
    for activity in activities_to_test:
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response.status_code == 200, \
            f"Failed to sign up for {activity}"


def test_signup_email_preserved_exactly(client):
    """
    Test that the exact email address is stored (case-sensitive, no modifications).
    """
    email = "ExactCase@Mergington.edu"
    activity_name = "Music Band"
    
    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    response = client.get("/activities")
    activities = response.json()
    assert email in activities[activity_name]["participants"]
