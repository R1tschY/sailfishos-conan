from conans import python_requires

base = python_requires("KF5BuildBase/0.1.2@r1tschy/stable")


class KConfigConanFile(base.get_conanfile()):
    name = "KConfig"
    description = "Persistent platform-independent application settings."
    homepage = "https://api.kde.org/frameworks/kconfig/html/index.html"
    version = "5.36.0"
    options = {"shared": [True, False], "gui": [True, False]}
    default_options = {"shared": False, "gui": False}

    def package(self):
        self.copy("*", dst="include", src="install/include/KF5/%sCore" % self.name)
        if self.options.gui:
            self.copy("*", dst="include", src="install/include/KF5/%sGui" % self.name)
        self.copy("*.a", dst="lib", src="install/lib", keep_path=False)
        self.copy("*.so", dst="lib", src="install/lib", keep_path=False)
        self.copy("*.qm", dst="share/locale", src="install/share", keep_path=False)

    def package_info(self):
        kf5name = self.name.replace("K", "KF5", 1)
        self.cpp_info.libs = [kf5name + "Core"]
        if self.options.gui:
            self.cpp_info.libs.append(kf5name + "Gui")
