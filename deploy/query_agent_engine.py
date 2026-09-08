"""Terminal chat against an already-deployed Vertex AI Agent Engine resource.

Sanity-checks a deployment made by deploy_agent_engine.py, without spinning
up the local web/CLI stack. Requires AGENT_ENGINE_RESOURCE_NAME in .env
(printed by deploy_agent_engine.py on success).

Usage:
    python deploy/query_agent_engine.py
"""

import os
import sys

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

USER_ID = "user"


def main() -> None:
    resource_name = os.environ.get("AGENT_ENGINE_RESOURCE_NAME", "").strip()
    if not resource_name:
        print("Error: AGENT_ENGINE_RESOURCE_NAME is not set in .env.")
        print("Run deploy/deploy_agent_engine.py first and paste its output into .env.")
        sys.exit(1)

    import vertexai
    from vertexai import agent_engines

    project = os.environ.get("GOOGLE_CLOUD_PROJECT", "").strip()
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "").strip()
    if project and location:
        vertexai.init(project=project, location=location)

    print(f"Connecting to {resource_name} ...")
    remote_agent = agent_engines.get(resource_name)
    session = remote_agent.create_session(user_id=USER_ID)
    session_id = session["id"]

    print("Connected. Type 'exit' to quit.\n" + "-" * 40)

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input or user_input.lower() in {"exit", "quit"}:
            break

        print("\nAgent: ", end="", flush=True)
        try:
            reply_text = ""
            for event in remote_agent.stream_query(
                user_id=USER_ID, session_id=session_id, message=user_input
            ):
                content = event.get("content") or {}
                for part in content.get("parts", []):
                    text = part.get("text")
                    if text:
                        reply_text += text
            print(reply_text or "[No response]")
        except Exception as e:
            print(f"\nError querying agent: {e}")


if __name__ == "__main__":
    main()
