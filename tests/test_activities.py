"""
Tests for the GET /activities endpoint.
"""

import pytest


def test_get_activities_returns_all_activities(client):
    """
    Test that GET /activities returns all activities.
    """
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    
    # Verify we have all expected activities
    assert len(activities) == 9
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert "Gym Class" in activities
    assert "Basketball Team" in activities
    assert "Tennis Club" in activities
    assert "Art Studio" in activities
    assert "Music Band" in activities
    assert "Debate Club" in activities
    assert "Science Olympiad" in activities


def test_get_activities_response_structure(client):
    """
    Test that each activity in the response has the required fields.
    """
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    
    required_fields = {"description", "schedule", "max_participants", "participants"}
    
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_name, str)
        assert isinstance(activity_data, dict)
        assert required_fields.issubset(activity_data.keys()), \
            f"Activity '{activity_name}' missing required fields"
        
        # Validate field types
        assert isinstance(activity_data["description"], str)
        assert isinstance(activity_data["schedule"], str)
        assert isinstance(activity_data["max_participants"], int)
        assert isinstance(activity_data["participants"], list)


def test_get_activities_data_integrity(client):
    """
    Test that activity data is correct and consistent.
    """
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    
    chess_club = activities["Chess Club"]
    assert chess_club["description"] == "Learn strategies and compete in chess tournaments"
    assert chess_club["schedule"] == "Fridays, 3:30 PM - 5:00 PM"
    assert chess_club["max_participants"] == 12
    assert isinstance(chess_club["participants"], list)
    assert len(chess_club["participants"]) > 0


def test_get_activities_max_participants_positive(client):
    """
    Test that max_participants is always positive.
    """
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    
    for activity_name, activity_data in activities.items():
        assert activity_data["max_participants"] > 0, \
            f"Activity '{activity_name}' has non-positive max_participants"


def test_get_activities_participants_within_limit(client):
    """
    Test that current participants don't exceed max_participants.
    """
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    
    for activity_name, activity_data in activities.items():
        assert len(activity_data["participants"]) <= activity_data["max_participants"], \
            f"Activity '{activity_name}' exceeds max_participants"
