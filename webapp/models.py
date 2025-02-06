from django.db import models



class Client(models.Model):
    
    class Meta:
        verbose_name = "cliente"
        verbose_name_plural = "clientes"

    name = models.CharField(max_length=100, verbose_name = "nombre")
    email = models.EmailField(null=True, blank=True, verbose_name ="correo electrónico")

    def __str__ (self):
        return self.name


class Piece(models.Model):
    class Meta:
        verbose_name = "pieza"
        verbose_name_plural = "piezas"

    name = models.CharField(max_length=100, verbose_name="nombre")

    def __str__(self):
        return self.name


class Product(models.Model):
    
    class Meta:
        verbose_name = "producto"
        verbose_name_plural = "productos"

    COLOR_CHOICES = [
        ('Rojo', 'Rojo'),
        ('Pizarra', 'Pizarra'),
        ('Salmón', 'Salmón')
    ]

    piece = models.ForeignKey(Piece, verbose_name="pieza", on_delete = models.CASCADE, null=False, blank=False, related_name="products")
    image = models.ImageField(verbose_name="imagen")
    size = models.CharField(max_length=100, verbose_name="medidas")
    pps = models.PositiveIntegerField(verbose_name="piezas por m2")
    price = models.PositiveIntegerField(verbose_name="valor")
    color = models.CharField(choices=COLOR_CHOICES, max_length=15)
    discount = models.DecimalField(decimal_places=2, max_digits=6, verbose_name = "descuento")

    def __str__ (self):
        return f'{self.piece.name} {self.color} {self.size}'


class Budget(models.Model):
    def __str__(self):
        return f'{self.product} {self.area} {self.client}'
    class Meta:
        verbose_name = "presupuesto"
        verbose_name_plural = "presupuestos"

    date = models.DateTimeField(auto_now_add = True, verbose_name="fecha")
    client = models.ForeignKey(Client, verbose_name = "cliente", related_name="budgets", on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, verbose_name ="pieza", on_delete=models.CASCADE, related_name="budgets")
    area = models.PositiveIntegerField(verbose_name="superficie a cubrir en m2")
    discount = models.BooleanField(default=False, verbose_name="con descuento")
    
    
    @property
    def total_q (self):
        
        q = self.product.pps * self.area
        return q
    
    @property
    def total (self):
        
        grand_total = self.total_q*self.product.price    

        # TODO GET_DISCOUNT
        """    
        if discount:
            grand_total = grand_total*self.discount
        """

        return grand_total



    