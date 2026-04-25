from datetime import datetime
from collections import Counter


def generate_html(results, output_file="report.html"):
    severity_colors = {
        "HIGH": "#ff4d4d",
        "MEDIUM": "#ffcc00",
        "LOW": "#66ff66"
    }

    counts = Counter(r["severity"] for r in results)

    html = f"""
    <html>
    <head>
        <title>RAVE3N Report</title>
        <style>
            body {{
                font-family: Arial;
                background: #0d1117;
                color: #e6edf3;
                padding: 20px;
            }}
            h1 {{
                color: #58a6ff;
            }}
            .summary {{
                margin: 15px 0;
                font-size: 18px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            th, td {{
                padding: 10px;
                border-bottom: 1px solid #30363d;
                text-align: left;
            }}
            th {{
                background: #161b22;
            }}
            .file-row {{
                color: #58a6ff;
                font-weight: bold;
                background: #0b1320;
            }}
        </style>
    </head>
    <body>

    <h1>🦅 RAVE3N Security Report</h1>
    <p>Generated: {datetime.now()}</p>

    <div class="summary">
        🔴 HIGH: {counts.get('HIGH',0)} &nbsp;&nbsp;
        🟡 MEDIUM: {counts.get('MEDIUM',0)} &nbsp;&nbsp;
        🟢 LOW: {counts.get('LOW',0)}
    </div>

    <table>
        <tr>
            <th>Severity</th>
            <th>Line</th>
            <th>Type</th>
            <th>Message</th>
            <th>Fix</th>
        </tr>
    """

    current_file = None

    for r in results:
        if r["file"] != current_file:
            html += f"""
            <tr class="file-row">
                <td colspan="5">📂 {r['file']}</td>
            </tr>
            """
            current_file = r["file"]

        color = severity_colors.get(r["severity"], "#ffffff")

        html += f"""
        <tr>
            <td style="color:{color}; font-weight:bold;">
                {r['severity']}
            </td>
            <td>{r['line']}</td>
            <td>{r['type']}</td>
            <td>{r['message']}</td>
            <td>{r.get('fix','')}</td>
        </tr>
        """

    html += """
    </table>
    </body>
    </html>
    """

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)