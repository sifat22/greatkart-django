from.models import Category

#show all category by this function beacuse its available in all templates
#next it add in settings
def menu_links(request):
    links=Category.objects.all()
    return dict(links=links)