import typer
from rich.console import Console
from rich.table import Table
from rich import box
from collections import Counter

from raven.scanner import scan_file
from raven.report import generate_html

# 🔥 ML Hook
from raven.ml_model import predict

app = typer.Typer()
console = Console()


SEVERITY_ORDER = {
    "HIGH": 3,
    "MEDIUM": 2,
    "LOW": 1
}


@app.command()
def scan(
    path: str,
    html: bool = False,
    output: str = "report.html",
    use_ml: bool = True
):
    """Scan a file for vulnerabilities"""

    results = scan_file(path)

    # =========================
    # 🤖 ML Hook (line-by-line)
    # =========================
    if use_ml:
        try:
            with open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            for i, line in enumerate(lines, start=1):
                pred, prob = predict(line)

                if pred == 1 and prob > 0.7:
                    results.append({
                        "line": i,
                        "severity": "MEDIUM",
                        "message": f"ML detected possible vulnerability ({prob:.2f})",
                        "type": "ml"
                    })
        except Exception as e:
            console.print(f"[yellow]ML skipped: {e}[/yellow]")

    if not results:
        console.print("\n[bold green]✅ No issues found[/bold green]\n")
        return

    # 🔥 Sort by severity
    results = sorted(
        results,
        key=lambda x: SEVERITY_ORDER.get(x["severity"], 0),
        reverse=True
    )

    # 📊 Summary
    counts = Counter(r["severity"] for r in results)

    console.print("\n[bold red]⚠ Security Scan Results[/bold red]\n")
    console.print(
        f"[red]HIGH:[/red] {counts.get('HIGH',0)}   "
        f"[yellow]MEDIUM:[/yellow] {counts.get('MEDIUM',0)}   "
        f"[green]LOW:[/green] {counts.get('LOW',0)}\n"
    )

    # 📋 Table Output
    table = Table(box=box.ROUNDED)

    table.add_column("Severity", justify="center")
    table.add_column("Line", justify="center")
    table.add_column("Type", justify="center")
    table.add_column("Message")

    for r in results:
        color = {
            "HIGH": "red",
            "MEDIUM": "yellow",
            "LOW": "green"
        }.get(r["severity"], "white")

        table.add_row(
            f"[{color}]{r['severity']}[/{color}]",
            str(r["line"]),
            r["type"],
            r["message"]
        )

    console.print(table)

    # =========================
    # 📄 HTML Report Hook
    # =========================
    if html:
        generate_html(results, output)
        console.print(f"\n[cyan]📄 HTML report generated: {output}[/cyan]")


if __name__ == "__main__":
    app()