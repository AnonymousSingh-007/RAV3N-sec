import typer
import os
from rich.console import Console
from rich.table import Table
from rich import box
from collections import Counter

from raven.scanner import scan_path
from raven.report import generate_html
from raven.ml_model import predict

app = typer.Typer()
console = Console()

SEVERITY_ORDER = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}


@app.command()
def scan(
    path: str,
    html: bool = False,
    output: str = "report.html",
    min_severity: str = "LOW",
    show_all: bool = False,
    use_ml: bool = True
):
    """Scan a file or directory for vulnerabilities"""

    results_map = scan_path(path)

    all_results = []

    # 📂 Flatten results
    for file, findings in results_map.items():
        for r in findings:
            r["file"] = os.path.relpath(file)
            all_results.append(r)

    # 🤖 ML scanning per file
    if use_ml:
        for file in results_map:
            try:
                with open(file, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                for i, line in enumerate(lines, start=1):
                    pred, prob = predict(line)

                    if pred == 1 and prob > 0.75:
                        all_results.append({
                            "file": os.path.relpath(file),
                            "line": i,
                            "severity": "MEDIUM",
                            "message": f"ML suspicious pattern ({prob:.2f})",
                            "type": "ml",
                            "confidence": prob,
                            "noisy": False,
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

        if r["type"] == "ml" and r["confidence"] < 0.75:
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

    table = Table(box=box.ROUNDED)
    table.add_column("Severity")
    table.add_column("Line")
    table.add_column("Type")
    table.add_column("Message")
    table.add_column("Fix")

    current_file = None

    for r in filtered:
        if r["file"] != current_file:
            console.print(f"\n[bold cyan]📂 {r['file']}[/bold cyan]")
            current_file = r["file"]

        color = {
            "HIGH": "red",
            "MEDIUM": "yellow",
            "LOW": "green"
        }[r["severity"]]

        table.add_row(
            f"[{color}]{r['severity']}[/{color}]",
            str(r["line"]),
            r["type"],
            r["message"],
            r.get("fix", "")
        )

    console.print(table)

    # 📄 HTML Report
    if html:
        generate_html(filtered, output)
        console.print(f"\n[cyan]📄 HTML report generated: {output}[/cyan]")


if __name__ == "__main__":
    app()