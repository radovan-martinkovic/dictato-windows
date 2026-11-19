#!/usr/bin/env python3
"""Prevedie slovensky model KInIT (parakeet-tdt-0.6b-v3-sk, .nemo) do GGUF,
ktory nacita Handy (transcribe.cpp).

Pouzitie:
    python convert_sk.py <transcribe.cpp root> <cesta k .nemo> <vystupny priecinok>

Model je doladena verzia nvidia/parakeet-tdt-0.6b-v3 (rovnaka architektura
aj tokenizer), takze staci prevzat profil v3 z prevodnika transcribe.cpp
a pridat ho pod novym nazvom.
"""
import importlib.util
import sys
from pathlib import Path

SLUG = "parakeet-tdt-0.6b-v3-sk"
REPO_ID = "kinit/parakeet-tdt-0.6b-v3-sk"


def main() -> int:
    if len(sys.argv) != 4:
        print(__doc__, file=sys.stderr)
        return 2
    tc_root = Path(sys.argv[1]).resolve()
    nemo_path = Path(sys.argv[2]).resolve()
    out_root = Path(sys.argv[3]).resolve()

    script = tc_root / "scripts" / "convert-parakeet.py"
    sys.path.insert(0, str(script.parent))
    spec = importlib.util.spec_from_file_location("convert_parakeet", script)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    profile = dict(mod.VARIANT_PROFILES["parakeet-tdt-0.6b-v3"])
    profile.update(
        variant="tdt-0.6b-v3-sk",
        display_name="Parakeet TDT 0.6B v3 Slovak (KInIT)",
        author="KInIT",
        organization="kinit",
        # Cita .nemo priamo, bez instalacie NeMo.
        prefer_direct_load=True,
    )
    mod.VARIANT_PROFILES[SLUG] = profile

    out_path = out_root / SLUG / f"{SLUG}-F32.gguf"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    mod.convert(str(nemo_path), out_path, repo_id=REPO_ID, revision=None)
    print(f"OK: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
