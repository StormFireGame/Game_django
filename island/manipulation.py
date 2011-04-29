from django.conf import settings

from bot.models import Bot

import time
import random
from PIL import Image

class IslandM:
    def __init__(self, island):
        self.island = island

    def get_time_left_to_move(self, hero_position):
        time_delay = settings.ISLAND_MOVE_DELAY
        hero_time = hero_position[2]

        if (int(time.time()) - int(hero_time)) < time_delay:
            return time_delay - (int(time.time()) - int(hero_time))

        return None

    def update_bots_position(self, coordinate_x, coordinate_y):
        bots = Bot.objects.filter(island=self.island,
                                  coordinate_x1__lte=coordinate_x,
                                  coordinate_y1__lte=coordinate_y,
                                  coordinate_x2__gte=coordinate_x,
                                  coordinate_y2__gte=coordinate_y,
                                  in_combat=False)

        for bot in bots:
            bot.current_coordinate_x = random.randint(bot.coordinate_x1,
                                                      bot.coordinate_x2)
            bot.current_coordinate_y = random.randint(bot.coordinate_y1,
                                                      bot.coordinate_y2)
            bot.save()

    def is_can_make_step(self, coordinate_x, coordinate_y, hero_position):
        x, y = int(hero_position[0]), int(hero_position[1])
        coordinate_x, coordinate_y = int(coordinate_x), int(coordinate_y)

        size = Image.open(self.island.image).size

        if (coordinate_x - x) > 1 or (x - coordinate_x) > 1 or \
           (coordinate_y - y) > 1 or (y - coordinate_y) > 1 or \
           coordinate_x > int(size[0] / settings.ISLAND_PART_DIMENSION) or \
           coordinate_y > int(size[1] / settings.ISLAND_PART_DIMENSION):
            return False

        return True

    def is_near_island(self, hero_location):
        return len(hero_location.split('&')) == 1 or \
               len(hero_location.split('&')) == 2