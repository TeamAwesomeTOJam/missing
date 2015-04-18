'''
Created on Apr 25, 2010

@author: nish
'''

def direction_to(to_x, to_y, from_x, from_y):
        distance = ((to_x - from_x) ** 2 + (to_y - from_y) ** 2) ** 0.5
        if distance:
            delta_x = (to_x - from_x) / distance
            delta_y = (to_y - from_y) / distance
        else:
            delta_x = 0.0000000000000000000000001
            delta_y = 0.0000000000000000000000001
        return delta_x, delta_y