'''
Created on 2010-04-23

@author: daniel
'''
from pyglet.window import key
keymap = {key.S     : 'save',
          key.UP    : 'up',
          key.DOWN  : 'down',
          key.LEFT  : 'left',
          key.RIGHT : 'right',
          key.SPACE : 'action',
          key.E     : 'edit mode',
          key.Q     : 'next tile',
          key.F     : 'next world',
          key._0    : '0',
          key._1    : '1',
          key._2    : '2',
          key._3    : '3',
          key._4    : '4',
          key._5    : '5',
          key._6    : '6',
          key._7    : '7',
          key._8    : '8',
          key._9    : '9',
          key.C     : 'change illumination',
          key.R     : 'rotate',
          key.T     : 'entity edit mode',
          key.BACKSPACE: 'delete',
          key.RETURN: 'done',
          key.O     : 'place orb',
          key.I     : 'place ghoul',
          key.P     : 'place player',
          key.U     : 'place assistant',
          key.B     : 'place breaker trigger',
          key.V     : 'mark breaker',
          key.D     : 'place door trigger',
          key.W     : 'mark door',
          #key.M     : 'place next floor',
          key.L     : 'toggle lights',
          key.J     : 'save',
          key.ESCAPE: 'quit',
          key.F1    : 'full screen'}

playerspeed = 200
assistant_speed = 140
ghoul_speed = 160

tile_width = 82
tile_height = 82