import ctypes
import os
import sys

mono_dir = os.environ.get("MONO_DIR")

if mono_dir:
    loaded = 0
    for filename in os.listdir(mono_dir):
        if not filename.endswith(".so"):
            continue
        if filename.startswith("libgdiplus"):
            print(f"Skipping {filename} (requires libcairo)")
            continue

        fullpath = os.path.join(mono_dir, filename)
        try:
            ctypes.CDLL(fullpath, mode=ctypes.RTLD_GLOBAL)
            loaded += 1
        except OSError as e:
            print(f"Failed to load {fullpath}: {e}")
            sys.exit(1)

    print(f"Successfully loaded {loaded} shared libraries from {mono_dir}")
