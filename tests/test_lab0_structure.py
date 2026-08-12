from pathlib import Path
import ast
import re


ROOT = Path(__file__).parents[1]
PKG = ROOT / "lab0_first_contact"
MODULE = PKG / "lab0_first_contact"


def read(path):
    assert path.exists(), f"Missing required file: {path.relative_to(ROOT)}"
    return path.read_text(encoding="utf-8")


def test_required_package_files_exist():
    required = [
        PKG / "package.xml",
        PKG / "setup.py",
        PKG / "setup.cfg",
        PKG / "resource" / "lab0_first_contact",
        MODULE / "__init__.py",
        MODULE / "status_publisher.py",
        MODULE / "status_monitor.py",
    ]
    missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
    assert not missing, "Missing required package files: " + ", ".join(missing)


def test_python_files_parse():
    for name in ["status_publisher.py", "status_monitor.py"]:
        path = MODULE / name
        ast.parse(read(path), filename=str(path))


def test_package_metadata_names_package_and_dependencies():
    xml = read(PKG / "package.xml")
    assert re.search(r"<name>\s*lab0_first_contact\s*</name>", xml)
    for dependency in ["rclpy", "std_msgs"]:
        assert dependency in xml, f"package.xml should declare {dependency}"


def test_setup_exposes_exact_executable_names():
    setup = read(PKG / "setup.py")
    assert re.search(r"status_publisher\s*=\s*lab0_first_contact\.status_publisher:main", setup)
    assert re.search(r"status_monitor\s*=\s*lab0_first_contact\.status_monitor:main", setup)


def test_publisher_uses_required_interface_topic_and_period():
    source = read(MODULE / "status_publisher.py")
    assert "std_msgs.msg" in source and "String" in source
    assert "/lab0/status" in source
    assert re.search(r"create_timer\s*\(\s*0\.5(?:0*)?\s*,", source)
    assert "status_publisher" in source
    assert "System ready" in source


def test_monitor_uses_required_interface_and_topic():
    source = read(MODULE / "status_monitor.py")
    assert "std_msgs.msg" in source and "String" in source
    assert "/lab0/status" in source
    assert "status_monitor" in source
    assert "create_subscription" in source


def test_evidence_files_have_no_remaining_response_placeholders():
    placeholders = []
    for path in (ROOT / "evidence").glob("*.md"):
        text = path.read_text(encoding="utf-8")
        if re.search(r"\[(?:Your|brief note|link|command|commands|relevant output|output of)", text, re.I):
            placeholders.append(path.name)
    assert not placeholders, "Complete the bracketed prompts in: " + ", ".join(placeholders)


def test_build_artifacts_are_not_committed():
    found = [name for name in ["build", "install", "log"] if (ROOT / name).exists()]
    assert not found, "Do not commit workspace artifacts: " + ", ".join(found)

