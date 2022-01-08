from setuptools import setup

setup(
   name='CyrusGeom2D',
   version='0.0.1',
   author='Cyrus 2D Team',
   author_email='nader.zare88@gmail.com',
   packages=['CyrusGeom2D', 'CyrusGeom2DTest'],
   # scripts=['bin/script1','bin/script2'],
   # url='http://pypi.python.org/pypi/PackageName/',
   license='LICENSE',
   description='An awesome package for geometry',
   # long_description=open('README.txt').read(),
   install_requires=[
   ],
   python_requires=">=3.6",
   test_suite='CyrusGeom2DTest',
   tests_require=['pytest']

)
