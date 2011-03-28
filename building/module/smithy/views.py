from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import F
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from building.models import Building
from building.module.smithy.models import BuildingSmithy, BuildingSmithyFeature
from hero.models import HeroThing

from hero.heromanipulation import hero_init
from building import buildingmanipulation
from building.module.smithy import smithymanipulation

PLUGIN = 'smithy'

@hero_init
def index(request, slug, template_name='building/module/smithy/index.html'):
    hero = request.hero
    building = Building.objects.get(slug=slug)
    variables = RequestContext(request, {'hero': hero,
                                         'building': building})
    
    buildingmanipulation.add_building_to_location(hero, building, slug)
    
    return render_to_response(template_name, variables)

@hero_init
def repair(request, slug, template_name='building/module/smithy/repair.html'):
    hero = request.hero
    building = Building.objects.get(slug=slug)
    
    herothings = hero.herothing_set.filter(dressed=False, away=False,
                                    stability_left__gt=F('stability_all'))
    percent_repair_money = BuildingSmithy.objects.get(building=building). \
                                                        percent_repair_money
    
    variables = RequestContext(request, {'hero': hero,
                                         'building': building,
                                         'herothings': herothings,
                                'percent_repair_money': percent_repair_money})
    return render_to_response(template_name, variables)

@hero_init
def repair_one(request, slug, id):
    hero = request.hero
    building = Building.objects.get(slug=slug)
    
    buildingsmithy = BuildingSmithy.objects.get(building=building)
    herothing = hero.herothing_set.get(id=id)
    
    smithymanipulation.repair_thing(herothing, buildingsmithy.percent_broken, 
                                    1)
    
    hero.money -= herothing.thing.price * \
                                    (buildingsmithy.percent_repair_money / 100)
    hero.save()

#
    messages.add_message(request, messages.SUCCESS, 'You repair one.')
    return HttpResponseRedirect(reverse('smithy_repair', args=[slug]))    

@hero_init
def repair_full(request, slug, id):
    hero = request.hero
    building = Building.objects.get(slug=slug)
    buildingsmithy = BuildingSmithy.objects.get(building=building)
    herothing = hero.herothing_set.get(id=id)
    
    count = herothing.stability_left - herothing.stability_all
    
    smithymanipulation.repair_thing(herothing, buildingsmithy.percent_broken, 
                                    count)
    
    hero.money -= count * (herothing.thing.price * \
                                (buildingsmithy.percent_repair_money / 100)) 
    
    hero.save()

#
    messages.add_message(request, messages.SUCCESS, 'You repair full.')
    return HttpResponseRedirect(reverse('smithy_repair', args=[slug]))

@hero_init
def modify(request, slug, template_name='building/module/smithy/modify.html'):
    hero = request.hero
    building = Building.objects.get(slug=slug)
    buildingsmithy = BuildingSmithy.objects.get(building=building)
    
    herothings = hero.herothing_set.filter(dressed=False, away=False)
    
    smithyfeatures = buildingsmithy.buildingsmithyfeature_set.all() 
    
    variables = RequestContext(request, {'hero': hero,
                                         'building': building,
                                         'herothings': herothings,
                                         'smithyfeatures': smithyfeatures})
    return render_to_response(template_name, variables)

@hero_init
def modify_select(request, slug, id_herothing, id_smithyfeature):
    hero = request.hero
    herothing = HeroThing.objects.get(id=id_herothing)
    smithyfeature = BuildingSmithyFeature.objects.get(id=id_smithyfeature)
    
    hero.money -= smithyfeature.money
    hero.save()
    
    herothing.herothingfeature_set.create(feature=smithyfeature.feature, 
                                          plus=smithyfeature.plus)
    
    #
    messages.add_message(request, messages.SUCCESS, 'You modify thing.')
    return HttpResponseRedirect(reverse('smithy_modify', args=[slug]))