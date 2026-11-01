#!/usr/bin/env python3
"""Create a real GitHub repository/project and advance planning in evidence stages.

Requires gh auth login and gh auth refresh -s project. Never fabricates screenshots.
The init command creates a new public repository from the IBM template.
"""
import argparse
from datetime import date, timedelta
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / ".board-state.json"
STORIES = {s["key"]: s for s in json.loads((ROOT / "docs/stories.json").read_text())}
COLUMNS = [
    "New issues",
    "Icebox",
    "Product backlog",
    "Sprint backlog",
    "In progress",
    "Review/QA",
    "Done",
    "Closed",
]


def gh(*args, payload=None):
    command = ["gh", *args]
    if payload is not None:
        command += ["--input", "-"]
    result = subprocess.run(
        command,
        input=json.dumps(payload) if payload is not None else None,
        text=True,
        capture_output=True,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return result.stdout.strip()


def api(path, method="GET", payload=None):
    result = gh("api", "--method", method, path, payload=payload)
    return json.loads(result) if result else None


def gql(query, variables=None):
    result = json.loads(
        gh("api", "graphql", payload={"query": query, "variables": variables or {}})
    )
    if result.get("errors"):
        raise RuntimeError(str(result["errors"]))
    return result["data"]


def mutation(name, input_type, value, selection):
    query = f"mutation($input:{input_type}!) {{ {name}(input:$input) {{ {selection} }} }}"
    return gql(query, {"input": value})[name]


def save(state):
    STATE.write_text(json.dumps(state, indent=2) + "\n")


def add_story(state, key):
    if key in state["issues"]:
        return
    story = STORIES[key]
    matches = api(f"repos/{state['repo']}/issues?state=all&per_page=100")
    issue = next((i for i in matches if i["title"] == story["title"]), None)
    if issue is None:
        issue = api(
            f"repos/{state['repo']}/issues",
            "POST",
            {"title": story["title"], "body": (ROOT / story["body_file"]).read_text()},
        )
    item = mutation(
        "addProjectV2ItemById",
        "AddProjectV2ItemByIdInput",
        {"projectId": state["project"], "contentId": issue["node_id"]},
        "item { id }",
    )["item"]
    state["issues"][key] = {"number": issue["number"], "item": item["id"], "url": issue["html_url"]}
    save(state)
    set_status(state, key, "New issues")


def field_value(state, key, field, value):
    mutation(
        "updateProjectV2ItemFieldValue",
        "UpdateProjectV2ItemFieldValueInput",
        {
            "projectId": state["project"],
            "itemId": state["issues"][key]["item"],
            "fieldId": field,
            "value": value,
        },
        "projectV2Item { id }",
    )


def set_status(state, key, status):
    field_value(
        state, key, state["status_field"], {"singleSelectOptionId": state["statuses"][status]}
    )
    state["issues"][key]["status"] = status
    save(state)


def refine(state, key):
    story = STORIES[key]
    gh(
        "issue",
        "edit",
        str(state["issues"][key]["number"]),
        "--repo",
        state["repo"],
        "--add-label",
        story["label"],
    )
    field_value(state, key, state["points_field"], {"number": story["points"]})


def sprint(state, number, keys):
    previous = None
    for key in keys:
        add_story(state, key)
        refine(state, key)
        gh(
            "issue",
            "edit",
            str(state["issues"][key]["number"]),
            "--repo",
            state["repo"],
            "--milestone",
            f"Sprint {number}",
        )
        field_value(
            state, key, state["sprint_field"], {"iterationId": state["sprints"][f"Sprint {number}"]}
        )
        set_status(state, key, "Sprint backlog")
        move = {"projectId": state["project"], "itemId": state["issues"][key]["item"]}
        if previous:
            move["afterId"] = previous
        mutation(
            "updateProjectV2ItemPosition",
            "UpdateProjectV2ItemPositionInput",
            move,
            "items { totalCount }",
        )
        previous = state["issues"][key]["item"]


def initialize(start):
    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    if state.get("initialization_complete"):
        raise RuntimeError(
            "State already exists. Continue with triage/refine/sprint commands; do not create duplicates."
        )
    viewer = gql("query { viewer { id login } }")["viewer"]
    repo = viewer["login"] + "/devops-capstone-project"
    if state and state.get("repo") != repo:
        raise RuntimeError("Saved repository does not belong to the active GitHub account")
    # Verify Projects access before creating any resources.
    gql("query { viewer { projectsV2(first:1) { totalCount } } }")
    # Refuse to silently overwrite or adopt an existing repository.
    check = subprocess.run(["gh", "repo", "view", repo], capture_output=True)
    if check.returncode == 0 and not state:
        raise RuntimeError(
            f"{repo} already exists. No changes made; request an explicit adoption workflow."
        )
    if check.returncode != 0:
        gh(
            "repo", "create", repo, "--public", "--template",
            "ibm-developer-skills-network/aolwx-devops-capstone-template",
            "--description", "Customer Accounts REST microservice — IBM DevOps Capstone",
        )
    state.setdefault("repo", repo)
    state.setdefault("issues", {})
    save(state)
    if "project" not in state:
        project = mutation(
            "createProjectV2", "CreateProjectV2Input",
            {"ownerId": viewer["id"], "title": "Customer Accounts Capstone"},
            "projectV2 { id number url }",
        )["projectV2"]
        state.update(project=project["id"], project_number=project["number"], project_url=project["url"])
        save(state)
    repository = api(f"repos/{repo}")
    mutation(
        "linkProjectV2ToRepository",
        "LinkProjectV2ToRepositoryInput",
        {"projectId": project["id"], "repositoryId": repository["node_id"]},
        "repository { id }",
    )
    fields = gql(
        "query($id:ID!){node(id:$id){... on ProjectV2{fields(first:50){nodes{"
        "... on ProjectV2Field{id name} ... on ProjectV2SingleSelectField{id name options{id name}}"
        "... on ProjectV2IterationField{id name configuration{iterations{id title} completedIterations{id title}}}"
        "}}}}}",
        {"id": project["id"]},
    )["node"]["fields"]["nodes"]
    status = next(f for f in fields if f.get("name") == "Status")
    state["status_field"] = status["id"]
    options = [
        {"name": n, "color": c, "description": n}
        for n, c in zip(
            COLUMNS, ["GRAY", "GRAY", "BLUE", "PURPLE", "YELLOW", "ORANGE", "GREEN", "GREEN"]
        )
    ]
    updated = mutation(
        "updateProjectV2Field",
        "UpdateProjectV2FieldInput",
        {"fieldId": status["id"], "singleSelectOptions": options},
        "projectV2Field { ... on ProjectV2SingleSelectField { options { id name } } }",
    )
    state["statuses"] = {o["name"]: o["id"] for o in updated["projectV2Field"]["options"]}
    save(state)
    points = next((f for f in fields if f.get("name") == "Story Points"), None)
    pts = {"projectV2Field": points} if points else mutation(
        "createProjectV2Field",
        "CreateProjectV2FieldInput",
        {"projectId": project["id"], "name": "Story Points", "dataType": "NUMBER"},
        "projectV2Field { ... on ProjectV2Field { id } }",
    )
    state["points_field"] = pts["projectV2Field"]["id"]
    save(state)
    iterations = [
        {
            "title": f"Sprint {i+1}",
            "startDate": (start + timedelta(days=7 * i)).isoformat(),
            "duration": 7,
        }
        for i in range(3)
    ]
    existing_sprint = next((f for f in fields if f.get("name") == "Sprint"), None)
    sf = existing_sprint or mutation(
        "createProjectV2Field",
        "CreateProjectV2FieldInput",
        {
            "projectId": project["id"],
            "name": "Sprint",
            "dataType": "ITERATION",
            "iterationConfiguration": {
                "duration": 7,
                "startDate": start.isoformat(),
                "iterations": iterations,
            },
        },
        "projectV2Field { ... on ProjectV2IterationField { id configuration { "
        "iterations { id title } completedIterations { id title } } } }",
    )["projectV2Field"]
    state["sprint_field"] = sf["id"]
    state["sprints"] = {
        i["title"]: i["id"]
        for i in sf["configuration"]["iterations"] + sf["configuration"]["completedIterations"]
    }
    save(state)
    for label, color in [("technical debt", "FBCA04"), ("enhancement", "A2EEEF")]:
        gh("label", "create", label, "--repo", repo, "--color", color, "--force")
    milestones = api(f"repos/{repo}/milestones?state=all&per_page=100")
    for i in range(3):
        if any(m["title"] == f"Sprint {i+1}" for m in milestones):
            continue
        api(
            f"repos/{repo}/milestones",
            "POST",
            {
                "title": f"Sprint {i+1}",
                "description": f"One week: {iterations[i]['startDate']} through "
                f"{(start + timedelta(days=7*i+6)).isoformat()}",
                "due_on": (start + timedelta(days=7 * i + 6)).isoformat() + "T23:59:59Z",
            },
        )
    for key in ["setup", "read", "update", "delete", "list", "docker", "kubernetes"]:
        add_story(state, key)
    state["initialization_complete"] = True
    save(state)
    print("Repository:", "https://github.com/" + repo)
    print("Project:", state["project_url"])
    print(
        "In GitHub Projects select Board layout, group by Status, show Labels, Sprint and Story Points."
    )
    print("Save the view. Capture Planning-userstories-done.png with all seven New issues visible.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "action",
        choices=["init", "triage", "refine", "sprint1", "sprint2", "sprint3", "status", "close"],
    )
    parser.add_argument("key", nargs="?", choices=STORIES)
    parser.add_argument("status", nargs="?", choices=COLUMNS)
    parser.add_argument(
        "--start", default=date.today().isoformat(), help="Sprint 1 start YYYY-MM-DD"
    )
    args = parser.parse_args()
    if args.action == "init":
        initialize(date.fromisoformat(args.start))
        return
    state = json.loads(STATE.read_text())
    if args.action == "triage":
        for key in ["setup", "read", "list", "update", "delete"]:
            set_status(state, key, "Product backlog")
        for key in ["docker", "kubernetes"]:
            set_status(state, key, "Icebox")
        print(
            "Capture planning-productbacklog-done.png showing the five backlog and two Icebox stories."
        )
    elif args.action == "refine":
        for key in list(state["issues"]):
            refine(state, key)
        print("Capture planning-labels-done.png with labels visible.")
    elif args.action.startswith("sprint"):
        number = int(args.action[-1])
        keys = {
            1: ["setup", "read", "list", "update", "delete"],
            2: ["ci", "security"],
            3: ["docker", "kubernetes", "cd"],
        }[number]
        sprint(state, number, keys)
        name = "planning-kanban-done" if number == 1 else f"sprint{number}-plan"
        print(f"Filter Sprint = Sprint {number}, preserve ranked order, and capture {name}.png.")
    elif args.action == "status":
        if not args.key or not args.status:
            parser.error("status requires KEY and STATUS; quote multiword statuses")
        set_status(state, args.key, args.status)
        print("Updated:", state["issues"][args.key]["url"], args.status)
    elif args.action == "close":
        if not args.key:
            parser.error("close requires KEY; capture the Done screenshot before closing")
        gh("issue", "close", str(state["issues"][args.key]["number"]), "--repo", state["repo"])
        set_status(state, args.key, "Closed")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, FileNotFoundError) as error:
        sys.exit(str(error))
