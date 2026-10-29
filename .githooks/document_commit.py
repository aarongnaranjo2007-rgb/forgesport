"""Añade a docs/changelog/<año>.md la documentación de un commit, generada con Gemini."""
import datetime
import json
import os
import re
import sys
import urllib.error
import urllib.request

MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite")
MAX_DIFF = 40000
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
    else:
        sys.exit("uso: document_commit.py commit <sha> <subject> <diff> | --self-test")
