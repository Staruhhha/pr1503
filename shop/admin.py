from django.contrib import admin
from shop.models import *

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'representor_FIO', 'representor_phone_number')
    list_display_links = ('name',)
    search_fields = ('name', 'representor_surname')
    list_editable = ('representor_phone_number',)
    ordering = ('name',)
    list_filter = ('isActive',)

    @admin.display(description="ФИО представителя")
    def representor_FIO(self, obj):
        if obj.representor_patronymic:
            return f"{obj.representor_surname} {obj.representor_name[0]}. {obj.representor_patronymic[0]}."
        return f"{obj.representor_surname} {obj.representor_name[0]}."


@admin.register(Supply)
class SupplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'supplier_name')
    list_display_links = ('id', 'date')
    search_fields = ('date', 'supplier_name')
    ordering = ('id',)

    @admin.display(description="Поставщик")
    def supplier_name(self, obj):
        return obj.supplier.name

@admin.register(Pos_supply)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'supply', 'quantity')
    list_display_links = ('id',)
    search_fields = ('product__name', 'supply__supplier__name')
    list_editable = ('quantity',)
    ordering = ('-supply__id',)



@admin.register(Category)
class SupplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    list_editable = ('description',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Order)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('customer_FIO', 'delivery_address', 'delivery_type', 'creation_date', 'finish_date')
    list_display_links = ('creation_date',)
    search_fields = ('delivery_address',)
    list_editable = ('finish_date',)
    ordering = ('-creation_date',)

    @admin.display(description="ФИО покупателя")
    def customer_FIO(self, obj):
        if obj.customer_patronymic:
            return f"{obj.customer_surname} {obj.customer_name[0]}. {obj.customer_patronymic[0]}."
        return f"{obj.customer_surname} {obj.customer_name[0]}."

@admin.register(Pos_order)
class SupplyAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'discount', 'quantity')
    list_display_links = None
    search_fields = ('product__name', 'order__id')
    list_editable = ('product', 'quantity', 'discount')
    ordering = ('-order__id',)


@admin.register(Parameter)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Pos_parameter)
class SupplyAdmin(admin.ModelAdmin):
    list_display = ('product', 'parameter', 'value')
    list_display_links = None
    search_fields = ('product__name', 'parameter__name')
    list_editable = ('product', 'parameter', 'value')
    ordering = ('-product__name',)


@admin.register(Product)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'description', 'isActive')
    search_fields = ('name',)
    list_filter = ('category', 'isActive')
    list_display_links = ('name',)
    list_editable = ('price', 'description', 'isActive')
    ordering = ('-id',)


@admin.register(Tag)
class SupplyAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ('name',)



