#!/usr/bin/env python3
"""Create a reproducible ZIP containing only the installable Skill folder."""

from __future__ import annotations

import hashlib
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from validate_package import ROOT, SKILL, validate


def main() -> None:
    _, errors = validate()
    if errors:
        raise SystemExit("Package validation failed:\n" + "\n".join(errors))
    output = ROOT / "dist" / "paper-to-idea.zip"
    output.parent.mkdir(parents=True, exist_ok=True)
    files = sorted(path for path in SKILL.rglob("*") if path.is_file())
    with ZipFile(output, "w") as archive:
        for path in files:
            resolved = path.resolve()
            if not resolved.is_relative_to(SKILL.resolve()):
                raise SystemExit(f"Skill file escapes package directory: {path.name}")
            info = ZipInfo(path.relative_to(SKILL.parent).as_posix(), (1980, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    print(f"Built dist/{output.name}: {len(files)} files")
    print(f"SHA256 {digest}")


if __name__ == "__main__":
    main()
