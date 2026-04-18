import typer
from rich import print
from raven.scanner import scan_file
from raven.report import generate_html

app = typer.Typer()


@app.command()
def scan(path: str, html: bool = False):
    """Scan a file for vulnerabilities"""

    results = scan_file(path)

    if not results:
        print("[green]✅ No issues found[/green]")
        return

    print(f"[bold red]⚠ Found {len(results)} issues[/bold red]\n")

    for r in results:
        color = "red" if r["severity"] == "HIGH" else "yellow"

        print(
            f"[{color}][{r['severity']}][/]{r['message']} "
            f"(line {r['line']}) [{r['type']}]"
        )

    if html:
        generate_html(results)
        print("\n[cyan]📄 HTML report generated: report.html[/cyan]")


if __name__ == "__main__":
    app()