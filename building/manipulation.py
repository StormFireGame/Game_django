from hero.manipulation import HeroM

class BuildingM:
    def __init__(self, building, hero):
        self.building = building
        self.hero = hero

    def add_to_location(self, slug):
        slugs = [ i.split(':')[1] for i in self.hero.location.split('&')[1:] ]

        if slug not in slugs:
            if self.building.parent and \
               self.building.parent.default_child and \
               self.building.parent.slug not in slugs:
                self.hero.location += '&' + \
                                        self.building.parent.module + ':' + \
                                                    self.building.parent.slug


            self.hero.location += '&' + self.building.module + ':' + \
                                                            self.building.slug
            self.hero.save()

    def remove_from_location(self, slug=None):
        if not slug:
            self.hero.location = self.hero.location.split('&')[0]
            self.hero.save()
            return

        slugs = [ i.split(':')[1] for i in self.hero.location.split('&')[1:] ]

        if len(slugs) and slug in slugs and slug != slugs[-1]:
            self.hero.location = '&'.join(self.hero.location.split('&')[0:-1])
            self.hero.save()

    def is_near_building(self, slug):
        slugs = [ i.split(':')[1] for i in self.hero.location.split('&')[1:] ]

        herom = HeroM(self.hero)
        x, y, time = herom.get_position_on_island()
        island = herom.get_island()
        
        if not len(slugs):
            if self.building.coordinate_x1 <= x and \
               self.building.coordinate_x2 >= x and \
               self.building.coordinate_y1 <= y and \
               self.building.coordinate_y2 >= y and \
               island == self.building.island:
                return True
        else:
            if (len(slugs) >= 2 and slug == slugs[-2]) or \
               (self.building.parent and \
               self.building.parent.slug == slugs[-1]) or \
               slug == slugs[-1] or \
               (self.building.parent and \
                self.building.parent.default_child == True):
                return True

        return False