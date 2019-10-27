from conans import python_requires

base = python_requires("KF5BuildBase/0.2.0@r1tschy/stable")


class KCoreAddonsConanFile(base.get_conanfile()):
    name = "KF5CoreAddons"
    lib_name = "KCoreAddons"
    description = "Addons to QtCore"
    version = "5.36.0"
