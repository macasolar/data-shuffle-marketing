"""The checker, checked: one fixture with a known problem of each kind, and a
clean piece that has to come back clean (or the checker is just noisy).
Ported from the --self-test of the old Node checker.
"""

import re
from pathlib import Path

import pytest

from ds.check import EM_DASH, check_piece, pieces


@pytest.fixture
def root(tmp_path: Path) -> Path:
    (tmp_path / "content" / "2026-11").mkdir(parents=True)
    (tmp_path / "facts").mkdir()
    (tmp_path / "facts" / "services.md").write_text("# ok\n")
    return tmp_path


BAD = f"""---
id: otro-id
fecha_publicacion: 2026-11-03 08:00
redes: [linkedin, tiktok]
formato: imagen
pilar: inventado
origen: post
plantilla: linkedin
estado: draft
fuentes: [facts/services.md, facts/no-existe.md]
---
Un guion largo {EM_DASH} aqui.
```json
{{ "kicker": "Datos", "titulo": "Un titulo con muchisimas palabras que no cabe de ninguna manera en el lienzo fijo", "cuerpo": "corto", "cta": "Escribenos" }}
```
"""

GOOD = """---
id: 2026-11-04-li-bien
fecha_publicacion: 2026-11-04 08:00
redes: [linkedin]
formato: imagen
pilar: datos
origen: facts
plantilla: linkedin
imagen: [output/x.png]
estado: draft
fuentes: [facts/services.md]
---
```json
{ "kicker": "Datos", "titulo": "Cuatro areas y ningun numero que cuadre", "cuerpo": "El cierre de mes se vuelve una negociacion entre versiones.", "cta": "Diagnostico gratis" }
```
"""


@pytest.mark.parametrize(
    "pattern",
    [
        r"em dash",
        r'`id` is "otro-id"',
        r'pilar: "inventado"',
        r'redes: "tiktok"',
        r"no `articulo`",
        r"no-existe\.md does not exist",
        r"`titulo` has \d+ words",
    ],
)
def test_bad_piece_is_caught(root: Path, pattern: str) -> None:
    bad = root / "content" / "2026-11" / "2026-11-03-li-mal.md"
    bad.write_text(BAD)
    problems = check_piece(bad, root)
    assert any(re.search(pattern, p) for p in problems), problems


def test_clean_piece_is_clean(root: Path) -> None:
    good = root / "content" / "2026-11" / "2026-11-04-li-bien.md"
    good.write_text(GOOD)
    assert check_piece(good, root) == []


def test_ready_piece_needs_sources_and_instagram_image(root: Path) -> None:
    f = root / "content" / "2026-11" / "2026-11-05-ig-x.md"
    f.write_text(
        "---\nid: 2026-11-05-ig-x\nfecha_publicacion: 2026-11-05\n"
        "redes: [instagram]\nformato: imagen\npilar: datos\norigen: facts\n"
        "estado: review\n---\n"
    )
    problems = check_piece(f, root)
    assert any("`fuentes` is empty" in p for p in problems)
    assert any("Instagram needs an image" in p for p in problems)


def test_broken_frontmatter_is_reported_not_raised(root: Path) -> None:
    f = root / "content" / "2026-11" / "x.md"
    f.write_text("---\nid: [unclosed\n---\n")
    assert check_piece(f, root)[0].startswith("frontmatter will not parse")


def test_plan_and_templates_are_not_pieces(root: Path) -> None:
    month = root / "content" / "2026-11"
    (month / "plan.md").write_text("# plan\n")
    (month / "2026-11-04-li-bien.md").write_text(GOOD)
    (root / "content" / "_templates").mkdir()
    (root / "content" / "_templates" / "post.md").write_text("x")
    assert [p.name for p in pieces(root)] == ["2026-11-04-li-bien.md"]
