class ThingM:
    def __init__(self, thing, hero):
        self.thing = thing
        self.hero = hero

    def is_available_to_dress(self):
        hero_feature = self.hero.feature
        if self.hero.level >= self.thing.level_need and \
           int(hero_feature.strength) >= self.thing.strength_need and \
           int(hero_feature.dexterity) >= self.thing.dexterity_need and \
           int(hero_feature.intuition) >= self.thing.intuition_need and \
           int(hero_feature.health) >= self.thing.health_need and \
           int(hero_feature.swords) >= self.thing.swords_need and \
           int(hero_feature.axes) >= self.thing.axes_need and \
           int(hero_feature.knives) >= self.thing.knives_need and \
           int(hero_feature.clubs) >= self.thing.clubs_need and \
           int(hero_feature.shields) >= self.thing.shields_need:
            return True
        else:
            return False