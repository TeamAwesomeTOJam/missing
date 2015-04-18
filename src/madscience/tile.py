'''
Created on Apr 23, 2010

@author: jonathan
'''
import math
import pyglet
from settings import tile_width, tile_height

class Tile(object):
    '''
    classdocs
    '''

    def __init__(self, floor, world, image, passable, illumination, transmitivity, reflectivity, x, y, orientation):
        self.world = world
        self.floor = floor
        name, rotation = image
        pic = pyglet.resource.image(name)
        pic.anchor_x = pic.width / 2
        pic.anchor_y = pic.height / 2
        
        if self.world:
            group = self.floor.background_group
        else:
            group = self.floor.foreground_group
            
        self.sprite = pyglet.sprite.Sprite(pic, 
                                           x,
                                           y,
                                           batch=self.floor.sprites,
                                           group=group)

        self.sprite.rotation = rotation
        self.passable = passable
        self.static_illumination = illumination
        self.transmitivity = transmitivity
        self.reflectivity = reflectivity
        self.clear_light()
        
        self.x = x
        self.y = y
        self.orientation = orientation
        self.width = tile_width
        self.height = tile_height
        self.assistant_preference = 0
    
    def clear_light(self):
        self.illumination = self.static_illumination
        self._light_sprite()
        self._transmitivity_counter = 0
        self._reflectivity_counter = 0
        
    def set_light(self, value):
        if self.transmitivity > 0.0:
            transmit = True
        else:
            transmit = False
        
        self.illumination = self.static_illumination + value
        self._light_sprite()
        return transmit, False
    
    def _light_sprite(self):
        if self.floor.do_lighting:
            scaled_value = max(32, min(255, int(self.illumination * 255)))
            self.sprite.color = (scaled_value, scaled_value, scaled_value)
        else:
            self.sprite.color = (255,255,255)
    
    def light_up(self):
        self.static_illumination = 0.9
    
    def activate(self):
        pass

        
class FloorTile(Tile):
    num_orientations = 1
    
    def __init__(self, floor, illumination, x, y, orientation):
        Tile.__init__(self, floor, True, ('tiles/floor.png', 0), True, illumination, 1.0, 0.0, x, y, orientation)


class AlternateFloor(Tile):
    num_orientations = 1
    
    def __init__(self, floor, illumination, x, y, orientation):
        Tile.__init__(self, floor, False, ('tiles/floor.png', 0), True, illumination, 1.0, 0.0, x, y, orientation)
        self.sprite.opacity = 0
        
        
class AlternateWall(Tile):
    num_orientations = 1
    
    def __init__(self, floor, illumination, x, y, orientation):
        Tile.__init__(self, floor, False, ('tiles/other_wall.png', 0), False, illumination, 0.0, 0.5, x, y, orientation)
        self.sprite.opacity = 128
        
        
class RealWall(Tile):
    num_orientations = 4
    def __init__(self, floor, illumination, x, y, orientation):
        self.choices = ['tiles/wall_straight_1.png', 'tiles/wall_straight_2.png', 'tiles/wall_straight_3.png', 'tiles/wall_straight_4.png']
        self.choices += ['tiles/corner_out_1.png', 'tiles/corner_out_2.png', 'tiles/corner_out_3.png', 'tiles/corner_out_4.png']
        Tile.__init__(self, floor, True, ('tiles/wall_straight_1.png', (360*orientation)/4), False, illumination, 0.0, 0.5, x, y, orientation)
        
class RealOuterCorner(Tile):
    num_orientations = 4
    
    def __init__(self, floor, illumination, x, y, orientation):
        self.choices = ['tiles/corner_1-1.png', 'tiles/corner_1.png', 'tiles/corner_1-2.png']
        self.choices += ['tiles/corner_2-1.png', 'tiles/corner_2.png', 'tiles/corner_2-2.png']
        self.choices += ['tiles/corner_3-1.png', 'tiles/corner_3.png', 'tiles/corner_3-2.png']
        self.choices += ['tiles/corner_4-1.png', 'tiles/corner_4.png', 'tiles/corner_4-2.png']
        #self.choices[orientation%3]
        Tile.__init__(self, floor, True, ('tiles/real_corner_outside.png', (360*(orientation))/4), False, illumination, 0.0, 0.5, x, y, orientation)

class RealInnerCorner(Tile):
    num_orientations = 4
    def __init__(self, floor, illumination, x, y, orientation):
        Tile.__init__(self, floor, True, ('tiles/real_corner.png', (360*(orientation))/4), False, illumination, 0.0, 0.5, x, y, orientation)
        
        
class Door(Tile):
    num_orientations = 8
    
    def __init__(self, floor, illumination, x, y, orientation, open=False):
        self.choices = ['tiles/wall_door_1_close-top.png', 'tiles/wall_door_1_close-bottom.png']
        self.opening = ['tiles/wall_door_1_open-top.png', 'tiles/wall_door_1_open-bottom.png']
        if open:
            image = self.opening[orientation % 2]
        else:
            image = self.choices[orientation % 2]
        Tile.__init__(self, floor, True, (image, (360*(orientation/2))/4), False, illumination, 0.0, 0.5, x, y, orientation)
        
    def open(self):
        self.opening = ['tiles/wall_door_1_open-top.png', 'tiles/wall_door_1_open-bottom.png']
        pic = pyglet.resource.image(self.opening[self.orientation % 2])
        pic.anchor_x = pic.width / 2
        pic.anchor_y = pic.height /2
        rot = self.sprite.rotation
        self.sprite.image = pic

        self.sprite.rotation = rot
        self.passable = True
        self.transmitivity = 1.0
        self.reflectivity = 0.0        
        
    def close(self):
        self = Door(self.floor, self.illumination, self.x, self.y, self.orientation, False)
        self.passable = False
        self.transmitivity = 0.0
        self.reflectivity = 0.5
        #self.image = ('tiles/doorclose.png', self.orientation)
    
    def activate(self):
        if self.passable:
            self.close()
        else:
            self.open()
        
        
class EmergencyLight(Tile):
    num_orientations = 1
    
    def __init__(self, floor, illumination, x, y, orientation):
        Tile.__init__(self, floor, True, ('tiles/light.png', 0), True, illumination, 1.0, 0.0, x, y, orientation)
        
        
class Machine(Tile):
    num_orientations = 1
    
    def __init__(self, floor, illumination, x, y, orientation):
        Tile.__init__(self, floor, True, ('tiles/machine.png', 0), False, illumination, 0.3, 0.8, x, y, orientation)
        
        
class CircuitBreaker(Tile):
    num_orientations = 4
    
    def __init__(self, floor, illumination, x, y, orientation):
        Tile.__init__(self, floor, True, ('tiles/wall_circuit_1.png', (360*orientation)/4), False, illumination, 0.0, 0.6, x, y, orientation)
        
        
class Portal(Tile):
    num_orientations = 4
    
    def __init__(self, floor, illumination, x, y, orientation):
        self.choices = ['tiles/floor_portal-bottom-left.png', 'tiles/floor_portal-bottom-right.png', 'tiles/floor_portal-top-left.png', 'tiles/floor_portal-top-right.png']
        Tile.__init__(self, floor, True, (self.choices[orientation], 0), False, illumination, 0.9, 0.7, x, y, orientation)
        
        
class RayVisitor(object):

    def __init__(self, floor, origin_x, origin_y, run, rise, callback):
        self.floor = floor
        self.origin_x = float(origin_x)
        self.origin_y = float(origin_y)
        self.run = float(run)
        self.rise = float(rise)
        self.step_size = 8.0
        self.callback = callback
    
    def visit(self):
        results = []
        for tile in self.get_tiles():
            try:
                results.append(self.callback(self, tile))
            except StopIteration:
                break
        return results
    
    def get_tiles(self):
        ray_length = (self.run ** 2 + self.rise ** 2) ** 0.5
        normalized_x = self.run / ray_length
        normalized_y = self.rise / ray_length
        
        x_step = normalized_x * self.step_size
        y_step = normalized_y * self.step_size
        
        x = self.origin_x
        y = self.origin_y
        for i in range(int(ray_length / self.step_size)):
            x += x_step * i
            y += y_step * i
            try:
                yield(self.floor.get_tile(x, y, True))
            except IndexError:
                break
        return 
    
    @staticmethod
    def generate_rays(floor, x, y, num_rays, length, start_angle, arc, callback):
        angle = (2 * math.pi) / num_rays
        curr_pos = start_angle
        while curr_pos < start_angle + arc:
            rise = math.sin(curr_pos) * length
            run = math.cos(curr_pos) * length
            yield RayVisitor(floor, x, y, run, rise, callback)
            curr_pos += angle
        return
        
world_tile_list = [FloorTile,RealWall,RealOuterCorner,RealInnerCorner,Door,CircuitBreaker,Portal]
other_tile_list = [AlternateFloor,AlternateWall]