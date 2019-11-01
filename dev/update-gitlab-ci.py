#!/usr/bin/env python3

from pathlib import Path
import sys
import textwrap


JOBS = {
    "extra-cmake-modules": {
      "archs": ["i486"]
    },
    "kcoreaddons": {
      "stage": "KF5 Tier 1",
      "deps": ["pkgconfig(Qt5Test)"]
    },
    "ki18n": {
      "stage": "KF5 Tier 1",
      "deps": [
        "pkgconfig(Qt5Test)",
        "pkgconfig(Qt5Script)",
        "gettext-devel",
      ]
    },
    "kconfig": {
      "stage": "KF5 Tier 1",
      "deps": ["pkgconfig(Qt5Test)"]
    },
    "libssh": {
      "deps": ["pkgconfig(openssl)"]
    },
    "qca": {
      "deps": ["git", "pkgconfig(Qt5Core)", "pkgconfig(openssl)"]
    },
}

DEFAULT_ARCHS = ["armv7hl", "i486"]

MAGIC = "\n# -- JOBS --\n"

TEMPLATE = """
{name} {arch}:
  stage: "{stage}"
  image: "r1tschy/sailfishos-platform-sdk:$ARCH"
  variables:
    ARCH: "{arch}"
    EXTRA_DEPS: "{requirements}"
  script:
    - "dev/buildenv $ARCH python ci_build.py {name}"
  only:
    changes:
      - "{name}/**/*"
"""


def main():
    gitlab_ci_path = Path(__file__).parent.parent / ".gitlab-ci.yml"

    with open(gitlab_ci_path, "r", encoding="utf-8") as fp:
        content = fp.read()

    try:
        start = content.index(MAGIC)
    except ValueError:
        print("Magic sequence missing", file=sys.stderr)
        sys.exit(1)

    content = content[: start + len(MAGIC)]

    template = textwrap.dedent(TEMPLATE.strip())

    jobs = "\n\n".join(
        [
            template.format(
              name=name, 
              requirements=" ".join(infos.get("deps", ())),
              arch=arch,
              stage=infos.get("stage", "no deps"))
            for name, infos in JOBS.items()
            for arch in infos.get("archs", DEFAULT_ARCHS)
        ]
    )

    with open(gitlab_ci_path, "w", encoding="utf-8") as fp:
        fp.write(content + jobs)


if __name__ == "__main__":
    main()
