import os
import sys
from pathlib import Path
import time
import argparse
import subprocess


def parse_arguments(argv):
    """Parse CLI options for nohup runner and return (opts, remainder).

    The remainder contains the target command and its arguments, possibly
    including an optional leading 'env' and environment variable assignments.
    """
    parser = argparse.ArgumentParser(
        prog="nrun",
        add_help=True,
        description="Run a command with nohup, logging, and optional PID file.",
    )
    parser.add_argument("--log-dir", default=None, help="Directory for log file. Defaults to current directory.")
    parser.add_argument(
        "--log-name",
        default="nrun_{pid}.log",
        help="Log file name or template. Supports {ts} and {pid}.",
    )
    parser.add_argument(
        "--ts-format",
        default="%Y%m%d_%H%M%S",
        help="strftime format for {ts} placeholder.",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--append", action="store_true", help="Force append to log file.")
    group.add_argument("--truncate", action="store_true", help="Force truncate log file.")
    parser.add_argument("--pid-file", default=None, help="Write background PID to this file.")
    parser.add_argument("--unbuffered", action="store_true", help="Inject PYTHONUNBUFFERED=1 unless already set.")
    parser.add_argument("--dry-run", action="store_true", help="Only print the final command without executing.")

    opts, remainder = parser.parse_known_args(argv)
    return opts, remainder


def split_env_and_command(parts):
    """Split leading env assignments and return (env_parts, command_parts).

    Accept and ignore a literal leading 'env'. Also ignore a literal leading
    'nohup' if present in user input to avoid duplication.
    """
    env_parts = []
    command_parts = []
    idx = 0
    if not parts:
        return env_parts, command_parts

    # Skip literal 'env' or 'nohup' if user provided
    while idx < len(parts) and parts[idx] in ("env", "nohup"):
        idx += 1

    # Collect KEY=VALUE assignments
    while idx < len(parts):
        token = parts[idx]
        if "=" in token and token.split("=", 1)[0].replace("_", "").isalnum():
            env_parts.append(token)
            idx += 1
        else:
            break

    if idx < len(parts):
        command_parts = parts[idx:]
    return env_parts, command_parts


def build_command(env_parts, command_parts, log_path, redirect_operator, inject_unbuffered):
    """Construct the shell command string with nohup, logging, and PID echo."""
    env_to_use = list(env_parts)
    if inject_unbuffered:
        has_unbuffered = any(p.startswith("PYTHONUNBUFFERED=") for p in env_to_use)
        if not has_unbuffered:
            env_to_use.append("PYTHONUNBUFFERED=1")
    prefix = " ".join(env_to_use + ["nohup"]) if env_to_use else "nohup"
    core_cmd = " ".join(command_parts)
    # '&' backgrounds the process; echo $! returns the PID of the last backgrounded process
    final_inner = f"{prefix} {core_cmd}{redirect_operator}{log_path} 2>&1 & echo $!"
    return final_inner


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: nrun [--options] [env VAR=VAL ...] cmd [args...]")
        sys.exit(1)

    # parse options and remainder
    opts, remainder = parse_arguments(sys.argv[1:])

    # working directory and time/pid
    current_path = Path.cwd()
    print("Current path: ", current_path)
    now_ts = time.strftime(opts.ts_format, time.localtime())
    self_pid = str(os.getpid())

    # split env and command parts
    env_parts, command_parts = split_env_and_command(remainder)
    if not command_parts:
        print("Error: no command provided.")
        sys.exit(2)

    # determine log directory and name
    log_dir = Path(opts.log_dir) if opts.log_dir else current_path
    try:
        os.makedirs(log_dir, exist_ok=True)
    except Exception as exc:
        print("Failed to create log directory:", log_dir, "error:", exc)
        sys.exit(3)

    log_name_template = opts.log_name or "nrun_{pid}.log"
    log_name = log_name_template.replace("{ts}", now_ts).replace("{pid}", self_pid)
    log_path = str(log_dir / log_name)

    # choose redirect operator
    if opts.truncate:
        redirect_operator = " > "
    elif opts.append:
        redirect_operator = " >> "
    else:
        redirect_operator = " >> " if os.path.exists(log_path) else " > "

    # build inner command to run in a shell
    inner_cmd = build_command(
        env_parts=env_parts,
        command_parts=command_parts,
        log_path=log_path,
        redirect_operator=redirect_operator,
        inject_unbuffered=opts.unbuffered,
    )

    print("Command line:", inner_cmd)

    if opts.dry_run:
        sys.exit(0)

    # execute using bash -c to capture $! and fetch PID
    try:
        completed = subprocess.run(["bash", "-c", inner_cmd], capture_output=True, text=True, check=True)
        bg_pid = completed.stdout.strip().splitlines()[-1] if completed.stdout else ""
    except subprocess.CalledProcessError as exc:
        print("Failed to launch command. Return code:", exc.returncode)
        if exc.stderr:
            print(exc.stderr)
        sys.exit(exc.returncode or 1)

    if bg_pid:
        print("Background PID:", bg_pid)
        if opts.pid_file:
            try:
                with open(opts.pid_file, "w", encoding="utf-8") as f:
                    f.write(bg_pid + "\n")
                print("PID written to:", opts.pid_file)
            except Exception as exc:
                print("Failed to write PID file:", opts.pid_file, "error:", exc)
                # do not fail the run due to PID file write error
    else:
        print("Warning: could not determine background PID.")

    sys.exit(0)
