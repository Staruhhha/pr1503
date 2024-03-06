from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from shop.forms import *
from shop.models import *
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'queries/index.html')

def query_all(request):
    products = Product.objects.all()

    context = {
        'list': products # list - ключ, который будет использоваться как переменная в HTML
    }
    return render(request, 'queries/query_all.html', context)

def get_one_product(request,id):
    product = get_object_or_404(Product, pk=id)
    return render(request, 'queries/query_one.html', {'obj': product})


def detail_product(request,id):
    if request.method == "POST":
        messages.success(request, 'Успешная покупка')
        return redirect('catalog_products_page')
    product = get_object_or_404(Product, pk=id)
    return render(request, 'queries/detail.html', {'obj': product})

def create_product(request):
    category = get_object_or_404(Category, pk=1)
    parameter = get_object_or_404(Parameter, pk=1)
    product = Product()
    product.name = 'Яблоко'
    product.price = 60
    product.category = category

    product.save()
    return render(request, 'queries/message.html', context={'message': 'Товар добавлен!'})

def get_suppliers(request):
    suppliers = Supplier.objects.all()
    context = {
        'list': suppliers # list - ключ, который будет использоваться как переменная в HTML
    }
    return render(request, 'supplier/catalog.html', context)

def detail_supplier(request, id):
    supplier = get_object_or_404(Supplier, pk=id)
    return render(request, 'supplier/detail.html', {'obj': supplier})
def create_supplier(request):
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = Supplier(**form.cleaned_data)
            supplier.save()
            messages.success(request, 'Поставщик успешно добавлен!')
            return redirect('suppliers_page')
        messages.error(request, 'Неверно заполнены поля')
    form = SupplierForm()
    context = {
        'form': form
    }
    return render(request, 'supplier/create_supplier.html', context)


from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required

def user_registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(user)
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('home_page')
        messages.error(request, 'Что-то пошло не так')
    else:
        form = RegistrationForm()
    return render(request, 'auth/registration.html', {'form': form})

def user_login(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            print('is_anon: ', request.user.is_anonymous)
            print('is_auth: ', request.user.is_authenticated)
            print(user)
            messages.success(request, 'Вы успешно авторизовались')
            return redirect('home_page')
        messages.error(request, 'Что-то пошло не так')
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.warning(request, 'Вы вышли из аккаунта')
    return redirect('user_login_page')


def anon(request):
    print('is_active:', request.user.is_active)
    print('is_anon:', request.user.is_anonymous)
    print('is_auth:', request.user.is_authenticated)
    print('is_staff:', request.user.is_staff)
    print('is_superuser:', request.user.is_superuser)

    # При проверке доступ указывается следующим образом:
    # <приложение>.<право>_<модель>
    # Права: add, change, view, delete

    print('Может ли добавлять товар?', request.user.has_perm('shop.add_product'))
    print('Может ли добавлять и изменять товар?', request.user.has_perms(['shop.add_product', 'shop.change_product']))


    return render(request, 'test/anon.html')

@login_required()
def auth(request):
    return render(request, 'test/auth.html')

@permission_required('shop.add_product')
def is_able_to_add_product(request):
    return render(request, 'test/can_add_product.html')

@permission_required(['shop.add_product', 'shop.change_product'])
def is_able_to_add_and_change_product(request):
    return render(request, 'test/can_add_change_product.html')

@permission_required('shop.change_delivery_type')
def is_able_to_change_delivery_type(request):
    return render(request, 'test/can_change_delivery_type.html')

@login_required()
def buy(request):

    return render(request, 'queries/purchase.html')

# View Generic
# ListView - Список объектов
# DetailView - Полная информация выбранного объекта
# UpdateView - Изменение
# CreateView - Создание
# DeleteView - Удаление

from django.views.generic import ListView, DeleteView, DetailView, UpdateView, CreateView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

class CategoryList(ListView):
    model = Category
    template_name = 'category/category_list.html'
    context_object_name = 'categories'
    extra_context = {
        'title': 'Список категорий'
    }
    allow_empty = True

    # from django.core.paginator import Paginator

    paginate_by = 1
    def get_queryset(self):
        return Category.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список категорий в get_context_data()'
        return context

class CategoryDetail(DetailView):
    model = Category
    template_name = 'category/category_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        return super().get_context_data(**kwargs)

class CategoryCreate(CreateView):
    model = Category
    form_class = CategoryForm
    extra_context = {
        'action': 'Создать'
    }
    template_name = 'category/category_form.html'
    # success_url = reverse_lazy('category_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        return super().get_context_data(**kwargs)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class CategoryUpdate(UpdateView):
    model = Category
    form_class = CategoryForm
    extra_context = {
        'action': 'Изменить'
    }
    template_name = 'category/category_form.html'

    @method_decorator(permission_required('shop.change_category'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class CategoryDelete(DeleteView):
    model = Category
    template_name = 'category/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')

    @method_decorator(permission_required('shop.delete_category'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


from shop.utils import CalculateMoney

class OrderDetail(DetailView, CalculateMoney):
    model = Order
    template_name = 'order/order_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = context.get('object')
        list_price = [pos_order.sum_pos_order() for pos_order in order.pos_order_set.all()]
        context['sum_price'] = self.sum_price(prices=list_price)
        return context

from django.core.mail import send_mail, send_mass_mail
from django.conf import settings

def contact_email(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            mail = send_mail(form.cleaned_data['subject'],
                             form.cleaned_data['content'],
                             settings.EMAIL_HOST_USER,
                             ['mail_for_django@mail.ru'],
                             fail_silently=True)
            if mail:
                messages.success(request, 'Письмо успешно добавлено!')
                return redirect('home_page')
            else:
                messages.error(request, 'Не удалось отправить письмо')
        else:
            messages.warning(request, 'Письмо неверно заполнено')
    else:
        form = ContactForm()
    return render(request, 'email/email.html', {'form': form})



from django.http import JsonResponse
from shop.serializers import *

# status - пакет со всеми статусными кодами для настройки отчета
from rest_framework import status

from rest_framework.response import Response

# api_view - декоратор, внутри него можно описывать доступные нам методы
from rest_framework.decorators import api_view

# viewsets - generic класс, c CRUD операциями
from rest_framework import viewsets

def test_json(request):
    return JsonResponse({
        'message': 'Данные в виде JSON',
        'api_test':  reverse_lazy('api_test'),
        'order_api_list': reverse_lazy('api_order_list'),
        'order_api_detail': reverse_lazy('api_order_detail'),
    })


@api_view(['GET', 'POST'])
def order_api_list(request, format=None):
    # Проверка запроса
    if request.method == 'GET':

        # Получаем данные из БД
        order_list = Order.objects.filter(exists=True)
        # Преобразуем данные в словарь с помощью сериализатора
        # По умолчанию сериализатор работает с одним объектом, но если у нас
        # список объектов то стоит включить параметр many
        serializer = OrderSerializer(order_list, many=True)
        print(serializer.data)
        return Response({'orders': serializer.data})

    elif request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            # Сохранение
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT', 'DELETE'])
def order_api_detail(request, pk, format=None):
    order_obj = get_object_or_404(Order, pk=pk)

    if order_obj:
        if request.method == 'GET':
            serializer = OrderSerializer(order_obj)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = OrderSerializer(order_obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Данные успешно обновлены', 'order': serializer.data})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            # Удаление объекта
            order_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        # Если объект не был найден
        return Response(status=status.HTTP_404_NOT_FOUND)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(isActive=True)
    serializer_class = ProductSerializer