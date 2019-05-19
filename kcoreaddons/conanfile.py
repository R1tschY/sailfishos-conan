from conans import python_requires

base = python_requires("KF5BuildBase/0.1.2@r1tschy/stable")


class KCoreAddonsConanFile(base.get_conanfile()):
    name = "KCoreAddons"
    description = "Addons to QtCore"
    version = "5.36.0"
