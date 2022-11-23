from django.contrib import admin
from .models import Size, Pizza

class PizzaAdmin(admin.ModelAdmin):
    list_display = ('id','topping1', 'topping2', 'size')


admin.site.register(Size)
admin.site.register(Pizza, PizzaAdmin)