import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_unregister_participant_removes_student_from_activity(client):
    original_activities = copy.deepcopy(activities)

    try:
        response = client.delete(
            "/activities/Chess Club/participants?email=michael@mergington.edu"
        )

        assert response.status_code == 200
        payload = response.json()
        assert payload["message"] == "Removed michael@mergington.edu from Chess Club"
        assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
        assert "daniel@mergington.edu" in activities["Chess Club"]["participants"]
    finally:
        activities.clear()
        activities.update(original_activities)
