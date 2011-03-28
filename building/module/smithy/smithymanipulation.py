import random

def repair_thing(herothing, percent_broken, count):
    i = 0
    while(i < count):
        if random.randint(0, 100) in range(percent_broken):
            herothing.stability_left -= 1
        if herothing.stability_left != herothing.stability_all:
            herothing.stability_all += 1
        else:
            break
        i += 1
    
    herothing.save()