# shop/views.py
from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Product, Order, ReturnRequest
from django.contrib.auth.decorators import user_passes_test
from .forms import ProductForm
from .forms import CustomUserCreationForm
from datetime import timedelta
from django.utils import timezone
from .models import ReturnRequest
from django.contrib.admin.views.decorators import staff_member_required
# Регистрация пользователя
def register(request):
    if request.method == 'POST': # Если форма отправлена
        form = CustomUserCreationForm(request.POST) # Создаем форму с данными из POST-запроса
        if form.is_valid(): # Если форма валидна
            user = form.save()
            user.balance = 10000  # Стартовый баланс
            user.save()
            login(request, user)
            return redirect('product_list') # Перенаправляем на страницу со списком товаров
    else:
        form = CustomUserCreationForm() # Если форма не отправлена, создаем пустую форму
    return render(request, 'register.html', {'form': form}) # Отправляем форму в шаблон

# Вход и выход пользователя
def login_view(request): 
    if request.method == 'POST': # Если форма отправлена
        form = AuthenticationForm(data=request.POST)
        if form.is_valid(): # Если форма валидна
            user = form.get_user()
            login(request, user)
            return redirect('product_list') # Перенаправляем на страницу со списком товаров
    else:
        form = AuthenticationForm() # Если форма не отправлена, создаем пустую форму
    return render(request, 'login.html', {'form': form})


# Выход пользователя
def logout_view(request):   
    logout(request)
    return redirect('product_list') # Перенаправляем на страницу со списком товаров

# Список товаров 
def product_list(request):
    products = Product.objects.all() # Получаем все товары из базы данных
    return render(request, 'product_list.html', {'products': products}) # Отправляем список товаров в шаблон


# Покупка товара
@require_POST # Обрабатываем только POST-запросы
@login_required # Проверяем, что пользователь авторизован
def buy_product(request, product_id): # Получаем ID товара из URL
    product = get_object_or_404(Product, id=product_id) # Получаем товар из базы данных
    quantity = int(request.POST.get('quantity')) # Получаем количество товара из формы

    if product.stock < quantity: # Проверяем, достаточно ли товара на складе
        messages.error(request, 'Недостаточно товара на складе.') 
    elif request.user.balance < product.price * quantity: # Проверяем, достаточно ли денег на балансе
        messages.error(request, 'Недостаточно денег на балансе.')
    else:
        # Всё норм — совершаем покупку
        product.stock -= quantity
        product.save()

        request.user.balance -= product.price * quantity
        request.user.save()

        Order.objects.create(   # Создаем заказ
            user=request.user,
            product=product,
            quantity=quantity,
        )

        messages.success(request, f'Покупка {product.name} успешно совершена!')    

    return redirect('product_list') # Перенаправляем на страницу со списком товаров

# Добавление товара
@user_passes_test(lambda u: u.is_superuser) # Проверяем, что пользователь является администратором
@login_required # Проверяем, что пользователь авторизован
def add_product(request): # Функция для добавления товара

    ''' 
    RU: Функция для добавления товара в базу данных.
    CZ: Funkce pro přidání produktu do databáze.'''
    if request.method == 'POST': # Если форма отправлена
        form = ProductForm(request.POST, request.FILES)     # Создаем форму с данными из POST-запроса
        if form.is_valid(): # Если форма валидна
            form.save() # Сохраняем товар в базе данных
            return redirect('product_list') # Перенаправляем на страницу со списком товаров
    else:
        form = ProductForm() # Если форма не отправлена, создаем пустую форму
    return render(request, 'add_product.html', {'form': form})  # Отправляем форму в шаблон для добавления товара

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    eligible_orders = []
    now = timezone.now()

    for order in orders:
        time_diff = now - order.created_at
        can_return = (
        not hasattr(order, 'returnrequest')
        )
        eligible_orders.append((order, can_return))

    return render(request, 'my_orders.html', {
        'eligible_orders': eligible_orders,
    })

@login_required
def request_return(request, order_id):
    '''
    RU: Функция для запроса возврата товара.
    CZ: Funkce pro požadavek na vrácení zboží.
    '''
    order = get_object_or_404(Order, id=order_id, user=request.user) # Получаем заказ по ID и проверяем, что он принадлежит текущему пользователю

    # Проверка: уже есть возврат?
    if ReturnRequest.objects.filter(order=order).exists():
        messages.error(request, 'Вы уже подали запрос на возврат этого товара.')
        return redirect('my_orders')



    ReturnRequest.objects.create(order=order, reason='Пользователь запросил возврат')
    messages.success(request, 'Запрос на возврат отправлен администратору.')
    return redirect('my_orders')


@user_passes_test(lambda u: u.is_superuser)
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('product_list')



@staff_member_required
def return_requests_view(request):
    requests = ReturnRequest.objects.select_related('order__product', 'order__user')
    return render(request, 'return_requests.html', {'requests': requests})

def confirm_return(request, request_id):
    if not request.user.is_superuser:
        messages.error(request, "Доступ запрещён.")
        return redirect('return_requests')

    return_request = get_object_or_404(ReturnRequest, id=request_id)
    
    # Возврат средств
    order = return_request.order
    user = order.user
    product = order.product

    user.balance += product.price * order.quantity
    user.save()

    # Вернуть товар на склад
    product.stock += order.quantity
    product.save()

    # Удалить заказ и заявку на возврат
    order.delete()
    return_request.delete()

    messages.success(request, "Возврат подтвержден и обработан.")
    return redirect('return_requests')