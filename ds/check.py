"""Checks every piece in content/ for the things a person misses and a machine
does not. Mechanical only: it cannot tell whether a claim is true, which is
what facts/ and the post-checker agent are for.
"""

import json
import re
from pathlib import Path
from typing import Any

import yaml

from ds.config import REPO

ESTADOS = ["idea", "draft", "review", "scheduled", "published", "rejected"]
REDES = ["linkedin", "facebook", "instagram", "gbp"]
FORMATOS = ["texto", "imagen", "carrusel", "reel"]
ORIGENES = ["post", "facts", "caso"]
PILARES = [
    "software-apis-integraciones",
    "datos",
    "automatizacion",
    "linux-cloud",
    "prueba",
    "como-trabajamos",
]

# Word limits per template. The canvas is a fixed height, so a longer text
# does not wrap, it falls off the image. Kept in step with
# brand/templates/README.md by hand: two short tables that disagree are
# easier to spot than a parser that silently stops matching.
LIMITES = {
    "linkedin": {"kicker": 5, "titulo": 12, "cuerpo": 22, "cta": 7},
    "instagram": {"kicker": 5, "titulo": 10, "cuerpo": 28, "cta": 7},
    "instagram-carousel": {"titulo": 9, "cuerpo": 30, "cta": 7},
    "google": {"kicker": 5, "titulo": 10, "cuerpo": 26, "cta": 7},
}
VIDEO_TEMPLATES = ["reel-explicacion", "reel-caso"]

# Written as an escape on purpose: the character itself must not appear in
# this repo, and that includes the checker that looks for it.
EM_DASH = "\u2014"

FRONTMATTER = re.compile(r"\A---[ \t]*\n(.*?)\n---[ \t]*(?:\n|\Z)", re.S)
CAMPOS = re.compile(r"```json\s*(.*?)```", re.S)
READY = ["draft", "review", "scheduled", "published"]


def words(value: Any) -> int:
    """Words as a reader counts them, with the <b> accent markup removed."""
    return len(re.sub(r"<[^>]+>", " ", str(value)).split())


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def check_piece(file: Path, root: Path = REPO) -> list[str]:
    problems: list[str] = []
    raw = file.read_text()
    piece_id = file.stem

    if EM_DASH in raw:
        line = raw[: raw.index(EM_DASH)].count("\n") + 1
        problems.append(f"line {line}: em dash (U+2014). CLAUDE.md rule 1.")

    match = FRONTMATTER.match(raw)
    try:
        data = (yaml.safe_load(match.group(1)) if match else None) or {}
    except yaml.YAMLError as err:
        return [f"frontmatter will not parse: {err}"]
    if not isinstance(data, dict):
        return ["frontmatter is not a key: value mapping"]

    for key in ["id", "fecha_publicacion", "redes", "formato", "pilar", "origen", "estado"]:
        if data.get(key) in (None, ""):
            problems.append(f"frontmatter: `{key}` is missing")

    if data.get("id") and data["id"] != piece_id:
        problems.append(f'frontmatter: `id` is "{data["id"]}" but the file is {piece_id}.md')
    for key, allowed in [
        ("estado", ESTADOS),
        ("formato", FORMATOS),
        ("pilar", PILARES),
        ("origen", ORIGENES),
    ]:
        if data.get(key) and data[key] not in allowed:
            problems.append(f'{key}: "{data[key]}" is not one of {", ".join(allowed)}')

    redes = _as_list(data.get("redes"))
    for red in redes:
        if red not in REDES:
            problems.append(f'redes: "{red}" is not one of {", ".join(REDES)}')

    # A piece that says it comes from an article has to say which one, or the
    # run has nothing to link to and publishes a post that leads nowhere.
    if data.get("origen") == "post" and not data.get("articulo"):
        problems.append("origen is `post` but there is no `articulo` to link to")

    # Every source has to exist. A piece citing a file that was renamed is a
    # claim with no backing, which is the one thing CLAUDE.md does not allow.
    fuentes = _as_list(data.get("fuentes"))
    for fuente in fuentes:
        path = str(fuente).split("#")[0]
        if not (root / path).exists():
            problems.append(f"fuentes: {path} does not exist")

    # Anything past `draft` has to be ready to publish.
    listo = data.get("estado") in READY
    if listo and not fuentes:
        problems.append(f"estado is {data['estado']} but `fuentes` is empty")
    if (
        listo
        and "instagram" in redes
        and not _as_list(data.get("imagen"))
        and data.get("formato") != "reel"
    ):
        problems.append("Instagram needs an image and `imagen` is empty")

    # The template fields, against the canvas they have to fit in.
    campos = CAMPOS.search(raw)
    plantilla = data.get("plantilla")
    if campos and plantilla in LIMITES:
        try:
            parsed = json.loads(campos.group(1))
        except json.JSONDecodeError as err:
            problems.append(f"the template fields are not valid JSON: {err}")
            parsed = None
        if isinstance(parsed, dict):
            for campo, limite in LIMITES[plantilla].items():
                value = parsed.get(campo)
                if listo and value in (None, ""):
                    problems.append(f"template field `{campo}` is empty")
                    continue
                if value and words(value) > limite:
                    problems.append(
                        f"`{campo}` has {words(value)} words, "
                        f"the {plantilla} template takes {limite}"
                    )
    elif campos and plantilla and plantilla not in VIDEO_TEMPLATES:
        problems.append(
            f'plantilla: "{plantilla}" is not a template in brand/templates/ '
            "or brand/canva-templates.md"
        )

    return problems


def pieces(root: Path = REPO) -> list[Path]:
    """Every piece file. plan.md lives in the same folder but is not a piece."""
    content = root / "content"
    if not content.is_dir():
        return []
    return sorted(
        f
        for month in content.iterdir()
        if month.is_dir() and not month.name.startswith("_")
        for f in month.glob("*.md")
        if f.name != "plan.md"
    )
