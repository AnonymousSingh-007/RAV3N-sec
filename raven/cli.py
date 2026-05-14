# raven/cli.py

import typer
from rich import print

from raven.scanner import scan_path

app = typer.Typer()


SEVERITY_COLORS = {
    "LOW": "green",
    "MEDIUM": "yellow",
    "HIGH": "red",
    "CRITICAL": "bold red"
}


@app.command()
def scan(path: str):

    print(f"\n[bold cyan]RAV3N-sec scanning:[/bold cyan] {path}\n")

    results = scan_path(path)

    total = 0

    if not results:
        print("[green]No vulnerabilities found.[/green]")
        return

    for file, findings in results.items():

        print(f"\n[bold white]FILE:[/bold white] {file}")

        for finding in findings:

            total += 1

            severity = finding["severity"]

            color = SEVERITY_COLORS.get(
                severity,
                "white"
            )

            print(
                f"""
[{color}]Line {finding['line']}[/]
[{color}]Severity:[/] {severity}
[{color}]Type:[/] {finding['type']}
[{color}]Confidence:[/] {finding['confidence']}
[{color}]Issue:[/] {finding['message']}
[{color}]Fix:[/] {finding['fix']}
"""
            )

    print(
        f"\n[bold red]Total Findings:[/] {total}\n"
    )


if __name__ == "__main__":
    app()