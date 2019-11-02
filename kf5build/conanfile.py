from conans import ConanFile, tools, CMake
import os
import textwrap


class KF5BuildBaseConanFile(ConanFile):
    name = "KF5BuildBase"
    version = "0.2.1"


def get_conanfile():
    class KF5ConanFileBase(ConanFile):
        lib_name = ...
        license = "LGPLv2.1+"
        homepage = "https://kde.org/products/frameworks/"
        url = "https://github.com/R1tschY/sailfishos-conan"

        settings = "os", "arch", "compiler", "build_type"
        generators = "cmake"

        options = {"shared": [True, False]}
        default_options = "shared=False"

        @property
        def download_folder(self):
            return "%s-%s" % (self.lib_name.lower(), self.version)

        @property
        def short_version(self):
            return ".".join(self.version.split(".")[:2])

        def source(self):
            zip_name = "%s.zip" % self.download_folder
            url = "http://download.kde.org/stable/frameworks/%s/%s" % (
                self.short_version,
                zip_name,
            )
            self.output.info("Downloading %s ..." % url)
            tools.download(url, zip_name)
            tools.unzip(zip_name)
            os.unlink(zip_name)

            tools.replace_in_file(
                "%s/CMakeLists.txt" % self.download_folder,
                "include(FeatureSummary)",
                textwrap.dedent(
                    """
                    include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
                    conan_basic_setup()
                    include(FeatureSummary)"""
                ),
            )

        def build(self):
            cmake = CMake(self, generator="Unix Makefiles")
            cmake.definitions.update(
                {
                    "CMAKE_INSTALL_PREFIX": os.path.join(self.build_folder, "install"),
                    "BUILD_QCH": "OFF",
                }
            )
            cmake.configure(source_folder=self.download_folder)
            cmake.build()
            cmake.build(target="install")

        def package(self):
            self.copy("*", dst="include", src="install/include/KF5/%s" % self.lib_name)
            self.copy("*.a", dst="lib", src="install/lib", keep_path=False)
            self.copy("*.so", dst="lib", src="install/lib", keep_path=False)
            self.copy("*.qm", dst="share/locale", src="install/share", keep_path=False)
            self.copy("*.cmake", dst="share", src="install/share", keep_path=False)

        def package_info(self):
            self.cpp_info.libs = [self.name]

    return KF5ConanFileBase
