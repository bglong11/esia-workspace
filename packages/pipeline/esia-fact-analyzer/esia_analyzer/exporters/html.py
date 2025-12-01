"""
HTML dashboard export for ESIA analysis results.
"""

import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Any


def export_html(
    output_path: Path,
    summary: Dict,
    issues: List[Dict],
    unit_issues: List[Dict],
    threshold_checks: List[Dict],
    gaps: List[Dict],
    factsheet: Dict,
    factsheet_summary: Dict = None,
    page_factsheet: Dict = None
):
    """
    Export analysis results to HTML dashboard with professional light theme.

    Args:
        output_path: Path to save HTML file
        summary: Analysis summary dictionary
        issues: List of consistency issues
        unit_issues: List of unit standardization issues
        threshold_checks: List of threshold check results
        gaps: List of gap analysis results
        factsheet: Organized factsheet dictionary
        factsheet_summary: Optional LLM-generated factsheet summary
        page_factsheet: Optional page-by-page distilled facts dictionary
    """
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ESIA Review Dashboard</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=Playfair+Display:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-primary: #fafafa;
            --bg-secondary: #ffffff;
            --bg-tertiary: #f5f5f5;
            --bg-accent: #e8f4f2;
            --text-primary: #1a1a1a;
            --text-secondary: #4a4a4a;
            --text-muted: #6b7280;
            --border-light: #e5e7eb;
            --border-medium: #d1d5db;
            --accent-teal: #0d9488;
            --accent-teal-light: #14b8a6;
            --accent-coral: #dc2626;
            --accent-coral-light: #ef4444;
            --accent-amber: #d97706;
            --accent-amber-light: #f59e0b;
            --accent-green: #059669;
            --accent-green-light: #10b981;
            --accent-blue: #2563eb;
            --accent-violet: #7c3aed;
            --shadow-sm: 0 1px 2px rgba(0,0,0,0.04);
            --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.03);
            --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.05), 0 4px 6px -2px rgba(0,0,0,0.03);
            --radius-sm: 6px;
            --radius-md: 10px;
            --radius-lg: 16px;
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}

        body {{
            font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            min-height: 100vh;
        }}

        /* Background pattern */
        .bg-pattern {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background:
                linear-gradient(135deg, rgba(13,148,136,0.03) 0%, transparent 50%),
                linear-gradient(225deg, rgba(37,99,235,0.02) 0%, transparent 50%),
                var(--bg-primary);
            z-index: -1;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 48px 32px;
        }}

        /* Header */
        header {{
            margin-bottom: 48px;
            padding-bottom: 32px;
            border-bottom: 1px solid var(--border-light);
        }}

        .header-top {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 24px;
            flex-wrap: wrap;
        }}

        h1 {{
            font-family: 'Playfair Display', Georgia, serif;
            font-size: 3rem;
            font-weight: 600;
            letter-spacing: -0.02em;
            color: var(--text-primary);
            line-height: 1.2;
        }}

        h1 span {{
            color: var(--accent-teal);
        }}

        .doc-meta {{
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.8rem;
            color: var(--text-muted);
            background: var(--bg-secondary);
            padding: 16px 20px;
            border-radius: var(--radius-md);
            border: 1px solid var(--border-light);
            box-shadow: var(--shadow-sm);
        }}

        .doc-meta strong {{
            color: var(--text-secondary);
            font-weight: 500;
        }}

        /* Stats Grid */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 48px;
        }}

        @media (max-width: 1200px) {{
            .stats-grid {{ grid-template-columns: repeat(2, 1fr); }}
        }}

        @media (max-width: 768px) {{
            .stats-grid {{ grid-template-columns: repeat(2, 1fr); }}
            h1 {{ font-size: 2rem; }}
            .container {{ padding: 24px 16px; }}
        }}

        .stat-card {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-light);
            border-radius: var(--radius-lg);
            padding: 24px;
            position: relative;
            overflow: hidden;
            transition: all 0.2s ease;
            box-shadow: var(--shadow-sm);
        }}

        .stat-card:hover {{
            box-shadow: var(--shadow-md);
            transform: translateY(-2px);
        }}

        .stat-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
        }}

        .stat-card.teal::before {{ background: var(--accent-teal); }}
        .stat-card.coral::before {{ background: var(--accent-coral); }}
        .stat-card.amber::before {{ background: var(--accent-amber); }}
        .stat-card.green::before {{ background: var(--accent-green); }}
        .stat-card.blue::before {{ background: var(--accent-blue); }}

        .stat-label {{
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--text-muted);
            margin-bottom: 12px;
        }}

        .stat-value {{
            font-family: 'IBM Plex Mono', monospace;
            font-size: 2.25rem;
            font-weight: 600;
            line-height: 1;
            margin-bottom: 6px;
        }}

        .stat-card.teal .stat-value {{ color: var(--accent-teal); }}
        .stat-card.coral .stat-value {{ color: var(--accent-coral); }}
        .stat-card.amber .stat-value {{ color: var(--accent-amber); }}
        .stat-card.green .stat-value {{ color: var(--accent-green); }}
        .stat-card.blue .stat-value {{ color: var(--accent-blue); }}

        .stat-sublabel {{
            font-size: 0.8rem;
            color: var(--text-muted);
        }}

        /* Section */
        .section {{
            margin-bottom: 40px;
        }}

        .section-header {{
            display: flex;
            align-items: center;
            gap: 16px;
            margin-bottom: 20px;
        }}

        h2 {{
            font-family: 'Playfair Display', Georgia, serif;
            font-size: 1.5rem;
            font-weight: 500;
            color: var(--text-primary);
        }}

        .section-badge {{
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.65rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            padding: 5px 10px;
            border-radius: 20px;
            background: var(--bg-tertiary);
            border: 1px solid var(--border-light);
            color: var(--text-muted);
        }}

        /* Tables */
        .table-wrapper {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-light);
            border-radius: var(--radius-lg);
            overflow: hidden;
            box-shadow: var(--shadow-sm);
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
        }}

        thead {{
            background: var(--bg-tertiary);
        }}

        th {{
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.65rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--text-muted);
            text-align: left;
            padding: 14px 20px;
            border-bottom: 1px solid var(--border-light);
        }}

        td {{
            padding: 14px 20px;
            border-bottom: 1px solid var(--border-light);
            color: var(--text-secondary);
            font-size: 0.875rem;
        }}

        tr:last-child td {{
            border-bottom: none;
        }}

        tr:hover {{
            background: var(--bg-tertiary);
        }}

        /* Status Badges */
        .badge {{
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 5px 12px;
            border-radius: 20px;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.65rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }}

        .badge-high, .badge-exceedance, .badge-missing {{
            background: rgba(220,38,38,0.08);
            color: var(--accent-coral);
            border: 1px solid rgba(220,38,38,0.2);
        }}

        .badge-medium, .badge-approaching {{
            background: rgba(217,119,6,0.08);
            color: var(--accent-amber);
            border: 1px solid rgba(217,119,6,0.2);
        }}

        .badge-low, .badge-compliant, .badge-present {{
            background: rgba(5,150,105,0.08);
            color: var(--accent-green);
            border: 1px solid rgba(5,150,105,0.2);
        }}

        .badge-info {{
            background: rgba(124,58,237,0.08);
            color: var(--accent-violet);
            border: 1px solid rgba(124,58,237,0.2);
        }}

        /* Empty state */
        .empty-state {{
            text-align: center;
            padding: 48px;
            color: var(--text-muted);
        }}

        .empty-state-icon {{
            font-size: 2.5rem;
            margin-bottom: 16px;
            opacity: 0.6;
        }}

        /* Unit standardization cards */
        .unit-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
            gap: 20px;
        }}

        .unit-card {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-light);
            border-radius: var(--radius-lg);
            padding: 24px;
            border-left: 4px solid var(--accent-amber);
            box-shadow: var(--shadow-sm);
        }}

        .unit-card-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 16px;
        }}

        .unit-card-title {{
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 4px;
        }}

        .unit-card-units {{
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.75rem;
            color: var(--accent-amber);
        }}

        .unit-examples {{
            margin-top: 16px;
            padding-top: 16px;
            border-top: 1px solid var(--border-light);
        }}

        .unit-example {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 0;
            font-size: 0.85rem;
        }}

        .unit-example-value {{
            font-family: 'IBM Plex Mono', monospace;
            color: var(--text-primary);
        }}

        .unit-example-page {{
            color: var(--text-muted);
            font-size: 0.75rem;
        }}

        .unit-recommendation {{
            margin-top: 16px;
            padding: 12px;
            background: var(--bg-accent);
            border-radius: var(--radius-sm);
            border: 1px solid rgba(13,148,136,0.15);
        }}

        .unit-recommendation-label {{
            font-size: 0.65rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--accent-teal);
            margin-bottom: 4px;
            font-weight: 600;
        }}

        .unit-recommendation-value {{
            font-family: 'IBM Plex Mono', monospace;
            color: var(--text-primary);
            font-size: 0.875rem;
        }}

        /* Collapsible Sections */
        .collapsible-section {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-light);
            border-radius: var(--radius-lg);
            margin-bottom: 16px;
            overflow: hidden;
            box-shadow: var(--shadow-sm);
        }}

        .collapsible-header {{
            width: 100%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 18px 24px;
            background: transparent;
            border: none;
            cursor: pointer;
            transition: background 0.2s ease;
            text-align: left;
        }}

        .collapsible-header:hover {{
            background: var(--bg-tertiary);
        }}

        .collapsible-title {{
            display: flex;
            align-items: center;
            gap: 12px;
            font-family: 'IBM Plex Sans', sans-serif;
            font-size: 1rem;
            font-weight: 600;
            color: var(--text-primary);
        }}

        .collapsible-icon {{
            font-size: 1.2rem;
        }}

        .collapsible-meta {{
            display: flex;
            align-items: center;
            gap: 16px;
        }}

        .coverage-pill {{
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.7rem;
            font-weight: 500;
            padding: 5px 12px;
            border-radius: 20px;
        }}

        .coverage-pill.teal {{
            background: rgba(13,148,136,0.1);
            color: var(--accent-teal);
        }}

        .coverage-pill.coral {{
            background: rgba(220,38,38,0.1);
            color: var(--accent-coral);
        }}

        .coverage-pill.amber {{
            background: rgba(217,119,6,0.1);
            color: var(--accent-amber);
        }}

        .chevron {{
            font-size: 0.75rem;
            color: var(--text-muted);
            transition: transform 0.3s ease;
        }}

        .collapsible-header.collapsed .chevron {{
            transform: rotate(-90deg);
        }}

        .collapsible-content {{
            border-top: 1px solid var(--border-light);
            max-height: none;
            overflow: visible;
            opacity: 1;
        }}

        .collapsible-content.collapsed {{
            max-height: 0;
            overflow: hidden;
            opacity: 0;
            border-top: none;
        }}

        .content-cell {{
            padding: 12px 20px;
        }}

        .content-item {{
            padding: 10px 14px;
            margin: 4px 0;
            background: var(--bg-tertiary);
            border-radius: var(--radius-sm);
            font-size: 0.85rem;
            line-height: 1.5;
            color: var(--text-secondary);
        }}

        .page-ref {{
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.7rem;
            color: var(--accent-teal);
            margin-left: 8px;
            font-weight: 500;
        }}

        .no-content {{
            color: var(--text-muted);
            font-style: italic;
            font-size: 0.85rem;
        }}

        /* Project Summary Section */
        .project-summary-content {{
            padding: 8px 0;
        }}

        .summary-section {{
            margin-bottom: 20px;
            padding: 20px;
            background: var(--bg-secondary);
            border-radius: var(--radius-md);
            border-left: 3px solid var(--accent-teal);
        }}

        .summary-section:last-child {{
            margin-bottom: 0;
        }}

        .summary-section-title {{
            font-family: 'IBM Plex Sans', system-ui, sans-serif;
            font-size: 0.95rem;
            font-weight: 600;
            color: var(--accent-teal);
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--border-subtle);
        }}

        .summary-section ul {{
            margin: 0;
            padding-left: 0;
            list-style: none;
        }}

        .summary-section li {{
            position: relative;
            padding-left: 20px;
            margin-bottom: 10px;
            line-height: 1.6;
            color: var(--text-secondary);
            font-size: 0.9rem;
        }}

        .summary-section li:last-child {{
            margin-bottom: 0;
        }}

        .summary-section li::before {{
            content: "•";
            position: absolute;
            left: 0;
            color: var(--accent-teal);
            font-weight: bold;
        }}

        .summary-section .page-ref {{
            color: var(--accent-teal);
            font-size: 0.85rem;
            font-weight: 500;
            background: rgba(13,148,136,0.1);
            padding: 1px 6px;
            border-radius: 3px;
            margin-left: 4px;
        }}

        .factsheet-paragraph {{
            margin-bottom: 16px;
            padding: 16px;
            background: var(--bg-secondary);
            border-radius: var(--radius-md);
            border-left: 3px solid var(--accent-teal);
        }}

        .factsheet-paragraph-title {{
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 8px;
            font-size: 0.9rem;
        }}

        .factsheet-paragraph-content {{
            color: var(--text-secondary);
            font-size: 0.875rem;
            line-height: 1.7;
        }}

        .fact-ids {{
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.7rem;
            color: var(--accent-teal);
            opacity: 0.8;
        }}

        /* Page Cards for Document Factsheet */
        .page-card {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-light);
            border-radius: var(--radius-md);
            margin-bottom: 12px;
            overflow: hidden;
            transition: all 0.2s ease;
        }}

        .page-card:hover {{
            box-shadow: var(--shadow-md);
        }}

        .page-header {{
            display: flex;
            align-items: center;
            padding: 14px 20px;
            cursor: pointer;
            background: var(--bg-tertiary);
            border-bottom: 1px solid var(--border-light);
            gap: 16px;
        }}

        .page-header:hover {{
            background: var(--bg-accent);
        }}

        .page-number {{
            font-family: 'IBM Plex Mono', monospace;
            font-weight: 600;
            font-size: 0.95rem;
            color: var(--accent-teal);
            min-width: 70px;
            background: rgba(13,148,136,0.1);
            padding: 4px 10px;
            border-radius: 4px;
        }}

        .page-section-context {{
            flex: 1;
            font-size: 0.85rem;
            color: var(--text-secondary);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .page-meta {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .fact-count {{
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.75rem;
            color: var(--text-muted);
            background: var(--bg-secondary);
            padding: 3px 8px;
            border-radius: 10px;
        }}

        .page-chevron {{
            color: var(--text-muted);
            transition: transform 0.2s ease;
            font-size: 0.8rem;
        }}

        .page-card.expanded .page-chevron {{
            transform: rotate(180deg);
        }}

        .page-facts-preview {{
            padding: 12px 20px;
            background: var(--bg-secondary);
        }}

        .page-card.expanded .page-facts-preview {{
            display: none;
        }}

        .page-facts-full {{
            display: none;
            padding: 16px 20px;
            background: var(--bg-secondary);
        }}

        .page-card.expanded .page-facts-full {{
            display: block;
        }}

        .page-facts-list {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}

        .page-fact-item {{
            padding: 10px 0;
            border-bottom: 1px solid var(--border-subtle);
            display: flex;
            align-items: flex-start;
            gap: 12px;
        }}

        .page-fact-item:last-child {{
            border-bottom: none;
        }}

        .page-fact-bullet {{
            width: 6px;
            height: 6px;
            background: var(--accent-teal);
            border-radius: 50%;
            margin-top: 7px;
            flex-shrink: 0;
        }}

        .page-fact-text {{
            flex: 1;
            font-size: 0.875rem;
            line-height: 1.6;
            color: var(--text-secondary);
        }}

        .view-source-btn {{
            font-size: 0.7rem;
            color: var(--accent-teal);
            background: rgba(13,148,136,0.1);
            border: none;
            padding: 4px 8px;
            border-radius: 4px;
            cursor: pointer;
            flex-shrink: 0;
            transition: all 0.2s ease;
        }}

        .view-source-btn:hover {{
            background: rgba(13,148,136,0.2);
        }}

        /* Side Panel for Source View */
        .source-side-panel {{
            position: fixed;
            top: 0;
            right: -450px;
            width: 450px;
            height: 100vh;
            background: var(--bg-secondary);
            border-left: 1px solid var(--border-light);
            box-shadow: -4px 0 20px rgba(0,0,0,0.1);
            z-index: 1000;
            transition: right 0.3s ease;
            display: flex;
            flex-direction: column;
        }}

        .source-side-panel.visible {{
            right: 0;
        }}

        .source-side-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 16px 20px;
            background: var(--bg-tertiary);
            border-bottom: 1px solid var(--border-light);
        }}

        .source-side-title {{
            font-weight: 600;
            color: var(--text-primary);
            font-size: 0.95rem;
        }}

        .source-page-ref {{
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.85rem;
            color: var(--accent-teal);
            background: rgba(13,148,136,0.1);
            padding: 4px 10px;
            border-radius: 4px;
        }}

        .source-close-btn {{
            background: none;
            border: none;
            color: var(--text-muted);
            cursor: pointer;
            font-size: 1.5rem;
            padding: 4px 8px;
            line-height: 1;
        }}

        .source-close-btn:hover {{
            color: var(--accent-coral);
        }}

        .source-side-content {{
            flex: 1;
            overflow-y: auto;
            padding: 20px;
        }}

        .source-chunk {{
            background: var(--bg-tertiary);
            border-radius: var(--radius-sm);
            padding: 14px 16px;
            margin-bottom: 12px;
            font-size: 0.85rem;
            line-height: 1.7;
            color: var(--text-secondary);
            border-left: 3px solid var(--accent-teal);
        }}

        .source-chunk:last-child {{
            margin-bottom: 0;
        }}

        /* Overlay when side panel is open */
        .source-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.3);
            z-index: 999;
            display: none;
        }}

        .source-overlay.visible {{
            display: block;
        }}

        /* Hide inline source panels */
        .source-panel {{
            display: none;
        }}

        /* Footer */
        footer {{
            margin-top: 64px;
            padding-top: 32px;
            border-top: 1px solid var(--border-light);
            text-align: center;
            color: var(--text-muted);
            font-size: 0.8rem;
        }}

        footer a {{
            color: var(--accent-teal);
            text-decoration: none;
            font-weight: 500;
        }}

        footer a:hover {{
            text-decoration: underline;
        }}

        /* Animations */
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(16px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        .animate-in {{
            animation: fadeInUp 0.4s ease forwards;
        }}

        .delay-1 {{ animation-delay: 0.05s; opacity: 0; }}
        .delay-2 {{ animation-delay: 0.1s; opacity: 0; }}
        .delay-3 {{ animation-delay: 0.15s; opacity: 0; }}
        .delay-4 {{ animation-delay: 0.2s; opacity: 0; }}
        .delay-5 {{ animation-delay: 0.25s; opacity: 0; }}
    </style>
</head>
<body>
    <div class="bg-pattern"></div>

    <!-- Source Side Panel -->
    <div class="source-overlay" id="source-overlay" onclick="closeSidePanel()"></div>
    <div class="source-side-panel" id="source-side-panel">
        <div class="source-side-header">
            <div>
                <span class="source-side-title">Original Text</span>
                <span class="source-page-ref" id="side-panel-page"></span>
            </div>
            <button class="source-close-btn" onclick="closeSidePanel()">&times;</button>
        </div>
        <div class="source-side-content" id="side-panel-content">
        </div>
    </div>

    <div class="container">
        <header class="animate-in">
            <div class="header-top">
                <h1>ESIA <span>Review</span></h1>
                <div class="doc-meta">
                    <strong>Document:</strong> {summary['document']}<br>
                    <strong>Pages:</strong> {summary['total_pages']} &middot;
                    <strong>Analyzed:</strong> {summary['analysis_date'][:10]}
                </div>
            </div>
        </header>

        <!-- Stats Grid -->
        <div class="stats-grid">
            <div class="stat-card teal animate-in delay-1">
                <div class="stat-label">Chunks Analyzed</div>
                <div class="stat-value">{summary['total_chunks']}</div>
                <div class="stat-sublabel">text segments</div>
            </div>
            <div class="stat-card {'coral' if summary['issues']['high_severity'] > 0 else 'green'} animate-in delay-2">
                <div class="stat-label">Consistency Issues</div>
                <div class="stat-value">{summary['issues']['total']}</div>
                <div class="stat-sublabel">{summary['issues']['high_severity']} high severity</div>
            </div>
            <div class="stat-card amber animate-in delay-3">
                <div class="stat-label">Unit Variations</div>
                <div class="stat-value">{summary['unit_issues']['total']}</div>
                <div class="stat-sublabel">mixed units</div>
            </div>
            <div class="stat-card {'coral' if summary['gaps']['missing'] > 0 else 'green'} animate-in delay-4">
                <div class="stat-label">Content Gaps</div>
                <div class="stat-value">{summary['gaps']['missing']}</div>
                <div class="stat-sublabel">of {summary['gaps']['total_checked']} expected</div>
            </div>
        </div>
'''

    # Project Summary Section (if available)
    if factsheet_summary and factsheet_summary.get('paragraphs'):
        # Count total bullet points for badge
        total_bullets = sum(
            len([l for l in factsheet_summary.get('paragraphs', {}).get(k, '').split('\n') if l.strip()])
            for k in ['project_overview', 'baseline', 'impacts', 'mitigation', 'residual_risks']
        )
        html += f'''
        <!-- Project Summary -->
        <div class="section animate-in">
            <div class="collapsible-section">
                <button class="collapsible-header" onclick="toggleSection(this)">
                    <div class="collapsible-title">
                        <span class="collapsible-icon">📋</span>
                        <span>Project Summary</span>
                    </div>
                    <div class="collapsible-meta">
                        <span class="section-badge">{total_bullets} Key Points</span>
                        <span class="chevron">▼</span>
                    </div>
                </button>
                <div class="collapsible-content" style="display: block;">
                    <div class="project-summary-content">
'''
        paragraphs = factsheet_summary.get('paragraphs', {})
        section_titles = {
            'project_overview': 'Project Overview',
            'baseline': 'Environmental & Social Baseline',
            'impacts': 'Major Anticipated Impacts',
            'mitigation': 'Mitigation & Management Measures',
            'residual_risks': 'Residual Risks & Compliance'
        }
        for key, title in section_titles.items():
            content = paragraphs.get(key, '')
            if content:
                # Convert bullet points to HTML list items
                lines = content.split('\n')
                list_items = []
                for line in lines:
                    line = line.strip()
                    if line.startswith('•'):
                        line = line[1:].strip()
                    if line:
                        # Standardize page references to [p. xxx] format
                        line = re.sub(r'\(p\.?\s*(\d+)\)', r'[p. \1]', line)
                        line = re.sub(r'\(pp\.?\s*(\d+(?:-\d+)?)\)', r'[pp. \1]', line)
                        # Highlight page references
                        line = re.sub(r'\[p\.\s*(\d+)\]', r'<span class="page-ref">[p. \1]</span>', line)
                        line = re.sub(r'\[pp\.\s*(\d+(?:-\d+)?)\]', r'<span class="page-ref">[pp. \1]</span>', line)
                        list_items.append(f'<li>{line}</li>')

                if list_items:
                    html += f'''
                        <div class="summary-section">
                            <div class="summary-section-title">{title}</div>
                            <ul>
{''.join(list_items)}
                            </ul>
                        </div>
'''
        html += '''
                    </div>
                </div>
            </div>
        </div>
'''

    # Document Factsheet Section (Page-based)
    total_pages = len(page_factsheet) if page_factsheet else 0
    total_facts = sum(len(p.get('distilled_facts', [])) for p in (page_factsheet or {}).values())

    html += f'''
        <!-- Document Factsheet Section -->
        <div class="section animate-in">
            <div class="collapsible-section">
                <button class="collapsible-header" onclick="toggleSection(this)">
                    <div class="collapsible-title">
                        <span class="collapsible-icon">📑</span>
                        <span>Document Factsheet</span>
                    </div>
                    <div class="collapsible-meta">
                        <span class="section-badge">{total_pages} pages &middot; {total_facts} facts</span>
                        <span class="chevron">▼</span>
                    </div>
                </button>
                <div class="collapsible-content">
                    <div style="padding: 24px;">
'''

    if page_factsheet:
        for page_num in sorted(page_factsheet.keys()):
            page_data = page_factsheet[page_num]
            section_context = page_data.get('section_context', '')
            if section_context and len(section_context) > 60:
                section_context = section_context[:60] + '...'
            distilled_facts = page_data.get('distilled_facts', [])
            original_chunks = page_data.get('original_chunks', [])

            # Preview: first 3 facts
            preview_facts = distilled_facts[:3]
            all_facts = distilled_facts

            html += f'''
                        <div class="page-card" id="page-{page_num}">
                            <div class="page-header" onclick="togglePageCard({page_num})">
                                <span class="page-number">p. {page_num}</span>
                                <span class="page-section-context">{section_context}</span>
                                <div class="page-meta">
                                    <span class="fact-count">{len(distilled_facts)} facts</span>
                                    <span class="page-chevron">▼</span>
                                </div>
                            </div>
                            <div class="page-facts-preview">
                                <ul class="page-facts-list">
'''
            # Preview facts
            for fact in preview_facts:
                fact_text = str(fact).replace('<', '&lt;').replace('>', '&gt;')
                if len(fact_text) > 150:
                    fact_text = fact_text[:150] + '...'
                html += f'''
                                    <li class="page-fact-item">
                                        <span class="page-fact-bullet"></span>
                                        <span class="page-fact-text">{fact_text}</span>
                                    </li>
'''
            if len(distilled_facts) > 3:
                html += f'''
                                    <li class="page-fact-item" style="color: var(--text-muted); font-style: italic;">
                                        <span class="page-fact-bullet" style="background: var(--text-muted);"></span>
                                        <span class="page-fact-text">+ {len(distilled_facts) - 3} more facts...</span>
                                    </li>
'''
            html += '''
                                </ul>
                            </div>
                            <div class="page-facts-full">
                                <ul class="page-facts-list">
'''
            # All facts with view source buttons
            for i, fact in enumerate(all_facts):
                fact_text = str(fact).replace('<', '&lt;').replace('>', '&gt;')
                html += f'''
                                    <li class="page-fact-item">
                                        <span class="page-fact-bullet"></span>
                                        <span class="page-fact-text">{fact_text}</span>
                                        <button class="view-source-btn" onclick="toggleSource({page_num}, {i}, event)">View source</button>
                                    </li>
'''
            html += '''
                                </ul>
'''
            # Source panel with original chunks
            if original_chunks:
                html += f'''
                                <div class="source-panel" id="source-panel-{page_num}">
                                    <div class="source-header">
                                        <span>Original Text</span>
                                        <button class="source-close-btn" onclick="closeSourcePanel({page_num})">&times;</button>
                                    </div>
'''
                for chunk in original_chunks[:10]:  # Limit to 10 chunks
                    chunk_text = chunk.get('text', '').replace('<', '&lt;').replace('>', '&gt;')
                    if len(chunk_text) > 500:
                        chunk_text = chunk_text[:500] + '...'
                    html += f'''
                                    <div class="source-chunk">{chunk_text}</div>
'''
                html += '''
                                </div>
'''
            html += '''
                            </div>
                        </div>
'''

    else:
        html += '''
                        <div class="empty-state">
                            <div class="empty-state-icon">📭</div>
                            <p>No factsheet data available. Run analysis with LLM enabled to generate page-by-page facts.</p>
                        </div>
'''

    html += '''
                    </div>
                </div>
            </div>
        </div>

        <!-- Consistency Issues Section -->
        <div class="section animate-in">
            <div class="collapsible-section">
                <button class="collapsible-header" onclick="toggleSection(this)">
                    <div class="collapsible-title">
                        <span class="collapsible-icon">⚡</span>
                        <span>Consistency Issues</span>
                    </div>
                    <div class="collapsible-meta">
                        <span class="section-badge">Like-for-Like Comparison</span>
                        <span class="chevron">▼</span>
                    </div>
                </button>
                <div class="collapsible-content">
'''

    if issues:
        html += '''
            <div class="table-wrapper" style="border: none; box-shadow: none;">
                <table>
                    <thead>
                        <tr>
                            <th>Severity</th>
                            <th>Parameter Context</th>
                            <th>Values Found</th>
                            <th>Normalized</th>
                        </tr>
                    </thead>
                    <tbody>
'''
        for issue in issues[:25]:
            severity = issue.get('severity', 'medium')
            badge_class = f"badge-{severity}"
            values_display = "<br>".join(issue.get('values', [])[:3])
            norm_display = f"{issue.get('normalized_values', [])[:3]} {issue.get('base_unit', '')}"

            html += f'''
                        <tr>
                            <td><span class="badge {badge_class}">{severity.upper()}</span></td>
                            <td style="color: var(--text-primary); font-weight: 500;">{issue.get('context', '')}</td>
                            <td style="font-family: 'IBM Plex Mono', monospace; font-size: 0.8rem;">{values_display}</td>
                            <td style="font-family: 'IBM Plex Mono', monospace; font-size: 0.8rem; color: var(--text-muted);">{norm_display}</td>
                        </tr>
'''
        html += '''
                    </tbody>
                </table>
            </div>
'''
    else:
        html += '''
            <div class="empty-state">
                <div class="empty-state-icon">✓</div>
                <p>No consistency issues detected. All like-for-like comparisons passed.</p>
            </div>
'''

    html += '''
                </div>
            </div>
        </div>

        <!-- Unit Standardization Section -->
        <div class="section animate-in">
            <div class="collapsible-section">
                <button class="collapsible-header" onclick="toggleSection(this)">
                    <div class="collapsible-title">
                        <span class="collapsible-icon">⚙️</span>
                        <span>Unit Standardization</span>
                    </div>
                    <div class="collapsible-meta">
                        <span class="section-badge">Mixed Units Detected</span>
                        <span class="chevron">▼</span>
                    </div>
                </button>
                <div class="collapsible-content">
'''

    if unit_issues:
        html += '''
            <div class="unit-cards" style="padding: 20px;">
'''
        for issue in unit_issues:
            units_list = ", ".join(issue.get('units_used', []))
            html += f'''
                <div class="unit-card">
                    <div class="unit-card-header">
                        <div>
                            <div class="unit-card-title">{issue.get('context', '')}</div>
                            <div class="unit-card-units">{units_list}</div>
                        </div>
                        <span class="badge badge-info">{len(issue.get('units_used', []))} units</span>
                    </div>
                    <div class="unit-examples">
                        <div style="font-size: 0.7rem; color: var(--text-muted); margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600;">Examples Found</div>
'''
            for ex in issue.get('examples', [])[:3]:
                html += f'''
                        <div class="unit-example">
                            <span class="unit-example-value">{ex['value']} {ex['unit']}</span>
                            <span class="unit-example-page">[p. {ex['page']}]</span>
                        </div>
'''
            html += f'''
                    </div>
                    <div class="unit-recommendation">
                        <div class="unit-recommendation-label">Recommended Standard</div>
                        <div class="unit-recommendation-value">Convert all to {issue.get('base_unit', '')}</div>
                    </div>
                </div>
'''
        html += '''
            </div>
'''
    else:
        html += '''
            <div class="empty-state">
                <div class="empty-state-icon">✓</div>
                <p>All parameters use consistent units throughout the document.</p>
            </div>
'''

    html += '''
                </div>
            </div>
        </div>

        <!-- Gap Analysis Section -->
        <div class="section animate-in">
            <div class="collapsible-section">
                <button class="collapsible-header" onclick="toggleSection(this)">
                    <div class="collapsible-title">
                        <span class="collapsible-icon">📋</span>
                        <span>Gap Analysis</span>
                    </div>
                    <div class="collapsible-meta">
                        <span class="section-badge">Expected Content</span>
                        <span class="chevron">▼</span>
                    </div>
                </button>
                <div class="collapsible-content">
'''

    # Group gaps by section
    gaps_by_section = defaultdict(list)
    for gap in gaps:
        gaps_by_section[gap.get('section', 'Other')].append(gap)

    # Section icons
    section_icons = {
        'Project Description': '📋',
        'Physical Baseline': '🌍',
        'Biological Baseline': '🌿',
        'Social Baseline': '👥',
        'Impact Assessment': '⚡',
        'Mitigation & Management': '🛡️',
    }

    for section_name, section_gaps in gaps_by_section.items():
        present_count = len([g for g in section_gaps if g['status'] == 'PRESENT'])
        total_count = len(section_gaps)
        icon = section_icons.get(section_name, '📄')
        status_class = 'teal' if present_count == total_count else 'coral' if present_count < total_count / 2 else 'amber'

        html += f'''
            <div class="collapsible-section" style="margin: 16px;">
                <button class="collapsible-header collapsed" onclick="toggleSection(this)">
                    <div class="collapsible-title">
                        <span class="collapsible-icon">{icon}</span>
                        <span>{section_name}</span>
                    </div>
                    <div class="collapsible-meta">
                        <span class="coverage-pill {status_class}">{present_count}/{total_count} found</span>
                        <span class="chevron">▼</span>
                    </div>
                </button>
                <div class="collapsible-content collapsed">
                    <table>
                        <thead>
                            <tr>
                                <th style="width: 25%;">Sub-section</th>
                                <th style="width: 10%;">Status</th>
                                <th style="width: 65%;">Content Found</th>
                            </tr>
                        </thead>
                        <tbody>
'''
        for gap in section_gaps:
            status = gap.get('status', 'UNKNOWN')
            badge_class = f"badge-{status.lower()}"
            matches = gap.get('matches', [])

            if matches:
                content_parts = []
                for m in matches:
                    content = m.get('content', '').replace('<', '&lt;').replace('>', '&gt;')
                    page = m.get('page', '?')
                    content_parts.append(f'<div class="content-item">{content} <span class="page-ref">[p. {page}]</span></div>')
                content_html = ''.join(content_parts)
            else:
                content_html = '<span class="no-content">No content found</span>'

            html += f'''
                            <tr>
                                <td style="font-weight: 500; color: var(--text-primary);">{gap.get('item', '')}</td>
                                <td><span class="badge {badge_class}">{status}</span></td>
                                <td class="content-cell">{content_html}</td>
                            </tr>
'''

        html += '''
                        </tbody>
                    </table>
                </div>
            </div>
'''

    html += '''
                </div>
            </div>
        </div>

        <footer>
            <p>ESIA Reviewer v2.0 &middot; Context-Aware Consistency Checking &middot; Unit Standardization Analysis</p>
            <p style="margin-top: 8px;">Reference: <a href="https://www.ifc.org/en/insights-reports/2007/ehs-guidelines" target="_blank">IFC EHS Guidelines</a></p>
        </footer>
    </div>

    <script>
        // Store source data for side panel
        const sourceData = {};

        function toggleSection(header) {
            header.classList.toggle('collapsed');
            const content = header.nextElementSibling;
            content.classList.toggle('collapsed');

            if (!header.classList.contains('collapsed')) {
                setTimeout(() => {
                    header.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                }, 100);
            }
        }

        function togglePageCard(pageNum) {
            const card = document.getElementById('page-' + pageNum);
            if (card) {
                card.classList.toggle('expanded');
            }
        }

        function toggleSource(pageNum, factIndex, event) {
            event.stopPropagation();
            // Get source chunks from the hidden inline panel
            const inlinePanel = document.getElementById('source-panel-' + pageNum);
            if (inlinePanel) {
                const chunks = inlinePanel.querySelectorAll('.source-chunk');
                let html = '';
                chunks.forEach(chunk => {
                    html += '<div class="source-chunk">' + chunk.innerHTML + '</div>';
                });
                openSidePanel(pageNum, html);
            }
        }

        function openSidePanel(pageNum, contentHtml) {
            document.getElementById('side-panel-page').textContent = 'Page ' + pageNum;
            document.getElementById('side-panel-content').innerHTML = contentHtml;
            document.getElementById('source-side-panel').classList.add('visible');
            document.getElementById('source-overlay').classList.add('visible');
            document.body.style.overflow = 'hidden';
        }

        function closeSidePanel() {
            document.getElementById('source-side-panel').classList.remove('visible');
            document.getElementById('source-overlay').classList.remove('visible');
            document.body.style.overflow = '';
        }

        // Close side panel with Escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeSidePanel();
            }
        });
    </script>
</body>
</html>
'''

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"HTML dashboard saved to: {output_path}")
