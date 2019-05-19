from conans import python_requires

base = python_requires("KF5BuildBase/0.1.2@r1tschy/stable")


class KI18nConanFile(base.get_conanfile()):
    name = "KI18n"
    description = "Advanced internationalization framework"
    homepage = "https://api.kde.org/frameworks/ki18n/html/index.html"
    version = "5.36.0"
