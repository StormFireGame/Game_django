import random

class SmithyM:
    def __init__(self, smithy, herothing):
        self.smithy = smithy
        self.herothing = herothing
        
    def repair(self, count):
        percent_broken = self.smithy.percent_broken
        i = 0
        while(i < count):
            if random.randint(0, 100) in range(percent_broken):
                self.herothing.stability_left -= 1
            if self.herothing.stability_left != self.herothing.stability_all:
                self.herothing.stability_all += 1
            else:
                break
            i += 1

        self.herothing.save()