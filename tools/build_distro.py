#!/usr/bin/env python3
import argparse
import re
import shutil
from pathlib import Path

FROM_RE = re.compile(r"^(\s*)from\s+zoia_lib\.([^\s]+)\s+import\s+([^#]+?)(\s*#.*)?$")
IMPORT_RE = re.compile(r"^(\s*)import\s+zoia_lib\.([^\s#]+)(\s+as\s+[^\s#]+)?(\s*#.*)?$")
TOP_MODULES = {"backend", "interface", "common"}


def rewrite_imports(text):
    lines = []
    for line in text.splitlines(keepends=True):
        line_end = "\n" if line.endswith("\n") else ""
        raw_line = line[:-1] if line_end else line

        from_match = FROM_RE.match(raw_line)
        if from_match:
            indent, module_path, imports, comment = from_match.groups()
            comment = comment or ""
            if module_path in TOP_MODULES:
                new_line = f"{indent}import {imports.strip()}{comment}"
            else:
                last = module_path.split(".")[-1]
                new_line = f"{indent}from {last} import {imports.strip()}{comment}"
            lines.append(new_line + line_end)
            continue

        import_match = IMPORT_RE.match(raw_line)
        if import_match:
            indent, module_path, alias, comment = import_match.groups()
            comment = comment or ""
            alias = alias or ""
            last = module_path.split(".")[-1]
            new_line = f"{indent}import {last}{alias}{comment}"
            lines.append(new_line + line_end)
            continue

        lines.append(line)

    return "".join(lines)


def rewrite_meipass_default(text):
    return re.sub(
        r"def\s+meipass\(resource,\s*is_ui=False\):",
        "def meipass(resource, is_ui=True):",
        text,
        count=1,
    )


def iter_sources(src_root, project_root):
    py_sources = []
    for subdir in ("backend", "interface", "common"):
        py_sources.extend((src_root / subdir).rglob("*.py"))

    ui_assets = list((src_root / "interface" / "resources").iterdir())
    ui_files = [src_root / "interface" / "ZOIALibrarian.ui"]
    schema_files = list((src_root / "common" / "schemas").glob("*.json"))
    doc_html_files = list((project_root / "documentation" / "resources").glob("*.html"))
    requirements_file = project_root / "requirements.txt"

    return (
        py_sources,
        ui_assets,
        ui_files,
        schema_files,
        doc_html_files,
        requirements_file,
    )


def copy_file(src_path, dest_dir, rewrite_python=False, adjust_meipass=False):
    dest_path = dest_dir / src_path.name
    if rewrite_python:
        text = src_path.read_text(encoding="utf-8")
        text = rewrite_imports(text)
        if adjust_meipass:
            text = rewrite_meipass_default(text)
        dest_path.write_text(text, encoding="utf-8")
    else:
        shutil.copy2(src_path, dest_path)


def build_distro(src_root, dest_root, project_root):
    (
        py_sources,
        ui_assets,
        ui_files,
        schema_files,
        doc_html_files,
        requirements_file,
    ) = iter_sources(src_root, project_root)
    dest_root.mkdir(parents=True, exist_ok=True)

    for py_path in py_sources:
        adjust_meipass = py_path.name == "utilities.py"
        copy_file(py_path, dest_root, rewrite_python=True, adjust_meipass=adjust_meipass)

    for asset_path in ui_assets:
        if asset_path.is_file():
            copy_file(asset_path, dest_root)

    for ui_path in ui_files:
        if ui_path.exists():
            copy_file(ui_path, dest_root)

    for schema_path in schema_files:
        copy_file(schema_path, dest_root)

    for doc_path in doc_html_files:
        copy_file(doc_path, dest_root)

    if requirements_file.exists():
        copy_file(requirements_file, dest_root)


def main():
    parser = argparse.ArgumentParser(
        description="Flatten zoia_lib into a distro directory with adjusted imports."
    )
    parser.add_argument(
        "--source",
        default="zoia_lib",
        help="Source directory containing the zoia_lib package.",
    )
    parser.add_argument(
        "--dest",
        default="distro",
        help="Destination directory for flattened distro files.",
    )
    args = parser.parse_args()

    src_root = Path(args.source).resolve()
    dest_root = Path(args.dest).resolve()

    if not src_root.exists():
        raise SystemExit(f"Source directory not found: {src_root}")

    build_distro(src_root, dest_root, project_root=Path(__file__).resolve().parent.parent)


if __name__ == "__main__":
    main()
