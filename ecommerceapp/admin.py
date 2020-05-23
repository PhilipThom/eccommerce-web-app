

# Register your models here.

from django.contrib import admin
from .models import Order,OrderItem,Item,Payment,Refund,Address,UserProfile

def make_refund_accepted(ModelAdmin,request,queryset):
	queryset.update(refund_requested=False,refund_granted=True)
make_refund_accepted.short_description='Updated orders to grant refund '	
# # Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display=['user','ordered','being_delivered','received','refund_requested','refund_granted','shipping_address','billing_address','payment']
    list_filter=['ordered','being_delivered','received','refund_requested','refund_granted']
    
    list_display_links=['user','shipping_address','billing_address','payment']
    search_fields=['user__username','ref_code']
    actions=[make_refund_accepted]
    
#     readonly_fields=['updated','timestamp']
#     prepopulated_fields={"slug":("title",)}
#     class Meta:
#         model=Product

# admin.site.register(Product,ProductAdmin)
# admin.site.register(ProductImage)
class AddressAdmin(admin.ModelAdmin):
	list_display=['user','street_address','apartment_address','country','zip','address_type','default']
	list_filter=['default','address_type','country']
	search_fields=['user','street_address','apartment_address','zip']

admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order,OrderAdmin)
admin.site.register(Payment)
admin.site.register(Address,AddressAdmin)
admin.site.register(UserProfile)


