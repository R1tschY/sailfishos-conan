from cpt.packager import ConanMultiPackager
import subprocess


if __name__ == "__main__":
    machine = subprocess.check_output("uname -m", shell=True)
    arch, _ = machine.split("-", 1)
    if not arch:
        raise LookupError("Failed to get gcc compile arch")
    arch = arch.decode("utf-8")

    builder = ConanMultiPackager()
    builder.add(
        settings={
            "os": "Linux",
            "os_build": "Linux",
            "compiler": "gcc",
            "compiler.libcxx": "libstdc++",
            "arch": arch,
            "arch_build": arch,
            "build_type": "Release",
        },
        options={},
        env_vars={},
        build_requires={},
    )
    builder.run()
