import typer
from rich.console import Console
from rich.table import Table
from rich import box
from collections import Counter

from raven.scanner import scan_file
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
    """Scan a file for vulnerabilities"""

    results = scan_file(path)

    # 🤖 ML hook
    if use_ml:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for i, line in enumerate(lines, start=1):
            pred, prob = predict(line)

            if pred == 1 and prob > 0.75:
                results.append({
                    "line": i,
                    "severity": "MEDIUM",
                    "message": f"ML suspicious pattern ({prob:.2f})",
                    "type": "ml",
                    "confidence": prob,
                    "noisy": False,
                    "fix": "Review this code for unsafe patterns"
                })

    # 🔥 Filter system
    min_level = SEVERITY_ORDER[min_severity.upper()]

    filtered = []
    for r in results:
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

    # sort
    filtered = sorted(
        filtered,
        key=lambda x: SEVERITY_ORDER[x["severity"]],
        reverse=True
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

    for r in filtered:
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

    if html:
        generate_html(filtered, output)
        console.print(f"\n[cyan]📄 HTML report generated: {output}[/cyan]")


if __name__ == "__main__":
    app()