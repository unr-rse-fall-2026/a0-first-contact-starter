#!/usr/bin/env python3
"""Friendly static checks for A0; these cannot observe a live ROS graph."""

from pathlib import Path
import ast
import os
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
BLUE, GREEN, YELLOW, RED = "\033[96m", "\033[92m", "\033[93m", "\033[91m"
BOLD, RESET = "\033[1m", "\033[0m"


class CheckFailure(Exception):
    pass


def require(condition, message):
    if not condition:
        raise CheckFailure(message)


def check_python_file(name):
    path = ROOT / name
    require(path.exists(), f"I could not find {name} in the repository root.")
    source = path.read_text(encoding="utf-8")
    require(
        source.startswith("#!/usr/bin/env python3"),
        f"{name} should begin with #!/usr/bin/env python3",
    )
    require(os.access(path, os.X_OK), f"{name} is not executable. Run: chmod +x {name}")
    try:
        tree = ast.parse(source, filename=name)
    except SyntaxError as error:
        raise CheckFailure(
            f"Python could not parse {name}: line {error.lineno}: {error.msg}"
        ) from error
    return source, tree


def imports_name(tree, module, imported_name):
    return any(
        isinstance(node, ast.ImportFrom)
        and node.module == module
        and any(alias.name == imported_name for alias in node.names)
        for node in ast.walk(tree)
    )


def calls_method(tree, method_name):
    return any(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == method_name
        for node in ast.walk(tree)
    )


def assigned_numbers(tree):
    """Return simple numeric assignments such as timer_period = 0.25."""
    values = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant):
            value = node.value.value
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        values[target.id] = float(value)
        elif (
            isinstance(node, ast.AnnAssign)
            and isinstance(node.target, ast.Name)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, (int, float))
            and not isinstance(node.value.value, bool)
        ):
            values[node.target.id] = float(node.value.value)
    return values


def timer_periods(tree):
    """Find literal or simple named first arguments passed to create_timer."""
    assignments = assigned_numbers(tree)
    periods = []
    for node in ast.walk(tree):
        if not (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "create_timer"
            and node.args
        ):
            continue
        arg = node.args[0]
        if isinstance(arg, ast.Constant) and isinstance(arg.value, (int, float)):
            periods.append(float(arg.value))
        elif isinstance(arg, ast.Name) and arg.id in assignments:
            periods.append(assignments[arg.id])
    return periods


def has_text(source, required, message):
    require(required in source, message)


def status_files():
    """The two status programs exist, use Python 3, and are executable."""
    check_python_file("status_publisher.py")
    check_python_file("status_monitor.py")


def status_publisher():
    """The status publisher creates the required String topic at 4 Hz."""
    source, tree = check_python_file("status_publisher.py")
    require(
        imports_name(tree, "std_msgs.msg", "String"),
        "Import String with: from std_msgs.msg import String",
    )
    has_text(source, "status_publisher", "Use status_publisher as the ROS node name.")
    has_text(source, "/lab0/status", "Create the publisher on the exact topic /lab0/status.")
    require(calls_method(tree, "create_publisher"), "Create a publisher with self.create_publisher(...).")
    require(
        any(abs(period - 0.25) < 1e-9 for period in timer_periods(tree)),
        "A 4 Hz timer needs a 0.25-second period. The checker accepts either "
        "create_timer(0.25, ...) or a variable such as timer_period = 0.25.",
    )
    has_text(source, "System ready", "Include the exact text 'System ready' in each message.")


def status_monitor():
    """The status monitor subscribes to the same String topic."""
    source, tree = check_python_file("status_monitor.py")
    require(
        imports_name(tree, "std_msgs.msg", "String"),
        "Import String with: from std_msgs.msg import String",
    )
    has_text(source, "status_monitor", "Use status_monitor as the ROS node name.")
    has_text(source, "/lab0/status", "Subscribe to the exact topic /lab0/status.")
    require(
        calls_method(tree, "create_subscription"),
        "Create a subscription with self.create_subscription(...).",
    )


def count_pair():
    """Both extension nodes use the Int32 contract and the publisher runs at 1 Hz."""
    pub_source, pub_tree = check_python_file("count_publisher.py")
    mon_source, mon_tree = check_python_file("count_monitor.py")
    for name, source, tree in [
        ("count_publisher.py", pub_source, pub_tree),
        ("count_monitor.py", mon_source, mon_tree),
    ]:
        require(
            imports_name(tree, "std_msgs.msg", "Int32"),
            f"{name} should import Int32 with: from std_msgs.msg import Int32",
        )
        has_text(source, "/lab0/count", f"{name} should use the exact topic /lab0/count.")
    has_text(pub_source, "count_publisher", "Use count_publisher as the publisher node name.")
    require(calls_method(pub_tree, "create_publisher"), "count_publisher.py should create a publisher.")
    require(
        any(abs(period - 1.0) < 1e-9 for period in timer_periods(pub_tree)),
        "A 1 Hz timer needs a 1.0-second period. The checker accepts either "
        "create_timer(1.0, ...) or a variable such as timer_period = 1.0.",
    )
    has_text(mon_source, "count_monitor", "Use count_monitor as the monitor node name.")
    require(
        calls_method(mon_tree, "create_subscription"),
        "count_monitor.py should create a subscription.",
    )


def evidence_complete():
    """Evidence templates no longer contain unanswered bracketed prompts."""
    evidence_dir = ROOT / "evidence"
    require(evidence_dir.is_dir(), "The evidence/ directory is missing.")
    expected = ["documentation.md", "inspection.md", "reflection.md"]
    missing = [name for name in expected if not (evidence_dir / name).exists()]
    require(not missing, "Missing evidence files: " + ", ".join(missing))
    placeholders = []
    pattern = re.compile(
        r"\[(?:Your|brief note|link|command|commands|relevant output|commands and output|output of)",
        re.I,
    )
    for name in expected:
        if pattern.search((evidence_dir / name).read_text(encoding="utf-8")):
            placeholders.append(name)
    require(not placeholders, "Replace the bracketed prompts in: " + ", ".join(placeholders))


CHECKS = {
    "status-files": (
        "Standalone status files",
        "Checks that both status programs are present, use Python 3, parse, and can run with ./filename.py.",
        status_files,
    ),
    "status-publisher": (
        "Status publisher specification",
        "Checks the source choices that should create a String publisher on /lab0/status at 4 Hz.",
        status_publisher,
    ),
    "status-monitor": (
        "Status monitor specification",
        "Checks that the monitor subscribes to the same topic using the same message type.",
        status_monitor,
    ),
    "count-pair": (
        "Int32 publisher/subscriber extension",
        "Checks that both endpoints use the /lab0/count Int32 contract and that the publisher runs at 1 Hz.",
        count_pair,
    ),
    "evidence": (
        "Evidence templates",
        "Checks that the written investigation and reflection prompts have been completed.",
        evidence_complete,
    ),
}


def main():
    requested = sys.argv[1:]
    unknown = [name for name in requested if name not in CHECKS]
    if unknown:
        print(f"{RED}Unknown check: {', '.join(unknown)}{RESET}")
        print("Available checks: " + ", ".join(CHECKS))
        return 2

    selected = requested or list(CHECKS)
    failures = 0
    print(f"\n{BOLD}{BLUE}A0 assignment checks{RESET}")
    print("These checks inspect your files; they do not replace live ROS graph verification.\n")
    for key in selected:
        title, explanation, function = CHECKS[key]
        print(f"{BOLD}{BLUE}CHECK: {title}{RESET}")
        print(f"Why: {explanation}")
        try:
            function()
        except CheckFailure as error:
            failures += 1
            print(f"{RED}NOT YET: {error}{RESET}\n")
        else:
            print(f"{GREEN}PASS: This part looks ready.{RESET}\n")

    passed = len(selected) - failures
    if failures:
        print(
            f"{BOLD}{YELLOW}Summary: {passed}/{len(selected)} checks passed. "
            f"Fix one message above, then run the checker again.{RESET}"
        )
        return 1
    print(f"{BOLD}{GREEN}Summary: all {len(selected)} checks passed.{RESET}")
    print("Next: run the ROS nodes and complete the required inspection evidence.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
