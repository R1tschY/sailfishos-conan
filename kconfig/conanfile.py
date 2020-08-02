from conans import python_requires

base = python_requires("KF5BuildBase/0.2.1@r1tschy/stable")


class KF5ConfigConanFile(base.get_conanfile()):
    name = "KF5Config"
    lib_name = "KConfig"
    sub_modules = ["Core", "Gui"]
    description = "Persistent platform-independent application settings."
    homepage = "https://api.kde.org/frameworks/kconfig/html/index.html"
    version = "5.36.0"

    requires = "extra-cmake-modules/5.68.0@r1tschy/stable",

    options = {"shared": [True, False]}
    default_options = {"shared": False}