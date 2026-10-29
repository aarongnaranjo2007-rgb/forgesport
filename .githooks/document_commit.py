"""Documenta commits y mantiene docs/ al día con Gemini."""
import datetime
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite")
MAX_DIFF = 40000
MAX_SOURCE = 60000
DOCS = {
    "project-overview": "visión general del proyecto, propósito, stack y arquitectura",
    "scope": "funcionalidades incluidas y excluidas del MVP",
    "cart-strategy": "reglas y comportamiento del carrito",
}
COMMIT_PROMPT = """Documenta el siguiente commit para el changelog de un proyecto.
Devuelve solo Markdown, sin bloques de código ni títulos, con exactamente estas viñetas:
- **Qué cambió:** una o dos frases.
- **Por qué:** el objetivo del cambio; si el diff no lo aclara escribe "no especificado".
- **Archivos:** los archivos tocados, separados por comas.
- **Impacto:** qué nota el usuario o qué se rompe si se revierte.
Escribe en español y no inventes nada que no esté en el diff.

Commit: {subject}

Diff:
{diff}"""
DOCS_PROMPT = """Actualiza la documentación de este repositorio para que describa el estado actual del código.

Devuelve SOLO un objeto JSON válido, sin bloques de código, con estas claves y como valor el Markdown completo de cada documento:
{keys}

Reglas:
- Español, conciso, sin relleno.
- No inventes: si algo no aparece en el código, el README o la documentación actual, no lo incluyas.
- Conserva el front matter y el título H1 de cada documento.
- Conserva lo que siga siendo correcto; reescribe solo lo que esté desactualizado.

README:
{readme}

Archivos:
{tree}

Código:
{source}

Documentación actual:
{current}"""


def insert_section(md, section, heading):
    """Mete la sección justo debajo del título del archivo."""
    i = md.find(heading)
    if i == -1:
        return md.rstrip() + "\n\n" + heading + "\n\n" + section + "\n"
    end = i + len(heading)
    rest = md[end:].strip("\n")
    body = section + ("\n\n" + rest if rest else "")
    return md[:end] + "\n\n" + body + "\n"


def target(root):
    """Archivo del año en curso, creado con su cabecera si aún no existe."""
    year = datetime.date.today().year
    path = os.path.join(root, "docs", "changelog", f"{year}.md")
    heading = f"# Changelog {year}"
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(f"---\ntitle: Changelog {year}\n---\n{heading}\n")
    return path, heading


def gemini(prompt, max_tokens=1024):
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        sys.exit("falta la variable GEMINI_API_KEY")
    body = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": max_tokens},
    }
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": key},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as res:
            data = json.load(res)
    except urllib.error.HTTPError as e:
        sys.exit(f"Gemini respondió {e.code}: {e.read().decode(errors='replace')[:300]}")
    return "".join(p.get("text", "") for p in data["candidates"][0]["content"]["parts"])


def unfence(text):
    return re.sub(r"^```\w*\n|```$", "", text.strip(), flags=re.M).strip()


def document_commit(root, sha, subject, diff_path):
    path, heading = target(root)
    with open(diff_path, encoding="utf-8", errors="replace") as f:
        diff = f.read()
    text = unfence(gemini(COMMIT_PROMPT.format(subject=subject, diff=diff[:MAX_DIFF])))
    section = f"## {subject} (`{sha}`)\n{text}"
    with open(path, encoding="utf-8") as f:
        md = f.read()
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(insert_section(md, section, heading))


def sync_docs(root):
    """Reescribe los documentos del proyecto según el código actual."""
    paths = subprocess.run(["git", "-C", root, "ls-files"], capture_output=True, text=True, encoding="utf-8").stdout.splitlines()
    read = lambda p: open(os.path.join(root, p), encoding="utf-8").read() if os.path.exists(os.path.join(root, p)) else ""
    source, total = [], 0
    for p in paths:
        if not p.endswith((".js", ".jsx", ".ts", ".tsx", ".json", ".css", ".html")) or p.startswith("docs/") or "node_modules" in p:
            continue
        try:
            text = read(p)
        except UnicodeDecodeError:
            continue
        if total + len(text) > MAX_SOURCE:
            break
        source.append(f"### {p}\n{text}")
        total += len(text)
    current = "\n\n".join(f"### docs/{k}.md\n{v}" for k, v in ((k, read(f"docs/{k}.md")) for k in DOCS) if v)
    keys = "\n".join(f'- "{k}": {v}' for k, v in DOCS.items())
    raw = unfence(gemini(DOCS_PROMPT.format(keys=keys, readme=read("README.md"), tree="\n".join(paths), source="\n\n".join(source), current=current), max_tokens=6000))
    try:
        docs = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit("Gemini no devolvió JSON válido")
    changed = False
    for name in DOCS:
        text = docs.get(name)
        path = os.path.join(root, "docs", f"{name}.md")
        if not isinstance(text, str) or not text.strip() or text == read(f"docs/{name}.md"):
            continue
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text.strip() + "\n")
        changed = True
    return changed


def self_test():
    md = "---\ntitle: Changelog 2026\n---\n# Changelog 2026\n\nIntro.\n"
    out = insert_section(md, "## x (`abc`)\n- **Qué cambió:** y", "# Changelog 2026")
    assert out == "---\ntitle: Changelog 2026\n---\n# Changelog 2026\n\n## x (`abc`)\n- **Qué cambió:** y\n\nIntro.\n", out
    assert insert_section("", "s", "# Changelog 2026") == "\n\n# Changelog 2026\n\ns\n"
    assert unfence("```md\nhola\n```") == "hola"
    assert json.loads(unfence('```json\n{"a": "b"}\n```')) == {"a": "b"}


if __name__ == "__main__":
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if sys.argv[1:] == ["--self-test"]:
        self_test()
        print("ok")
    elif sys.argv[1] == "commit":
        document_commit(root, *sys.argv[2:5])
    elif sys.argv[1] == "docs":
        sync_docs(root)
    else:
        sys.exit("uso: document_commit.py commit <sha> <subject> <diff> | docs | --self-test")
