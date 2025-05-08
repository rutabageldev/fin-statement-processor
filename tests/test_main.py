from src import main


def test_main_logs_all_levels(monkeypatch, caplog):
    monkeypatch.setenv("APP_NAME", "Test App")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")

    caplog.set_level("DEBUG")
    main.main()

    messages = caplog.text
    assert "Debug-level log" in messages
    assert "Info-level log" in messages
    assert "Warning-level log" in messages
    assert "Error-level log" in messages
    assert "Critical-level log" in messages
