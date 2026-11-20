import os, re, subprocess

base_dir = r"C:\Users\я\Desktop\Quantum_Galileo_Phase_Dynamics"
md_path = os.path.join(base_dir, "Quantum_Galileo_Phase_Dynamics.md")
html_path = os.path.join(base_dir, "Quantum_Galileo_Phase_Dynamics.html")
pdf_path = os.path.join(base_dir, "Quantum_Galileo_Phase_Dynamics.pdf")

with open(md_path, "r", encoding="utf-8") as f:
    text = f.read()

chart_path = os.path.join(base_dir, "quantum_galileo_phase_dynamics.png")
chart_url = "file:///" + chart_path.replace("\\", "/")

lines = text.split("\n")
html_lines = []
in_table = False
table_html = []

for line in lines:
    sline = line.strip()
    
    # Table parsing
    if sline.startswith("|") and sline.endswith("|"):
        cells = [c.strip() for c in sline[1:-1].split("|")]
        if all(re.match(r"^:?-+:?$", c) for c in cells):
            continue
        if not in_table:
            in_table = True
            table_html = ["<table class='academic-table'>"]
            table_html.append("<thead><tr>" + "".join([f"<th>{c}</th>" for c in cells]) + "</tr></thead><tbody>")
        else:
            table_html.append("<tr>" + "".join([f"<td>{c}</td>" for c in cells]) + "</tr>")
        continue
    else:
        if in_table:
            table_html.append("</tbody></table>")
            html_lines.append("\n".join(table_html))
            in_table = False
            table_html = []

    # Callouts
    if sline.startswith(">"):
        content = sline[1:].strip()
        if content.startswith("[!NOTE]"):
            content = "<b>NOTE:</b> " + content[7:].strip()
        html_lines.append(f"<div class='callout'>{content}</div>")
        continue

    # Headings
    if sline.startswith("# "):
        html_lines.append(f"<div class='title'>{sline[2:]}</div>")
        continue
    elif sline.startswith("## "):
        html_lines.append(f"<div class='section-title'>{sline[3:]}</div>")
        continue
    elif sline.startswith("### "):
        html_lines.append(f"<div class='subsection-title'>{sline[4:]}</div>")
        continue

    # Horizontal rules
    if sline == "---":
        html_lines.append("<hr class='divider'>")
        continue

    # Empty lines
    if not sline:
        html_lines.append("<div style='height: 6px;'></div>")
        continue

    # Bullet points
    if sline.startswith("* ") or sline.startswith("- "):
        html_lines.append(f"<div class='bullet'>&bull; {sline[2:]}</div>")
        continue
    
    # Numbered points
    num_match = re.match(r"^(\d+)\.\s+(.*)$", sline)
    if num_match:
        html_lines.append(f"<div class='bullet'><b>{num_match.group(1)}.</b> {num_match.group(2)}</div>")
        continue

    # Normal text
    html_lines.append(f"<p>{sline}</p>")

if in_table:
    table_html.append("</tbody></table>")
    html_lines.append("\n".join(table_html))

body_content = "\n".join(html_lines)

# Inject figure container
fig_html = f"""
<div class="figure-container">
    <img src="{chart_url}" style="width: 100%; max-width: 950px; border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.15);" alt="Quantum Galileo Phase Dynamics">
    <div class="figure-caption">
        <b>Figure 1: Quantum Galileo phase evolution and mesoscopic gravitational decoherence benchmark.</b><br>
        <b>(A)</b> Gravitational cubic phase shift accumulated by an atomic wave packet of $^{{87}}\\mathrm{{Rb}}$ as a function of separation time $T$, verifying the analytical UPD prediction $\\Delta\\Phi = \\frac{{m g^2 T^3}}{{3\\hbar}}$ against the empirical observation ($\\approx 80\\ \\mathrm{{rad}}$ at $T = 1.22\\ \\mathrm{{ms}}$) reported in <i>Science Advances</i>.<br>
        <b>(B)</b> Spatial wave packet trajectories in Earth's gravitational field comparing the held branch ($z=0$) in the atom-chip trap against the free-fall branch ($z = -\\frac{{1}}{{2}}gt^2$), reaching vertical separation $\\Delta z \\approx 7.30\\ \\mu\\mathrm{{m}}$.<br>
        <b>(C)</b> Gravitational coherence lifetime $\\tau(M)$ across 18 orders of magnitude in mass, establishing that atomic matter waves possess lifetimes of $\\tau > 4\\times 10^5\\ \\mathrm{{years}}$ ($P_{{\\mathrm{{collapse}}}} \\sim 10^{{-16}}$), while spontaneous collapse occurs at the mesoscopic threshold $M_{{\\mathrm{{crit}}}} \\approx 3.13 \\times 10^{{12}}\\ \\mathrm{{amu}}$ ($\\tau_{{\\mathrm{{crit}}}} \\approx 10\\ \\mathrm{{ms}}$) probed in <i>Experimentum Crucis 1</i>.<br>
        <b>(D)</b> Power-law mass-scaling discrimination comparing Unified Phase Dynamics ($\\Gamma \\propto M^{{2.00}}$) against Diósi--Penrose ($\\Gamma \\propto M^{{1.67}}$), thermal blackbody radiation ($\\Gamma \\propto M^{{1.00}}$), and background gas collisions ($\\Gamma \\propto M^{{0.67}}$).
    </div>
</div>
"""

# Replace the text block figure placeholder in Section 6
sec6_placeholder = re.search(r"<div class='section-title'>6\. Numerical Simulation and Visualization</div>.*?(?=<div class='section-title'>7\.|$)", body_content, re.DOTALL)
if sec6_placeholder:
    replacement = "<div class='section-title'>6. Numerical Simulation and Visualization</div>\n" + fig_html
    body_content = body_content[:sec6_placeholder.start()] + replacement + body_content[sec6_placeholder.end():]
else:
    body_content += fig_html

full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Gravitational Phase Evolution and Mesoscopic Decoherence Thresholds: Testing Unified Phase Dynamics against Atom Interferometry and Quantum Equivalence Principle Experiments</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js" 
            onload="renderMathInElement(document.body, {{delimiters: [
                {{left: '$$', right: '$$', display: true}},
                {{left: '$', right: '$', display: false}},
                {{left: '\\\\begin{{equation}}', right: '\\\\end{{equation}}', display: true}},
                {{left: '\\\\[', right: '\\\\]', display: true}}
            ]}});"></script>
    <style>
        @page {{
            size: A4;
            margin: 20mm 18mm 20mm 18mm;
            @bottom-right {{
                content: counter(page);
                font-family: 'Times New Roman', Times, serif;
                font-size: 9pt;
            }}
        }}
        body {{
            font-family: 'Times New Roman', Times, serif;
            font-size: 10.5pt;
            line-height: 1.5;
            color: #111;
            margin: 0;
            padding: 10px;
        }}
        .title {{
            font-size: 18pt;
            font-weight: bold;
            text-align: center;
            margin-bottom: 8px;
            line-height: 1.25;
            color: #0b1a30;
        }}
        .section-title {{
            font-size: 13pt;
            font-weight: bold;
            border-bottom: 1.5px solid #0b1a30;
            padding-bottom: 3px;
            margin-top: 20px;
            margin-bottom: 8px;
            color: #0b1a30;
        }}
        .subsection-title {{
            font-size: 11pt;
            font-weight: bold;
            margin-top: 14px;
            margin-bottom: 5px;
            color: #1a365d;
        }}
        p {{
            margin: 0 0 8px 0;
            text-align: justify;
            text-justify: inter-word;
        }}
        .bullet {{
            margin: 0 0 4px 18px;
            text-align: justify;
        }}
        .callout {{
            background: #f0f4f8;
            border-left: 4px solid #0d6efd;
            padding: 8px 12px;
            margin: 10px 0;
            font-size: 9.8pt;
        }}
        .divider {{
            border: 0;
            height: 1px;
            background: #ccc;
            margin: 15px 0;
        }}
        .figure-container {{
            text-align: center;
            margin: 18px 0;
            page-break-inside: avoid;
        }}
        .figure-caption {{
            font-size: 9pt;
            line-height: 1.35;
            color: #333;
            margin-top: 8px;
            text-align: justify;
            padding: 0 15px;
        }}
        .academic-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 14px 0;
            font-size: 8.5pt;
            page-break-inside: avoid;
        }}
        .academic-table th {{
            border-top: 2px solid #0b1a30;
            border-bottom: 1.5px solid #0b1a30;
            padding: 6px 4px;
            text-align: left;
            background-color: #f7fafc;
        }}
        .academic-table td {{
            border-bottom: 1px solid #e2e8f0;
            padding: 4px 4px;
        }}
        .academic-table tr:last-child td {{
            border-bottom: 2px solid #0b1a30;
        }}
    </style>
</head>
<body>
{body_content}
</body>
</html>
"""

with open(html_path, "w", encoding="utf-8") as f:
    f.write(full_html)
print(f"HTML successfully written to: {html_path}")

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(edge_path):
    edge_path = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

edge_cmd = [
    edge_path,
    "--headless",
    "--disable-gpu",
    "--run-all-compositor-stages-before-draw",
    "--virtual-time-budget=8000",
    f"--print-to-pdf={pdf_path}",
    html_path
]

res = subprocess.run(edge_cmd, capture_output=True, text=True)
print(f"Edge exit code: {res.returncode}")
if os.path.exists(pdf_path):
    print(f"PDF successfully created: {pdf_path} ({os.path.getsize(pdf_path)} bytes)")
else:
    print("PDF creation failed.")
