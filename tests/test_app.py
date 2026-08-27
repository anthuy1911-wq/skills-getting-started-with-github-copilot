from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_unregister_participant_removes_email():
    original = activities["Chess Club"]["participants"][:]
    response = client.delete("/activities/Chess%20Club/participants?email=michael@mergington.edu")

    assert response.status_code == 200
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
    assert response.json()["message"] == "Unregistered michael@mergington.edu from Chess Club"

    activities["Chess Club"]["participants"] = original


def test_unregister_participant_raises_for_missing_email():
    response = client.delete("/activities/Chess%20Club/participants?email=missing@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
