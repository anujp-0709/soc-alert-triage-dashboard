def get_mitre_mapping(rule_name: str):
    """
    Returns MITRE mapping for a given rule name.
    Beginner version: a simple dictionary.
    """
    mapping = {
        "Brute Force Login Attempts": {
            "tactic": "Credential Access",
            "technique_id": "T1110",
            "technique_name": "Brute Force",
        }
    }

    return mapping.get(rule_name, {"tactic": "", "technique_id": "", "technique_name": ""})
