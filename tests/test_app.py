import os
import sys
import pytest

# Ensure src is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from app import app, activities
from fastapi.testclient import TestClient


def test_get_activities():
    with TestClient(app) as client:
        resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Basketball" in data


def test_signup_and_unregister_cycle():
    activity_name = "Chess Club"
    email = "test-participant@example.com"

    # Ensure clean state
    if email in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].remove(email)

    with TestClient(app) as client:
        # Sign up
        r = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert r.status_code == 200
        assert email in activities[activity_name]["participants"]

        # Duplicate signup should fail
        r_dup = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert r_dup.status_code == 400

        # Unregister
        r_del = client.delete(f"/activities/{activity_name}/signup?email={email}")
        assert r_del.status_code == 200
        assert email not in activities[activity_name]["participants"]
