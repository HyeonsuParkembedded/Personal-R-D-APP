def create_project(client) -> int:
    response = client.post(
        "/api/projects",
        json={"name": "Issue Test Project", "description": "For hardware issue tests", "status": "design"},
    )
    assert response.status_code == 201
    return response.json()["id"]


def make_issue_payload(project_id: int, title: str = "Test Issue", severity: str = "low") -> dict:
    return {
        "project_id": project_id,
        "title": title,
        "category": "sensor",
        "severity": severity,
        "symptoms": "Test symptoms",
        "reproduction_conditions": "Always",
        "suspected_cause": "Unknown",
        "attempted_fixes": "None",
        "status": "open",
        "related_git_issue": None,
    }


def test_create_and_get_hardware_issue(client) -> None:
    project_id = create_project(client)

    create_res = client.post("/api/hardware-issues", json=make_issue_payload(project_id))
    assert create_res.status_code == 201
    issue = create_res.json()
    assert issue["title"] == "Test Issue"
    assert issue["project_id"] == project_id

    get_res = client.get(f"/api/hardware-issues/{issue['id']}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == issue["id"]


def test_list_hardware_issues_by_severity(client) -> None:
    project_id = create_project(client)

    client.post("/api/hardware-issues", json=make_issue_payload(project_id, "Critical Issue", "critical"))
    client.post("/api/hardware-issues", json=make_issue_payload(project_id, "Low Issue", "low"))

    critical_res = client.get(f"/api/hardware-issues?project_id={project_id}&severity=critical")
    assert critical_res.status_code == 200
    results = critical_res.json()
    assert all(i["severity"] == "critical" for i in results)
    assert any(i["title"] == "Critical Issue" for i in results)


def test_update_hardware_issue_status(client) -> None:
    project_id = create_project(client)
    create_res = client.post("/api/hardware-issues", json=make_issue_payload(project_id))
    issue_id = create_res.json()["id"]

    patch_res = client.patch(f"/api/hardware-issues/{issue_id}", json={"status": "fixed"})
    assert patch_res.status_code == 200
    assert patch_res.json()["status"] == "fixed"


def test_delete_hardware_issue(client) -> None:
    project_id = create_project(client)
    create_res = client.post("/api/hardware-issues", json=make_issue_payload(project_id))
    issue_id = create_res.json()["id"]

    delete_res = client.delete(f"/api/hardware-issues/{issue_id}")
    assert delete_res.status_code == 204

    get_res = client.get(f"/api/hardware-issues/{issue_id}")
    assert get_res.status_code == 404


def test_create_issue_invalid_project(client) -> None:
    res = client.post("/api/hardware-issues", json=make_issue_payload(project_id=99999))
    assert res.status_code == 404
