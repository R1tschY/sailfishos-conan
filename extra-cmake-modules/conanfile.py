from conans import ConanFile, tools, CMake
import os


class ExtraCmakeModulesConanFile(ConanFile):
    name = "extra-cmake-modules"
    version = "5.68.0"

    license = "LGPLv2.1+"
    homepage = "http://api.kde.org/frameworks-api/frameworks5-apidocs/extra-cmake-modules/html/index.html"
    description = "Extra CMake modules"

    url = "https://github.com/R1tschY/sailfishos-conan"
    author = "Richard Liebscher <richard.liebscher@gmail.com>"

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

    def build(self):
        cmake = CMake(self, generator="Unix Makefiles")
        cmake.definitions["CMAKE_INSTALL_PREFIX"] = \
            os.path.join(self.build_folder, "install")
        cmake.configure(source_folder=self.download_folder)
        cmake.build(target="install")

    def package(self):
        self.copy("*", dst="share", src="install/share")
