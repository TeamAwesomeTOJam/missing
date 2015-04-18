import math
import tile


class Light(object):
    
    def __init__(self, floor, size, rays, intensity, x, y):
        self.floor = floor
        self.size = size
        self.rays = rays
        self.intensity = intensity
        self.x = x
        self.y = y
        self.on = True
           
    def light_visitor(self, ray, visited_tile):
        distance = ((visited_tile.x - self.x) ** 2 + (visited_tile.y - self.y) ** 2)
        value = self.intensity / max(distance, 0.0000000000000001)
        transmit, reflect = visited_tile.set_light(value)
        if not transmit:
            raise StopIteration()
    
    def do_lighting(self):
        if self.on and self.intensity > 0:
            for ray in tile.RayVisitor.generate_rays(self.floor, self.x, self.y, self.rays, self.size, 
                                                          0, 2 * math.pi, self.light_visitor):
                ray.visit()