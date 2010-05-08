from combat.models import Combat

import time

def get_location(location):
    return location.split(':')[0]

def in_combat(hero):
    return not Combat.objects.filter(combathero__hero=hero) \
                                            .exclude(is_active=2).count() == 0  

def is_cancel(hero):
    try:
        combat = \
            Combat.objects.filter(combathero__hero=hero, is_active=0).get()
        if combat.combathero_set.count() == 1:
            return combat
        else:
            return False
    except Combat.DoesNotExist:
        return False

def is_fight(hero):
    try:
        combat = \
            Combat.objects.filter(combathero__hero=hero, combathero__team=0, 
                                  type=0, is_active=0).get()
        return combat.combathero_set.count() == 2
    except Combat.DoesNotExist:
        return False

def is_refuse(hero):
    try:
        combat = \
            Combat.objects.filter(combathero__hero=hero, type=0, is_active=0) \
                                                                        .get()
        if combat.combathero_set.count() == 2:
            return combat
    except Combat.DoesNotExist:
        return False

def is_combat(hero):
    combat = Combat.objects.filter(combathero__hero=hero) \
                                            .exclude(is_active=2, type=0).get()
    
    time_start = int(time.mktime(combat.start_date_time.timetuple()))
    if (int(time.time()) - time_start) >= combat.time_wait:
        combat.is_active = 1
        combat.save()
        return True
    
    combat.time_wait_left = combat.time_wait - (int(time.time()) - time_start)   
    combat.save()
    return False     