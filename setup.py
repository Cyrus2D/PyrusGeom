"""PyrusGeom Setup file
"""
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='PyrusGeom',
    version='0.0.2',
    author='Cyrus 2D Team',
    author_email='nader.zare88@gmail.com',

    description='A package for handling geometry and math in SS2D',
    long_description=long_description,
    long_description_content_type="text/markdown",

    url='https://github.com/Cyrus2D/PyrusGeom',
    project_urls={
        "Issues" : "https://github.com/Cyrus2D/PyrusGeom/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPL-3)",
        "Operating System :: OS Independent",
    ],
    license='LICENSE',

    package_dir={"": "PyrusGeom"},
    packages=setuptools.find_packages(where="PyrusGeom"),

    python_requires=">=3.6",
    test_suite='tests',
)
