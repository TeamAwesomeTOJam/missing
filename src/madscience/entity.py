'''
Created on Apr 23, 2010

@author: jonathan
'''
import pyglet
from tile import RayVisitor
import math
from settings import assistant_speed
from settings import ghoul_speed
import light
import random
from util import *

class Entity(object):
    '''
    classdocs
    '''

    def __init__(self, floor, world, animations, default_animation, sounds, width, height, x, y, y_offset=0, dialog_color=(255,255,255,255)):
        '''
        Constructor
        '''
        self.floor = floor
        self.orientation = 0
        self.animations = {}
        self.load_animations(animations)
        self.sprite = pyglet.sprite.Sprite(self.animations[default_animation][self.orientation],
                                           batch=self.floor.sprites,
                                           group=self.floor.midground_group)
        self.sprite.event(self.on_animation_end)
        
        self.sounds = {}
        self.load_sounds(sounds)
        
        self.dialog = pyglet.text.Label('', x=x, y=y+height,
                                        font_size=16, bold=True,
                                        color=dialog_color,
                                        anchor_x='center', batch=self.floor.sprites, 
                                        group=self.floor.overlay_group)
        self.width = width
        self.height = height
        
        self._x = 0
        self._y = 0
        
        self.y_offset = y_offset
        
        self.x = x
        self.y = y
        
        self.dx = 0
        self.dy = 0
        
        self.world = world
        
    def _get_x(self):
        return self._x
    
    def _set_x(self, x):
        self._x = x
        self.sprite.x = self._x
        self.dialog.x = self._x
        #self.sound_player.position = (self._x, self._y, 0)
        
    x = property(_get_x, _set_x)
        
    def _get_y(self):
        return self._y
    
    def _set_y(self, y):
        self._y = y
        self.sprite.y = self._y - self.y_offset
        self.dialog.y = self._y + self.height * 3 - self.y_offset
        #self.sound_player.position = (self._x, self._y, 0)
        
    y = property(_get_y, _set_y)
        
    def say(self, text, duration):
        self.dialog.text = text
        pyglet.clock.schedule_once(self.shut_up, duration)
        
    def shut_up(self, dt=None):
        self.dialog.text = ''
    
    def load_animations(self, animation_map):
        self.animations = {}
        
        for name, info in animation_map.iteritems():
            path, turns, duration = info
            frame_duration = duration / 16.0
            self.animations[name] = []
            
            for turn in range(turns):
                frames = []
                for i in range(16):
                    file_name = '%04d.png' % (i,)
                    try:
                        image = pyglet.resource.image(path + '/' + str(turn) + '/' + file_name)
                        image.anchor_x = image.width / 2
                    except pyglet.resource.ResourceNotFoundException: 
                        break
                    else:
                        frames.append(pyglet.image.AnimationFrame(image, frame_duration))
                animation = pyglet.image.Animation(frames)
                self.animations[name].append(animation)
        
    def play_animation(self, name, reset=False):
        turn = min(len(self.animations[name]), self.orientation)
        animation = self.animations[name][turn]
        if reset or self.sprite.image != animation:
            self.sprite.image = animation
        
    def on_animation_end(self):
        pass
    
    def load_sounds(self, sound_map):
        for name, info in sound_map.iteritems():
            path, loop = info
            self.sounds[name] = pyglet.resource.media(path, streaming=False)
            
    def play_sound(self, name):
        self.sounds[name].play()
    
    def delete(self):
        pass
    
    def on_update(self, dt):
        if self.dx != 0 or self.dy != 0:
            collisions = self.floor.check_collision(self, self.x + self.dx * dt, self.y + self.dy * dt)
            for collision in collisions:
                self.on_collision(collision)
                
            if all(isinstance(item, Entity) for item in 
                   self.floor.check_collision(self, self.x + self.dx * dt, self.y)):
                self.x += self.dx * dt
                
            if all(isinstance(item, Entity) for item in 
                   self.floor.check_collision(self, self.x, self.y + self.dy * dt)):
                self.y += self.dy * dt

            atan = math.atan2(self.dy, self.dx)
            if atan < 0:
                atan = 2 * math.pi - atan
            self.orientation = min(int((2 * atan / math.pi) + 0.5), 3)
        
        if self.floor.do_lighting:
            my_tile = self.floor.get_tile(self.x, self.y, self.world)   
            scaled_value = min(255, int(my_tile.illumination * 255))
            self.sprite.color = (scaled_value, scaled_value, scaled_value)
        else:
            self.sprite.color = (255,255,255)
           
    def on_collision(self, other):
        pass
    
    def hide(self):
        pass
    
    def show(self):
        pass
        
        
class PlayerEntity(Entity):

    def __init__(self, floor, x, y):
        animations = {'run' : ('sprites/scientist/run', 4, 0.25),
                      'idle' : ('sprites/scientist/idle', 4, 1)
                      }
        default_animation = 'idle'
        sounds = {}
        
        Entity.__init__(self, floor, False, animations, default_animation, sounds, 48, 48, x, y, 21, (200,64,255,255))
        self.max_orb_power = 10000.0
        self.orb_power = 10000.0
        self.sprite.opacity = 180
        self.light = light.Light(self.floor, 100, 64, self.orb_power, self.x, self.y)

    def _get_x(self):
        return Entity._get_x(self)
    
    def _set_x(self, x):
        Entity._set_x(self, x)
        pyglet.media.Listener.position = (self._x, self._y, 0)
        
    x = property(_get_x, _set_x)
        
    def _get_y(self):
        return Entity._get_y(self)
    
    def _set_y(self, y):
        Entity._set_y(self, y)
        pyglet.media.Listener.position = (self._x, self._y, 0)
        
    y = property(_get_y, _set_y)

    def on_update(self, dt):
        Entity.on_update(self, dt)
        
        if self.light.on:
            self.orb_power = max(self.orb_power - dt * 200, 0)
            self.light.intensity = self.orb_power
            
        self.light.x = self.x
        self.light.y = self.y

        if self.dx != 0 or self.dy != 0:
            self.play_animation('run')
        else:
            self.play_animation('idle')
            
    def action(self, updown):
        if updown > 0:
            self.light.on = not self.light.on
            if self.light.on:
                pass
            
    def on_collision(self, other):
        if isinstance(other, OrbEntity):
            self.orb_power = min(other.power + self.orb_power, self.max_orb_power)
            
    
class AssistantEntity(Entity):
    
    def __init__(self, floor, x, y):
        animations = {'run' : ('sprites/assistant/run', 4, 0.25),
                      'idle' : ('sprites/assistant/idle', 4, 1),
                      'cower' : ('sprites/assistant/idle', 4, 1),
                      'activate' : ('sprites/assistant/activate', 4, 0.5),
                      }
        sounds = {'death' : ('sounds/ENDING DEATH 1.wav', False)}
        default_animation = 'idle'
        Entity.__init__(self, floor, True, animations, default_animation, sounds, 48, 48, x, y, 21, (255,255,64,255))
        self.activating_trigger = False
        self.trigger_counter = 0
    
    def on_collision(self, collision):
        if isinstance(collision, TriggerEntity):
            self.activating_trigger = True
            self.orientation = collision.orientation
            
            if self.trigger_counter >= collision.delay:
                collision.activate()
                self.floor.remove_entity(collision)
                self.trigger_counter = 0
                self.activating_trigger = False
        
    def on_update(self, dt):
        currtile = self.floor.get_tile(self.x, self.y, True)
        if self.activating_trigger:
            self.dx = 0
            self.dy = 0
            self.trigger_counter += dt
        else:
            wanted = self.floor.look_for_brightest(currtile)
      
            if ((wanted.x - self.x) + (wanted.y - self.y)) != 0:
                delta_x, delta_y = direction_to(wanted.x, wanted.y, self.x, self.y)
            else:
                delta_x = (wanted.x - self.x)
                delta_y = (wanted.y - self.y)
            
            if(wanted != currtile): 
                self.dx = delta_x * assistant_speed
                self.dy = delta_y * assistant_speed
            else:
                self.dx = 0
                self.dy = 0
        
        Entity.on_update(self, dt)
        if self.dx != 0 or self.dy != 0:
            self.play_animation('run')
        else:
            if self.activating_trigger:
                self.play_animation('activate')
            elif currtile.illumination == 0:
                self.play_animation('cower')
            else: 
                self.play_animation('idle')
        
        
class GhoulEntity(Entity):
    
    def __init__(self, floor, x, y):
        animations = {'run' : ('sprites/ghoul/idle', 4, 0.25),
                      'idle' : ('sprites/ghoul/idle', 4, 1),
                      'cower' : ('sprites/ghoul/idle', 4, 1)
                      }
        default_animation = 'idle'
        Entity.__init__(self, floor, True, animations, default_animation, {}, 48, 48, x, y, 21, (128,255,64,255))
        self.in_light_timer = 0
        self.fleeing = False
        self.flee_dx = 0
        self.flee_dy = 0
        self.random_xdir = 1
        self.random_ydir = 1
        self.random_timer = 0
        self.lose_timer = 0
        
    def find_assistant(self, ray, tile):
        if tile.transmitivity == 0:
            raise StopIteration
        
        if tile == self.floor.get_tile(self.floor.assistant.x, self.floor.assistant.y, True):
            return True
        return False
        
    def on_update(self, dt):
        currtile = self.floor.get_tile(self.x, self.y, True)
        if currtile.illumination > 0.1:
            if currtile.illumination < 0.4:
                brightest = self.floor.look_for_brightest(currtile)
                delta_x, delta_y = direction_to(brightest.x, brightest.y, currtile.x, currtile.y)
                self.dx = -1 * delta_x * ghoul_speed
                self.dy = -1 * delta_y * ghoul_speed
            else:
                self.in_light_timer += dt
                self.dx = 0
                self.dy = 0
        else:
            self.in_light_timer = max(self.in_light_timer - (dt/1.5), 0)
            asstile = self.floor.get_tile(self.floor.assistant.x, self.floor.assistant.y, True)
            ray = RayVisitor(self.floor, self.x, self.y, (asstile.x - self.x) * 1.2, (asstile.y - self.y) * 1.2, self.find_assistant)
            if any(ray.visit()):
                if ((self.floor.assistant.x - self.x) + (self.floor.assistant.x - self.y)) != 0:
                    delta_x, delta_y = direction_to(self.floor.assistant.x, self.floor.assistant.y, self.x, self.y)
                else:
                    delta_x = 0
                    delta_y = 0
        
    
                self.dx = delta_x * ghoul_speed
                self.dy = delta_y * ghoul_speed

                
                if abs(self.x - self.floor.assistant.x) < 5 and abs(self.y - self.floor.assistant.y) < 5:
                    self.dx = 0
                    self.dy = 0
                    self.lose_timer += dt
                    self.floor.assistant.play_sound('death')
                    if self.lose_timer > 2:
                        self.floor.lose = True
                        self.lose_timer = 0
                        #lose!
                else:
                    self.lose_timer = max(self.lose_timer - dt, 0)
            else:
                self.random_timer += dt
                if self.random_timer > 3:
                    self.random_xdir = random.choice([-1,0,1])
                    self.random_ydir = random.choice([-1,0,1])
                    self.random_timer = 0
                
                self.dx = self.random_xdir * random.random() * ghoul_speed
                self.dy = self.random_ydir * random.random() * ghoul_speed
                
            if self.floor.get_tile(self.x + self.dx * dt, self.y, True).illumination > 0.1:
                self.dx = 0
            if self.floor.get_tile(self.x, self.y + self.dy * dt, True).illumination > 0.1:
                self.dy = 0
        
        if self.in_light_timer > 2 and not self.fleeing:
            self.fleeing = True
            brightest = self.floor.look_for_brightest(currtile)
                        
            if brightest == currtile:
                brightest = self.floor.get_tile(self.floor.assistant.x, self.floor.assistant.y, True)
                
            if not brightest == currtile:
                delta_x, delta_y = direction_to(brightest.x, brightest.y, self.x, self.y)

                self.flee_dx = -1 * delta_x * ghoul_speed * 2
                self.flee_dy = -1 * delta_y * ghoul_speed  * 2
                
            else:
                self.flee_dx = self.random_xdir * random.random() * ghoul_speed * 2
                self.flee_dy = self.random_ydir * random.random() * ghoul_speed * 2

           
        if self.fleeing:
            self.dx = self.flee_dx
            self.dy = self.flee_dy
            if self.in_light_timer == 0:
                self.fleeing = False
        
        Entity.on_update(self, dt)
            
        if self.dx != 0 or self.dy != 0:
            self.play_animation('run')
        else:
            if currtile.illumination > 0.4:
                self.play_animation('cower')
            else:
                self.play_animation('idle')
            

class OrbEntity(Entity):
    
    def __init__(self, floor, x, y):
        animations = {'idle' : ('sprites/orb/activate', 1, 2)}
        default_animation = 'idle'
        Entity.__init__(self, floor, False, animations, default_animation, {}, 128, 128, x, y)
        self.power = 8000.0


class TriggerEntity(Entity):
    
    def __init__(self, floor, world, animations, x, y, orientation=0, delay=0):
        default_animation = 'show'
        Entity.__init__(self, floor, world, animations, default_animation, {}, 24, 24, x, y)
        self.orientation = orientation
        self.delay = delay
        self.marks = []
        self.sprite.visible = False
        self.floor.get_tile(x, y, world).assistant_preference = 0.1
    
    def delete(self):
        
        while self.marks:
            self.floor.remove_entity(self.marks.pop())
    
    def activate(self):
        pass
    
    def hide(self):
        self.sprite.visible = False
    
    def show(self):
        self.sprite.visible = True
     

class DoorTriggerEntity(TriggerEntity):
    
    def __init__(self, floor, x, y, orientation, delay=0):
        animations = {'show': ('sprites/door_trigger/show', 1, 1)}
        TriggerEntity.__init__(self, floor, True, animations, x, y, orientation, delay)
    
    def activate(self):
        for m in self.marks:
            m.tile.activate()
    
    
class BreakerTriggerEntity(TriggerEntity):
    
    def __init__(self, floor, x, y, orientation, delay=0):
        animations = {'show': ('sprites/breaker_trigger/show', 1, 1)}
        TriggerEntity.__init__(self, floor, True, animations, x, y, orientation, delay)
        self.floor.breakers += 1
    
    def activate(self):
        for m in self.marks:
            m.tile.light_up()
        self.floor.on_breaker_thrown(self)


class MarkEntity(Entity):
    
    def __init__(self,floor,tile_x, tile_y, x,y,trigger, animations):
        default_animation = 'show'
        Entity.__init__(self, floor, True, animations, default_animation, {}, 5, 5, x, y)
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.trigger = trigger
        self.trigger.marks.append(self)
        
    def _get_tile(self):
        return self.floor.world_tiles[self.tile_x][self.tile_y]
    
    def _set_tile(self):
        pass
    
    tile = property(_get_tile,_set_tile)
        
    def delete(self):
        if self in self.trigger.marks: 
            self.trigger.marks.remove(self)
    
    def hide(self):
        self.sprite.visible = False
    
    def show(self):
        self.sprite.visible = True

class DoorMarkEntity(MarkEntity):
    
    def __init__(self,floor,tile_x,tile_y,x,y,trigger):
        animations = {'show': ('sprites/mark/show', 1, 1)}
        MarkEntity.__init__(self,floor,tile_x,tile_y,x,y,trigger,animations)

class BreakerMarkEntity(MarkEntity):
    
    def __init__(self,floor,tile_x,tile_y,x,y,trigger):
        animations = {'show': ('sprites/bmark/show', 1, 1)}
        MarkEntity.__init__(self,floor,tile_x,tile_y,x,y,trigger,animations)

class TargetEntity(Entity):
    
    def __init__(self,floor, x,y):
        animations = {'show': ('sprites/target/show', 1, 1)}
        default_animation = 'show'
        Entity.__init__(self, floor, True, animations, default_animation, {}, 24, 24, x, y)
        
    def hide(self):
        self.sprite.visible = False
    
    def show(self):
        self.sprite.visible = True

class NextFloorEntity(Entity):
    
    def __init__(self,floor,x,y):
        animations = {'show': ('sprites/next_floor/show', 1, 1)}
        default_animation = 'show'
        Entity.__init__(self, floor, True, animations, default_animation, {}, 24, 24, x, y)
    
    def hide(self):
        self.sprite.visible = False
    
    def show(self):
        self.sprite.visible = True