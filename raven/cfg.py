# raven/cfg.py

import json


LEVEL_MAP = {
    "HIGH": "error",
    "MEDIUM": "warning",
    "LOW": "note"
}


def generate_sarif(results, output_file="report.sarif"):

    sarif = {
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "RAV3N-sec",
                        "version": "0.2.0",
                    }
                },
                "results": []
            }
        ]
    }

    sarif_results = sarif["runs"][0]["results"]

    for r in results:

        sarif_results.append({
            "ruleId": r["rule_id"],

            "level": LEVEL_MAP.get(
                r["severity"],
                "warning"
            ),

            "message": {
                "text": r["message"]
            },

            "locations": [
                {
                    "physicalLocation": {
                        "artifactLocation": {
                            "uri": r["file"]
                        },
                        "region": {
                            "startLine": r["line"]
                        }
                    }
                }
            ]
        })

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(sarif, f, indent=2)