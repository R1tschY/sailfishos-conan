#!/usr/bin/env python3

from cpt.packager import ConanMultiPackager
import subprocess
import argparse
import os
import ast

CONAN_ARCH = {"i486": "x86", "armv7l": "armv7", "armv7hl": "armv7"}


def get_reference(file_path: str):
    with open(file_path, "r", encoding="utf-8") as fp:
        content = fp.read()

    module = ast.parse(content, file_path)
    conan_file = next(
        (stmt for stmt in module.body if isinstance(stmt, ast.ClassDef)), None
    )
    if conan_file is None:
        raise RuntimeError(f"missing conan class in {file_path}")

    name = version = None
    for stmt in conan_file.body:
        if isinstance(stmt, ast.Assign):
            if any(e.id == "name" for e in stmt.targets):
                name = ast.literal_eval(stmt.value)
            if any(e.id == "version" for e in stmt.targets):
                version = ast.literal_eval(stmt.value)

    if name is None or version is None:
        raise RuntimeError(f"name or version missing in conan file {file_path}")

    return name, version


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("path", default=None)
    args = argparser.parse_args()

    arch = subprocess.check_output("uname -m", shell=True, encoding="utf-8").strip()
    if not arch:
        raise LookupError("Failed to get gcc compile arch")
    conan_arch = CONAN_ARCH.get(arch, arch)

    os.chdir(args.path)

    name, version = get_reference("conanfile.py")
    builder = ConanMultiPackager(
        remotes=[
            ("https://api.bintray.com/conan/r1tschy/sailfishos", True, "sailfishos")
        ],
        reference=f"{name}/{version}",
    )

    settings = {"arch": conan_arch, "arch_build": conan_arch, "build_type": "Release"}
    builder.add(
        settings=settings,
        options={f"{name}:shared": False}
    )
    builder.add(
        settings=settings,
        options={f"{name}:shared": True}
    )
    builder.run()


if __name__ == "__main__":
    main()
