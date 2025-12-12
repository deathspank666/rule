import json
import os

JSON_DIR = "json"
RAW_DIR = "raw"

def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def write_txt(filepath, lines):
    with open(filepath, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")

def extract_domains(rule_data):
    domains = []

    if "domain" in rule_data and isinstance(rule_data["domain"], list):
        domains.extend(rule_data["domain"])

    if "domain_suffix" in rule_data and isinstance(rule_data["domain_suffix"], list):
        domains.extend(rule_data["domain_suffix"])

    return domains

def main():
    for filename in os.listdir(JSON_DIR):
        if not filename.endswith(".json"):
            continue

        json_path = os.path.join(JSON_DIR, filename)
        rule_name = filename[:-5]
        txt_path = os.path.join(RAW_DIR, f"{rule_name}.txt")

        data = load_json(json_path)

        domains = extract_domains(data)

        domains = sorted(set(domains))

        write_txt(txt_path, domains)
        print(f"✔ Generated: {txt_path}")

if __name__ == "__main__":
    main()
