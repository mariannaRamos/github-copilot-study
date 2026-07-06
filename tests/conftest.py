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
    initial_participants = {
        "Chess Club": ["michael@mergington.edu", "daniel@mergington.edu"],
        "Programming Class": ["emma@mergington.edu", "sophia@mergington.edu"],
        "Gym Class": ["john@mergington.edu", "olivia@mergington.edu"],
        "Basketball Team": ["james@mergington.edu", "lucas@mergington.edu"],
        "Tennis Club": ["sarah@mergington.edu"],
        "Art Studio": ["grace@mergington.edu", "aiden@mergington.edu"],
        "Music Band": ["noah@mergington.edu", "ava@mergington.edu"],
        "Debate Club": ["isabella@mergington.edu"],
        "Science Olympiad": ["tyler@mergington.edu", "mia@mergington.edu"],
    }

    for activity_name, activity in activities.items():
        activity["participants"] = list(initial_participants.get(activity_name, []))
    
    return activities


@pytest.fixture(autouse=True)
def auto_reset(reset_activities):
    """
    Auto-use fixture that resets activities after each test to ensure isolation.
    This is applied automatically to all tests.
    """
    pass
