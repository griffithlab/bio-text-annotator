from pathlib import Path
import json


def write_report(report: dict, output_path: str):
    """
    Write aggregated report to disk as JSON.

    Args:
        report: Aggregated report dictionary.
        output_path: Output JSON file path.
    """

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(
            report,
            f,
            indent=2,
            ensure_ascii=False
        )