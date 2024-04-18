from .command import run_command


def test_run_command():
    # Run a command that should return 0
    exit_code, stdout, stderr = run_command("echo hello")
    assert exit_code == 0
    assert stdout == "hello\n"
    assert stderr == ""

    # Run a command that should return 1
    exit_code, stdout, stderr = run_command("exit 1")
    assert exit_code == 1
    assert stdout == ""
    assert stderr == ""
