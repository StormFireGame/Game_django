from building.models import Building

from PIL import Image
import time

def get_map_size(image):
    image = Image.open(image)
    return image.size

def get_hero_position(hero):  
    return [ int(i) for i in 
                        hero.location.split('&')[0].split('_')[1].split('|')]

def join_hero_location(hero, coordinate_x, coordinate_y):
    current_position = get_hero_position(hero)
    
    if (int(coordinate_x) - int(current_position[0])) <= 1 and \
       (int(current_position[0]) - int(coordinate_x)) <= 1 and \
       (int(coordinate_y) - int(current_position[1])) <= 1 and \
       (int(current_position[1]) - int(coordinate_y)) <= 1:
        hero.location = '%s_%s|%s|%s' % (hero.location.split('_')[0], 
                                         coordinate_x, coordinate_y, 
                                         int(time.time()))
        hero.save()

##
def get_time_left_to_move(hero, time_delay=15):
    hero_time = get_hero_position(hero)[2]
    
    if (int(time.time()) - int(hero_time)) < time_delay:
        return time_delay - (int(time.time()) - int(hero_time))
    
    return None

def get_building(hero_position):
    x = hero_position[0]
    y = hero_position[1]
    try:
        building = Building.objects.filter(coordinate_x1__lte=x, 
                                           coordinate_y1__lte=y, 
                                           coordinate_x2__gte=x, 
                                           coordinate_y2__gte=y).get()
        return building
    except Building.DoesNotExist:
        return None

def get_island(hero):
    return int(hero.location.split('&')[0].split('_')[0])