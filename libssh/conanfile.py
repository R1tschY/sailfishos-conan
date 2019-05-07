from conans import ConanFile, tools, CMake
import os
import textwrap


class LibSshConanFile(ConanFile):
    name = "libssh"
    version = "0.8.7"

    license = "LGPLv2.1"
    homepage = "https://www.libssh.org/"
    description = "The SSH library!"

    url = "https://github.com/R1tschY/sailfishos-conan"
    author = "Richard Liebscher <richard.liebscher@gmail.com>"

    settings = "os", "arch", "compiler", "build_type"
    generators = "cmake"

    @property
    def download_folder(self):
        return "%s-%s" % (self.name.lower(), self.version)

    @property
    def short_version(self):
        return ".".join(self.version.split(".")[:2])

    def source(self):
        # TODO: check signature
        zip_name = "%s.tar.xz" % self.download_folder
        url = "https://www.libssh.org/files/%s/%s" % (self.short_version, zip_name)
        self.output.info("Downloading %s ..." % url)
        tools.download(url, zip_name)
        tools.unzip(zip_name)
        os.unlink(zip_name)

        tools.replace_in_file(
            "%s/CMakeLists.txt" % self.download_folder,
            "set(APPLICATION_NAME ${PROJECT_NAME})",
            textwrap.dedent(
                """
                include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
                conan_basic_setup()
                set(APPLICATION_NAME ${PROJECT_NAME})
                """
            ),
        )

    def build(self):
        cmake = CMake(self, generator="Unix Makefiles")
        cmake.definitions["CMAKE_INSTALL_PREFIX"] = os.path.join(
            self.build_folder, "install"
        )
        cmake.definitions.update(
            dict.fromkeys(
                ["WITH_ZLIB", "WITH_SFTP", "WITH_SERVER", "WITH_STATIC_LIB"], True
            )
        )
        cmake.configure(source_folder=self.download_folder)
        cmake.build()
        self.run("cmake --build . --target install")

    def package(self):
        self.copy("*", dst="include", src="install/include")
        self.copy("*.a", dst="lib", src="install/lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["ssh", "ssl", "crypto", "z"]
        self.cpp_info.defines = ["LIBSSH_STATIC=1", "WITH_SERVER"]
