#!/usr/bin/env python

"""Installer for misspelling-check.

This installs the misspelling command and the misspellings.check module.
"""

import os
import sys
from distutils import log
from distutils.core import setup
from distutils.core import Command
if sys.version_info < (2, 7):
  import unittest2 as unittest
else:
  import unittest

BASE_DIR = os.path.dirname(globals().get('__file__', os.getcwd()))


class TestCommand(Command):
  description = 'Runs all available tests.'
  user_options = []

  def initialize_options(self):
    pass

  def finalize_options(self):
    pass

  def run(self):
    test_dir = os.path.join(BASE_DIR, 'tests')

    tests = unittest.TestLoader().discover(test_dir)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(tests)
    if not result.wasSuccessful():
      sys.exit(1)


class CleanCommand(Command):
  description = 'Remove all generated files.'
  user_options = []

  def initialize_options(self):
    pass

  def finalize_options(self):
    pass

  def run(self):
    # Configure for this project.
    suffixes2del = ['MANIFEST', '.pyc', '.test_out']
    dirs2del = ['./build', './dist', './tests/logs']
    dirs2ign = ['./.git']
    # End config.
    doomed = set()
    # Change to base dir.
    os.chdir(BASE_DIR)
    for root, dirs, files in os.walk('.'):
      # Handle root dirs.
      if root in dirs2ign:
        continue
      if root in dirs2del:
        doomed.add(root)
      # Handle files.
      for f in files:
        accused = os.path.join(root, f)
        for suffix in suffixes2del:
          if f.endswith(suffix):
            doomed.add(accused)
            break
        if accused not in doomed:
          for d2del in dirs2del:
            if accused.startswith(d2del):
              doomed.add(accused)
              break
      # Handle dirs.
      for d in dirs:
        accused = os.path.join(root, d)
        for d2ign in dirs2ign:
          if accused.startswith(d2ign):
            dirs.remove(d)
            break
        if d in dirs:
          for d2del in dirs2del:
            if accused.startswith(d2del):
              doomed.add(accused)
              break
    # Probably not required, but just to be safe.
    for accused in doomed:
      for d2ign in dirs2ign:
        if accused.startswith(d2ign):
          doomed.remove(accused)
          break
    for accused in sorted(doomed, reverse=True):
      log.info('removing "%s"', os.path.normpath(accused))
      if not self.dry_run:
        try:
          os.unlink(accused)
        except:
          try:
            os.rmdir(accused)
          except:
            log.warn('unable to remove "%s"', os.path.normpath(accused))

setup(
  cmdclass={'test': TestCommand,
            'dist_clean': CleanCommand
           },
  name='misspellings',
  version='1.3',
  url='https://github.com/lyda/misspell-check',
  author='Kevin Lyda',
  author_email='kevin@ie.suberic.net',
  description='A tool to detect misspellings',
  long_description=open('README').read(),
  py_modules=['misspellings_lib'],
  scripts=['misspellings', ],
  keywords='check code spelling spellcheck',
  license='GNU General Public License v3',
  platforms=['POSIX'],
  # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
  classifiers=['Development Status :: 5 - Production/Stable',
                 'Environment :: Console',
                 'License :: OSI Approved'
                 ' :: GNU General Public License v3 (GPLv3)',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 2.6',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Topic :: Utilities',
                 ],
)
