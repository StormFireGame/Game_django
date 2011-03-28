def is_available_to_dress(hero, thing):
    if hero.level >= thing.level_need and \
       int(hero.feature.strength) >= thing.strength_need and \
       int(hero.feature.dexterity) >= thing.dexterity_need and \
       int(hero.feature.intuition) >= thing.intuition_need and \
       int(hero.feature.health) >= thing.health_need and \
       int(hero.feature.swords) >= thing.swords_need and \
       int(hero.feature.axes) >= thing.axes_need and \
       int(hero.feature.knives) >= thing.knives_need and \
       int(hero.feature.clubs) >= thing.clubs_need and \
       int(hero.feature.shields) >= thing.shields_need:
        return True
    else:
        return False