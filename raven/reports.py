from datetime import datetime


def generate_html(results, output_file="report.html"):
    severity_colors = {
        "HIGH": "#ff4d4d",
        "MEDIUM": "#ffcc00",
        "LOW": "#66ff66"
    }

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
        </style>
    </head>
    <body>

    <h1>🦅 RAVE3N Security Report</h1>
    <p>Generated: {datetime.now()}</p>

    <table>
        <tr>
            <th>Severity</th>
            <th>Line</th>
            <th>Type</th>
            <th>Message</th>
        </tr>
    """

    for r in results:
        color = severity_colors.get(r["severity"], "#ffffff")

        html += f"""
        <tr>
            <td style="color:{color}; font-weight:bold;">
                {r['severity']}
            </td>
            <td>{r['line']}</td>
            <td>{r['type']}</td>
            <td>{r['message']}</td>
        </tr>
        """

    html += """
    </table>
    </body>
    </html>
    """

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)