import ctypes
import os

ansys_em = os.environ.get("ANSYS_EM")
mono_dir = os.environ.get("MONO_DIR")


if mono_dir and ansys_em:
    loaded = 0
    fullpath = os.path.join(ansys_em, "libEDBCWrapper.so")
    try:
        ctypes.CDLL(fullpath, mode=ctypes.RTLD_GLOBAL)
        loaded += 1
    except OSError as e:
        print(f"WARNING: Failed to load {fullpath}: {e}")

    # for filename in os.listdir(mono_dir):
    #     if not filename.endswith(".so"):
    #         continue
    #
    #     fullpath = os.path.join(mono_dir, filename)
    #
    #     try:
    #         ctypes.CDLL(fullpath, mode=ctypes.RTLD_GLOBAL)
    #         loaded += 1
    #     except OSError as e:
    #         print(f"WARNING: Failed to load {fullpath}: {e}")

    print(f"Successfully loaded {loaded} shared libraries from {mono_dir}")
