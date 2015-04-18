'''
Created on Apr 23, 2010

@author: nish
'''
import pyglet
import entity
import math
from tile import RayVisitor, FloorTile, AlternateFloor, RealWall, AlternateWall, RealOuterCorner
from settings import tile_width, tile_height 
from entity import MarkEntity

class Floor(object):
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        self.sprites = pyglet.graphics.Batch()
        self.sprite_group = pyglet.graphics.Group()
        self.background_group = pyglet.graphics.OrderedGroup(0, self.sprite_group)
        self.midground_group = pyglet.graphics.OrderedGroup(1, self.sprite_group)
        self.foreground_group = pyglet.graphics.OrderedGroup(2, self.sprite_group)
        self.overlay_group = pyglet.graphics.OrderedGroup(3, self.sprite_group)
        
        self.breakers = 0
        self.breakers_thrown = 0
        
        self.lose = False
        self.win = False
        
        self.do_lighting = True
        
        self.world_tiles = [[FloorTile(self, 0, j * tile_width, i * tile_height, 0) for i in range(self.height)] for j in range(self.width)]
        self.other_tiles = [[AlternateFloor(self, 1.0, j * tile_width, i * tile_height, 0) for i in range(self.height)] for j in range(self.width)]
        
        for i in range(self.width):
            for j in range(self.height):
                if i == 0:
                    self.other_tiles[i][j] = AlternateWall(self, 1.0, i * tile_width, j * tile_height, 0)
                    if j==0:
                        self.world_tiles[i][j] = RealOuterCorner(self, 0, i * tile_width, j * tile_height, 0)
                    elif j==self.width -1:
                        self.world_tiles[i][j] = RealOuterCorner(self, 0, i * tile_width, j * tile_height, 1)
                    else:
                        self.world_tiles[i][j] = RealWall(self, 0, i * tile_width, j * tile_height, 0)

                elif i==self.height-1:
                    self.other_tiles[i][j] = AlternateWall(self, 1.0, i * tile_width, j * tile_height, 0)
                    if j ==0:
                        self.world_tiles[i][j] = RealOuterCorner(self, 0, i * tile_width, j * tile_height, 3)
                    elif j==self.width-1:
                        self.world_tiles[i][j] = RealOuterCorner(self, 0, i * tile_width, j * tile_height, 2)
                    else:
                        self.world_tiles[i][j] = RealWall(self, 0, i * tile_width, j * tile_height, 2)

                elif j==0:
                    self.other_tiles[i][j] = AlternateWall(self, 1.0, i * tile_width, j * tile_height, 0)
                    self.world_tiles[i][j] = RealWall(self, 0, i * tile_width, j * tile_height, 3)

                elif j==self.width-1:
                    self.other_tiles[i][j] = AlternateWall(self, 1.0, i * tile_width, j * tile_height, 0)
                    self.world_tiles[i][j] = RealWall(self, 0, i * tile_width, j * tile_height, 1)

        
        self.entities = []

        self.player = entity.PlayerEntity(self, tile_width, tile_height)
        self.entities.append(self.player)
        
        self.assistant = entity.AssistantEntity(self, tile_width, tile_height)
        self.entities.append(self.assistant)
    
    def add_entity(self,entity):
        if not entity in self.entities:
            self.entities.append(entity)
    
    def remove_entity(self,entity):
        if entity == self.player or entity == self.assistant:
            return
        if entity in self.entities:
            self.entities.remove(entity)
            entity.sprite.delete()
            entity.delete()
        
        
    def get_tile(self, x, y, real_world):
        tile_x = int(math.floor((x / tile_width) + 0.5))
        tile_y = int(math.floor((y / tile_height) + 0.5))
        
        if tile_x < 0 or tile_y < 0:
            raise IndexError
        
        if real_world:
            return self.world_tiles[tile_x][tile_y]
        else:
            return self.other_tiles[tile_x][tile_y]
    
    def look_for_brightest(self, currtile):
        def list_tiles(self, tile):
            if tile.transmitivity == 0:
                raise StopIteration
            return tile

        brightest = currtile
        for ray in RayVisitor.generate_rays(currtile.floor, currtile.x, currtile.y, 20, 300, 0, 2 * math.pi, list_tiles):
            tiles = ray.visit()
            for t in tiles:
                if isinstance(self, entity.AssistantEntity):
                    pref = t.assisstant_preference
                else:
                    pref = 0
                if brightest == None or t.illumination + pref > brightest.illumination:
                    brightest = t
                        
        return brightest
        
    def check_collision(self, entity, x, y):
        upx = int(math.floor(((x + entity.width/2.0) / tile_width) + 0.5))
        upy = int(math.floor(((y + entity.height/2.0) / tile_height) + 0.5))
        btx = int(math.floor(((x - entity.width/2.0) / tile_width) + 0.5))
        bty = int(math.floor(((y - entity.height/2.0) / tile_height) + 0.5))
        collisions = []
        if upx > self.width-1 or upy > self.height-1 or btx < 0 or bty < 0:
            pass
#            return True
   
        if entity.world:
            for sp in [thing for thing in self.entities if thing.world and thing != entity and not isinstance(thing, MarkEntity)]:
                if y + entity.height/2.0 < sp.y - sp.height/2.0:
                    pass
                elif y - entity.height/2.0 > sp.y + sp.height/2.0:
                    pass
                elif x + entity.width/2.0 < sp.x - sp.width/2.0:
                    pass
                elif x - entity.width/2.0 > sp.x + sp.width/2.0:
                    pass
                else:
                    collisions.append(sp)
                
            tile_list = []
            for i in range(btx, upx + 1):
                for j in range(bty, upy + 1):
                    tile_list.append(self.world_tiles[i][j])
                
            for tile in tile_list:
                if tile.passable == False:
                    collisions.append(tile)
            
        else:
            for sp in [thing for thing in self.entities if not thing.world and thing != entity and not isinstance(thing, MarkEntity)]:
                if y + entity.height/2.0 < sp.y - sp.height/2.0:
                    pass
                elif y - entity.height/2.0 > sp.y + sp.height/2.0:
                    pass
                elif x + entity.width/2.0 < sp.x - sp.width/2.0:
                    pass
                elif x - entity.width/2.0 > sp.x + sp.width/2.0:
                    pass
                else:
                    collisions.append(sp)
                
            
            tile_list = []
            for i in range(btx, upx + 1):
                for j in range(bty, upy + 1):
                    tile_list.append(self.other_tiles[i][j])
                
            for tile in tile_list:
                if tile.passable == False:
                    collisions.append(tile)
                
        return collisions
    
    def lighting(self):
        for column in self.world_tiles:
            for tile in column:
                tile.clear_light()
                
        self.player.light.do_lighting()
    
    def on_update(self, dt):
        self.lighting()

        for entity in self.entities:
            entity.on_update(dt)
        
    def on_draw(self):
        self.sprites.draw()
        
    def on_breaker_thrown(self, breaker):
        self.breakers_thrown += 1
        if self.breakers_thrown >= self.breakers:
            pass
            #self.win = True
            # WIN!
        

