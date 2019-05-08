from cpt.packager import ConanMultiPackager
import subprocess


CONAN_ARCH = {"i486": "x86", "armv7h": "armv7", "armv7hl": "armv7"}


if __name__ == "__main__":
    arch = subprocess.check_output("uname -m", shell=True)
    if not arch:
        raise LookupError("Failed to get gcc compile arch")
    arch = arch.decode("utf-8")
    conan_arch = CONAN_ARCH.get(arch, arch)

    builder = ConanMultiPackager()
    builder.add(
        settings={"arch": conan_arch, "build_type": "Release"},
        options={},
        env_vars={},
        build_requires={},
    )
    builder.run()
