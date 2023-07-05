from django.contrib import admin
from .models import Product,Variation,ReviewRating,productGallery
import admin_thumbnails
# Register your models here.
@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = productGallery
    extra = 1 

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','price','stock','category','modified_date','is_available')
    prepopulated_fields = {'slug':("product_name",)}
    inlines = [ProductGalleryInline]

class VaiationAdmin(admin.ModelAdmin):
    list_display = ('product','variation_category','variation_value','is_active','created_date')
    list_editable = ('is_active',)
    list_filter = ('product','variation_category','variation_value')

admin.site.register(Product,ProductAdmin)
admin.site.register(Variation,VaiationAdmin) 
admin.site.register(ReviewRating) 
admin.site.register(productGallery) 
