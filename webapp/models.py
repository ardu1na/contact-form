from django.db import models
from decimal import Decimal


class Client(models.Model):
    class Meta:
        verbose_name = "cliente"
        verbose_name_plural = "clientes"

    name = models.CharField(max_length=100, verbose_name="nombre")
    email = models.EmailField(null=True, blank=True, verbose_name="correo electrónico")

    def __str__(self):
        return self.name


class Piece(models.Model):
    class Meta:
        verbose_name = "pieza"
        verbose_name_plural = "piezas"

    name = models.CharField(max_length=100, verbose_name="nombre")
    image = models.ImageField(verbose_name="Paño", null=True, blank=True, upload_to="piezas/")

    def __str__(self):
        return self.name


class Product(models.Model):
    class Meta:
        verbose_name = "producto"
        verbose_name_plural = "productos"

    COLOR_CHOICES = [
        ("Rojo", "Rojo"),
        ("Pizarra", "Pizarra"),
        ("Salmón", "Salmón"),
    ]

    piece = models.ForeignKey(
        Piece, verbose_name="pieza", on_delete=models.CASCADE, related_name="products"
    )
    image = models.ImageField(verbose_name="imagen",upload_to="piezas/")
    size = models.CharField(max_length=100, verbose_name="medidas")
    pps = models.PositiveIntegerField(verbose_name="piezas por m2")
    price = models.PositiveIntegerField(verbose_name="valor")
    color = models.CharField(choices=COLOR_CHOICES, max_length=15)
    discount = models.DecimalField(
        decimal_places=2, max_digits=6, verbose_name="descuento", default=0, null=True, blank=True
    )

    def __str__(self):
        return f"{self.piece.name} {self.color} {self.size}"


class Budget(models.Model):
    class Meta:
        verbose_name = "presupuesto"
        verbose_name_plural = "presupuestos"

    date = models.DateTimeField(auto_now_add=True, verbose_name="fecha")
    client = models.ForeignKey(
        Client, verbose_name="cliente", related_name="budgets", on_delete=models.SET_NULL, null=True, blank=True
    )
    product = models.ForeignKey(
        Product, verbose_name="pieza", on_delete=models.CASCADE, related_name="budgets"
    )
    area = models.PositiveIntegerField(verbose_name="superficie a cubrir en m2")
    discount = models.BooleanField(default=False, verbose_name="con descuento")

    def __str__(self):
        return f"{self.product} {self.area} {self.client}"

    @property
    def total_q(self):
        """Cantidad total de piezas necesarias para cubrir el área"""
        return self.product.pps * self.area

    @property
    def total(self):
        """Total antes del descuento"""
        return Decimal(self.total_q) * Decimal(self.product.price)

    @property
    def net_total(self):
        """Total con descuento aplicado (si corresponde)"""
        if self.discount:
            discount = self.product.discount
            return self.total * (Decimal("1") - discount / Decimal("100"))
        return self.total