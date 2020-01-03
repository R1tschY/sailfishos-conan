import os

from conans import ConanFile, CMake, tools


class QcaTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.definitions["QCA_SHARED"] = "ON" if self.options["Qca-qt5"].shared else "OFF"
        cmake.configure()
        cmake.build()

    def test(self):
        return
        if not tools.cross_building(self.settings):
            os.chdir("bin")
            self.run(".%sexample" % os.sep)
