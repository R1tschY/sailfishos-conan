from cpt.packager import ConanMultiPackager
import subprocess
import argparse
import os

CONAN_ARCH = {"i486": "x86", "armv7l": "armv7", "armv7hl": "armv7"}


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("path", default=None)
    args = argparser.parse_args()

    arch = subprocess.check_output("uname -m", shell=True, encoding="utf-8").strip()
    if not arch:
        raise LookupError("Failed to get gcc compile arch")
    conan_arch = CONAN_ARCH.get(arch, arch)

    os.chdir(args.path)

    builder = ConanMultiPackager()
    builder.add(
        settings={
            "arch": conan_arch,
            "arch_build": conan_arch,
            "build_type": "Release",
        },
        options={},
        env_vars={},
        build_requires={},
    )
    builder.run()
