from datetime import datetime, timezone
from pathlib import Path


def create_project(client) -> int:
    response = client.post(
        "/api/projects",
        json={
            "name": "GraphRAG Capstone",
            "description": "Embedded and AI mixed capstone",
            "status": "design",
        },
    )
    assert response.status_code == 201
    return response.json()["id"]


def test_project_crud_and_timeline(client) -> None:
    project_id = create_project(client)

    repository_response = client.post(
        f"/api/projects/{project_id}/repositories",
        json={
            "platform": "github",
            "name": "labpilot-api",
            "owner": "hyuns",
            "url": "https://github.com/hyuns/labpilot-api",
            "last_synced_at": datetime.now(timezone.utc).isoformat(),
        },
    )
    assert repository_response.status_code == 201

    log_response = client.post(
        "/api/experiment-logs",
        json={
            "project_id": project_id,
            "title": "LoRa Range Test",
            "recorded_at": datetime.now(timezone.utc).isoformat(),
            "objective": "Measure field range",
            "board_firmware_version": "v0.2.1",
            "conditions": "Open field, 5C, clear sky",
            "result": "Stable at 900m",
            "issues": "RSSI drops near trees",
            "next_action": "Tune antenna",
            "related_git_reference": "commit:abc123",
        },
    )
    assert log_response.status_code == 201

    issue_response = client.post(
        "/api/hardware-issues",
        json={
            "project_id": project_id,
            "title": "GPS cold start delay",
            "category": "sensor",
            "severity": "high",
            "symptoms": "Initial fix takes more than 2 minutes",
            "reproduction_conditions": "Power-on after 12 hours idle",
            "suspected_cause": "Weak antenna placement",
            "attempted_fixes": "Moved module and reflashed firmware",
            "status": "investigating",
            "related_git_issue": "github#12",
        },
    )
    assert issue_response.status_code == 201
    issue_id = issue_response.json()["id"]

    upload_response = client.post(
        f"/api/hardware-issues/{issue_id}/attachments",
        files={"file": ("wiring.jpg", b"binary-image-data", "image/jpeg")},
    )
    assert upload_response.status_code == 201
    upload_payload = upload_response.json()
    assert upload_payload["file_name"] == "wiring.jpg"
    assert Path(upload_payload["storage_path"]).exists()

    timeline_response = client.get(f"/api/projects/{project_id}/timeline")
    assert timeline_response.status_code == 200
    timeline = timeline_response.json()
    assert len(timeline) == 3
    assert {event["event_type"] for event in timeline} == {
        "experiment_log",
        "hardware_issue",
        "github_repository",
    }

    summary_response = client.get(f"/api/projects/{project_id}/summary")
    assert summary_response.status_code == 200
    summary = summary_response.json()
    assert summary["experiment_log_count"] == 1
    assert summary["hardware_issue_count"] == 1
    assert summary["repository_count"] == 1
    assert len(summary["open_hardware_issues"][0]["attachments"]) == 1


def test_project_status_update_and_delete(client) -> None:
    project_id = create_project(client)

    status_response = client.patch(
        f"/api/projects/{project_id}/status",
        json={"status": "integration"},
    )
    assert status_response.status_code == 200
    assert status_response.json()["status"] == "integration"

    delete_response = client.delete(f"/api/projects/{project_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/api/projects/{project_id}")
    assert get_response.status_code == 404


def test_filtering_endpoints(client) -> None:
    project_id = create_project(client)

    client.post(
        "/api/hardware-issues",
        json={
            "project_id": project_id,
            "title": "Power brownout",
            "category": "power",
            "severity": "critical",
            "symptoms": "Random reboot under TX load",
            "reproduction_conditions": "Battery under 3.7V",
            "suspected_cause": "Peak current draw",
            "attempted_fixes": "Added capacitor bank",
            "status": "open",
        },
    )
    client.post(
        "/api/hardware-issues",
        json={
            "project_id": project_id,
            "title": "Cable noise",
            "category": "mechanical_wiring",
            "severity": "low",
            "symptoms": "Intermittent sensor spike",
            "reproduction_conditions": "Motor running nearby",
            "suspected_cause": "Unshielded line",
            "attempted_fixes": "Shortened wire path",
            "status": "deferred",
        },
    )

    critical_response = client.get(f"/api/hardware-issues?project_id={project_id}&severity=critical")
    assert critical_response.status_code == 200
    payload = critical_response.json()
    assert len(payload) == 1
    assert payload[0]["title"] == "Power brownout"
