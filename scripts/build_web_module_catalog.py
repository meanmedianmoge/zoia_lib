"""Build the browser module catalog from the desktop editor schema."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "zoia_lib/common/schemas/ModuleIndex.json"
TARGET = ROOT / "web/data/modules.json"


def main():
    source = json.loads(SOURCE.read_text())
    catalog = {}
    for module_id, module in source.items():
        blocks = []
        for name, block in module.get("blocks", {}).items():
            blocks.append({"name": name, **block})
        defaults = module.get("param_defaults", {})
        parameters = [name for name, _ in sorted(defaults.items(), key=lambda item: item[1].get("order", 0))]
        catalog[module_id] = {
            "name": module.get("name", f"Module {module_id}"),
            "category": module.get("category", "Unknown"),
            "cpu": module.get("cpu", 0),
            "description": module.get("description", "").strip(),
            "defaultBlocks": module.get("default_blocks", 1),
            "minBlocks": module.get("min_blocks", 1),
            "maxBlocks": module.get("max_blocks", module.get("default_blocks", 1)),
            "parameters": parameters,
            "parameterDefaults": {name: meta.get("value", 0) for name, meta in defaults.items()},
            "options": module.get("options", {}),
            "blocks": blocks,
        }
    TARGET.write_text(json.dumps(catalog, separators=(",", ":")) + "\n")


if __name__ == "__main__":
    main()
