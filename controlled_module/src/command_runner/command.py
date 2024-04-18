import subprocess


def run_command(command_str: str) -> tuple[int, str, str]:
    """Run a command in the shell and return the exit code, stdout, and stderr."""
    # Run the command in the shell and capture the stdout and stderr
    process = subprocess.Popen(
        command_str,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    stdout, stderr = process.communicate()
    # Get the exit code of the process
    exit_code = process.returncode
    return exit_code, stdout, stderr
