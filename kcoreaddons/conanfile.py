from conans import python_requires

base = python_requires("KF5BuildBase/0.1@sailfish/stable")


class KCoreAddonsConanFile(base.KF5ConanFileBase):
    name = "KCoreAddons"
    description = "Addons to QtCore"
    version = "5.36.0"
