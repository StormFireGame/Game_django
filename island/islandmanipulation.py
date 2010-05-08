from PIL import Image
import time

def get_map_size(image):
    image = Image.open(image)
    return image.size

def get_hero_location(location):  
    return location.split('_')[1].split(':')[0].split('|')

def join_hero_location(location, coordinate_x, coordinate_y):
    current_position = location.split('_')[1].split(':')[0].split('|')
    
    if (int(coordinate_x) - int(current_position[0])) > 1 or \
        (int(current_position[0]) - int(coordinate_x)) > 1 or \
        (int(coordinate_y) - int(current_position[1])) > 1 or \
        (int(current_position[1]) - int(coordinate_y)) > 1:
        return location
    
    return '%s_%s|%s:%s' % (location.split('_')[0], coordinate_x, coordinate_y, 
                            int(time.time()))
    
def get_time_left(location, time_delay=15):
    hero_time = location.split('_')[1].split(':')[1]
    
    if (int(time.time()) - int(hero_time)) < time_delay:
        return time_delay - (int(time.time()) - int(hero_time))
    
    return 0    