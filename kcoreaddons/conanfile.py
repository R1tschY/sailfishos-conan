from conans import ConanFile, tools, CMake
import os
import textwrap


class KCoreAddonsConanFile(ConanFile):
    name = "KCoreAddons"
    version = "5.36.0"
    description = "Addons to QtCore"
    license = "LGPLv2"
    url = "https://github.com/r1tschy/conan-kf5"

    settings = "os", "arch", "compiler", "build_type"
    generators = "cmake"

    options = {"shared": [True, False]}
    default_options = "shared=False"

    download_folder = "%s-%s" % (name.lower(), version)
    short_version = ".".join(version.split(".")[:2])

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
        # Ninja has strange bug in Sailfish SDK i486 target
        cmake = CMake(self, generator="Unix Makefiles")
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
        self.copy("*.qm", dst="share/locale", src="install/share")

    def package_info(self):
        self.cpp_info.libs = [self.name.replace("K", "KF5", 1)]
