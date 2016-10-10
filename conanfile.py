from conans import ConanFile, tools, CMake
import os
from os import path
import glob
from shutil import copyfile

class LibgitCppConan(ConanFile):
    """
    Conan package for libgit2cpp library at https://github.com/AndreyG/libgit2cpp
    """
    name = "libgit2cpp"
    version = "0.0-8863fac"
    license=""
    #recipe repository
    url = "https://github.com/paulobrizolara/libgit2cpp-conan"

    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared" : [True, False],
        "use_boost" : [True, False],
        "std" : ["c++11", "c++14", "c++1y"]
    }
    default_options = "shared=True", "std=c++11", "use_boost=False", "Boost:header_only=True"
    generators = "cmake"
    exports = ("CMakeLists.txt",)
    requires = ("libgit2/0.24.2@paulobrizolara/stable",)

    REPO = "https://github.com/paulobrizolara/libgit2cpp.git"
    CLONED_DIR = name
    COMMIT = "8863fac"

    SRC_DIR = "."

    def config(self):
        self.SRC_DIR = self.CLONED_DIR

    def source(self):
        self.run('git clone %s %s' % (self.REPO, self.CLONED_DIR))
        self.run('git checkout %s' % self.COMMIT, cwd=self.CLONED_DIR)

    def requirements(self):
        if self.options.use_boost:
            self.requires("Boost/1.60.0@lasote/stable")

    def build(self):
        self.run("ls")

        #Make build dir
        build_dir = self.try_make_dir(os.path.join(".", "build"))

        #Change to build dir
        os.chdir(build_dir)

        cmake = CMake(self.settings)

        src_dir = self.conanfile_directory

        self.run('cmake "%s" %s %s' % (src_dir, cmake.command_line, self.cmake_args()))
        self.run('cmake --build . --target install %s' % cmake.build_config)


    def package(self):
        self.copy("*.h", src=path.join(self.SRC_DIR, "include"), dst="include", keep_path=True)

    def package_info(self):
        self.cpp_info.libs = ["git2cpp"]

        if self.options.std:
            self.cpp_info.cppflags = ["-std=%s" % self.options.std]


####################################### Helpers ################################################

    def cmake_args(self):
        """Generate arguments for cmake"""

        if not hasattr(self, 'package_folder'):
            self.package_folder = "dist"

        args = [
                self.cmake_bool_option("BUILD_SHARED_LIBS", self.options.shared),
                self.cmake_bool_option("USE_BOOST", self.options.use_boost)
        ]
        args += ['-DCMAKE_INSTALL_PREFIX="%s"' % self.package_folder]

        return ' '.join(args)

    def cmake_bool_option(self, name, value):
        return "-D%s=%s" % (name.upper(), "ON" if value else "OFF");

    def try_make_dir(self, dir):
        try:
            os.mkdir(dir)
        except OSError:
            #dir already exist
            pass

        return dir
