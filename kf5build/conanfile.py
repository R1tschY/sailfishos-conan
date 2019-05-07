from conans import ConanFile, tools, CMake
import os
import textwrap


class KF5ConanFileBase(ConanFile):
    name = "KF5BuildBase"
    version = "0.1"

    license = "LGPLv2"
    url = "https://github.com/R1tschY/sailfishos-conan"

    settings = "os", "arch", "compiler", "build_type"
    generators = "cmake"

    options = {"shared": [True, False]}
    default_options = "shared=False"

    @property
    def download_folder(self):
        return "%s-%s" % (self.name.lower(), self.version)

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
        cmake = CMake(self, generator="Ninja")
        cmake.definitions["CMAKE_INSTALL_PREFIX"] = os.path.join(
            self.build_folder, "install"
        )
        cmake.configure(source_folder=self.download_folder)
        cmake.build()
        self.run("cmake --build . --target install")

    def package(self):
        self.copy("*", dst="include", src="install/include/KF5/%s" % self.name)
        self.copy("*.a", dst="lib", src="install/lib", keep_path=False)
        self.copy("*.so", dst="lib", src="install/lib", keep_path=False)
        self.copy("*.qm", dst="share/locale", src="install/share", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = [self.name.replace("K", "KF5", 1)]