from building import views as base_views

MODULE = 'castle'

def index(request, slug):
    return base_views.index(request, slug)