from django.http import HttpResponse

# Create your views here.


def cut_detail(request, id):
    return HttpResponse("cut id %s" % id)
