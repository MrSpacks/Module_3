# shop/views.py
from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Product, Order

# Регистрация пользователя
def register(request):
    if request.method == 'POST': # Если форма отправлена
        form = UserCreationForm(request.POST) # Создаем форму с данными из POST-запроса
        if form.is_valid(): # Если форма валидна
            user = form.save()
            user.balance = 10000  # Стартовый баланс
            user.save()
            login(request, user)
            return redirect('product_list') # Перенаправляем на страницу со списком товаров
    else:
        form = UserCreationForm() # Если форма не отправлена, создаем пустую форму
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