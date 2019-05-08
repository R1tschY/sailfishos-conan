from conans import ConanFile, tools, CMake
import os
import textwrap
import re


def sub_in_file(filename, pattern, repl, flags=0):
    with open(filename, "r", encoding="utf-8") as fp:
        content = fp.read()

    content, n = re.subn(pattern, repl, content, flags=flags)
    if n == 0:
        raise LookupError("pattern not found in file %s" % filename)

    with open(filename, "w", encoding="utf-8") as fp:
        fp.write(content)


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

        sub_in_file(
            "%s/CMakeLists.txt" % self.download_folder,
            r"(project\(libssh [^)]+\))",
            textwrap.dedent(
                r"""
                \1

                # Conan
                include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
                conan_basic_setup()
                
                # Do not build shared lib
                set(CMAKE_SKIP_INSTALL_ALL_DEPENDENCY true)
                """
            ),
        )
        # Do not install shared lib
        sub_in_file(
            "%s/src/CMakeLists.txt" % self.download_folder,
            r"(install\(\s*TARGETS\s*\$\{LIBSSH_SHARED_LIBRARY\})",
            r"\1 OPTIONAL ",
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
        cmake.build(target="ssh_static")
        cmake.build(target="install")

    def package(self):
        self.copy("*", dst="include", src="install/include")
        self.copy("*.a", dst="lib", src="install/lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["ssh", "ssl", "crypto", "z"]
        self.cpp_info.defines = ["LIBSSH_STATIC=1", "WITH_SERVER"]
