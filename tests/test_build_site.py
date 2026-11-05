from app.build_site import build_info, render


def test_build_info_uses_github_env(monkeypatch):
    monkeypatch.setenv("GITHUB_SHA", "abcdef1234567890")
    monkeypatch.setenv("GITHUB_RUN_NUMBER", "42")
    info = build_info()
    assert info["commit"] == "abcdef1"
    assert info["run_number"] == "42"


def test_build_info_local_fallback(monkeypatch):
    monkeypatch.delenv("GITHUB_SHA", raising=False)
    assert build_info()["commit"] == "local"


def test_render_contains_info():
    page = render({"commit": "abc1234"})
    assert "abc1234" in page
    assert "<!doctype html>" in page
