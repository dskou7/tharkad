#!/usr/bin/env python3
"""
This script fetches the list of models from tharkad's models endpoint and updates the opencode configuration file with the latest model information. 
It creates a backup of the original config before making changes.

machine generated. might suck.
"""

import json
import sys
import urllib.request
import urllib.error
from pathlib import Path


def fetch_models(url: str) -> list[dict]:
    """Fetch models from tharkad API."""
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.load(resp)
            return data.get("data", [])
    except urllib.error.URLError as e:
        print(f"Error: Failed to reach tharkad at {url}", file=sys.stderr)
        print(f"  {e}", file=sys.stderr)
        sys.exit(1)


def sync_models(tharkad_url: str, config_path: Path) -> None:
    """Sync tharkad models to opencode config."""
    models = fetch_models(tharkad_url)

    with open(config_path) as f:
        config = json.load(f)

    models_section = {}
    for m in models:
        model_id = m["id"]
        name = m["aliases"][0] if m.get("aliases") else model_id
        models_section[model_id] = {
            "name": name,
            "options": {"structuredOutputs": True},
        }

    config["provider"]["llama.cpp"]["models"] = models_section

    backup_path = config_path.parent / f"{config_path.name}.bak"
    with open(backup_path, "w") as f:
        json.dump(config, f, indent=2)

    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    print(f"Updated {len(models_section)} models:")
    for model_id, info in models_section.items():
        print(f"  {model_id} → {info['name']}")


def main():
    tharkad_url = "http://192.168.1.12:8080/v1/models"
    config_path = Path.home() / ".config" / "opencode" / "opencode.json"

    sync_models(tharkad_url, config_path)


if __name__ == "__main__":
    main()
