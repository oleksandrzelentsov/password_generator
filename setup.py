from distutils.core import setup, Extension

module = Extension("pasgens", sources=["pasgens.c"])

setup(
    version="2.0",
    description="This is a package for Password Generator which is Simple (pasgens)",
    ext_modules=[module]
)
