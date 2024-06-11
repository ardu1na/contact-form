from django.db import models

class Message(models.Model):
    asunto = models.CharField(max_length=500)
    texto = models.TextField()
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=50)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Mensaje"
        verbose_name_plural = "Mensajes"

    def __str__ (self):
        return f'{self.asunto} | {self.fecha} | Mensaje de {self.nombre}'