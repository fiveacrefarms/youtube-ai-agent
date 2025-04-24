import os
import requests

# Configuration
GITHUB_TOKEN = "YOUR_PERSONAL_ACCESS_TOKEN"  # Replace with your GitHub Personal Access Token
REPO_OWNER = "fiveacrefarms"  # Replace with the owner of the repository
REPO_NAME = "youtube-ai-agent"  # Replace with the repository name
OUTPUT_DIR = r"C:\Users\captk\youtube-ai-agent\downloaded_artifacts"  # Directory where artifacts will be saved

# GitHub API URLs
BASE_URL = "https://api.github.com"
WORKFLOW_RUNS_URL = f"{BASE_URL}/repos/{REPO_OWNER}/{REPO_NAME}/actions/runs"

def ensure_output_directory():
    """
    Ensure the output directory exists.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"[INFO] Output directory ensured: {OUTPUT_DIR}")

def get_latest_workflow_run():
    """
    Get the latest workflow run from the GitHub repository.
    Returns:
        dict: A dictionary containing the workflow run details, or None if not found.
    """
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    response = requests.get(WORKFLOW_RUNS_URL, headers=headers)

    if response.status_code != 200:
        print(f"[ERROR] Failed to fetch workflow runs: {response.status_code} {response.text}")
        return None

    runs = response.json().get("workflow_runs", [])
    if not runs:
        print("[WARNING] No workflow runs found.")
        return None

    # Return the latest workflow run
    return runs[0]

def download_artifacts(run_id):
    """
    Download artifacts from the specified workflow run.
    Args:
        run_id (int): The workflow run ID.
    """
    artifacts_url = f"{WORKFLOW_RUNS_URL}/{run_id}/artifacts"
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    response = requests.get(artifacts_url, headers=headers)

    if response.status_code != 200:
        print(f"[ERROR] Failed to fetch artifacts: {response.status_code} {response.text}")
        return

    artifacts = response.json().get("artifacts", [])
    if not artifacts:
        print("[WARNING] No artifacts found for the workflow run.")
        return

    for artifact in artifacts:
        artifact_name = artifact["name"]
        download_url = artifact["archive_download_url"]

        print(f"[INFO] Downloading artifact: {artifact_name}")
        artifact_response = requests.get(download_url, headers=headers, stream=True)

        if artifact_response.status_code != 200:
            print(f"[ERROR] Failed to download artifact {artifact_name}: {artifact_response.status_code}")
            continue

        output_path = os.path.join(OUTPUT_DIR, f"{artifact_name}.zip")
        with open(output_path, "wb") as file:
            for chunk in artifact_response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"[INFO] Artifact downloaded: {output_path}")

def main():
    """
    Main function to download artifacts from the latest workflow run.
    """
    ensure_output_directory()
    latest_run = get_latest_workflow_run()

    if latest_run:
        run_id = latest_run["id"]
        print(f"[INFO] Latest workflow run ID: {run_id}")
        download_artifacts(run_id)
    else:
        print("[ERROR] No workflow run found.")

if __name__ == "__main__":
    main()
