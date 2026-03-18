from datetime import UTC, datetime


def create_project(client) -> int:
    response = client.post(
        "/api/projects",
        json={"name": "Log Test Project", "description": "For experiment log tests", "status": "design"},
    )
    assert response.status_code == 201
    return response.json()["id"]


def make_log_payload(project_id: int, title: str = "Test Log") -> dict:
    return {
        "project_id": project_id,
        "title": title,
        "recorded_at": datetime.now(UTC).isoformat(),
        "objective": "Test objective",
        "board_firmware_version": "v1.0.0",
        "conditions": "Lab bench",
        "result": "Pass",
        "issues": "",
        "next_action": "",
        "related_git_reference": None,
    }


def test_create_and_get_experiment_log(client) -> None:
    project_id = create_project(client)

    create_res = client.post("/api/experiment-logs", json=make_log_payload(project_id))
    assert create_res.status_code == 201
    log = create_res.json()
    assert log["title"] == "Test Log"
    assert log["project_id"] == project_id

    get_res = client.get(f"/api/experiment-logs/{log['id']}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == log["id"]


def test_list_experiment_logs_by_project(client) -> None:
    project_id = create_project(client)

    client.post("/api/experiment-logs", json=make_log_payload(project_id, "Log A"))
    client.post("/api/experiment-logs", json=make_log_payload(project_id, "Log B"))

    list_res = client.get(f"/api/experiment-logs?project_id={project_id}")
    assert list_res.status_code == 200
    titles = {log["title"] for log in list_res.json()}
    assert {"Log A", "Log B"}.issubset(titles)


def test_update_experiment_log(client) -> None:
    project_id = create_project(client)
    create_res = client.post("/api/experiment-logs", json=make_log_payload(project_id))
    log_id = create_res.json()["id"]

    patch_res = client.patch(f"/api/experiment-logs/{log_id}", json={"result": "Updated result"})
    assert patch_res.status_code == 200
    assert patch_res.json()["result"] == "Updated result"


def test_delete_experiment_log(client) -> None:
    project_id = create_project(client)
    create_res = client.post("/api/experiment-logs", json=make_log_payload(project_id))
    log_id = create_res.json()["id"]

    delete_res = client.delete(f"/api/experiment-logs/{log_id}")
    assert delete_res.status_code == 204

    get_res = client.get(f"/api/experiment-logs/{log_id}")
    assert get_res.status_code == 404


def test_create_log_invalid_project(client) -> None:
    res = client.post("/api/experiment-logs", json=make_log_payload(project_id=99999))
    assert res.status_code == 404
