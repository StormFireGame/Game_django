def add_building_to_location(hero, building, slug):
    slugs = [ i.split(':')[1] for i in hero.location.split('&')[1:] ]
    
    if slug not in slugs:
        hero.location += '&' + building.plugin + ':' + building.slug
        hero.save()

def remove_building_from_location(hero, slug=None):
    if not slug:
        hero.location = hero.location.split('&')[0]
        hero.save()
        return
    
    slugs = [ i.split(':')[1] for i in hero.location.split('&')[1:] ]
    
    if len(slugs) and slug in slugs and slug != slugs[-1]:
        hero.location = '&'.join(hero.location.split('&')[0:-1])
        hero.save()