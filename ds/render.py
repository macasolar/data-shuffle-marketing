"""Renders one brand/templates/*.html into a PNG with headless Chrome.

Why not Canva, and why not an image model: brand/visual.md, and at more
length in the website repo's brand/README.md. Rendering from the real logo
SVG and the real font files gives the brand, not something that resembles it.

Why an HTTP server for a local file: fonts do not load over file://, so the
capture would come out in a fallback typeface.
"""

import contextlib
import json
import os
import re
import shutil
import signal
import subprocess
import tempfile
import threading
import time
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from ds.config import REPO

TEMPLATES = REPO / "brand" / "templates"
FONTS = REPO / "brand" / "fonts"

# The window is asked for taller than the canvas on purpose. Chrome's viewport
# comes out about 99px shorter than the window it is given, and because the
# templates set `overflow: hidden` the part below the viewport is never
# painted: the capture came back with the footer and half the logo missing.
# The slack is cropped off again at the end.
VIEWPORT_SLACK = 160
SIZE = re.compile(r"html,\s*body\s*{\s*width:\s*(\d+)px;\s*height:\s*(\d+)px")


class RenderError(Exception):
    pass


def chrome_binary() -> str:
    for name in (os.environ.get("CHROME_BIN"), "google-chrome", "chromium", "chromium-browser"):
        if name and shutil.which(name):
            return name
    raise RenderError("No Chrome found. Install google-chrome or chromium, or set CHROME_BIN.")


class _Handler(SimpleHTTPRequestHandler):
    """Serves the templates folder, and /fonts/ from brand/fonts.

    _base.css asks for ../fonts/*, which the browser normalises to /fonts/*.
    Without this the woff2 files 404 and the capture comes out in a fallback
    typeface, which is the whole thing this pipeline exists to avoid.
    """

    def translate_path(self, path: str) -> str:
        rel = path.split("?")[0].lstrip("/")
        base = FONTS.parent if rel.startswith("fonts/") else TEMPLATES
        target = (base / rel).resolve()
        if not any(target == d or d in target.parents for d in (TEMPLATES, FONTS)):
            return str(TEMPLATES / "__forbidden__")
        return str(target)

    def log_message(self, format: str, *args: object) -> None:
        pass


def fill(html: str, data: dict[str, object], template: str) -> str:
    """{{field}} substitution. A missing field is an error, not an empty box:
    a piece published with a blank headline is worse than a run that stops.
    """
    missing: list[str] = []

    def sub(m: re.Match[str]) -> str:
        value = data.get(m.group(1))
        if value in (None, ""):
            missing.append(m.group(1))
            return ""
        return str(value)

    out = re.sub(r"\{\{(\w+)\}\}", sub, html)
    if missing:
        raise RenderError(f"{template}: fields missing from the data: {', '.join(missing)}")
    return out


def render(template: str, data_path: Path, out_path: Path, timeout_s: float = 45) -> str:
    template = template.removesuffix(".html")
    html_path = TEMPLATES / f"{template}.html"
    if not html_path.exists():
        raise RenderError(f"No template at {html_path}")

    html = html_path.read_text()
    size = SIZE.search(html)
    if not size:
        raise RenderError(f'{template}: no "html, body {{ width: Npx; height: Npx }}" rule')
    width, height = int(size.group(1)), int(size.group(2))
    html = fill(html, json.loads(data_path.read_text()), template)

    # A killed run leaves its temp page behind, so they are swept on the way in.
    for stale in TEMPLATES.glob("_render-*.html"):
        stale.unlink(missing_ok=True)
    tmp_page = TEMPLATES / f"_render-{os.getpid()}.html"
    tmp_page.write_text(html)

    out = out_path.resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.unlink(missing_ok=True)
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(_Handler, directory=str(TEMPLATES)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    profile = tempfile.mkdtemp(prefix="ds-render-")
    try:
        args = [
            chrome_binary(),
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            "--force-device-scale-factor=1",
            f"--user-data-dir={profile}",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-sync",
            "--disable-extensions",
            "--disable-background-networking",
            "--disable-features=Translate,BackForwardCache",
            f"--window-size={width},{height + VIEWPORT_SLACK}",
            f"--screenshot={out}",
            f"http://127.0.0.1:{server.server_address[1]}/{tmp_page.name}",
        ]
        # Docker's default seccomp profile blocks Chrome's sandbox. Only local
        # templates from this repo are loaded, so the image turns it off.
        if os.environ.get("CHROME_NO_SANDBOX") == "1":
            args.insert(1, "--no-sandbox")
        # Chrome writes the file and then may stay alive trying to register for
        # push notifications, so the wait is on the file, not the process.
        chrome = subprocess.Popen(
            args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True
        )
        deadline, last = time.monotonic() + timeout_s, -1
        while time.monotonic() < deadline:
            time.sleep(0.25)
            if not out.exists():
                continue
            # Written in chunks: wait for the size to settle or the PNG is cut.
            now = out.stat().st_size
            if now > 0 and now == last:
                break
            last = now
        with contextlib.suppress(ProcessLookupError):
            os.killpg(chrome.pid, signal.SIGKILL)
        chrome.wait(timeout=10)
    finally:
        server.shutdown()
        tmp_page.unlink(missing_ok=True)
        shutil.rmtree(profile, ignore_errors=True)

    if not out.exists():
        raise RenderError("Chrome did not write the file.")
    # The slack comes back as extra height below the canvas; crop to the exact
    # size the network expects.
    try:
        subprocess.run(
            ["convert", str(out), "-crop", f"{width}x{height}+0+0", "+repage", str(out)],
            check=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as err:
        raise RenderError(
            f"ImageMagick crop failed ({err}); the capture at {out} is "
            f"{VIEWPORT_SLACK}px too tall. Install imagemagick."
        ) from err
    return f"{out_path}  {width}x{height}  ({template})"
