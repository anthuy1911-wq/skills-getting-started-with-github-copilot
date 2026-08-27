"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "address": "Room 101, Library Wing",
        "fee": 15,
        "max_participants": 12,
        "participants": [
            {"email": "michael@mergington.edu", "student_class": "9", "dob": "2009-02-14", "interest": "Strategy"},
            {"email": "daniel@mergington.edu", "student_class": "10", "dob": "2009-05-10", "interest": "Tactics"}
        ]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "address": "Room 204, Computer Lab",
        "fee": 20,
        "max_participants": 20,
        "participants": [
            {"email": "emma@mergington.edu", "student_class": "11", "dob": "2008-06-03", "interest": "Web apps"},
            {"email": "sophia@mergington.edu", "student_class": "10", "dob": "2009-09-11", "interest": "Python"}
        ]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "address": "North Gym, Main Building",
        "fee": 10,
        "max_participants": 30,
        "participants": [
            {"email": "john@mergington.edu", "student_class": "9", "dob": "2010-01-24", "interest": "Basketball"},
            {"email": "olivia@mergington.edu", "student_class": "11", "dob": "2008-04-30", "interest": "Volleyball"}
        ]
    },
    "Soccer Team": {
        "description": "Practice soccer skills and compete in school matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "address": "Field House, East Campus",
        "fee": 25,
        "max_participants": 22,
        "participants": []
    },
    "Basketball Team": {
        "description": "Develop basketball skills and play competitive games",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "address": "South Gym, Main Building",
        "fee": 25,
        "max_participants": 15,
        "participants": []
    },
    "Art Club": {
        "description": "Explore drawing, painting, and other visual art techniques",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "address": "Room 150, Arts Center",
        "fee": 12,
        "max_participants": 18,
        "participants": []
    },
    "Drama Club": {
        "description": "Practice acting and produce performances for the school community",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "address": "Auditorium Stage, Main Hall",
        "fee": 18,
        "max_participants": 20,
        "participants": []
    },
    "Debate Club": {
        "description": "Build critical thinking and public speaking skills through debate",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "address": "Room 315, Humanities Wing",
        "fee": 14,
        "max_participants": 16,
        "participants": []
    },
    "Science Club": {
        "description": "Investigate scientific questions through experiments and discussion",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "address": "Science Lab 2, West Building",
        "fee": 16,
        "max_participants": 20,
        "participants": []
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


def _participant_email(participant):
    if isinstance(participant, dict):
        return participant.get("email")
    return participant


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(
    activity_name: str,
    email: str,
    student_class: str = "",
    dob: str = "",
    interest: str = "",
):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if any(_participant_email(participant) == email for participant in activity["participants"]):
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")

    # Add student with additional details
    activity["participants"].append({
        "email": email,
        "student_class": student_class,
        "dob": dob,
        "interest": interest,
    })
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/participants")
def unregister_participant(activity_name: str, email: str):
    """Unregister a student from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]
    matching_participant = next(
        (participant for participant in activity["participants"] if _participant_email(participant) == email),
        None,
    )
    if matching_participant is None:
        raise HTTPException(status_code=404, detail="Participant not found")

    activity["participants"].remove(matching_participant)
    return {"message": f"Unregistered {email} from {activity_name}"}

