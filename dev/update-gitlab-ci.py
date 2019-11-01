#!/usr/bin/env python3

from pathlib import Path
import sys
import textwrap

ANY_JOBS = {
    "extra-cmake-modules": [],
}

JOBS = {
    "kcoreaddons": ["pkgconfig(Qt5Test)"],
    "ki18n": [
        "pkgconfig(Qt5Test)",
        "pkgconfig(Qt5Script)",
        "gettext-devel",
    ],
    "libssh": ["pkgconfig(openssl)"],
    "kconfig": ["pkgconfig(Qt5Test)"],
    "qca": ["git", "pkgconfig(Qt5Core)", "pkgconfig(openssl)"],
}

MAGIC = "\n# -- JOBS --\n"

ANY_TEMPLATE = """
{name}:
  image: "r1tschy/sailfishos-platform-sdk:$ARCH"
  variables:
    ARCH: "i486"
    EXTRA_DEPS: "{requirements}"
  script:
    - "dev/buildenv $ARCH python ci_build.py {name}"
  only:
    changes:
      - "{name}/**/*"
"""

TEMPLATE = """
{name} armv7hl:
  image: "r1tschy/sailfishos-platform-sdk:$ARCH"
  variables:
    ARCH: "armv7hl"
    EXTRA_DEPS: "{requirements}"
  script:
    - "dev/buildenv $ARCH python ci_build.py {name}"
  only:
    changes:
      - "{name}/**/*"

{name} i486:
  image: "r1tschy/sailfishos-platform-sdk:$ARCH"
  variables:
    ARCH: "i486"
    EXTRA_DEPS: "{requirements}"
  script:
    - "dev/buildenv $ARCH python ci_build.py {name}"
  only:
    changes:
      - "{name}/**/*"

"""


def format_requirements(req):
    return " ".join(f"'{r}'" for r in req)


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
    any_template = textwrap.dedent(ANY_TEMPLATE.strip())

    jobs = "\n\n".join(
        [
            any_template.format(name=name, requirements=" ".join(reqs))
            for name, reqs in ANY_JOBS.items()
        ]
    )
    jobs += "\n\n" + "\n\n".join(
        [
            template.format(name=name, requirements=" ".join(reqs))
            for name, reqs in JOBS.items()
        ]
    )

    with open(gitlab_ci_path, "w", encoding="utf-8") as fp:
        fp.write(content + jobs)


if __name__ == "__main__":
    main()
