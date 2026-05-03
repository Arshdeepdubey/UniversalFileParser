class HTMLGenerator:
    @staticmethod
    def generate_view(data: list, columns: list, stats: dict) -> str:
        """Generates a responsive HTML table with VS Code theme support."""
        
        # Build Table Headers
        headers_html = "".join([f"<th>{col}</th>" for col in columns])
        
        # Build Table Rows (Preview limit 10)
        rows_html = ""
        for row in data[:10]:
            cells = "".join([f"<td>{row.get(col, '')}</td>" for col in columns])
            rows_html += f"<tr>{cells}</tr>"

        html_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{ font-family: var(--vscode-font-family); color: var(--vscode-editor-foreground); padding: 20px; }}
                .stats-container {{ display: flex; gap: 20px; margin-bottom: 20px; background: var(--vscode-editor-background); border: 1px solid var(--vscode-panel-border); padding: 15px; border-radius: 4px; }}
                .stat-card {{ display: flex; flex-direction: column; }}
                .stat-label {{ font-size: 10px; text-transform: uppercase; opacity: 0.8; }}
                .stat-value {{ font-size: 18px; font-weight: bold; color: var(--vscode-textLink-foreground); }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
                th {{ text-align: left; background: var(--vscode-list-hoverBackground); padding: 10px; border: 1px solid var(--vscode-panel-border); }}
                td {{ padding: 10px; border: 1px solid var(--vscode-panel-border); font-size: 12px; }}
                tr:nth-child(even) {{ background: var(--vscode-input-background); opacity: 0.9; }}
            </style>
        </head>
        <body>
            <h2>Universal File Parser | Preview</h2>
            
            <div class="stats-container">
                <div class="stat-card"><span class="stat-label">File Type</span><span class="stat-value">{stats.get('type')}</span></div>
                <div class="stat-card"><span class="stat-label">Total Rows</span><span class="stat-value">{stats.get('rows')}</span></div>
                <div class="stat-card"><span class="stat-label">Columns</span><span class="stat-value">{len(columns)}</span></div>
            </div>

            <table>
                <thead><tr>{headers_html}</tr></thead>
                <tbody>{rows_html}</tbody>
            </table>
        </body>
        </html>
        """
        return html_template