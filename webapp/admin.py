from django.contrib import admin

from webapp.models import Piece, Product, Client, Budget


admin.site.register(Piece)
admin.site.register(Product)
admin.site.register(Client)


class BudgetAdmin(admin.ModelAdmin):
    list_display = ('client', 'date', 'product', 'get_total_q', 'get_total')


    def get_total_q(self, obj):
        return f'{obj.total_q} piezas'
    get_total_q.short_description = "Cantidad"

    def get_total(self, obj):
        return f'{obj.total} euros'
    get_total.short_description = "Total"

admin.site.register(Budget, BudgetAdmin)

