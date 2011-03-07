from building import views as base_views

PLUGIN = 'castle'

def index(request, slug, template_name='building/module/castle/index.html'):
    return base_views.index(request, slug)