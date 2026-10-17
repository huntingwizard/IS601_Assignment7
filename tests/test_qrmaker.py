import sys
import runpy
import pytest
import main

VALID_URL = "https://github.com/huntingwizard/IS601_Assignment7"


def test_valid_url():
    assert main.is_valid_url(VALID_URL)


def test_invalid_url():
    assert not main.is_valid_url("not-a-url")


def test_generate_qr_code_creates_file(tmp_path):
    out = tmp_path / "qr.png"
    main.generate_qr_code(VALID_URL, out)
    assert out.exists()


def test_setup_logging_runs():
    main.setup_logging() 


def test_create_directory_success(tmp_path):
    new_dir = tmp_path / "a" / "b"
    main.create_directory(new_dir)
    assert new_dir.is_dir()


def test_create_directory_failure_exits(tmp_path):
    bad = tmp_path / "not_a_dir"
    bad.write_text("x")
    with pytest.raises(SystemExit) as exc:
        main.create_directory(bad)
    assert exc.value.code == 1


def test_generate_qr_code_invalid_url_creates_nothing(tmp_path):
    out = tmp_path / "qr.png"
    main.generate_qr_code("not-a-url", out)
    assert not out.exists()


def test_generate_qr_code_handles_exception(tmp_path, monkeypatch, caplog):
    def boom(*args, **kwargs):
        raise RuntimeError("boom")

    monkeypatch.setattr(main.qrcode, "QRCode", boom)
    out = tmp_path / "qr.png"
    main.generate_qr_code(VALID_URL, out)
    assert not out.exists()
    assert "An error occurred" in caplog.text


def test_main_creates_qr_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["main.py", "--url", VALID_URL])
    main.main()
    files = list((tmp_path / main.QR_DIRECTORY).glob("QRCode_*.png"))
    assert len(files) == 1


def test_main_as_script(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["main.py", "--url", VALID_URL])
    runpy.run_module("main", run_name="__main__")
    assert list((tmp_path / main.QR_DIRECTORY).glob("QRCode_*.png"))