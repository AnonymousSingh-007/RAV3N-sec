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


def generate_html(results):

    html = """
    <html>
    <head>
        <title>RAV3N-sec Report</title>
        <style>
            body {
                font-family: Arial;
                background: #111;
                color: #eee;
                padding: 20px;
            }

            .finding {
                border: 1px solid #444;
                margin-bottom: 15px;
                padding: 15px;
                border-radius: 8px;
            }

            .HIGH { border-left: 6px solid red; }
            .CRITICAL { border-left: 6px solid darkred; }
            .MEDIUM { border-left: 6px solid orange; }
            .LOW { border-left: 6px solid green; }

        </style>
    </head>
    <body>

    <h1>RAV3N-sec Scan Report</h1>
    """

    for file, findings in results.items():

        html += f"<h2>{file}</h2>"

        for finding in findings:

            html += f"""
            <div class='finding {finding["severity"]}'>
                <h3>{finding["message"]}</h3>

                <p><b>Line:</b> {finding["line"]}</p>
                <p><b>Severity:</b> {finding["severity"]}</p>
                <p><b>Type:</b> {finding["type"]}</p>
                <p><b>Confidence:</b> {finding["confidence"]}</p>
                <p><b>Fix:</b> {finding["fix"]}</p>
            </div>
            """

    html += "</body></html>"

    with open("raven_report.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("\n[bold green]HTML report saved:[/] raven_report.html")


@app.command()
def scan(
    path: str,
    html: bool = typer.Option(
        False,
        "--html",
        help="Generate HTML report"
    )
):

    print(f"\n[bold cyan]RAV3N-sec scanning:[/] {path}\n")

    results = scan_path(path)

    total = 0

    if not results:
        print("[green]No vulnerabilities found.[/green]")
        return

    for file, findings in results.items():

        print(f"\n[bold white]FILE:[/] {file}")

        for finding in findings:

            total += 1

            severity = finding["severity"]

            color = SEVERITY_COLORS.get(
                severity,
                "white"
            )

            print(
                f"""
[{color}]Line:[/] {finding['line']}
[{color}]Severity:[/] {severity}
[{color}]Type:[/] {finding['type']}
[{color}]Confidence:[/] {finding['confidence']}
[{color}]Issue:[/] {finding['message']}
[{color}]Fix:[/] {finding['fix']}
"""
            )

    print(f"\n[bold red]Total Findings:[/] {total}")

    if html:
        generate_html(results)


if __name__ == "__main__":
    app()