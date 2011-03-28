from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from building.models import Building
from building.module.commission.models import BuildingCommissionHeroThing, \
                                              BuildingCommission
from thing.models import Thing

from building.module.commission.forms import PutForm

from hero.heromanipulation import hero_init, update_capacity
from building import buildingmanipulation

PLUGIN = 'commission'

@hero_init
def index(request, slug, 
          template_name='building/module/commission/index.html'):
    hero = request.hero
    building = Building.objects.get(slug=slug)
    
    variables = RequestContext(request, {'hero': hero,
                                         'building': building})
    
    buildingmanipulation.add_building_to_location(hero, building, slug)
    
    return render_to_response(template_name, variables)

@hero_init
def view(request, slug, type, template_name='building/module/commission/view.html'):
    hero = request.hero
    building = Building.objects.get(slug=slug)

    type_num = [i[0] for i in Thing.TYPES if i[1].lower() == type][0]
    commissionherothings = BuildingCommissionHeroThing.objects.filter(
                                            herothing__thing__type=type_num). \
                                                exclude(herothing__hero=hero)

    variables = RequestContext(request, {'hero': hero,
                                         'building': building,
                                'commissionherothings': commissionherothings})
    
    return render_to_response(template_name, variables)

@hero_init
def buy(request, slug, id):
    hero = request.hero
    building = Building.objects.get(slug=slug)
    
    commissionherothing = BuildingCommissionHeroThing.objects.get(id=id)
    percent = BuildingCommission.objects.get(building=building).percent
    price = commissionherothing.price
    
    hero.money -= price
    hero.save()
    
    commissionherothing.herothing.hero.money += price - \
                                            round((price * (percent / 100)))  
    commissionherothing.herothing.hero.save()
    
    commissionherothing.herothing.away = False
    commissionherothing.herothing.hero = hero
    commissionherothing.herothing.save()
    
    commissionherothing.delete()
    
    update_capacity(hero)
#
    messages.add_message(request, messages.SUCCESS, 'You buy thing.')
    return HttpResponseRedirect(reverse('commission', args=[slug]))

#Put
@hero_init
def put(request, slug, template_name='building/module/commission/put.html'):
    hero = request.hero
    building = Building.objects.get(slug=slug)
    
    herothings = hero.herothing_set.filter(dressed=False, away=False)
    
    variables = RequestContext(request, {'hero': hero,
                                         'building': building,
                                         'herothings': herothings})
    
    return render_to_response(template_name, variables)

@hero_init
def put_select(request, slug, id,
           template_name='building/module/commission/put_select.html'):
    hero = request.hero
    building = Building.objects.get(slug=slug)
    
    herothing = hero.herothing_set.get(id=id)
    
    if request.method == 'POST':
        form = PutForm(request.POST)
        if form.is_valid():
            herothing.away = True
            herothing.save()
            
            commissionherothing = BuildingCommissionHeroThing(
                                                            building=building,
                                                        herothing=herothing,
                                            price=form.cleaned_data['price'])
            commissionherothing.save()
            
            update_capacity(hero)
#
            messages.add_message(request, messages.SUCCESS, 'You put thing.')
            return HttpResponseRedirect(reverse('commission', args=[slug]))
    else:
        form = PutForm()
        
    variables = RequestContext(request, {'hero': hero,
                                         'building': building,
                                         'herothing': herothing,
                                         'form': form})
    
    return render_to_response(template_name, variables)
#End

#Take
@hero_init
def take(request, slug, template_name='building/module/commission/take.html'):
    hero = request.hero
    building = Building.objects.get(slug=slug)
    
    commissionherothings = BuildingCommissionHeroThing.objects. \
                                                filter(herothing__hero=hero)
    
    variables = RequestContext(request, {'hero': hero,
                                         'building': building,
                                'commissionherothings': commissionherothings})
    
    return render_to_response(template_name, variables)

@hero_init
def take_select(request, slug, id):
    hero = request.hero
    
    commissionherothing = BuildingCommissionHeroThing.objects.get(id=id)
    commissionherothing.herothing.away = False
    commissionherothing.herothing.save()
    commissionherothing.delete()
    
    update_capacity(hero)
#
    messages.add_message(request, messages.SUCCESS, 'You take thing.')
    return HttpResponseRedirect(reverse('commission', args=[slug]))
#End