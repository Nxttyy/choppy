from django.http import HttpResponse


# Create your views here.
def shop_profile(request, id):
    return HttpResponse("shop id %s" % id)


def shops_near_me(request):
    return HttpResponse("shops near you")
