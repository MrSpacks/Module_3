from django.contrib.auth.models import AbstractUser
from django.db import models


# Пользователь - расширить так, чтобы добавить поле кошелек (храним кол-во денег).
class CustomUser(AbstractUser):
    balance = models.DecimalField( max_digits=10, decimal_places=2, default=0.00)

# Товар - название, описание товара, цена, картинка (не обязательно), кол-во на складе.
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
order_status = [
    ('1', 'Ожидание'),
    ('2', 'Выполнен'),
    ('3', 'Отменен')
]
# Заказ - связь с пользователем, связь с товаром, дата создания заказа, статус (ожидание, выполнен, отменен)
class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=order_status, default='1')

    def __str__(self):
        return f"Order {self.id} by {self.user.username} for {self.product.name}"
    
# Возврат - содержит информацию, о затребованном возврате ( связь с покупкой, время запроса)
class ReturnRequest(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)
    reason = models.TextField()

    def __str__(self):
        return f"Return request for Order {self.order.id} by {self.order.user.username}"
