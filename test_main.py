#!/usr/bin/env python3
"""Local tests for news-image-20261124 v5 (stdlib only)."""
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))


def run(cmd, cwd=None, env=None):
    e = dict(os.environ)
    if env:
        e.update(env)
    return subprocess.run(cmd, cwd=cwd, env=e, capture_output=True, text=True)


def test_atlas():
    sys.path.insert(0, ROOT)
    import importlib
    import main as m
    a = m.Atlas(os.path.join(ROOT, "atlas.bin"))
    assert "masthead" in a.fonts and "body" in a.fonts
    w = a.text_width("masthead", "Tuesday 24 November 2026")
    assert 500 < w < 976, w
    assert a.text_width("body", "") == 0
    assert a.text_width("body", "hello world") > 0
    print("atlas OK, masthead width:", w)


def test_wrap():
    sys.path.insert(0, ROOT)
    import main as m
    a = m.Atlas(os.path.join(ROOT, "atlas.bin"))
    lines = m.wrap(a, "hero", "Three tankers hit by mines in Hormuz, Guards say", 298)
    assert len(lines) == 2, lines
    assert all(a.text_width("hero", ln) <= 298 for ln in lines)
    print("wrap OK:", lines)


def test_render():
    out = os.path.join(ROOT, "entry-v5.png")
    r = run([sys.executable, "main.py"], cwd=ROOT)
    assert r.returncode == 0, r.stderr
    assert os.path.exists(out)
    size = os.path.getsize(out)
    assert size < 1048576, size
    with open(out, "rb") as f:
        head = f.read(33)
    assert head[:8] == b"\x89PNG\r\n\x1a\n"
    import struct
    w, h = struct.unpack(">II", head[16:24])
    assert (w, h) == (1024, 1024), (w, h)
    print("render OK: %d bytes, %dx%d" % (size, w, h))
    return open(out, "rb").read()


def test_determinism(data):
    h1 = hashlib.sha256(data).hexdigest()
    r = run([sys.executable, "main.py"], cwd=ROOT)
    assert r.returncode == 0
    h2 = hashlib.sha256(open(os.path.join(ROOT, "entry-v5.png"), "rb").read()).hexdigest()
    assert h1 == h2, (h1, h2)
    print("determinism OK:", h1[:16])


def test_clean_dir():
    tmp = tempfile.mkdtemp(prefix="v5-clean-")
    try:
        env = {"MAKEFUN_OUTPUT_DIR": os.path.join(tmp, "out"),
               "PATH": os.environ.get("PATH", "")}
        r = run([sys.executable, os.path.join(ROOT, "main.py")],
                cwd="/", env=env)
        assert r.returncode == 0, r.stderr
        p = os.path.join(tmp, "out", "entry.png")
        assert os.path.exists(p), "no $MAKEFUN_OUTPUT_DIR/entry.png"
        print("clean-dir OK (cwd=/, no env leak):", os.path.getsize(p), "bytes")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_no_network_imports():
    lines = open(os.path.join(ROOT, "main.py")).read().splitlines()
    imports = [ln for ln in lines
               if ln.startswith("import ") or ln.startswith("from ")]
    src = "\n".join(imports)
    for bad in ("socket", "urllib", "requests", "http", "PIL", "numpy"):
        assert bad not in src, bad
    print("no-network-imports OK:", [ln.strip() for ln in imports])


if __name__ == "__main__":
    test_atlas()
    test_wrap()
    data = test_render()
    test_determinism(data)
    test_clean_dir()
    test_no_network_imports()
    print("ALL TESTS PASSED")
