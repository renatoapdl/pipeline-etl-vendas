# Gera o PDF do currículo a partir de CURRICULO_PDF.md (única fonte de texto).
#
# Marcadores suportados no .md:
#   <!-- NOVA-PAGINA -->          força o próximo conteúdo a começar numa página nova
#   <!-- ESPACO=6mm -->           insere um espaço em branco vertical (ex.: ESPACO=4mm)
#
# Ajustes de layout ficam no bloco CSS abaixo (margens da página, tamanho de fonte,
# altura de linha e margens verticais). Não dependem do texto no .md.
#
# Uso:  python gerar_curriculo_pdf.py
# Saída: PROJETOS\LANDING PAGE\assets\curriculo.pdf  (e um HTML intermediário no Temp).

import pathlib, re, subprocess, tempfile

MD = r"C:\Users\renat\Documents\OPENCODE\CARREIRA\arquivos-md\CURRICULO_PDF.md"
HTML_OUT = pathlib.Path(tempfile.gettempdir()) / "opencode" / "curriculo.html"
PDF_OUT = r"C:\Users\renat\Documents\OPENCODE\PROJETOS\LANDING PAGE\assets\curriculo.pdf"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

CSS = """
@page { size: A4; margin: 15mm 14mm 14mm 14mm; }
* { box-sizing: border-box; }
body { font-family: 'Segoe UI', Calibri, Arial, sans-serif; color: #1f2430; font-size: 10.2pt; line-height: 1.42; margin: 0; }
h1 { font-size: 19pt; margin: 0 0 1.5mm; letter-spacing: .5px; color: #16213e; }
.headline { font-size: 11pt; font-weight: 600; margin: 0 0 1mm; }
.contact, .links { font-size: 9.5pt; color: #3a4256; }
.links a { color: #1a2a6c; text-decoration: none; }
.topline { border-bottom: 1.6pt solid #16213e; margin-bottom: 4mm; padding-bottom: 2.5mm; }
h2 { font-size: 11.5pt; text-transform: uppercase; letter-spacing: .4px; color: #16213e; border-bottom: 1pt solid #9aa3b2; margin: 4.5mm 0 2mm; padding-bottom: .8mm; }
h3 { font-size: 10.8pt; margin: 2.8mm 0 .8mm; color: #1f2430; }
.jobhead { margin: 2.8mm 0 .4mm; }
.jobhead .title { font-size: 10.8pt; font-weight: 700; }
.jobhead .date { float: right; font-weight: 600; font-size: 9.6pt; color: #3a4256; }
.clearfix::after { content: ""; display: block; clear: both; }
.role { font-weight: 600; font-size: 9.8pt; }
.meta { font-size: 9.4pt; color: #3a4256; margin-bottom: 1.2mm; }
ul { margin: .6mm 0 1.4mm 0; padding-left: 5mm; }
li { margin-bottom: .7mm; }
p, li { orphans: 2; widows: 2; }
a { color: #1a2a6c; text-decoration: none; }
code { font-family: 'Cascadia Mono', Consolas, monospace; font-size: 8.6pt; background: #eef1f6; padding: 0 2px; border-radius: 2px; }
.keep { break-inside: avoid; page-break-inside: avoid; margin-bottom: 1mm; }
.newpage { break-before: page; page-break-before: always; }
.spacer { height: 4mm; }
"""

SEC = {
    "RESUMO PROFISSIONAL": "Resumo Profissional",
    "EXPERIÊNCIA PROFISSIONAL": "Experiência Profissional",
    "PROJETOS RELEVANTES": "Projetos Relevantes",
    "COMPETÊNCIAS E QUALIFICAÇÕES": "Competências e Qualificações",
    "FORMAÇÃO ACADÊMICA": "Formação Acadêmica",
    "CERTIFICAÇÕES": "Certificações",
}


def links(t):
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)


def plain(t):
    return t.replace("**", "")


def rich(t):
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    return t


def parse(lines):
    name = None
    in_header = False
    sec = None
    top = []
    out = []
    job = None
    comp_group = None
    in_formacao_title = False

    def render_keep(sub, items):
        parts = ['<div class="keep">']
        if sub:
            parts.append(f'<p><strong>{sub}:</strong></p>')
        parts.append("<ul>")
        for it in items:
            parts.append(f"<li>{it}</li>")
        parts.append("</ul></div>")
        return "".join(parts)

    def close_job():
        nonlocal job, comp_group
        if not job:
            return
        if job["kind"] == "projeto":
            parts = [f'<div class="keep"><h3>{job["title"]}</h3>']
            if job.get("meta"):
                parts.append(f'<p class="meta"><strong>Stack:</strong> {job["meta"]}</p>')
            parts.append("<ul>")
            for b in job.get("bullets", []):
                parts.append(f"<li>{b}</li>")
            parts.append("</ul></div>")
            out.append("".join(parts))
        else:
            parts = ['<div class="keep"><div class="jobhead clearfix">',
                     f'<span class="title">{job["title"]}</span>',
                     f'<span class="date">{job.get("date", "")}</span></div>']
            if job.get("role"):
                parts.append(f'<p class="role">{job["role"]}</p>')
            if job.get("meta"):
                parts.append(f'<p class="meta">{job["meta"]}</p>')
            parts.append("</div>")
            out.append("".join(parts))
            for u in job.get("units", []):
                out.append(render_keep(u["sub"], u["items"]))
        job = None
        comp_group = None

    def close_comp():
        nonlocal comp_group
        if comp_group:
            items = rich("; ".join(comp_group["items"]))
            out.append(f'<div class="keep"><p><strong>{comp_group["title"]}:</strong> ' +
                       items + "</p></div>")
            comp_group = None

    for raw in lines:
        line = raw.rstrip()
        s = line.strip()

        if s == "<div align=\"center\">":
            in_header = True
            continue
        if s == "</div>":
            in_header = False
            continue
        if s == "<!-- NOVA-PAGINA -->":
            out.append('<div class="newpage"></div>')
            continue
        m = re.match(r"<!-- ESPACO=(\d+(?:\.\d+)?)mm -->", s)
        if m:
            out.append(f'<div class="spacer" style="height:{m.group(1)}mm"></div>')
            continue

        if name is None and line.startswith("# "):
            name = plain(line[2:])
            continue

        if in_header:
            if s.startswith("**") and s.endswith("**"):
                top.append(f'<p class="headline">{plain(s)}</p>')
            elif "[" in s:
                top.append(f'<p class="links">{links(s)}</p>')
            else:
                top.append(f'<p class="contact">{s}</p>')
            continue

        if line.startswith("## "):
            close_job(); close_comp()
            sec = line[3:].strip()
            out.append(f"<h2>{SEC.get(sec, sec)}</h2>")
            continue

        if line.startswith("---"):
            continue

        if line.startswith("### "):
            close_job(); close_comp()
            title = line[4:].strip()
            if sec == "EXPERIÊNCIA PROFISSIONAL":
                job = {"kind": "emprego", "title": title, "role": None, "date": "",
                       "meta": None, "units": []}
            elif sec == "PROJETOS RELEVANTES":
                job = {"kind": "projeto", "title": title, "meta": None, "bullets": []}
            elif sec == "COMPETÊNCIAS E QUALIFICAÇÕES":
                comp_group = {"title": title, "items": []}
            else:
                out.append(f"<h3>{title}</h3>")
            continue

        if line.startswith("- "):
            item = rich(links(s[2:]))
            if comp_group is not None:
                comp_group["items"].append(item)
            elif job is not None and job["kind"] == "projeto":
                job["bullets"].append(item)
            elif job is not None:
                if not job["units"] or job["units"][-1]["sub"] is None and "sub" != "":
                    pass
                u = job["units"][-1] if job["units"] else None
                if u is None or u["sub"] is None and u["items"]:
                    u = None
                if u is None:
                    job["units"].append({"sub": None, "items": []})
                    u = job["units"][-1]
                u["items"].append(item)
            else:
                out.append(f'<div class="keep"><ul><li>{item}</li></ul></div>')
            continue

        sub = re.match(r"\*\*(.+?):\*\*$", s)
        if sub and job is not None and job["kind"] == "emprego":
            job["units"].append({"sub": sub.group(1), "items": []})
            continue

        if job is not None and job["kind"] == "emprego":
            m = re.match(r"\*\*(.+?)\*\* \| (.+)", s)
            if m and job["role"] is None:
                job["role"], job["date"] = m.group(1), m.group(2)
                continue
            if job["role"] is not None and job["meta"] is None:
                job["meta"] = links(s)
                continue
        elif job is not None and job["kind"] == "projeto":
            if s.startswith("**") and "Stack" in s:
                job["meta"] = plain(s)[plain(s).find(":") + 1:].strip()
                continue

        if sec == "FORMAÇÃO ACADÊMICA":
            if s.startswith("**") and "—" in s:
                out.append('<div class="keep"><div class="jobhead clearfix">'
                           f'<span class="title">{plain(s)}</span></div></div>')
                in_formacao_title = True
                continue
            if in_formacao_title:
                m = re.search(r"(\d{4}[ –-] \d{4}|[A-Za-zçã]+\s+\d{4}[ –-] \d{4})", s)
                if m:
                    out[-1] = out[-1].replace("</div></div>",
                                              f'<span class="date">{m.group(1)}</span></div></div>')
                    in_formacao_title = False
                continue

        if sec == "RESUMO PROFISSIONAL":
            out.append(f"<p>{rich(links(s))}</p>")
            continue

        out.append(f"<p>{rich(links(s))}</p>")

    close_job(); close_comp()
    return name, top, out


def build():
    src = pathlib.Path(MD).read_text(encoding="utf-8")
    name, top, out = parse(src.splitlines())
    html = ("<!DOCTYPE html>\n<html lang=\"pt-br\">\n<head>\n<meta charset=\"UTF-8\">\n"
            f"<title>Currículo — {name}</title>\n<style>{CSS}</style>\n</head>\n<body>\n"
            '<div class="topline">\n<h1>' + name + "</h1>\n" + "\n".join(top) +
            "\n</div>\n" + "\n".join(out) + "\n</body>\n</html>")
    HTML_OUT.parent.mkdir(parents=True, exist_ok=True)
    HTML_OUT.write_text(html, encoding="utf-8")
    return html


def make_pdf():
    cmd = [EDGE, "--headless", "--disable-gpu", "--no-first-run",
           "--no-pdf-header-footer",
           f"--user-data-dir={pathlib.Path(tempfile.gettempdir()) / 'opencode' / 'edgeprofile'}",
           f"--print-to-pdf={PDF_OUT}", f"file:///{HTML_OUT.as_posix()}"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    out = (r.stdout or "") + (r.stderr or "")
    m = re.search(r"(\d+) bytes written to file", out)
    print("edge:", (m.group(1) + " bytes") if m else out.strip()[:200])
    try:
        import pypdf
        pdf = pypdf.PdfReader(PDF_OUT)
        print("paginas:", len(pdf.pages))
    except Exception:
        pass


if __name__ == "__main__":
    build()
    make_pdf()
    print("html:", HTML_OUT)
    print("pdf :", PDF_OUT)