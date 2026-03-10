#!/usr/bin/env python3
"""
Report Generators
"""

import json
import csv
from datetime import datetime
from typing import List
from dataclasses import asdict

from .models import JavaFileInfo


class ConsoleReporter:
    """Console report generator"""
    
    @staticmethod
    def print_report(files: List[JavaFileInfo], detailed: bool = False):
        """Print console report"""
        print(f"\n{'='*120}")
        print("Java Codebase Analysis Report")
        print(f"{'='*120}\n")
        
        print(f"Total Files: {len(files)}")
        print(f"Total Lines: {sum(f.lines for f in files):,}\n")
        
        # Group by category
        by_category = {}
        for f in files:
            if f.category not in by_category:
                by_category[f.category] = []
            by_category[f.category].append(f)
        
        # Print by category
        for category in sorted(by_category.keys()):
            files_list = by_category[category]
            total_lines = sum(f.lines for f in files_list)
            
            print(f"\n{category.upper()} ({len(files_list)} files, {total_lines:,} lines)")
            print("-" * 120)
            
            for f in sorted(files_list, key=lambda x: x.class_name):
                confidence = f.confidence * 100
                desc = f" | {f.description[:40]}..." if f.description else ""
                print(f"  {f.class_name:<40} | {f.package:<35} | {f.lines:>5} lines | {confidence:.0f}%{desc}")


class JSONReporter:
    """JSON report generator"""
    
    @staticmethod
    def export(files: List[JavaFileInfo], output_file: str):
        """Export to JSON"""
        data = {
            'total_files': len(files),
            'total_lines': sum(f.lines for f in files),
            'files': [asdict(f) for f in files]
        }
        
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✓ JSON exported to: {output_file}")


class CSVReporter:
    """CSV report generator"""
    
    @staticmethod
    def export(files: List[JavaFileInfo], output_file: str):
        """Export to CSV"""
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Class', 'Package', 'Category', 'Lines', 'Confidence', 'Description'])
            
            for file in files:
                writer.writerow([
                    file.class_name,
                    file.package,
                    file.category,
                    file.lines,
                    f"{file.confidence*100:.1f}%",
                    file.description[:100]
                ])
        
        print(f"✓ CSV exported to: {output_file}")


class HTMLReporter:
    """HTML report generator"""
    
    @staticmethod
    def export(files: List[JavaFileInfo], output_file: str):
        """Export to HTML"""
        # Group by category
        by_category = {}
        for f in files:
            if f.category not in by_category:
                by_category[f.category] = []
            by_category[f.category].append(f)
        
        rows = ""
        for category in sorted(by_category.keys()):
            for f in sorted(by_category[category], key=lambda x: x.class_name):
                conf = f.confidence * 100
                color = '#27ae60' if conf >= 90 else '#f39c12' if conf >= 70 else '#e74c3c'
                rows += f"""
    <tr>
        <td>{f.class_name}</td>
        <td>{f.package}</td>
        <td>{category}</td>
        <td>{f.lines}</td>
        <td><span style="color:{color};font-weight:bold;">{conf:.0f}%</span></td>
        <td>{f.description[:60]}</td>
    </tr>
"""
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Java Analysis Report</title>
    <style>
        body {{ font-family: Arial; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        .stats {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 20px 0; }}
        .stat {{ background: #3498db; color: white; padding: 20px; text-align: center; border-radius: 8px; }}
        .stat-value {{ font-size: 32px; font-weight: bold; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th {{ background: #34495e; color: white; padding: 12px; text-align: left; }}
        td {{ padding: 10px; border-bottom: 1px solid #ecf0f1; }}
        tr:hover {{ background: #f9f9f9; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Java Codebase Analysis Report</h1>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-value">{len(files)}</div>
                <div>Total Files</div>
            </div>
            <div class="stat">
                <div class="stat-value">{sum(f.lines for f in files):,}</div>
                <div>Lines of Code</div>
            </div>
            <div class="stat">
                <div class="stat-value">{len(set(f.category for f in files))}</div>
                <div>Categories</div>
            </div>
        </div>
        
        <h2>Files</h2>
        <table>
            <tr><th>Class</th><th>Package</th><th>Category</th><th>Lines</th><th>Confidence</th><th>Description</th></tr>
            {rows}
        </table>
    </div>
</body>
</html>
"""
        
        with open(output_file, 'w') as f:
            f.write(html)
        
        print(f"✓ HTML exported to: {output_file}")