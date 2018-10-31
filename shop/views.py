from django.core.paginator import Paginator
from django.shortcuts import render_to_response

from goods.models import Category, Good
from orders.models import Order


def index(request):
    categories = Category.objects.all()
    goods = Good.objects.order_by('-id')
    page = Paginator(Paginator(goods, 8).page(1), 4)
    rows = [page.page(num).object_list for num in range(1, page.num_pages + 1)]
    return render_to_response('index.html', context={'categories': categories, 'rows': rows})


def goods(request):
    goods = Good.objects.all()
    pg = int(request.GET.get('page', 1))
    categories = Category.objects.all()
    cat_id = request.GET.get('category')
    if cat_id:
        goods = goods.filter(category_id=cat_id)
    goods = goods.order_by('-id')
    pages = Paginator(goods, 20)
    page = Paginator(pages.page(pg), 4)
    rows = [page.page(num).object_list for num in range(1, page.num_pages + 1)]
    return render_to_response('goods.html',
                              context={'categories': categories, 'rows': rows, 'next': pages.num_pages > 1})


def good_page(request, id):
    good = Good.objects.get(id=id)
    order = Order.objects.filter(client=request.user).last()
    now_item = order.orderitem_set.filter(id=id).last()
    return render_to_response('good_page.html',
                              {'good': good, 'order': order, 'now_item': now_item})


def registration(request):
    if request.method == "GET":
        return render_to_response('registration.html')
