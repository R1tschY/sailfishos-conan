import textwrap
import os

from conans import ConanFile, tools, CMake

# TODO: select plugins from conan and build and add them in cpp_libs


class QcaConanFile(ConanFile):
    name = "Qca-qt5"
    description = "Straightforward and cross-platform crypto API, using Qt datatypes and conventions."
    version = "2.2.1"
    license = "LGPLv2.1+"

    homepage = "https://userbase.kde.org/QCA"
    url = "https://github.com/R1tschY/sailfishos-conan"

    settings = "os", "arch", "compiler", "build_type"
    generators = "cmake"

    options = {"shared": [True, False], "plugins": ["none", "all", "auto"]}
    default_options = {"shared": False, "plugins": "auto"}

    def source(self):
        self.run(
            "git clone -b 'v%s'"
            " --single-branch --depth 1"
            " https://anongit.kde.org/qca.git qca" % self.version
        )

        tools.replace_in_file(
            "qca/CMakeLists.txt",
            "project(qca)",
            textwrap.dedent(
                """
                project(qca)
                include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
                conan_basic_setup()
                """
            ),
        )

    def build(self):
        cmake = CMake(self, generator="Unix Makefiles")
        cmake.definitions.update(
            {
                "CMAKE_INSTALL_PREFIX": os.path.join(self.build_folder, "install"),
                "BUILD_TESTS": "OFF",
                "BUILD_TOOLS": "OFF",
                "BUILD_PLUGINS": self.options.plugins,
                "BUILD_SHARED_LIBS": self.options.shared,
            }
        )
        cmake.configure(source_folder="qca")
        cmake.build()
        cmake.build(target="install")

    def package(self):
        self.copy("*", dst="include", src="install/include/Qca-qt5/QtCrypto")
        self.copy("*.a", dst="lib", src="install/lib", keep_path=False)
        self.copy("*.so", dst="lib", src="install/lib", keep_path=False)
        self.copy("*.qm", dst="share/locale", src="install/share", keep_path=False)
        self.copy("*.cmake", dst="share", src="install/share", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = [
            "qca-ossl", "ssl", "crypto", "qca-qt5"
        ]

