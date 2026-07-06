"""
Pytest configuration and shared fixtures for FastAPI tests.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Provides a TestClient instance for testing the FastAPI application.
    """
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """
    Fixture to reset activities to their initial state before each test.
    This ensures test isolation since activities are stored in-memory.
    
    Yields the activities dict for test use, then resets it after the test.
    """
    # Store the original state
    original_activities = {
        key: {
            "description": value["description"],
            "schedule": value["schedule"],
            "max_participants": value["max_participants"],
            "participants": value["participants"].copy()  # Copy the list
        }
        for key, value in activities.items()
    }
    
    yield activities
    
    # Reset to original state after test
    activities.clear()
    activities.update(original_activities)


@pytest.fixture
def clean_activities():
    """
    Fixture that provides a fresh activities dict with initial data.
    Use this when you want a clean slate for a test.
    """
    # Reset participants to initial state before the test
    for activity in activities.values():
        activity["participants"] = [
            "michael@mergington.edu", "daniel@mergington.edu"
        ] if activity.get("description") and "Chess" in activity["description"] else \
        ["emma@mergington.edu", "sophia@mergington.edu"] if "Programming" in activity.get("description", "") else \
        ["john@mergington.edu", "olivia@mergington.edu"] if "Gym" in activity.get("description", "") else \
        ["james@mergington.edu", "lucas@mergington.edu"] if "Basketball" in activity.get("description", "") else \
        ["sarah@mergington.edu"] if "Tennis" in activity.get("description", "") else \
        ["grace@mergington.edu", "aiden@mergington.edu"] if "Art" in activity.get("description", "") else \
        ["noah@mergington.edu", "ava@mergington.edu"] if "Music" in activity.get("description", "") else \
        ["isabella@mergington.edu"] if "Debate" in activity.get("description", "") else \
        ["tyler@mergington.edu", "mia@mergington.edu"] if "Science" in activity.get("description", "") else []
    
    return activities


@pytest.fixture(autouse=True)
def auto_reset(reset_activities):
    """
    Auto-use fixture that resets activities after each test to ensure isolation.
    This is applied automatically to all tests.
    """
    pass
