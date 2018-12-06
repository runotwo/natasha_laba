import datetime
import json

from django.contrib.auth import authenticate, login, models, logout
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render_to_response, redirect
from lazysignup.decorators import allow_lazy_user, require_nonlazy_user

from api.models import Config
from goods.models import Category, Good
from orders.models import Order, Address, OrderItem


@allow_lazy_user
def index(request):
    categories = Category.objects.all()
    goods = Good.objects.order_by('-id')
    page = Paginator(Paginator(goods, 8).page(1), 4)
    rows = [page.page(num).object_list for num in range(1, page.num_pages + 1)]
    return render_to_response('index.html',
                              context={'categories': categories, 'rows': rows, 'user': request.user,
                                       'is_lazy': hasattr(request.user, 'lazyuser')})


@allow_lazy_user
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
                              context={'categories': categories, 'rows': rows, 'next': pages.num_pages > 1,
                                       'user': request.user,
                                       'is_lazy': hasattr(request.user, 'lazyuser')})


@allow_lazy_user
def good_page(request, id):
    if not request.user.is_authenticated:
        return redirect(to='/registration')
    good = Good.objects.get(id=id)
    last_order = Order.objects.filter(client=request.user).last()
    if not last_order or last_order.status != 'created':
        last_order = Order.objects.create(client=request.user)
    now_item = None
    if last_order:
        now_item = last_order.orderitem_set.filter(good_id=id).last()
    return render_to_response('good_page.html',
                              {'good': good, 'order': last_order, 'now_item': now_item, 'user': request.user,
                               'is_lazy': hasattr(request.user, 'lazyuser')})


@allow_lazy_user
def registration(request):
    if request.method == "GET":
        return render_to_response('registration.html')
    if request.method == 'POST':
        body = json.loads(request.body)
        username = body.get('email')
        password = body.get('pass')
        first_name = body.get('first_name')
        phone = body.get('phone')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'redirect': '/'})
        if models.User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Пользователь с таким email уже есть'})
        user = models.User(username=username, email=username, first_name=first_name)
        user.set_password(password)
        user.save()
        config = Config(user=user, number=phone)
        config.save()
        login(request, user)
        return JsonResponse({'redirect': '/'})


@require_nonlazy_user(to='/login')
def change(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return redirect(to='/login')
        return render_to_response('change.html', {'user': request.user, 'config': request.user.config,
                                                  'is_lazy': hasattr(request.user, 'lazyuser')})
    if request.method == 'POST':
        body = json.loads(request.body)
        name = body.get('name')
        last = body.get('last')
        phone = body.get('phone')
        request.user.config.number = phone
        request.user.first_name = name
        request.user.last_name = last
        request.user.config.save()
        request.user.save()
        return JsonResponse({'redirect': '/lk'})


@require_nonlazy_user(to='/login')
def lk(request):
    return render_to_response('lk.html', {'user': request.user, 'config': Config.objects.get(user=request.user),
                                          'is_lazy': hasattr(request.user, 'lazyuser')})


@allow_lazy_user
def cart(request):
    return render_to_response('cart.html', {'user': request.user,
                                            'is_lazy': hasattr(request.user, 'lazyuser')})


@allow_lazy_user
def order(request):
    body = json.loads(request.body)
    city = body.get('city')
    street = body.get('street')
    house_number = body.get('house_number')
    apartment_number = body.get('apartment_number')
    index = body.get('index')
    name = body.get('name')
    phone = body.get('phone')
    last_order = Order.objects.filter(client=request.user).last()
    if not last_order or last_order.status != 'created':
        last_order = Order.objects.create(client=request.user)
    if city:
        address = Address.objects.create(
            city=city,
            street=street,
            house_number=house_number,
            apartment_number=apartment_number,
            index=index
        )
        request.user.config.address = address
        request.user.config.save()
        last_order.address = address
    if name:
        request.user.first_name = name
        request.user.save()
        config, _ = Config.objects.get_or_create(user=request.user)
        config.number = phone
        config.save()
    for item in last_order.orderitem_set.all():
        item.good.count -= item.count
        item.good.save()
    last_order.status = 'await'
    last_order.save()
    return JsonResponse({'redirect': '/'})


@allow_lazy_user
def orders(request):
    orders = Order.objects.filter(client=request.user).exclude(status='created').order_by('-id')
    return render_to_response('orders.html', {'user': request.user, 'orders': orders,
                                              'is_lazy': hasattr(request.user, 'lazyuser')})


@allow_lazy_user
def search(request):
    string = (request.GET.get('string') or '').lower()
    items = Good.objects.filter(name__icontains=string)
    n_items = Good.objects.filter(name__icontains=string.capitalize())
    items = items.union(n_items)
    n_items = Good.objects.filter(category__name__icontains=string.capitalize())
    items = items.union(n_items)
    n_items = Good.objects.filter(category__name__icontains=string)
    items = items.union(n_items).distinct()
    categories = Category.objects.all()
    page = Paginator(items, 4)
    rows = [page.page(num).object_list for num in range(1, page.num_pages + 1)]
    return render_to_response('goods.html',
                              context={'categories': categories, 'rows': rows, 'next': False, 'user': request.user,
                                       'search_string': string,
                                       'is_lazy': hasattr(request.user, 'lazyuser')})


def lout(request):
    logout(request)
    return redirect(to='/')


def lin(request):
    if request.method == 'GET':
        return render_to_response('login.html')
    if request.method == 'POST':
        body = json.loads(request.body)
        username = body.get('email')
        password = body.get('pass')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'redirect': '/'})
        else:
            return JsonResponse({'error': 'Такого пользователя не существует'}, status=400)


def analytics(request):
    return render_to_response('analytics.html')


def analytics_items(request):
    queryset = OrderItem.objects.all()
    fmt = '%d.%m.%y'
    date_gte = request.GET.get('date__gte')
    date_lte = request.GET.get('date__lte')
    if date_gte:
        date_gte = datetime.datetime.strptime(date_gte, fmt)
        if not date_lte:
            queryset = queryset.filter(order__date=date_gte)
        else:
            queryset = queryset.filter(order__date__gte=date_gte)
    if date_lte:
        date_lte = datetime.datetime.strptime(date_lte, fmt)
        queryset = queryset.filter(order__date__lte=date_lte)
    from django.db import models
    res = list(queryset.values('good__name').annotate(
        sum_val=models.Sum(
            models.F('good__price') * models.F('count') - models.F('good__cost_price') * models.F('count'))).annotate(
        sum_price=models.Sum(models.F('good__price') * models.F('count'))).annotate(
        sum_count=models.Sum('count')))
    return JsonResponse(sorted(res, key=lambda x: x['sum_val'], reverse=True), safe=False)
