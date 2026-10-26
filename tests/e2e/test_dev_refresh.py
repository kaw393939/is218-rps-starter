"""Saved-file browser refresh in a disposable copy of the unfinished starter."""

from pathlib import Path
from queue import Empty, Queue
import os
import re
import shutil
import subprocess
import sys
from threading import Thread

import pytest
from playwright.sync_api import Page, expect

pytestmark = pytest.mark.e2e
PROJECT = Path(__file__).resolve().parents[2]


@pytest.fixture(name="launch_game")
def fixture_launch_game(tmp_path, request):
    """Launch the actual command on an OS-assigned port, and clean up on exit."""
    for path in PROJECT.glob("*.py"):
        shutil.copy2(path, tmp_path / path.name)
    for folder in ("templates", "static"):
        shutil.copytree(PROJECT / folder, tmp_path / folder)
    output = Queue()
    arguments = getattr(request, "param", [])
    with subprocess.Popen(
        [sys.executable, "run.py", *arguments],
        cwd=tmp_path,
        env={**os.environ, "PORT": "0", "PYTHONUNBUFFERED": "1"},
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    ) as process:

        def collect_output():
            for line in process.stdout:
                output.put(line)

        Thread(target=collect_output, daemon=True).start()
        logs = []
        try:
            while True:
                try:
                    line = output.get(timeout=15)
                except Empty:
                    pytest.fail("Local game did not start:\n" + "".join(logs))
                logs.append(line)
                address = re.search(r"Running on (http://127\.0\.0\.1:\d+)", line)
                if address:
                    break
            yield tmp_path, address.group(1)
        finally:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)


def test_saved_python_template_css_and_js_refresh_browser(page: Page, launch_game):
    """Each save updates a real open page, with no manual refresh/navigation."""
    project, address = launch_game
    page.goto(address)
    page.get_by_role("button", name="Rock", exact=True).click()
    expect(page.get_by_label("This round’s choices")).to_be_visible()

    template = project / "templates" / "index.html"
    template.write_text(
        template.read_text().replace("Your next move?", "Saved template arrived"),
        encoding="utf-8",
    )
    expect(page.get_by_role("heading", name="Saved template arrived")).to_be_visible()
    expect(page.get_by_label("This round’s choices")).to_have_count(0)

    stylesheet = project / "static" / "style.css"
    with stylesheet.open("a", encoding="utf-8") as saved:
        saved.write("\nbody { background-color: rgb(1, 2, 3); }\n")
    expect(page.locator("body")).to_have_css("background-color", "rgb(1, 2, 3)")

    javascript = project / "static" / "saved.js"
    javascript.write_text(
        'document.body.dataset.savedScript = "first";', encoding="utf-8"
    )
    template.write_text(
        template.read_text().replace(
            "</head>", '<script defer src="/static/saved.js"></script></head>'
        ),
        encoding="utf-8",
    )
    expect(page.locator("body")).to_have_attribute("data-saved-script", "first")
    javascript.write_text(
        'document.body.dataset.savedScript = "changed";', encoding="utf-8"
    )
    expect(page.locator("body")).to_have_attribute("data-saved-script", "changed")

    python = project / "app.py"
    python.write_text(
        python.read_text().replace(
            "moves=MOVES,", 'moves={"rock": "PYTHON SAVE ARRIVED"},'
        ),
        encoding="utf-8",
    )
    expect(page.get_by_role("button", name="Rock", exact=True)).to_contain_text(
        "PYTHON SAVE ARRIVED", timeout=15000
    )
    expect(page.get_by_role("status")).to_contain_text("game rules not built yet")


@pytest.mark.parametrize("launch_game", [["--plain"]], indirect=True)
def test_plain_mode_omits_browser_refresh(page: Page, launch_game):
    """The optional demo mode has no polling script or development endpoint."""
    _, address = launch_game
    page.goto(address)
    expect(page.locator('script[src*="dev-refresh"]')).to_have_count(0)
    assert page.request.get(address + "/__dev__/revision").status == 404
    page.get_by_role("button", name="Paper", exact=True).click()
    expect(page.get_by_label("This round’s choices")).to_be_visible()
