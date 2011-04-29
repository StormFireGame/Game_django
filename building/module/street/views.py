from building import views as base_views

PLUGIN = 'street'

def index(request, slug):
    return base_views.index(request, slug)