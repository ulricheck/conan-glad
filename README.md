## This repository holds a conan recipe for glad.

[Conan.io](https://conan.io) package for [the glad opengl wrapper](https://github.com/Dav1dde/glad) project

## Add Remote

    $ conan remote add camposs "https://conan.campar.in.tum.de/api/conan/conan-camposs"

## For Users: Use this package

### Basic setup

    $ conan install glad/0.1.27@camposs/stable

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

    [requires]
    glad/0.1.27@camposs/stable

    [generators]
    txt

Complete the installation of requirements for your project running:

    $ mkdir build && cd build && conan install ..
    
Note: It is recommended that you run conan install from a build directory and not the root of the project directory.  This is because conan generates *conanbuildinfo* files specific to a single build configuration which by default comes from an autodetected default profile located in ~/.conan/profiles/default .  If you pass different build configuration options to conan install, it will generate different *conanbuildinfo* files.  Thus, they shoudl not be added to the root of the project, nor committed to git. 

## For Packagers: Publish this Package

The example below shows the commands used to publish to campar conan repository. To publish to your own conan respository (for example, after forking this git repository), you will need to change the commands below accordingly. 

## Build and package

The following command both runs all the steps of the conan file, and publishes the package to the local system cache.  This includes downloading dependencies from "build_requires" and "requires" , and then running the build() method.

    $ conan create . camposs/stable

## Upload

    $ conan upload -r camposs glad/0.1.27@camposs/stable

## Glad Options

Note: the api option has been seperated in 2, api_type and api_version. This fixes option parsing in python.

```
profile = compatibility
    OpenGL profile { compatibility, core }
api_type = gl
    API type like "gl,gles,..."
api_version = 3.2
    API version like "3.2, 4.1", no version means latest
extensions =
    Path to extensions file or comma separated list of extensions, if missing all extensions are included
spec = gl
    Name of the spec { gl, egl, glx, wgl }
no_loader = False
    No loader { True, False }
```

## Example

A conanfile.txt example.

```
[requires]
glad/0.1.27@camposs/stable

...

[options]
glad:profile=compatibility
glad:api_type=gl
glad:api_version=4.1
glad:spec=gl
glad:no_loader=False
```
