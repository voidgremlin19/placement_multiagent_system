"""Deploy the placement_coordinator agent graph to Vertex AI Agent Engine.

Creates a real, billed GCP resource (a reasoningEngine). Run this only
after filling in GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION, and
GOOGLE_CLOUD_STAGING_BUCKET in .env (see .env.example) and completing the
one-time setup in the README's "Deploy to GCP" section (billing enabled,
`gcloud auth application-default login`, aiplatform API enabled, staging
bucket created).

Usage:
    python deploy/deploy_agent_engine.py
"""

import os
import sys

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

REQUIRED_VARS = ("GOOGLE_CLOUD_PROJECT", "GOOGLE_CLOUD_LOCATION", "GOOGLE_CLOUD_STAGING_BUCKET")


def _require_env() -> dict:
    values = {name: os.environ.get(name, "").strip() for name in REQUIRED_VARS}
    missing = [name for name, value in values.items() if not value]
    if missing:
        print(f"Error: missing required .env vars: {', '.join(missing)}")
        print("See .env.example and the README's 'Deploy to GCP' section.")
        sys.exit(1)
    return values


def main() -> None:
    env = _require_env()

    import vertexai
    from vertexai import agent_engines
    from vertexai.preview.reasoning_engines import AdkApp

    from placement_agent.coordinator import root_agent

    vertexai.init(
        project=env["GOOGLE_CLOUD_PROJECT"],
        location=env["GOOGLE_CLOUD_LOCATION"],
        staging_bucket=f"gs://{env['GOOGLE_CLOUD_STAGING_BUCKET']}",
    )

    app = AdkApp(agent=root_agent, enable_tracing=True)

    print("Deploying placement_coordinator to Vertex AI Agent Engine...")
    print("(This uploads a package and provisions a managed endpoint — usually a few minutes.)")

    remote_agent = agent_engines.create(
        agent_engine=app,
        requirements=["google-adk==2.8.0", "google-genai==2.22.0"],
        extra_packages=["placement_agent"],
        display_name="placement-agent",
        env_vars={
            "GOOGLE_GENAI_USE_VERTEXAI": "TRUE",
            "GOOGLE_CLOUD_PROJECT": env["GOOGLE_CLOUD_PROJECT"],
            "GOOGLE_CLOUD_LOCATION": env["GOOGLE_CLOUD_LOCATION"],
        },
    )

    print("\nDeployed successfully.")
    print(f"Resource name: {remote_agent.resource_name}")
    print("\nAdd this to your .env to use query_agent_engine.py / delete_agent_engine.py:")
    print(f'AGENT_ENGINE_RESOURCE_NAME="{remote_agent.resource_name}"')


if __name__ == "__main__":
    main()
