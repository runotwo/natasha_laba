from django.shortcuts import render_to_response
from goods.models import Category, Good


def index(request):
    categories = Category.objects.all()
    goods = Good.objects.order_by('-id')[:4]
    return render_to_response('index.html', context={'categories': categories, 'goods': goods})

def registration(request):
    return render_to_response('registration.html')
