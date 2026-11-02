"""The renderer against real Chrome. Skipped where there is no Chrome."""

import json
import shutil
import struct
from pathlib import Path

import pytest

from ds import render


def png_size(path: Path) -> tuple[int, int]:
    width, height = struct.unpack(">II", path.read_bytes()[16:24])
    return width, height


def test_missing_field_stops_the_render() -> None:
    with pytest.raises(render.RenderError, match="titulo"):
        render.fill("<h1>{{titulo}}</h1><p>{{cuerpo}}</p>", {"cuerpo": "x"}, "linkedin")


@pytest.mark.skipif(
    not (
        shutil.which("convert")
        and any(shutil.which(c) for c in ("google-chrome", "chromium", "chromium-browser"))
    ),
    reason="needs Chrome and ImageMagick",
)
def test_linkedin_renders_at_canvas_size(tmp_path: Path) -> None:
    data = tmp_path / "d.json"
    data.write_text(
        json.dumps(
            {
                "kicker": "Datos",
                "titulo": "Cuatro <b>areas</b>",
                "cuerpo": "Texto de prueba.",
                "cta": "Escribenos",
            }
        )
    )
    out = tmp_path / "out.png"
    render.render("linkedin", data, out)
    assert png_size(out) == (1200, 627)
    assert not list(render.TEMPLATES.glob("_render-*.html"))
