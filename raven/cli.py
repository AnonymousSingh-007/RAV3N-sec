import typer
import os
from rich.console import Console
from rich.tree import Tree
from collections import Counter

from raven.scanner import scan_path
from raven.report import generate_html
from raven.ml_model import predict

app = typer.Typer()
console = Console()

SEVERITY_ORDER = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}


@app.command(help="""
Scan files or directories for vulnerabilities.

Examples:

  python -m raven.cli scan app.py
  python -m raven.cli scan ./project --min-severity MEDIUM
  python -m raven.cli scan . --html --output report.html
  python -m raven.cli scan . --show-all
  python -m raven.cli scan . --use-ml
""")
def scan(
    path: str,
    html: bool = False,
    output: str = "report.html",
    min_severity: str = "LOW",
    show_all: bool = False,
    use_ml: bool = True,
    min_confidence: float = 0.75
):
    """Scan a file or directory for vulnerabilities"""

    results_map = scan_path(path)
    all_results = []

    # 📂 Flatten rule results
    for file, findings in results_map.items():
        for r in findings:
            r["file"] = os.path.relpath(file)
            all_results.append(r)

    # 🤖 ML scanning (CONTROLLED)
    if use_ml:
        for file in results_map:
            try:
                with open(file, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                ml_hits = 0
                MAX_ML_HITS = 20  # 🔥 prevents explosion

                for i, line in enumerate(lines, start=1):
                    if ml_hits >= MAX_ML_HITS:
                        break

                    pred, prob = predict(line)

                    # 🔥 Avoid duplicate detection on same line
                    already_flagged = any(
                        r["file"] == os.path.relpath(file) and r["line"] == i
                        for r in all_results
                    )

                    if pred == 1 and prob > min_confidence and not already_flagged:
                        ml_hits += 1

                        all_results.append({
                            "file": os.path.relpath(file),
                            "line": i,
                            "severity": "MEDIUM",
                            "message": "ML detected anomaly",
                            "type": "ml",
                            "confidence": prob,
                            "noisy": True,  # 🔥 mark as noisy
                            "fix": "Review this code for unsafe patterns"
                        })

            except Exception:
                continue

    # 🔥 Filtering
    min_level = SEVERITY_ORDER[min_severity.upper()]

    filtered = []
    for r in all_results:
        if SEVERITY_ORDER[r["severity"]] < min_level:
            continue

        if r.get("noisy") and not show_all:
            continue

        if r["type"] == "ml" and r.get("confidence", 0) < min_confidence:
            continue

        filtered.append(r)

    if not filtered:
        console.print("\n[bold green]✅ No issues found[/bold green]\n")
        return

    # 🔥 Sort results
    filtered = sorted(
        filtered,
        key=lambda x: (x["file"], -SEVERITY_ORDER[x["severity"]])
    )

    counts = Counter(r["severity"] for r in filtered)

    console.print("\n[bold red]⚠ Security Scan Results[/bold red]\n")
    console.print(
        f"[red]HIGH:[/red] {counts.get('HIGH',0)}   "
        f"[yellow]MEDIUM:[/yellow] {counts.get('MEDIUM',0)}   "
        f"[green]LOW:[/green] {counts.get('LOW',0)}\n"
    )

    # 🌳 TREE OUTPUT
    tree = Tree("[bold red]📊 Scan Results[/bold red]")

    current_file = None
    file_node = None

    for r in filtered:
        if r["file"] != current_file:
            file_node = tree.add(f"[bold cyan]📂 {r['file']}[/bold cyan]")
            current_file = r["file"]

        color = {
            "HIGH": "red",
            "MEDIUM": "yellow",
            "LOW": "green"
        }[r["severity"]]

        confidence_text = ""
        if "confidence" in r:
            confidence_text = f" [dim](conf: {r['confidence']:.2f})[/dim]"

        file_node.add(
            f"[{color}]{r['severity']}[/{color}] "
            f"(line {r['line']}) [{r['type']}] → {r['message']}"
            f"{confidence_text}\n"
            f"[dim]Fix: {r.get('fix','')}[/dim]"
        )

    console.print(tree)

    # 📄 HTML
    if html:
        generate_html(filtered, output)
        console.print(f"\n[cyan]📄 HTML report generated: {output}[/cyan]")


if __name__ == "__main__":
    app()