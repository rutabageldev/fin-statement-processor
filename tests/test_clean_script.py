import subprocess
import shutil
import os
import stat


def test_clean_script_removes_expected_files(tmp_path):
    # Setup structure
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    clean_script = scripts_dir / "clean.sh"

    # Copy script in
    shutil.copy("scripts/clean.sh", clean_script)
    clean_script.chmod(clean_script.stat().st_mode | stat.S_IEXEC)

    # Create dummy files
    (tmp_path / ".venv").mkdir()
    (tmp_path / "__pycache__").mkdir()
    (tmp_path / ".pytest_cache").mkdir()
    (tmp_path / ".mypy_cache").mkdir()
    (tmp_path / ".coverage").write_text("dummy coverage")
    (tmp_path / "dummy.pyc").write_text("bytecode")

    # Run the cleanup script
    subprocess.run(
        ["bash", str(clean_script), "--all"],
        cwd=tmp_path,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Assert cleanup happened
    assert not (tmp_path / ".venv").exists()
    assert not (tmp_path / "__pycache__").exists()
    assert not (tmp_path / ".pytest_cache").exists()
    assert not (tmp_path / "mypy_cache").exists()
    assert not (tmp_path / ".coverage").exists()
    assert not (tmp_path / "dummy.pyc").exists()


def test_clean_script_dry_run_does_not_delete(tmp_path):
    # Setup structure
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    clean_script = scripts_dir / "clean.sh"

    # Copy script in
    shutil.copy("scripts/clean.sh", clean_script)
    clean_script.chmod(clean_script.stat().st_mode | stat.S_IEXEC)

    # Create dummy files
    (tmp_path / ".venv").mkdir()
    (tmp_path / "__pycache__").mkdir()
    (tmp_path / ".pytest_cache").mkdir()
    (tmp_path / ".mypy_cache").mkdir()
    (tmp_path / ".coverage").write_text("dummy coverage")
    (tmp_path / "dummy.pyc").write_text("bytecode")

    # Run the cleanup script
    result = subprocess.run(
        ["bash", str(clean_script), "--all", "--dry-run"],
        cwd=tmp_path,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    output_lines = result.stdout.splitlines()

    # --- Assert output includes all expected dry-run notices ---
    assert any("Would delete: .venv" in line for line in output_lines)
    assert any("__pycache__" in line for line in output_lines)
    assert any("dummy.pyc" in line for line in output_lines)
    assert any(".pytest_cache" in line for line in output_lines)
    assert any(".mypy_cache" in line for line in output_lines)
    assert any(".coverage" in line for line in output_lines)

    # Assert cleanup happened
    assert (tmp_path / ".venv").exists()
    assert (tmp_path / "__pycache__").exists()
    assert (tmp_path / ".pytest_cache").exists()
    assert (tmp_path / ".mypy_cache").exists()
    assert (tmp_path / ".coverage").exists()
    assert (tmp_path / "dummy.pyc").exists()
