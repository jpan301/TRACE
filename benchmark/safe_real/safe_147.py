# source: SentrySafe / src/sentry/preprod/snapshots/image_diff/odiff.py
# function: _find_odiff_binary

def _find_odiff_binary() -> str:
    suffix = ODIFF_PLATFORM_SUFFIXES.get((platform.machine(), platform.system()))

    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "pyproject.toml").exists():
            if suffix:
                raw = parent / "node_modules" / "odiff-bin" / "raw_binaries" / f"odiff-{suffix}"
                if raw.exists():
                    return str(raw)
            break

    found = shutil.which("odiff")
    if found:
        return found
    raise FileNotFoundError("odiff binary not found. Run 'pnpm install' to install odiff-bin.")