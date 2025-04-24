import os
import requests

# Fetch GitHub-provided environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_OWNER = os.getenv("GITHUB_REPOSITORY_OWNER")  # Automatically set to the repository owner
REPO_NAME = os.getenv("GITHUB_REPOSITORY").split("/")[1]  # Automatically set to the repository name
OUTPUT_DIR = r"C:\Users\captk\youtube-ai-agent\downloaded_artifacts"  # Directory to save artifacts

def ensure_output_directory():
    """
    Ensure the output directory exists.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"[INFO] Output directory ensured: {OUTPUT_DIR}")

def download_artifacts():
    """
    Fetch and download the latest artifacts.
    """
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    workflow_runs_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/runs"

    # Fetch the latest workflow runs
    print("[INFO] Fetching workflow runs...")
    response = requests.get(workflow_runs_url, headers=headers)

    if response.status_code != 200:
        print(f"[ERROR] Failed to fetch workflow runs: {response.status_code} {response.text}")
        return

    runs = response.json().get("workflow_runs", [])
    if not runs:
        print("[WARNING] No workflow runs found.")
        return

    # Get the latest workflow run
    latest_run = runs[0]
    run_id = latest_run["id"]
    artifacts_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/runs/{run_id}/artifacts"

    # Fetch artifacts for the latest workflow run
    print(f"[INFO] Fetching artifacts for workflow run ID: {run_id}...")
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

        print(f"[INFO] Downloading artifact: {artifact_name}...")
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
    Main function to download artifacts.
    """
    ensure_output_directory()
    download_artifacts()

if __name__ == "__main__":
    main()
