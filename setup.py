#!/usr/bin/env python
import os, sys
sys.path.append(os.path.join(sys.path[0], 'src'))

from distutils.core import setup

# The main entry point of the program
script_file = 'runmadscience.py'

# Create a list of data files.  Add everything in the 'res/' directory.
data_files = []
for file in os.listdir('res'):
    file = os.path.join('res', file)
    if os.path.isfile(file):
        data_files.append(file)

# Setup args that apply to all setups, including ordinary distutils.
setup_args = dict(
    data_files=[('res', data_files), ('', ['editor help.txt', 'madscience.lvl'])],
    package_dir = {'': 'src'},
    packages=['pyglet', 'madscience'],
)

# py2exe options
try:
    import py2exe
    setup_args.update(dict(
        windows=[dict(
            script=script_file,
 #           icon_resources=[(1, 'assets/app.ico')],
        )],
    ))
except ImportError:
    pass

# py2app options
try:
    import py2app
    setup_args.update(dict(
        app=[script_file],
        options=dict(py2app=dict(
            argv_emulation=True,
#            iconfile='assets/app.icns',
        )),
    ))
except ImportError:
    pass

setup(**setup_args)