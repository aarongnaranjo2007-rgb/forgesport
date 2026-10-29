"""Añade a docs/changelog.md la documentación de un commit, generada con Gemini."""
import json
import os
import re
import sys
import urllib.error
import urllib.request

MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite")
MAX_DIFF = 40000
PROMPT = """Documenta el siguiente commit para el changelog de un proyecto.
Devuelve solo Markdown, sin bloques de código ni títulos, con exactamente estas viñetas:
- **Qué cambió:** una o dos frases.
- **Por qué:** el objetivo del cambio; si el diff no lo aclara escribe "no especificado".
- **Archivos:** los archivos tocados, separados por comas.
- **Impacto:** qué nota el usuario o qué se rompe si se revierte.
Escribe en español y no inventes nada que no esté en el diff.

Commit: {subject}

Diff:
{diff}"""


def insert_section(md, section):
    """Mete la sección justo debajo de '# Changelog' (o crea el título)."""
    marker = "# Changelog"
    i = md.find(marker)
    if i == -1:
        return md.rstrip() + "\n\n# Changelog\n\n" + section + "\n"
    end = i + len(marker)
    return md[:end] + "\n\n" + section + "\n\n" + md[end:].lstrip("\n")


def generate(subject, diff):
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        sys.exit("falta la variable GEMINI_API_KEY")
    body = {
        "contents": [{"role": "user", "parts": [{"text": PROMPT.format(subject=subject, diff=diff[:MAX_DIFF])}]}],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 1024},
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
    text = "".join(p.get("text", "") for p in data["candidates"][0]["content"]["parts"])
    return re.sub(r"^```\w*\n|```$", "", text.strip(), flags=re.M).strip()


def self_test():
    md = "---\ntitle: Changelog\n---\n# Changelog\n\nIntro.\n"
    out = insert_section(md, "## x (`abc`)\n- **Qué cambió:** y")
    assert out == "---\ntitle: Changelog\n---\n# Changelog\n\n## x (`abc`)\n- **Qué cambió:** y\n\nIntro.\n", out
    assert insert_section("", "s") == "\n\n# Changelog\n\ns\n"


if __name__ == "__main__":
    if sys.argv[1:] == ["--self-test"]:
        self_test()
        print("ok")
    else:
        sha, subject, diff_path = sys.argv[1:4]
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(root, "docs", "changelog.md")
        with open(diff_path, encoding="utf-8", errors="replace") as f:
            diff = f.read()
        section = f"## {subject} (`{sha}`)\n{generate(subject, diff)}"
        with open(path, encoding="utf-8") as f:
            md = f.read()
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(insert_section(md, section))
