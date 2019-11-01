import os

from conans import ConanFile, CMake, tools


class ExtraCmakeModulesTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        pass  # test that it configures
