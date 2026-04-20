from datetime import datetime


def generate_html(results, output_file="report.html"):
    html = f"""
    <html>
    <head>
    <style>
        body {{ background:#0d1117; color:#e6edf3; font-family:Arial; }}
        table {{ width:100%; border-collapse:collapse; }}
        th, td {{ padding:10px; border-bottom:1px solid #333; }}
        th {{ background:#161b22; }}
        .HIGH {{ color:#ff4d4d; }}
        .MEDIUM {{ color:#ffcc00; }}
        .LOW {{ color:#66ff66; }}
    </style>
    </head>
    <body>

    <h1>🦅 RAVE3N Report</h1>
    <p>{datetime.now()}</p>

    <table>
    <tr>
        <th>Severity</th>
        <th>Line</th>
        <th>Type</th>
        <th>Message</th>
        <th>Fix</th>
    </tr>
    """

    for r in results:
        html += f"""
        <tr>
            <td class="{r['severity']}">{r['severity']}</td>
            <td>{r['line']}</td>
            <td>{r['type']}</td>
            <td>{r['message']}</td>
            <td>{r.get('fix','')}</td>
        </tr>
        """

    html += "</table></body></html>"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)