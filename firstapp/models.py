
from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils import timezone

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager

# class UserType(models.Model):
#     CUSTOMER = 1
#     SELLER = 2
#     TYPE_CHOICES = (
#         (SELLER, 'Seller'),
#         (CUSTOMER, 'Customer')
#     )

#     id = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, primary_key=True)

#     def __str__(self):
#         return self.get_id_display()

class CustomUser(AbstractBaseUser, PermissionsMixin):
    # username = None
    email = models.EmailField(_('email address'), unique=True)  
    name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    # if you require phone number field in your project
    # phone_regex = RegexValidator( regex = r'^\d{10}$',message = "phone number should exactly be in 10 digits")
    # phone = models.CharField(max_length=255, blank = True, null=True)  # you can set it unique = True

    # 1st way use for customer and seller model
    # is_customer = models.BooleanField(default=True)
    # is_seller = models.BooleanField(default = False)

    #2nd way
    # type = (
    #     (1, 'Seller'),
    #     (2, 'Customer')
    # )
    # user_type = models.IntegerField(choices = type, default=1)

    # 3rd way - to choose multiple user types -- user can be seller and customer -- so many to many field
    # usertype = models.ManyToManyField(UserType)


    # other ways with extra fields


 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    # using proxy models
    class Types(models.TextChoices):
        SELLER = "Seller", "SELLER"
        CUSTOMER = "Customer", "CUSTOMER"

    default_type = Types.CUSTOMER
    type = models.CharField(_('Type'), max_length=255, choices=Types.choices, default=default_type)

    def save(self, *args, **kwargs):
        if not self.id:
            self.type = self.default_type
        return super().save(*args, **kwargs)


# Model Managers for proxy models
from django.db.models import Q

class SellerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type = CustomUser.Types.SELLER)
        # return super().get_queryset(*args, **kwargs).filter(Q(type__contains = CustomUser.Types.SELLER))

class CustomerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type = CustomUser.Types.CUSTOMER)
        # return super().get_queryset(*args, **kwargs).filter(Q(type__contains = CustomUser.Types.CUSTOMER))


# Proxy Models. They do not create a seperate table
class Seller(CustomUser):
    default_type = CustomUser.Types.SELLER
    objects = SellerManager()
    class Meta:
        proxy = True
    
    def sell(self):
        print("I can sell")


    @property
    def showAdditional(self):
        return self.selleradditional

   
class Customer(CustomUser):
    default_type = CustomUser.Types.CUSTOMER
    objects = CustomerManager()
    class Meta:
        proxy = True 

    def buy(self):
        print("I can buy")

    @property
    def showAdditional(self):
        return self.customeradditional

class CustomerAdditional(models.Model):
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    address = models.CharField(max_length=1000)


class SellerAdditional(models.Model):
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    gst = models.CharField(max_length=10)
    warehouse_location = models.CharField(max_length=1000)


# class Customer(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     address = models.CharField(max_length=100)

# class Seller(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     gst = models.CharField(max_length=10)
#     warehouse_location = models.CharField(max_length=100)






class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=15)
    price = models.FloatField()

    def __str__(self):
        return self.product_name

    @classmethod
    def update_price(cls, prodid, price):
        obj = cls.objects.get(prod_id=prodid)
        obj.price = price
        obj.save()
        return obj
    
    @classmethod
    def create_prod(cls, name, price):
        prod = Product(product_name=name, price=price)
        prod.save()
        return prod

class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)


class ProductInCart(models.Model):
    class Meta:
        unique_together = (('cart', 'product'),)
    product_in_cart_id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField()



class Order(models.Model):
    status_choices = (
        (1, 'Not Packed'),
        (2, 'Ready For Shipment'),
        (3, 'Shipped'),
        (4, 'Delivered')
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.IntegerField(choices = status_choices, default=1)



class Deal(models.Model):
    user = models.ManyToManyField(CustomUser)
    deal_name = models.CharField(max_length=255)

from django.core.validators import RegexValidator


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    query = models.TextField()

    