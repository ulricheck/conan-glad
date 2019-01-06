#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os
from shutil import copyfile


class GladConan(ConanFile):
    name = "glad"
    version = "0.1.27"
    description = "Multi-Language GL/GLES/EGL/GLX/WGL Loader-Generator based on the official specs."
    url = "https://github.com/ulricheck/conan-glad"
    homepage = "https://github.com/Dav1dde/glad"
    license = "MIT"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "profile": ["compatibility", "core"], # OpenGL profile.
        "api_type": "ANY", # API type like "gl, gles"
        "api_version": "ANY", # API version like "3.2, 4.1", no version means latest
        "extensions": "ANY", # Path to extensions file or comma separated list of extensions, if missing all extensions are included
        "spec": ["gl", "egl", "glx", "wgl"], # Name of the spec
        "no_loader": [True, False] # No loader
    }

    default_options = (
        "shared=False",
        "fPIC=True",
        "profile=compatibility",
        "api_type=gl",
        "api_version=3.2",
        "extensions=",
        "spec=gl",
        "no_loader=False"
    )

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        source_url = "https://github.com/Dav1dde/%s/archive/v%s.zip" % (self.name, self.version)
        tools.get(source_url)
        extracted_dir = "glad-%s" % (self.version)

        #Rename to "source_subfolder" is a convention to simplify later steps
        os.rename(extracted_dir, self.source_subfolder)

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        if self.settings.compiler != 'Visual Studio':
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC

        cmake.definitions["GLAD_PROFILE"] = self.options.profile
        cmake.definitions["GLAD_API"] = "%s=%s" % (self.options.api_type, self.options.api_version)
        if self.options.extensions:
            cmake.definitions["GLAD_EXTENSIONS"] = self.options.extensions

        cmake.definitions["GLAD_SPEC"] = self.options.spec
        cmake.definitions["GLAD_NO_LOADER"] = self.options.no_loader

        if self.settings.build_type == "Release":
            cmake.definitions["GLAD_GENERATOR"] = "c"
        else:
            cmake.definitions["GLAD_GENERATOR"] = "c-debug"

        cmake.definitions["GLAD_EXPORT"] = True
        cmake.definitions["GLAD_INSTALL"] = True
        cmake.configure(build_folder=self.build_subfolder)
        return cmake


    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        cmake = self.configure_cmake()
        cmake.install()
        
    def package_info(self):
        self.cpp_info.defines.append("HAVE_GLAD")
        if self.options.shared and self.settings.os == "Windows":
             self.cpp_info.defines.append("GLAD_GLAPI_EXPORT")

        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("dl")
