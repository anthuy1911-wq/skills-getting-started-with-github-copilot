from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_signup_saves_student_details():
    original = activities["Science Club"]["participants"][:]
    response = client.post(
        "/activities/Science%20Club/signup?email=student@mergington.edu&student_class=10&dob=2009-05-18&interest=Robotics"
    )

    assert response.status_code == 200
    stored = next(
        participant for participant in activities["Science Club"]["participants"]
        if participant.get("email") == "student@mergington.edu"
    )
    assert stored["student_class"] == "10"
    assert stored["dob"] == "2009-05-18"
    assert stored["interest"] == "Robotics"

    activities["Science Club"]["participants"] = original


def test_unregister_participant_removes_email():
    original = activities["Chess Club"]["participants"][:]
    response = client.delete("/activities/Chess%20Club/participants?email=michael@mergington.edu")

    assert response.status_code == 200
    assert "michael@mergington.edu" not in [
        participant.get("email") if isinstance(participant, dict) else participant
        for participant in activities["Chess Club"]["participants"]
    ]
    assert response.json()["message"] == "Unregistered michael@mergington.edu from Chess Club"

    activities["Chess Club"]["participants"] = original


def test_unregister_participant_raises_for_missing_email():
    response = client.delete("/activities/Chess%20Club/participants?email=missing@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
