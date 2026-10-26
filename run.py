"""Start the local game with saved-file browser refresh, or --plain without it."""

import argparse
import os
from pathlib import Path

from app import app
from dev import DevelopmentRequestHandler, enable_browser_refresh

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--plain",
        action="store_true",
        help="disable automatic server restart and browser refresh for a stable demo",
    )
    options = parser.parse_args()
    if not options.plain:
        enable_browser_refresh(app)
    app.run(
        host="127.0.0.1",
        port=int(os.environ.get("PORT", "5050")),
        debug=False,
        use_debugger=False,
        use_reloader=not options.plain,
        request_handler=DevelopmentRequestHandler if not options.plain else None,
        extra_files=sorted(str(path) for path in Path(__file__).parent.glob("*.py")),
    )
