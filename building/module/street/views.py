from building import views as base_views

PLUGIN = 'street'

def index(request, slug, template_name='building/module/street/index.html'):
    return base_views.index(request, slug)