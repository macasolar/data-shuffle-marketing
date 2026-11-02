"""The pre-commit hook, run for real in a throwaway git repo."""

import shutil
import subprocess
from pathlib import Path

import pytest

from ds.config import REPO

HOOK = REPO / ".githooks" / "pre-commit"


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=True, capture_output=True, text=True
    ).stdout


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.email", "t@t")
    git(tmp_path, "config", "user.name", "t")
    hooks = tmp_path / ".githooks"
    hooks.mkdir()
    shutil.copy(HOOK, hooks / "pre-commit")
    git(tmp_path, "config", "core.hooksPath", ".githooks")
    (tmp_path / "version.txt").write_text("0.2.9\n")
    git(tmp_path, "add", "-A")
    return tmp_path


def test_each_commit_bumps_and_carries_the_version(repo: Path) -> None:
    git(repo, "commit", "-q", "-m", "one")
    assert git(repo, "show", "HEAD:version.txt") == "0.2.10\n"
    (repo / "a").write_text("x")
    git(repo, "add", "a")
    git(repo, "commit", "-q", "-m", "two")
    assert git(repo, "show", "HEAD:version.txt") == "0.2.11\n"
    assert git(repo, "status", "--porcelain") == ""


def test_a_bad_version_blocks_the_commit(repo: Path) -> None:
    (repo / "version.txt").write_text("next\n")
    git(repo, "add", "version.txt")
    with pytest.raises(subprocess.CalledProcessError):
        git(repo, "commit", "-q", "-m", "x")


def test_version_matches_the_real_file() -> None:
    from ds.cli import version

    assert version() == (REPO / "version.txt").read_text().strip()
