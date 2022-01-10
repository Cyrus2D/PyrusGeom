from setuptools import setup

setup(
   name='PyrusGeom',
   version='0.0.1',
   author='Cyrus 2D Team',
   author_email='nader.zare88@gmail.com',
   packages=['PyrusGeom', 'PyrusGeomTest'],
   # scripts=['bin/script1','bin/script2'],
   # url='http://pypi.python.org/pypi/PackageName/',
   license='LICENSE',
   description='An awesome package for geometry',
   # long_description=open('README.txt').read(),
   install_requires=[
   ],
   python_requires=">=3.6",
   test_suite='PyrusGeomTest',
)
