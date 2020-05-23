

#Create your models here.
from django.db.models.signals import post_save
from django.db.models import Sum
from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django_countries.fields import CountryField

# # Products models

# class Product(models.Model):
#     title=models.CharField(max_length=100)
#     description=models.TextField(null=True,blank=True)
#     price=models.DecimalField(decimal_places=2,max_digits=1000000)
#     sale_price=models.DecimalField(decimal_places=2,max_digits=1000000,null=True,blank=True)
#     slug=models.SlugField(unique=True)
#     timestamp=models.DateTimeField(auto_now_add=True,auto_now=False)
#     updated=models.DateTimeField(auto_now_add=False,auto_now=True)
#     active=models.BooleanField(default=True)

#     def __str__(self):
#         return self.title
#     class Meta:
#         unique_together=('title','slug') 
        

# class ProductImage(models.Model):
#     product=models.ForeignKey(Product, on_delete=models.CASCADE)
#     image=models.ImageField(upload_to='products/images')
#     active=models.BooleanField(default=True)
#     updated=models.DateTimeField(auto_now_add=False,auto_now=True)
#     thumbnail=models.BooleanField(default=False)
#     featured=models.BooleanField(default=False)  

#     def __str__(self):
#         return self.product.title

CATEGORY_CHOICES=(
    ('S','Shirt'),
    ('SW','Sport wear'),
    ('OW','Outwear'),
    ('MS','MenSuit'),
    ('MJ','MenJeans'),
    ('W','Women'),
    ('K','Kids'),
    
) 
LABEL_CHOICES=(
    ('P','primary'),
    ('S','secondary'),
    ('D','danger'),
    # ('D','new'),
    # ('N','new'),
    
)
ADDRESS_CHOICES=(
    ('B','Billing'),
    ('S','Shipping'),
   
    
)                
class UserProfile(models.Model):
    user=models.OneToOneField(
        settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    stripe_customer_id=models.CharField(max_length=50,blank=True,null=True)
    one_click_purchasing=models.BooleanField(default=False)
    def __str__(self):
        return self.user.username
    

class Item(models.Model):
    title=models.CharField(max_length=100)
    discountprice=models.FloatField(blank=True,null=True)
    price=models.FloatField()
    description=models.TextField(null=True,blank=True)
    category=models.CharField(choices=CATEGORY_CHOICES,max_length=10,default=False)
    # label=models.CharField(choices=LABEL_CHOICES,max_length=10,default=False)
    label=models.CharField(choices=LABEL_CHOICES,max_length=10,blank=True,null=True)
    slug=models.SlugField()
    image=models.ImageField()
   
    def __str__(self):
        return self.title



    def get_absolute_url(self):
    #{{ item.get_absolute_url }}
        return reverse("ecommerceapp:product", kwargs={'slug': self.slug})

    def get_add_to_cart_url(self):
        return reverse("ecommerceapp:add-to-cart", kwargs={'slug': self.slug})

    def get_remove_from_cart_url(self):
        return reverse("ecommerceapp:remove-from-cart", kwargs={'slug': self.slug})    
         
        
    

class OrderItem(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered=models.BooleanField(default=False)

    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    def __str__(self):
        return f"{self.quantity} of {self.item.title}"
        #return self.title
    def get_total_item_price(self):
            return self.quantity * self.item.price
    def get_total_discount_item_price(self):
            return self.quantity * self.item.discountprice   
    def get_total_amount_saved(self):
            return self.get_total_item_price() - self.get_total_discount_item_price()  
    def get_final_price(self):   
        if self.item.discountprice:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()                     
    
    
class Order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ref_code=models.CharField(max_length=20,blank=True,null=True)
    items=models.ManyToManyField(OrderItem)
    start_date=models.DateTimeField(auto_now_add=True)
    ordered_date=models.DateTimeField()
    ordered=models.BooleanField(default=False)
    billing_address=models.ForeignKey(
        'Address',related_name='billing_address',on_delete=models.SET_NULL,blank=True,null=True)
    shipping_address=models.ForeignKey(
        'Address',related_name='shipping_address',on_delete=models.SET_NULL,blank=True,null=True)
    payment=models.ForeignKey(
        'Payment',on_delete=models.SET_NULL,blank=True,null=True)  
    being_delivered=models.BooleanField(default=False)  
    received=models.BooleanField(default=False)
    refund_requested=models.BooleanField(default=False)  
    refund_granted=models.BooleanField(default=False)



    def __str__(self):
        return self.user.username
    def get_total(self):
        total=0
        for order_item in self.items.all():
            total +=order_item.get_final_price()   
        return total     


class Address(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    street_address=models.CharField(max_length=60)
    apartment_address=models.CharField(max_length=60)
    country=CountryField(multiple=False)
    zip=models.CharField(max_length=60)
    address_type=models.CharField(max_length=1,choices=ADDRESS_CHOICES)
    default=models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name_plural='Addresses'
        

class Payment(models.Model):
    stripe_charge_id=models.CharField(max_length=50)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,blank=True,null=True)
    amount=models.FloatField()
    timestamp=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username
#model for refund request
class Refund(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    reason=models.TextField()
    accepted=models.BooleanField(default=False)
    email=models.EmailField()

    def __str__():

        return f"{self.pk}" 

def userprofile_receiver(sender,instance,created,*args, **kwargs):
    if created:
        userprofile=UserProfile.objects.create(user=instance)
post_save.connect(userprofile_receiver,sender=settings.AUTH_USER_MODEL)                
                
    

    

    



          
    
    






