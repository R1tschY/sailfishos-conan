import os

from conans import ConanFile, CMake, tools


class KF5CoreAddonsTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    requires = "extra-cmake-modules/5.36.0@r1tschy/stable",

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        if not tools.cross_building(self.settings):
            os.chdir("bin")
            self.run(".%sexample" % os.sep)
