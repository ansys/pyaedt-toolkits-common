import ctypes
import os

mono_dir = os.environ.get("MONO_DIR")

if mono_dir:
    loaded = 0
    for filename in os.listdir(mono_dir):
        # Only load .so files
        if not filename.endswith(".so"):
            continue

        fullpath = os.path.join(mono_dir, filename)

        try:
            ctypes.CDLL(fullpath, mode=ctypes.RTLD_GLOBAL)
            loaded += 1
        except OSError as e:
            print(f"WARNING: Failed to load {fullpath}: {e}")

    print(f"Successfully loaded {loaded} shared libraries from {mono_dir}")
