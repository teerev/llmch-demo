from pretend_productivity.app import build_output


def test_build_output_smoke() -> None:
    out = build_output(2)
    assert out[0].startswith("Pretending to work hard...")

    # Per-iteration log and progress lines
    assert "[INFO] Starting task 1" in out
    assert "[INFO] Starting task 2" in out
    assert "Progress: [#####-----] 50%" in out

    # Dramatic CPU usage line after each progress line
    assert out.count("CPU Usage: 99%") == 2

    assert out[-1].endswith("All tasks complete.")
