#!/usr/bin/env python
import os, sys
sys.path.append(os.path.join(sys.path[0], 'src'))

import pyglet
import madscience


if __name__ == "__main__":
    pyglet.options['audio'] = ('alsa', 'openal', 'silent')
    
    pyglet.resource.path = ['res']
    pyglet.resource.reindex()
    
    if len(sys.argv) > 1:
        load_name = sys.argv[1]
    else:
        load_name = 'madscience.lvl'

    window = madscience.GameWindow(load_name)
    pyglet.app.run()
