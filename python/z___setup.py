from skbuild import setup

import os

SRC_PATH = os.path.relpath(os.path.join(os.path.dirname(__file__), "pybertini"))


EXCLUDE_FROM_PACKAGES = []

setup(
      name='pybertini',
      version='1.0.alpha5',
      description='Software for numerical algebraic geometry',
      url='http://github.com/bertiniteam/b2',
      author='Bertini Team',
      author_email='amethyst@mpi-cbg.de',

      license='GPL3 with permitted additional clauses',

      packages=["pybertini"],
      package_dir = {'pybertini': SRC_PATH},


      include_package_data=True,
      package_data= {"":["_pybertini.so"]},
      zip_safe=False,
      python_requires=">3.12",
      )

# dependencies to add
# sphinxcontrib-bibtex


# from setuptools.command.egg_info import egg_info

# class EggInfoCommand(egg_info):

#     def run(self):
#         if "build" in self.distribution.command_obj:
#             build_command = self.distribution.command_obj["build"]

#             self.egg_base = build_command.build_base

#             self.egg_info = os.path.join(self.egg_base, os.path.basename(self.egg_info))

#         egg_info.run(self)

# setup(
#     # ...
#     cmdclass={
#         "egg_info": EggInfoCommand,
#     },
#     #...
# )

