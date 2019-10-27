from conans import python_requires

base = python_requires("KF5BuildBase/0.2.0@r1tschy/stable")


class KF5ConfigConanFile(base.get_conanfile()):
    name = "KF5Config"
    lib_name = "KConfig"
    description = "Persistent platform-independent application settings."
    homepage = "https://api.kde.org/frameworks/kconfig/html/index.html"
    version = "5.36.0"
    options = {"shared": [True, False], "gui": [True, False]}
    default_options = {"shared": False, "gui": False}

    def package(self):
        self.copy("*", dst="include", src="install/include/KF5/%sCore" % self.lib_name)
        if self.options.gui:
            self.copy("*", dst="include", src="install/include/KF5/%sGui" % self.lib_name)
        self.copy("*.a", dst="lib", src="install/lib", keep_path=False)
        self.copy("*.so", dst="lib", src="install/lib", keep_path=False)
        self.copy("*.qm", dst="share/locale", src="install/share", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = [self.name + "Core"]
        if self.options.gui:
            self.cpp_info.libs.append(self.name + "Gui")
