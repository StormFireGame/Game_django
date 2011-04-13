from building.models import Building
from bot.models import Bot

from PIL import Image
import time
import random

def get_map_size(image):
    image = Image.open(image)
    return image.size

def get_hero_position(hero):  
    return [ int(i) for i in 
                        hero.location.split('&')[0].split('_')[1].split('|')]

def join_hero_location(hero, coordinate_x, coordinate_y):
    
    hero.location = '%s_%s|%s|%s' % (hero.location.split('_')[0], 
                                     coordinate_x, coordinate_y, 
                                     int(time.time()))
    hero.save()

##
def get_time_left_to_move(hero):
    time_delay = 15
    hero_time = get_hero_position(hero)[2]
    
    if (int(time.time()) - int(hero_time)) < time_delay:
        return time_delay - (int(time.time()) - int(hero_time))
    
    return None

def get_buildings(hero_position):
    x, y = hero_position[0], hero_position[1]
    buildings = Building.objects.filter(coordinate_x1__lte=x,
                                        coordinate_y1__lte=y, 
                                        coordinate_x2__gte=x, 
                                        coordinate_y2__gte=y)
    return buildings
    
def get_island(hero):
    return int(hero.location.split('&')[0].split('_')[0])

def get_bots(hero_position):
    x, y = hero_position[0], hero_position[1]
    
    bots = Bot.objects.filter(current_coordinate_x=x, current_coordinate_y=y, 
                              in_combat=False)
    return bots

def update_bots_position(coordinate_x, coordinate_y):
    bots = Bot.objects.filter(coordinate_x1__lte=coordinate_x,
                              coordinate_y1__lte=coordinate_y, 
                              coordinate_x2__gte=coordinate_x, 
                              coordinate_y2__gte=coordinate_y, in_combat=False)
    
    for bot in bots:
        bot.current_coordinate_x = random.randint(bot.coordinate_x1, 
                                                  bot.coordinate_x2)
        bot.current_coordinate_y = random.randint(bot.coordinate_y1, 
                                                  bot.coordinate_y2)
        bot.save()