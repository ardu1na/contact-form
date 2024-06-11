from datetime import datetime
from django.db import models

class Message(models.Model):
    asunto = models.CharField(max_length=500)
    texto = models.TextField()
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=50)
    fecha = models.DateTimeField(auto_now_add=True)

    leido = models.BooleanField(default=False)
    spam = models.BooleanField(default=False)
    eliminado = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Mensaje"
        verbose_name_plural = "Mensajes"

    def __str__ (self):
        time = self.fecha.strftime("%d/%m/%Y %X")
        return f' Mensaje de {self.nombre} | {self.asunto} | {time}'