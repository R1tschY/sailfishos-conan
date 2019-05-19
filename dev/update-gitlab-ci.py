#!/usr/bin/env python3

from pathlib import Path
import sys
import textwrap

MAGIC = "\n# -- JOBS --\n"
JOBS = ["kcoreaddons", "ki18n", "libssh"]
TEMPLATE = """
{name} armv7hl:
  image: "coderus/sailfishos-platform-sdk:latest"
  variables:
    ARCH: "armv7hl"
  script:
    - "dev/buildenv $ARCH python ci_build.py {name}"
  only:
    changes:
      - "{name}/**/*"

{name} i486:
  image: "coderus/sailfishos-platform-sdk:latest"
  variables:
    ARCH: "i486"
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
    jobs = "\n\n".join([template.format(name=job) for job in JOBS])

    with open(gitlab_ci_path, "w", encoding="utf-8") as fp:
        fp.write(content + jobs)


if __name__ == "__main__":
    main()
