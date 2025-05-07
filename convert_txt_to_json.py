# convert_txt_to_json.py

import json
from pathlib import Path

FILENAME = "unavailable-in-russia"
EXCLUDED_DOMAINS = {
    "tiktok.com", "tiktokv.com", "ttwstatic.com", "docker.io",
    "google.com", "googleapis.com", "github.com", "githubcopilot.com",
    "githubusercontent.com", "netflix.com", "fast.com", "chatgpt.com",
    "openai.com", "oaistatic.com", "oaiusercontent.com", "epicgames.com",
    "microsoft.com", "x.ai"
}

RAW_PATH = Path(f"raw/{FILENAME}.txt")
JSON_PATH = Path(f"json/{FILENAME}.json")

def load_raw_domains() -> set[str]:
    with RAW_PATH.open(encoding="utf-8") as f:
        return {
            line.strip() for line in f
            if line.strip() and not line.startswith("#") and line.strip() not in EXCLUDED_DOMAINS
        }

def load_existing_json() -> dict:
    if JSON_PATH.exists():
        with JSON_PATH.open(encoding="utf-8") as f:
            return json.load(f)
    return {
        "version": 3,
        "name": FILENAME,
        "description": "Domains unavailable from Russia",
        "rules": [{"domain": [], "domain_suffix": []}]
    }

def split_domains(domains: set[str]) -> tuple[list[str], list[str]]:
    direct, suffix = [], []
    for d in sorted(domains):
        (direct if d.count(".") == 1 else suffix).append(d)
    return direct, suffix

def save_json(data: dict):
    with JSON_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    new_domains = load_raw_domains()
    direct, suffix = split_domains(new_domains)

    existing = load_existing_json()
    current_direct = set(existing["rules"][0].get("domain", []))
    current_suffix = set(existing["rules"][0].get("domain_suffix", []))

    if set(direct) == current_direct and set(suffix) == current_suffix:
        print("No changes detected. Skipping update.")
        return

    existing["rules"][0]["domain"] = direct
    existing["rules"][0]["domain_suffix"] = suffix
    save_json(existing)
    print(f"Updated {JSON_PATH} with {len(direct)} domains and {len(suffix)} suffixes.")

if __name__ == "__main__":
    main()
