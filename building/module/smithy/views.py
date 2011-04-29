from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import F
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.conf import settings

from building.models import Building
from building.module.smithy.models import BuildingSmithyFeature
from hero.models import HeroThing

from hero.manipulation import hero_init, in_given_location
from building.manipulation import BuildingM
from building.module.smithy.manipulation import SmithyM

MODULE = 'smithy'

@hero_init
def index(request, slug, template_name='building/module/smithy/index.html'):
    hero = request.hero
    try:
        building = Building.objects.get(slug=slug)
    except Building.DoesNotExist:
        return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))
    
    buildingm = BuildingM(building, hero)

    if not buildingm.is_near_building(slug):
        return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))

    buildingm.add_to_location(slug)

    variables = RequestContext(request, {'hero': hero,
                                         'building': building})
    
    return render_to_response(template_name, variables)

@hero_init
@in_given_location
def repair(request, slug, template_name='building/module/smithy/repair.html'):
    hero = request.hero
    try:
        building = Building.objects.get(slug=slug)
    except Building.DoesNotExist:
        return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))
    
    herothings = hero.herothing_set.filter(dressed=False, away=False,
                                        stability_left__gt=F('stability_all'))
    percent_repair_money = building.buildingsmithy_set.get(). \
                                                        percent_repair_money
    
    variables = RequestContext(request, {'hero': hero,
                                         'building': building,
                                         'herothings': herothings,
                                'percent_repair_money': percent_repair_money})
    return render_to_response(template_name, variables)

# Repair
@hero_init
@in_given_location
def repair_one(request, slug, herothing_id):
    hero = request.hero
    try:
        building = Building.objects.get(slug=slug)
        herothing = hero.herothing_set.get(id=herothing_id, dressed=False,
                                           away=False,)
    except (Building.DoesNotExist, HeroThing.DoesNotExist):
        return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))

    smithy = building.buildingsmithy_set.get()

    price = herothing.thing.price * (smithy.percent_repair_money / 100)

    if hero.money < price:
#
        messages.add_message(request, messages.ERROR,
                             'You have not enough money.')
    else:
        SmithyM(smithy, herothing).repair(1)

        hero.money -= price
        hero.save()

#
        messages.add_message(request, messages.SUCCESS, 'You repair one.')
    return HttpResponseRedirect(reverse('smithy_repair', args=[slug]))    

@hero_init
@in_given_location
def repair_full(request, slug, herothing_id):
    hero = request.hero
    try:
        building = Building.objects.get(slug=slug)
        herothing = hero.herothing_set.get(id=herothing_id, dressed=False,
                                           away=False,)
    except (Building.DoesNotExist, HeroThing.DoesNotExist):
        return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))

    smithy = building.buildingsmithy_set.get()

    count = herothing.stability_left - herothing.stability_all
    price = count * (herothing.thing.price * \
                                        (smithy.percent_repair_money / 100))
    if hero.money < price:
#
        messages.add_message(request, messages.ERROR,
                             'You have not enough money.')
    else:
        SmithyM(smithy, herothing).repair(count)
    
        hero.money -= price
        hero.save()
#
        messages.add_message(request, messages.SUCCESS, 'You repair full.')
    return HttpResponseRedirect(reverse('smithy_repair', args=[slug]))
# End repair

# Modify
@hero_init
@in_given_location
def modify(request, slug, template_name='building/module/smithy/modify.html'):
    hero = request.hero
    try:
        building = Building.objects.get(slug=slug)
    except Building.DoesNotExist:
        return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))

    herothings = hero.herothing_set.filter(dressed=False, away=False)

    smithy = building.buildingsmithy_set.get()
    smithyfeatures = smithy.buildingsmithyfeature_set.all()
    
    variables = RequestContext(request, {'hero': hero,
                                         'building': building,
                                         'herothings': herothings,
                                         'smithyfeatures': smithyfeatures})
    
    return render_to_response(template_name, variables)

@hero_init
@in_given_location
def modify_select(request, slug, id_herothing, id_smithyfeature):
    hero = request.hero
    try:
        building = Building.objects.get(slug=slug)
        smithy = building.buildingsmithy_set.get()
        smithyfeature = smithy.buildingsmithyfeature_set. \
                                                    get(id=id_smithyfeature)
        herothing = HeroThing.objects.get(id=id_herothing, dressed=False,
                                          away=False,)
    except (Building.DoesNotExist, BuildingSmithyFeature.DoesNotExist,
            HeroThing.DoesNotExist):
        return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))

    if hero.money < smithyfeature.money:
#
        messages.add_message(request, messages.ERROR,
                             'You have not enough money.')
    else:
        hero.money -= smithyfeature.money
        hero.save()

        herothing.herothingfeature_set.create(feature=smithyfeature.feature,
                                              plus=smithyfeature.plus)

#
        messages.add_message(request, messages.SUCCESS, 'You modify thing.')
    return HttpResponseRedirect(reverse('smithy_modify', args=[slug]))
# End modify