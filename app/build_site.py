"""Build a small static web page into ./site.

The pipeline runs this in the "build" job, uploads ./site as an artifact,
and the "deploy" job publishes it to GitHub Pages. The page shows which
commit / run produced it, so you can SEE the pipeline's result live.

Run locally:  python -m app.build_site
"""

import html
import os
from datetime import datetime, timezone
from pathlib import Path

from app import __version__
from app.calculator import add, average, divide, multiply


def build_info() -> dict[str, str]:
    """Collect info from the environment variables GitHub Actions provides.

    When run locally these are missing, so we fall back to "local".
    """
    return {
        "version": __version__,
        "commit": os.environ.get("GITHUB_SHA", "local")[:7],
        "branch": os.environ.get("GITHUB_REF_NAME", "local"),
        "run_number": os.environ.get("GITHUB_RUN_NUMBER", "local"),
        "actor": os.environ.get("GITHUB_ACTOR", "you"),
        "workflow": os.environ.get("GITHUB_WORKFLOW", "local build"),
        "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
    }


def render(info: dict[str, str]) -> str:
    rows = "\n".join(
        f"<tr><th>{html.escape(k)}</th><td>{html.escape(v)}</td></tr>"
        for k, v in info.items()
    )
    demo = [
        ("add(2, 3)", add(2, 3)),
        ("multiply(4, 5)", multiply(4, 5)),
        ("divide(10, 4)", divide(10, 4)),
        ("average([1, 2, 3, 4])", average([1, 2, 3, 4])),
    ]
    demo_rows = "\n".join(f"<tr><th><code>{c}</code></th><td>{r}</td></tr>" for c, r in demo)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CI/CD Demo</title>
<style>
  body {{ font-family: system-ui, sans-serif; max-width: 640px; margin: 2rem auto;
         padding: 0 1rem; background: #0d1117; color: #e6edf3; }}
  h1 {{ color: #3fb950; }}
  table {{ border-collapse: collapse; width: 100%; margin-bottom: 2rem; }}
  th, td {{ text-align: left; padding: .5rem; border-bottom: 1px solid #30363d; }}
  th {{ color: #8b949e; font-weight: 500; width: 45%; }}
</style>
</head>
<body>
<h1>Deployed by GitHub Actions</h1>
<p>This page was built and deployed automatically by the pipeline.</p>
<h2>Build info</h2>
<table>{rows}</table>
<h2>App output (tested code)</h2>
<table>{demo_rows}</table>
</body>
</html>
"""


def main() -> None:
    out = Path("site")
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(render(build_info()), encoding="utf-8")
    print(f"Built {out / 'index.html'}")


if __name__ == "__main__":
    main()
