from cpt.packager import ConanMultiPackager
import subprocess


CONAN_ARCH = {"i486": "x86", "armv7h": "armv7", "armv7hl": "armv7"}


if __name__ == "__main__":
    arch = subprocess.check_output("uname -m", shell=True, encoding="utf-8").strip()
    if not arch:
        raise LookupError("Failed to get gcc compile arch")
    conan_arch = CONAN_ARCH[arch]

    builder = ConanMultiPackager()
    builder.add(
        settings={"arch": conan_arch, "build_type": "Release"},
        options={},
        env_vars={},
        build_requires={},
    )
    builder.run()
