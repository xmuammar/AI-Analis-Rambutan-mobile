"""Flask entry point used by desktop development and the Android WebView bootstrap."""

import logging
import os

from app import create_app


def run_android() -> None:
    """Run Flask on the loopback interface for the embedded Android WebView."""
    app = create_app()
    app.run(
        host="127.0.0.1",
        port=int(os.getenv("FLASK_PORT", "5000")),
        debug=False,
        threaded=True,
        use_reloader=False,
    )


def run_desktop() -> None:
    app = create_app()
    app.run(
        host=os.getenv("FLASK_HOST", "127.0.0.1"),
        port=int(os.getenv("FLASK_PORT", "5000")),
        debug=os.getenv("FLASK_DEBUG", "0") == "1",
        threaded=True,
        use_reloader=False,
    )


if __name__ == "__main__":
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
    if os.getenv("ANDROID_ARGUMENT") or os.getenv("ANDROID_PRIVATE"):
        run_android()
    else:
        run_desktop()
