from datetime import datetime


def generate_html(results, output_file="report.html"):
    html = f"""
    <html>
    <head>
        <title>RAVE3N Report</title>
        <style>
            body {{ font-family: Arial; background: #111; color: #eee; }}
            .high {{ color: red; }}
            .medium {{ color: orange; }}
        </style>
    </head>
    <body>
        <h1>RAVE3N Security Report</h1>
        <p>Generated: {datetime.now()}</p>
        <hr>
    """

    for r in results:
        severity_class = r["severity"].lower()
        html += f"""
        <p class="{severity_class}">
        [{r['severity']}] Line {r['line']} - {r['message']}
        </p>
        """

    html += "</body></html>"

    with open(output_file, "w") as f:
        f.write(html)