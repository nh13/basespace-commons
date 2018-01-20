import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.version_info < (3,6):
	sys.exit('Sorry, Python < 3.6 is not supported!')

setup(
    name = "basespace-commons",
    author = "Nils Homer",
    author_email = "nilshomer@gmail.com",
    version = "0.1.0",
    description = "a library for use in basespace apps",
    long_description = "a library for use in basespace apps",
    url = "https://github.com/nh13/basespace-commons",
    license = "MIT",
    packages = ["basespace_commons"],
    package_dir = {"basespace_commons" : "src/basespace_commons"},
    package_data = {},
    install_requires = [],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
)
