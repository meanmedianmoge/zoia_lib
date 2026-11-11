#!/usr/bin/env python3
import argparse
import re
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Callable, Match, Union

ROOT = Path(__file__).resolve().parent.parent

def normalize_version(raw: str) -> str:
    value = raw.strip()
    if not value:
        raise ValueError("Version cannot be empty.")
    try:
        Decimal(value)
    except InvalidOperation as exc:
        raise ValueError(f"Invalid version '{raw}'. Use a numeric value like 2.1.") from exc
    if "." not in value:
        raise ValueError(f"Invalid version '{raw}'. Include a decimal point (example: 2.1).")
    return value

def update_once(
    text: str,
    pattern: re.Pattern,
    replacement: Union[str, Callable[[Match[str]], str]],
    label: str,
) -> str:
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise RuntimeError(f"Expected exactly 1 '{label}' match, found {len(matches)}.")
    match = matches[0]
    repl = replacement(match) if callable(replacement) else replacement
    start, end = match.span()
    return text[:start] + repl + text[end:]

def update_version(new_version: str, dry_run: bool = False) -> list[str]:
    updates = [
        (
            Path("macOS/ZOIALibrarian.spec"),
            re.compile(r"(?m)^version = os\.environ\.get\('ZOIA_VERSION', '[^']+'\)$"),
            f"version = os.environ.get('ZOIA_VERSION', '{new_version}')",
            "macOS bundle version",
        ),
        (
            Path("zoia_lib/interface/ZOIALibrarian.ui"),
            re.compile(r'ZOIA Librarian - Version [0-9]+(?:\.[0-9]+)?'),
            f"ZOIA Librarian - Version {new_version}",
            "ui source title version",
        ),
        (
            Path("tools/zoia_lib_windows.spec"),
            re.compile(r"(?m)^(version[ \t]*=[ \t]*['\"])[^'\"]+(['\"][ \t]*)$"),
            f"version = '{new_version}'",
            "windows spec version",
        ),
        (
            Path("tools/zoia_lib_mac.spec"),
            re.compile(r"(?m)^(version[ \t]*=[ \t]*['\"])[^'\"]+(['\"][ \t]*)$"),
            f"version = '{new_version}'",
            "mac spec version",
        ),
        (
            Path("tools/zoia_lib_linux.spec"),
            re.compile(r"(?m)^(version[ \t]*=[ \t]*['\"])[^'\"]+(['\"][ \t]*)$"),
            f"version = '{new_version}'",
            "linux spec version",
        ),
        (
            Path("zoia_lib/backend/patch.py"),
            re.compile(r"(?m)^([ \t]*self\._version[ \t]*=[ \t]*)[0-9]+(?:\.[0-9]+)?([ \t]*)$"),
            f"self._version = {new_version}",
            "backend patch version",
        ),
        (
            Path("zoia_lib/interface/ZOIALibrarian_main.py"),
            re.compile(
                r"(?m)^([ \t]*self\._version[ \t]*=[ \t]*)(?:['\"]+)[0-9]+(?:\.[0-9]+)?(?:['\"]+)([ \t]*)$"
            ),
            f"'{new_version}'",
            "main window version",
        ),
        (
            Path("zoia_lib/interface/ZOIALibrarian.py"),
            re.compile(r'ZOIA Librarian - Version [0-9]+(?:\.[0-9]+)?'),
            f"ZOIA Librarian - Version {new_version}",
            "ui title version",
        ),
    ]

    changed = []
    for rel_path, pattern, replacement, label in updates:
        path = ROOT / rel_path
        text = path.read_text(encoding="utf-8")
        if label == "backend patch version":
            updated = update_once(
                text,
                pattern,
                lambda m, v=new_version: f"{m.group(1)}{v}{m.group(2)}",
                label,
            )
        elif label == "main window version":
            updated = update_once(
                text,
                pattern,
                lambda m, v=new_version: f"{m.group(1)}'{v}'{m.group(2)}",
                label,
            )
        elif "spec version" in label:
            updated = update_once(
                text,
                pattern,
                lambda m, v=new_version: f"{m.group(1)}{v}{m.group(2)}",
                label,
            )
        else:
            updated = update_once(text, pattern, replacement, label)
        if updated != text:
            changed.append(str(rel_path))
            if not dry_run:
                path.write_text(updated, encoding="utf-8")
    project = ROOT / "macOS/ZOIALibrarian.xcodeproj/project.pbxproj"
    text = project.read_text(encoding="utf-8")
    updated, count = re.subn(r"MARKETING_VERSION = [0-9.]+;", f"MARKETING_VERSION = {new_version};", text)
    if count != 2:
        raise RuntimeError(f"Expected 2 Xcode marketing versions, found {count}.")
    if updated != text:
        changed.append(str(project.relative_to(ROOT)))
        if not dry_run:
            project.write_text(updated, encoding="utf-8")
    return changed

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Bump app version across source and build scripts."
    )
    parser.add_argument("version", help="Version number (example: 2.1)")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print files that would change without writing them.",
    )
    args = parser.parse_args()

    try:
        version = normalize_version(args.version)
        changed = update_version(version, dry_run=args.dry_run)
    except (ValueError, RuntimeError, FileNotFoundError) as exc:
        print(f"Error: {exc}")
        return 1

    if args.dry_run:
        if changed:
            print("Would update:")
            for path in changed:
                print(f"- {path}")
        else:
            print("No changes needed.")
        return 0

    if changed:
        print("Updated:")
        for path in changed:
            print(f"- {path}")
    else:
        print("No changes needed.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
