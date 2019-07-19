#!/usr/bin/env python3

from pathlib import Path
import sys
import textwrap

MAGIC = "\n# -- JOBS --\n"
JOBS = {
    "kcoreaddons": ["extra-cmake-modules", "pkgconfig(Qt5Test)"],
    "ki18n": [
        "extra-cmake-modules",
        "pkgconfig(Qt5Test)",
        "pkgconfig(Qt5Script)",
        "gettext-devel",
    ],
    "libssh": ["pkgconfig(openssl)"],
    "kconfig": ["extra-cmake-modules", "pkgconfig(Qt5Test)"],
}
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
    jobs = "\n\n".join(
        [
            template.format(name=name, requirements=" ".join(f"{r}" for r in reqs))
            for name, reqs in JOBS.items()
        ]
    )

    with open(gitlab_ci_path, "w", encoding="utf-8") as fp:
        fp.write(content + jobs)


if __name__ == "__main__":
    main()
