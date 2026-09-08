"""Delete a deployed Vertex AI Agent Engine resource to stop billing.

Requires AGENT_ENGINE_RESOURCE_NAME in .env. Asks for confirmation before
deleting, since this permanently removes the managed endpoint.

Usage:
    python deploy/delete_agent_engine.py
"""

import os
import sys

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def main() -> None:
    resource_name = os.environ.get("AGENT_ENGINE_RESOURCE_NAME", "").strip()
    if not resource_name:
        print("Error: AGENT_ENGINE_RESOURCE_NAME is not set in .env. Nothing to delete.")
        sys.exit(1)

    confirm = input(f"Delete {resource_name}? This cannot be undone. Type 'yes' to confirm: ").strip()
    if confirm.lower() != "yes":
        print("Aborted.")
        return

    import vertexai
    from vertexai import agent_engines

    project = os.environ.get("GOOGLE_CLOUD_PROJECT", "").strip()
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "").strip()
    if project and location:
        vertexai.init(project=project, location=location)

    print(f"Deleting {resource_name} ...")
    agent_engines.get(resource_name).delete(force=True)
    print("Deleted. Remove AGENT_ENGINE_RESOURCE_NAME from .env.")


if __name__ == "__main__":
    main()
