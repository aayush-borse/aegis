"""Tests for the workspace verification engine."""


from aegis.verification.engine import verify_workspace


def test_verify_workspace_invalid_path() -> None:
    result = verify_workspace("nonexistent_workspace_path_12345")
    assert result.success is False
    assert result.exit_code == 2
    assert "not found" in result.stderr