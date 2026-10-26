"""Browser refresh support enabled only by the local development launcher."""

from hashlib import sha256
from pathlib import Path
from uuid import uuid4

from flask import Flask
from werkzeug.serving import WSGIRequestHandler


class DevelopmentRequestHandler(WSGIRequestHandler):
    """Keep successful refresh polls from drowning out useful terminal output."""

    def log_request(self, code="-", size="-"):
        if code == 200 and getattr(self, "path", None) == "/__dev__/revision":
            return
        super().log_request(code, size)


def enable_browser_refresh(app: Flask) -> None:
    """Refresh on asset edits or after Werkzeug restarts for Python edits."""
    project = Path(app.root_path)
    boot = uuid4().hex
    app.config.update(TEMPLATES_AUTO_RELOAD=True, SEND_FILE_MAX_AGE_DEFAULT=0)
    app.jinja_env.auto_reload = True

    def revision():
        # The boot token changes only once the new Python process is serving.
        # Asset content is checked directly, including added/deleted files.
        digest = sha256(boot.encode())
        for folder in ("templates", "static"):
            for path in sorted((project / folder).rglob("*")):
                if path.is_file() and path.suffix in {".html", ".css", ".js"}:
                    digest.update(str(path.relative_to(project)).encode())
                    digest.update(path.read_bytes())
        return digest.hexdigest()

    @app.context_processor
    def refresh_context():
        return {"dev_refresh_revision": revision()}

    @app.get("/__dev__/revision")
    def refresh_revision():
        return {"revision": revision()}

    @app.after_request
    def prevent_stale_assets(response):
        response.headers["Cache-Control"] = "no-store"
        return response
