from conans import python_requires

base = python_requires("KF5BuildBase/0.2.1@r1tschy/stable")


class KF5I18nConanFile(base.get_conanfile()):
    name = "KF5I18n"
    lib_name = "KI18n"
    description = "Advanced internationalization framework"
    homepage = "https://api.kde.org/frameworks/ki18n/html/index.html"
    version = "5.36.0"

    requires = "extra-cmake-modules/%s@r1tschy/stable" % version,
