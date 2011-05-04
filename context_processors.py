def hero(request):
    try:
        return {'hero': request.hero}
    except AttributeError:
        return {}